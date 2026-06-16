#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import json
import math
import posixpath
import re
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "asvg": "http://schemas.microsoft.com/office/drawing/2016/SVG/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rels": "http://schemas.openxmlformats.org/package/2006/relationships",
}

EMU_PER_PT = 12700
SVG_HEADER = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export slide elements from PPTX files as standalone SVG files."
    )
    parser.add_argument("--input-dir", default="assets/raw")
    parser.add_argument("--output-dir", default="tmp/exported-graphics-svg")
    return parser.parse_args()


def sanitize_filename(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    cleaned = cleaned.strip("._")
    return cleaned or "unnamed"


def slide_sort_key(path: str) -> tuple[int, str]:
    match = re.search(r"slide(\d+)\.xml$", path)
    return (int(match.group(1)), path) if match else (10**9, path)


def load_relationships(zip_file: zipfile.ZipFile, rels_path: str) -> dict[str, str]:
    rels: dict[str, str] = {}
    if rels_path not in zip_file.namelist():
        return rels

    root = ET.fromstring(zip_file.read(rels_path))
    for rel in root.findall("rels:Relationship", NS):
        rel_id = rel.attrib.get("Id")
        target = rel.attrib.get("Target")
        if rel_id and target:
            rels[rel_id] = target
    return rels


def resolve_target(base_part: str, target: str) -> str:
    return posixpath.normpath(posixpath.join(posixpath.dirname(base_part), target))


def xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def matrix_identity() -> tuple[float, float, float, float, float, float]:
    return (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def matrix_multiply(
    left: tuple[float, float, float, float, float, float],
    right: tuple[float, float, float, float, float, float],
) -> tuple[float, float, float, float, float, float]:
    a1, b1, c1, d1, e1, f1 = left
    a2, b2, c2, d2, e2, f2 = right
    return (
        a1 * a2 + c1 * b2,
        b1 * a2 + d1 * b2,
        a1 * c2 + c1 * d2,
        b1 * c2 + d1 * d2,
        a1 * e2 + c1 * f2 + e1,
        b1 * e2 + d1 * f2 + f1,
    )


def translate(tx: float, ty: float) -> tuple[float, float, float, float, float, float]:
    return (1.0, 0.0, 0.0, 1.0, tx, ty)


def scale(sx: float, sy: float) -> tuple[float, float, float, float, float, float]:
    return (sx, 0.0, 0.0, sy, 0.0, 0.0)


def rotate(angle_deg: float) -> tuple[float, float, float, float, float, float]:
    radians = math.radians(angle_deg)
    cos_v = math.cos(radians)
    sin_v = math.sin(radians)
    return (cos_v, sin_v, -sin_v, cos_v, 0.0, 0.0)


def matrix_to_svg(matrix: tuple[float, float, float, float, float, float]) -> str:
    return "matrix({:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f})".format(*matrix)


def parse_theme_colors(zip_file: zipfile.ZipFile) -> dict[str, str]:
    theme_path = None
    for name in sorted(zip_file.namelist()):
        if name == "ppt/theme/theme1.xml":
            theme_path = name
            break
        if theme_path is None and name.startswith("ppt/theme/") and name.endswith(".xml"):
            theme_path = name

    if theme_path is None:
        return {}

    root = ET.fromstring(zip_file.read(theme_path))
    scheme = root.find(".//a:clrScheme", NS)
    if scheme is None:
        return {}

    colors: dict[str, str] = {"lt1": "FFFFFF"}
    for child in scheme:
        tag = child.tag.split("}")[-1]
        sub = list(child)[0] if list(child) else child
        raw = sub.attrib.get("val") or sub.attrib.get("lastClr") or "000000"
        if raw.lower() in {"window", "windowtext"}:
            raw = "FFFFFF" if raw.lower() == "window" else "000000"
        colors[tag] = raw

    # Default DrawingML logical color mapping.
    colors["bg1"] = colors.get("lt1", "FFFFFF")
    colors["tx1"] = colors.get("dk1", "000000")
    colors["bg2"] = colors.get("lt2", "F3F3F0")
    colors["tx2"] = colors.get("dk2", "000028")
    return colors


def clamp_color(value: float) -> int:
    return max(0, min(255, int(round(value))))


def apply_lum_mod(rgb: tuple[int, int, int], amount: int) -> tuple[int, int, int]:
    factor = amount / 100000.0
    return tuple(clamp_color(channel * factor) for channel in rgb)


def apply_lum_off(rgb: tuple[int, int, int], amount: int) -> tuple[int, int, int]:
    offset = 255.0 * amount / 100000.0
    return tuple(clamp_color(channel + offset) for channel in rgb)


def apply_tint(rgb: tuple[int, int, int], amount: int) -> tuple[int, int, int]:
    factor = amount / 100000.0
    return tuple(clamp_color(channel + (255 - channel) * factor) for channel in rgb)


def apply_shade(rgb: tuple[int, int, int], amount: int) -> tuple[int, int, int]:
    factor = amount / 100000.0
    return tuple(clamp_color(channel * factor) for channel in rgb)


def resolve_color_node(node: ET.Element | None, theme_colors: dict[str, str]) -> tuple[str | None, float]:
    if node is None:
        return None, 1.0

    tag = node.tag.split("}")[-1]
    if tag == "noFill":
        return None, 1.0

    if tag == "solidFill":
        for child in node:
            return resolve_color_node(child, theme_colors)
        return None, 1.0

    if tag == "srgbClr":
        hex_color = node.attrib.get("val", "000000")
    elif tag == "schemeClr":
        scheme_name = node.attrib.get("val", "")
        hex_color = theme_colors.get(scheme_name, "000000")
    elif tag == "sysClr":
        hex_color = node.attrib.get("lastClr", "000000")
    else:
        return None, 1.0

    rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    opacity = 1.0

    for child in node:
        name = child.tag.split("}")[-1]
        amount = int(child.attrib.get("val", "0"))
        if name == "lumMod":
            rgb = apply_lum_mod(rgb, amount)
        elif name == "lumOff":
            rgb = apply_lum_off(rgb, amount)
        elif name == "tint":
            rgb = apply_tint(rgb, amount)
        elif name == "shade":
            rgb = apply_shade(rgb, amount)
        elif name == "alpha":
            opacity *= amount / 100000.0

    return "#{:02X}{:02X}{:02X}".format(*rgb), opacity


def get_fill_style(sp_pr: ET.Element | None, theme_colors: dict[str, str]) -> dict[str, str]:
    if sp_pr is None:
        return {"fill": "none"}

    solid_fill = sp_pr.find("a:solidFill", NS)
    if solid_fill is None:
        no_fill = sp_pr.find("a:noFill", NS)
        if no_fill is not None:
            return {"fill": "none"}
        return {"fill": "none"}

    color, opacity = resolve_color_node(solid_fill, theme_colors)
    style = {"fill": color or "none"}
    if opacity < 1.0:
        style["fill-opacity"] = f"{opacity:.4f}"
    return style


def get_line_style(sp_pr: ET.Element | None, theme_colors: dict[str, str]) -> dict[str, str]:
    if sp_pr is None:
        return {"stroke": "none"}

    ln = sp_pr.find("a:ln", NS)
    if ln is None or ln.find("a:noFill", NS) is not None:
        return {"stroke": "none"}

    color_node = None
    if ln.find("a:solidFill", NS) is not None:
        color_node = ln.find("a:solidFill", NS)
    else:
        for child in ln:
            if child.tag.split("}")[-1] in {"schemeClr", "srgbClr", "sysClr"}:
                color_node = child
                break

    color, opacity = resolve_color_node(color_node, theme_colors)
    width_emu = float(ln.attrib.get("w", "12700"))
    style = {
        "stroke": color or "#000000",
        "stroke-width": f"{width_emu / EMU_PER_PT:.3f}",
        "stroke-linecap": "round" if ln.find("a:round", NS) is not None else "butt",
        "stroke-linejoin": "miter",
    }
    if opacity < 1.0:
        style["stroke-opacity"] = f"{opacity:.4f}"
    return style


def style_to_svg(style: dict[str, str]) -> str:
    return " ".join(f'{key}="{xml_escape(value)}"' for key, value in style.items())


def has_visible_paint(style: dict[str, str]) -> bool:
    return style.get("fill", "none") != "none" or style.get("stroke", "none") != "none"


def get_xfrm(el: ET.Element, path: str) -> ET.Element | None:
    sp_pr = el.find(path, NS)
    if sp_pr is None:
        return None
    return sp_pr.find("a:xfrm", NS)


def parse_shape_matrix(xfrm: ET.Element | None, local_width: float, local_height: float) -> tuple[float, float, float, float, float, float]:
    if xfrm is None:
        return matrix_identity()

    off = xfrm.find("a:off", NS)
    ext = xfrm.find("a:ext", NS)
    if off is None or ext is None:
        return matrix_identity()

    x = float(off.attrib.get("x", "0"))
    y = float(off.attrib.get("y", "0"))
    cx = float(ext.attrib.get("cx", "0"))
    cy = float(ext.attrib.get("cy", "0"))

    rot_deg = float(xfrm.attrib.get("rot", "0")) / 60000.0
    flip_h = xfrm.attrib.get("flipH") == "1"
    flip_v = xfrm.attrib.get("flipV") == "1"

    sx = cx / local_width if local_width else 1.0
    sy = cy / local_height if local_height else 1.0

    matrix = matrix_identity()
    matrix = matrix_multiply(matrix, translate(x, y))
    matrix = matrix_multiply(matrix, translate(cx / 2.0, cy / 2.0))
    if rot_deg:
        matrix = matrix_multiply(matrix, rotate(rot_deg))
    if flip_h or flip_v:
        matrix = matrix_multiply(matrix, scale(-1.0 if flip_h else 1.0, -1.0 if flip_v else 1.0))
    matrix = matrix_multiply(matrix, translate(-cx / 2.0, -cy / 2.0))
    matrix = matrix_multiply(matrix, scale(sx, sy))
    return matrix


def parse_group_matrix(xfrm: ET.Element | None) -> tuple[float, float, float, float, float, float]:
    if xfrm is None:
        return matrix_identity()

    off = xfrm.find("a:off", NS)
    ext = xfrm.find("a:ext", NS)
    ch_off = xfrm.find("a:chOff", NS)
    ch_ext = xfrm.find("a:chExt", NS)
    if off is None or ext is None or ch_off is None or ch_ext is None:
        return matrix_identity()

    x = float(off.attrib.get("x", "0"))
    y = float(off.attrib.get("y", "0"))
    cx = float(ext.attrib.get("cx", "0"))
    cy = float(ext.attrib.get("cy", "0"))
    ch_x = float(ch_off.attrib.get("x", "0"))
    ch_y = float(ch_off.attrib.get("y", "0"))
    ch_cx = float(ch_ext.attrib.get("cx", "1"))
    ch_cy = float(ch_ext.attrib.get("cy", "1"))

    rot_deg = float(xfrm.attrib.get("rot", "0")) / 60000.0
    flip_h = xfrm.attrib.get("flipH") == "1"
    flip_v = xfrm.attrib.get("flipV") == "1"

    sx = cx / ch_cx if ch_cx else 1.0
    sy = cy / ch_cy if ch_cy else 1.0

    matrix = matrix_identity()
    matrix = matrix_multiply(matrix, translate(x, y))
    matrix = matrix_multiply(matrix, translate(cx / 2.0, cy / 2.0))
    if rot_deg:
        matrix = matrix_multiply(matrix, rotate(rot_deg))
    if flip_h or flip_v:
        matrix = matrix_multiply(matrix, scale(-1.0 if flip_h else 1.0, -1.0 if flip_v else 1.0))
    matrix = matrix_multiply(matrix, translate(-cx / 2.0, -cy / 2.0))
    matrix = matrix_multiply(matrix, scale(sx, sy))
    matrix = matrix_multiply(matrix, translate(-ch_x, -ch_y))
    return matrix


def parse_formula(formula: str, ctx: dict[str, float]) -> float:
    parts = formula.split()
    if not parts:
        return 0.0

    if parts[0] == "*/" and len(parts) == 4:
        a = ctx.get(parts[1], float(parts[1]) if parts[1].isdigit() else 0.0)
        b = ctx.get(parts[2], float(parts[2]) if parts[2].isdigit() else 0.0)
        c = ctx.get(parts[3], float(parts[3]) if parts[3].isdigit() else 1.0)
        return (a * b) / c if c else 0.0

    try:
        return float(parts[-1])
    except ValueError:
        return ctx.get(parts[-1], 0.0)


def build_custom_geom_path(cust_geom: ET.Element) -> tuple[str, float, float]:
    path_list = cust_geom.find("a:pathLst", NS)
    if path_list is None:
        return "", 1.0, 1.0

    paths = []
    width = 1.0
    height = 1.0

    for path in path_list.findall("a:path", NS):
        width = float(path.attrib.get("w", "1"))
        height = float(path.attrib.get("h", "1"))
        ctx = {"w": width, "h": height, "l": 0.0, "t": 0.0, "r": width, "b": height}

        gd_list = cust_geom.find("a:gdLst", NS)
        if gd_list is not None:
            for gd in gd_list.findall("a:gd", NS):
                ctx[gd.attrib.get("name", "")] = parse_formula(gd.attrib.get("fmla", ""), ctx)

        commands: list[str] = []
        for cmd in path:
            name = cmd.tag.split("}")[-1]
            if name == "moveTo":
                pt = cmd.find("a:pt", NS)
                if pt is not None:
                    commands.append(f"M {ctx.get(pt.attrib['x'], float(pt.attrib['x'])):.3f} {ctx.get(pt.attrib['y'], float(pt.attrib['y'])):.3f}")
            elif name == "lnTo":
                pt = cmd.find("a:pt", NS)
                if pt is not None:
                    commands.append(f"L {ctx.get(pt.attrib['x'], float(pt.attrib['x'])):.3f} {ctx.get(pt.attrib['y'], float(pt.attrib['y'])):.3f}")
            elif name == "cubicBezTo":
                pts = cmd.findall("a:pt", NS)
                if len(pts) == 3:
                    coords = []
                    for pt in pts:
                        coords.append(f"{ctx.get(pt.attrib['x'], float(pt.attrib['x'])):.3f} {ctx.get(pt.attrib['y'], float(pt.attrib['y'])):.3f}")
                    commands.append("C " + " ".join(coords))
            elif name == "close":
                commands.append("Z")
        if commands:
            paths.append(" ".join(commands))

    return " ".join(paths), width, height


def build_preset_path(prst: str) -> tuple[str, float, float] | None:
    if prst == "rect":
        return "M 0 0 L 100 0 L 100 100 L 0 100 Z", 100.0, 100.0
    if prst == "roundRect":
        return (
            "M 15 0 L 85 0 Q 100 0 100 15 L 100 85 Q 100 100 85 100 L 15 100 Q 0 100 0 85 L 0 15 Q 0 0 15 0 Z",
            100.0,
            100.0,
        )
    if prst == "ellipse":
        return "M 50 0 A 50 50 0 1 1 49.999 0 Z", 100.0, 100.0
    if prst == "diamond":
        return "M 50 0 L 100 50 L 50 100 L 0 50 Z", 100.0, 100.0
    if prst == "homePlate":
        return "M 0 0 L 72 0 L 100 50 L 72 100 L 0 100 Z", 100.0, 100.0
    if prst == "flowChartExtract":
        return "M 0 0 L 72 0 L 100 50 L 72 100 L 0 100 L 20 50 Z", 100.0, 100.0
    if prst == "chevron":
        return "M 0 0 L 70 0 L 100 50 L 70 100 L 0 100 L 25 50 Z", 100.0, 100.0
    if prst == "star5":
        return (
            "M 50 0 L 61 35 L 98 35 L 68 57 L 79 91 "
            "L 50 70 L 21 91 L 32 57 L 2 35 L 39 35 Z",
            100.0,
            100.0,
        )
    if prst == "heart":
        return (
            "M 50 92 C 20 72 0 50 0 28 C 0 11 14 0 28 0 "
            "C 39 0 47 8 50 16 C 53 8 61 0 72 0 C 86 0 100 11 100 28 "
            "C 100 50 80 72 50 92 Z",
            100.0,
            100.0,
        )
    if prst == "arc":
        return "M 10 90 A 40 40 0 1 1 90 10", 100.0, 100.0
    if prst == "line":
        return "M 0 0 L 100 100", 100.0, 100.0
    return None


def render_shape_vector(
    shape: ET.Element,
    parent_matrix: tuple[float, float, float, float, float, float],
    theme_colors: dict[str, str],
) -> str:
    sp_pr = shape.find("p:spPr", NS)
    if sp_pr is None:
        return ""

    cust_geom = sp_pr.find("a:custGeom", NS)
    prst_geom = sp_pr.find("a:prstGeom", NS)

    if cust_geom is not None:
        path_data, local_width, local_height = build_custom_geom_path(cust_geom)
    elif prst_geom is not None:
        preset = build_preset_path(prst_geom.attrib.get("prst", ""))
        if preset is None:
            path_data = ""
            local_width = local_height = 1.0
        else:
            path_data, local_width, local_height = preset
    else:
        path_data = ""
        local_width = local_height = 1.0

    xfrm = get_xfrm(shape, "p:spPr")
    shape_matrix = matrix_multiply(parent_matrix, parse_shape_matrix(xfrm, local_width, local_height))

    fragments: list[str] = []
    if path_data:
        style = get_fill_style(sp_pr, theme_colors)
        style.update(get_line_style(sp_pr, theme_colors))
        if has_visible_paint(style):
            fragments.append(
                f'<path d="{xml_escape(path_data)}" transform="{matrix_to_svg(shape_matrix)}" {style_to_svg(style)} />'
            )

    return "".join(fragments)


def render_connector(
    connector: ET.Element,
    parent_matrix: tuple[float, float, float, float, float, float],
    theme_colors: dict[str, str],
) -> str:
    sp_pr = connector.find("p:spPr", NS)
    if sp_pr is None:
        return ""

    xfrm = get_xfrm(connector, "p:spPr")
    matrix = matrix_multiply(parent_matrix, parse_shape_matrix(xfrm, 100.0, 100.0))
    style = {"fill": "none"}
    style.update(get_line_style(sp_pr, theme_colors))
    if not has_visible_paint(style):
        return ""
    return f'<path d="M 0 0 L 100 100" transform="{matrix_to_svg(matrix)}" {style_to_svg(style)} />'


def render_picture(
    picture: ET.Element,
    parent_matrix: tuple[float, float, float, float, float, float],
    relationships: dict[str, str],
    slide_path: str,
    zip_file: zipfile.ZipFile,
) -> str:
    blip = picture.find("p:blipFill/a:blip", NS)
    if blip is None:
        return ""

    image_rel_id = blip.attrib.get(f"{{{NS['r']}}}embed")
    if not image_rel_id:
        return ""

    target = relationships.get(image_rel_id)
    if not target:
        return ""

    image_part = resolve_target(slide_path, target)
    try:
        image_bytes = zip_file.read(image_part)
    except KeyError:
        return ""

    svg_blip = blip.find("a:extLst/a:ext/asvg:svgBlip", NS)
    xfrm = get_xfrm(picture, "p:spPr")
    matrix = matrix_multiply(parent_matrix, parse_shape_matrix(xfrm, 1.0, 1.0))

    if svg_blip is not None:
        svg_rel_id = svg_blip.attrib.get(f"{{{NS['r']}}}embed")
        if svg_rel_id and svg_rel_id in relationships:
            svg_part = resolve_target(slide_path, relationships[svg_rel_id])
            try:
                svg_markup = zip_file.read(svg_part).decode("utf-8")
                return f'<g transform="{matrix_to_svg(matrix)}">{svg_markup}</g>'
            except Exception:
                pass

    ext = image_part.split(".")[-1].lower()
    mime_map = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif"}
    mime_type = mime_map.get(ext, "application/octet-stream")
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return (
        f'<image x="0" y="0" width="1" height="1" preserveAspectRatio="none" '
        f'transform="{matrix_to_svg(matrix)}" href="data:{mime_type};base64,{encoded}" />'
    )


def line_style_from_ln(ln: ET.Element | None, theme_colors: dict[str, str]) -> dict[str, str]:
    if ln is None or ln.find("a:noFill", NS) is not None:
        return {"stroke": "none"}

    color_node = None
    if ln.find("a:solidFill", NS) is not None:
        color_node = ln.find("a:solidFill", NS)
    else:
        for child in ln:
            if child.tag.split("}")[-1] in {"schemeClr", "srgbClr", "sysClr"}:
                color_node = child
                break
    color, opacity = resolve_color_node(color_node, theme_colors)
    width_emu = float(ln.attrib.get("w", "12700"))
    style = {
        "stroke": color or "#000000",
        "stroke-width": f"{width_emu / EMU_PER_PT:.3f}",
        "stroke-linecap": "round" if ln.find("a:round", NS) is not None else "butt",
        "fill": "none",
    }
    if opacity < 1.0:
        style["stroke-opacity"] = f"{opacity:.4f}"
    return style


def render_table(
    graphic_frame: ET.Element,
    parent_matrix: tuple[float, float, float, float, float, float],
    theme_colors: dict[str, str],
) -> str:
    tbl = graphic_frame.find("a:graphic/a:graphicData/a:tbl", NS)
    xfrm = graphic_frame.find("p:xfrm", NS)
    if tbl is None or xfrm is None:
        return ""

    grid_cols = tbl.findall("a:tblGrid/a:gridCol", NS)
    rows = tbl.findall("a:tr", NS)
    total_width = sum(float(col.attrib.get("w", "0")) for col in grid_cols) or 1.0
    total_height = sum(float(row.attrib.get("h", "0")) for row in rows) or 1.0
    matrix = matrix_multiply(parent_matrix, parse_shape_matrix(xfrm, total_width, total_height))

    fragments = [f'<g transform="{matrix_to_svg(matrix)}">']
    y = 0.0
    for row in rows:
        row_height = float(row.attrib.get("h", "0"))
        x = 0.0
        cells = row.findall("a:tc", NS)
        for col_index, cell in enumerate(cells):
            col_width = float(grid_cols[col_index].attrib.get("w", "0")) if col_index < len(grid_cols) else 0.0
            tc_pr = cell.find("a:tcPr", NS)

            fill_style = {"fill": "none"}
            if tc_pr is not None and tc_pr.find("a:solidFill", NS) is not None:
                color, opacity = resolve_color_node(tc_pr.find("a:solidFill", NS), theme_colors)
                fill_style = {"fill": color or "none"}
                if opacity < 1.0:
                    fill_style["fill-opacity"] = f"{opacity:.4f}"
            if has_visible_paint(fill_style):
                fragments.append(
                    f'<rect x="{x:.3f}" y="{y:.3f}" width="{col_width:.3f}" height="{row_height:.3f}" {style_to_svg(fill_style)} />'
                )

            if tc_pr is not None:
                line_specs = [
                    ("lnL", x, y, x, y + row_height),
                    ("lnR", x + col_width, y, x + col_width, y + row_height),
                    ("lnT", x, y, x + col_width, y),
                    ("lnB", x, y + row_height, x + col_width, y + row_height),
                ]
                for name, x1, y1, x2, y2 in line_specs:
                    line_el = tc_pr.find(f"a:{name}", NS)
                    style = line_style_from_ln(line_el, theme_colors)
                    if style.get("stroke") != "none":
                        fragments.append(
                            f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" {style_to_svg(style)} />'
                        )

            x += col_width
        y += row_height

    if len(fragments) == 1:
        return ""
    fragments.append("</g>")
    return "".join(fragments)


def render_group(
    group: ET.Element,
    parent_matrix: tuple[float, float, float, float, float, float],
    relationships: dict[str, str],
    slide_path: str,
    zip_file: zipfile.ZipFile,
    theme_colors: dict[str, str],
) -> str:
    xfrm = get_xfrm(group, "p:grpSpPr")
    group_matrix = matrix_multiply(parent_matrix, parse_group_matrix(xfrm))
    parts: list[str] = []

    for child in group:
        local = child.tag.split("}")[-1]
        if local in {"nvGrpSpPr", "grpSpPr"}:
            continue
        parts.append(
            render_drawable(child, group_matrix, relationships, slide_path, zip_file, theme_colors)
        )
    return "".join(parts)


def render_drawable(
    element: ET.Element,
    parent_matrix: tuple[float, float, float, float, float, float],
    relationships: dict[str, str],
    slide_path: str,
    zip_file: zipfile.ZipFile,
    theme_colors: dict[str, str],
) -> str:
    local = element.tag.split("}")[-1]
    if local == "sp":
        return render_shape_vector(element, parent_matrix, theme_colors)
    if local == "cxnSp":
        return render_connector(element, parent_matrix, theme_colors)
    if local == "pic":
        return render_picture(element, parent_matrix, relationships, slide_path, zip_file)
    if local == "grpSp":
        return render_group(element, parent_matrix, relationships, slide_path, zip_file, theme_colors)
    if local == "graphicFrame":
        return render_table(element, parent_matrix, theme_colors)
    return ""


def top_level_drawables(slide_root: ET.Element) -> list[ET.Element]:
    sp_tree = slide_root.find("p:cSld/p:spTree", NS)
    if sp_tree is None:
        return []

    items: list[ET.Element] = []
    for child in sp_tree:
        local = child.tag.split("}")[-1]
        if local in {"nvGrpSpPr", "grpSpPr"}:
            continue
        items.append(child)
    return items


def element_name(element: ET.Element) -> str:
    local = element.tag.split("}")[-1]
    if local == "grpSp":
        c_nv_pr = element.find("p:nvGrpSpPr/p:cNvPr", NS)
    elif local == "graphicFrame":
        c_nv_pr = element.find("p:nvGraphicFramePr/p:cNvPr", NS)
    elif local == "pic":
        c_nv_pr = element.find("p:nvPicPr/p:cNvPr", NS)
    elif local == "cxnSp":
        c_nv_pr = element.find("p:nvCxnSpPr/p:cNvPr", NS)
    else:
        c_nv_pr = element.find("p:nvSpPr/p:cNvPr", NS)
    return c_nv_pr.attrib.get("name", local) if c_nv_pr is not None else local


def element_bbox(element: ET.Element) -> tuple[float, float, float, float] | None:
    local = element.tag.split("}")[-1]
    if local == "grpSp":
        xfrm = get_xfrm(element, "p:grpSpPr")
    elif local == "graphicFrame":
        xfrm = element.find("p:xfrm", NS)
    else:
        xfrm = get_xfrm(element, "p:spPr")
    if xfrm is None:
        return None

    off = xfrm.find("a:off", NS)
    ext = xfrm.find("a:ext", NS)
    if off is None or ext is None:
        return None

    x = float(off.attrib.get("x", "0"))
    y = float(off.attrib.get("y", "0"))
    cx = float(ext.attrib.get("cx", "0"))
    cy = float(ext.attrib.get("cy", "0"))
    if cx <= 0 or cy <= 0:
        return None
    return x, y, cx, cy


def is_meaningful(element: ET.Element) -> bool:
    local = element.tag.split("}")[-1]
    if local in {"pic", "grpSp", "cxnSp"}:
        return True
    if local == "graphicFrame":
        return element.find("a:graphic/a:graphicData/a:tbl", NS) is not None
    if local != "sp":
        return False
    return element.find("p:spPr/a:prstGeom", NS) is not None or element.find("p:spPr/a:custGeom", NS) is not None


def write_svg(path: Path, width: float, height: float, inner_markup: str) -> None:
    width_px = max(width / EMU_PER_PT, 1.0)
    height_px = max(height / EMU_PER_PT, 1.0)
    svg = (
        f"{SVG_HEADER}\n"
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width_px:.3f}px" height="{height_px:.3f}px" '
        f'viewBox="0 0 {width:.3f} {height:.3f}">\n'
        f'{inner_markup}\n'
        f"</svg>\n"
    )
    path.write_text(svg, encoding="utf-8")


def export_pptx(pptx_path: Path, output_root: Path) -> dict:
    deck_output = output_root / pptx_path.stem
    deck_output.mkdir(parents=True, exist_ok=True)

    manifest_entries = []
    stats = Counter()

    with zipfile.ZipFile(pptx_path) as zip_file:
        theme_colors = parse_theme_colors(zip_file)
        slide_paths = sorted(
            [name for name in zip_file.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml")],
            key=slide_sort_key,
        )

        for slide_path in slide_paths:
            slide_no = slide_sort_key(slide_path)[0]
            rels_path = f"ppt/slides/_rels/slide{slide_no}.xml.rels"
            relationships = load_relationships(zip_file, rels_path)
            slide_root = ET.fromstring(zip_file.read(slide_path))
            drawables = top_level_drawables(slide_root)
            stats["slides"] += 1

            for index, drawable in enumerate(drawables, start=1):
                stats["top_level_elements"] += 1
                if not is_meaningful(drawable):
                    stats["skipped_non_meaningful"] += 1
                    continue

                bbox = element_bbox(drawable)
                if bbox is None:
                    stats["skipped_missing_bbox"] += 1
                    continue

                x, y, cx, cy = bbox
                inner = render_drawable(
                    drawable,
                    translate(-x, -y),
                    relationships,
                    slide_path,
                    zip_file,
                    theme_colors,
                )
                if not inner.strip():
                    stats["skipped_empty_render"] += 1
                    continue

                local = drawable.tag.split("}")[-1]
                out_name = (
                    f"slide{slide_no:03d}_elem{index:03d}_{sanitize_filename(element_name(drawable))}.svg"
                )
                out_path = deck_output / out_name
                write_svg(out_path, cx, cy, inner)
                stats["exported_elements"] += 1
                stats[f"exported_{local}"] += 1

                manifest_entries.append(
                    {
                        "slide": slide_no,
                        "element_index": index,
                        "element_type": local,
                        "element_name": element_name(drawable),
                        "output_file": str(out_path.relative_to(output_root.parent)),
                    }
                )

    manifest_path = deck_output / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "pptx": str(pptx_path),
                "output_dir": str(deck_output),
                "stats": dict(stats),
                "exports": manifest_entries,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    return {
        "pptx": str(pptx_path),
        "output_dir": str(deck_output),
        "manifest": str(manifest_path),
        "stats": dict(stats),
    }


def main() -> int:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pptx_files = sorted(
        path for path in input_dir.glob("*.pptx") if not path.name.startswith("~$")
    )
    if not pptx_files:
        print(f"No .pptx files found in {input_dir}")
        return 1

    results = []
    totals = Counter()
    bad_files: list[dict[str, str]] = []
    for pptx_path in pptx_files:
        try:
            result = export_pptx(pptx_path, output_dir)
        except zipfile.BadZipFile as exc:
            bad_files.append({"pptx": str(pptx_path), "error": str(exc)})
            print(f"{pptx_path.name}: skipped_bad_zip={exc}")
            continue

        results.append(result)
        totals.update(result["stats"])
        stats = result["stats"]
        print(
            f"{pptx_path.name}: exported={stats.get('exported_elements', 0)} "
            f"skipped={stats.get('skipped_non_meaningful', 0) + stats.get('skipped_missing_bbox', 0) + stats.get('skipped_empty_render', 0)}"
        )

    summary_path = output_dir / "summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "input_dir": str(input_dir),
                "output_dir": str(output_dir),
                "totals": dict(totals),
                "bad_files": bad_files,
                "files": results,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"TOTAL: exported={totals.get('exported_elements', 0)} "
        f"slides={totals.get('slides', 0)} "
        f"top_level_elements={totals.get('top_level_elements', 0)}"
    )
    print(f"Summary written to {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
