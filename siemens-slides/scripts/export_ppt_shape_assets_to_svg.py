#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_SCRIPT = SCRIPT_DIR / "export_ppt_slide_elements_to_svg.py"
spec = importlib.util.spec_from_file_location("export_ppt_slide_elements_to_svg", BASE_SCRIPT)
base = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = base
spec.loader.exec_module(base)


NS = base.NS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export reusable PPT shape assets to SVG."
    )
    parser.add_argument("--input-dir", default="assets/raw")
    parser.add_argument("--output-dir", default="tmp/reference-components/shape-assets")
    parser.add_argument(
        "--exclude-geoms",
        default="rect,roundRect",
        help="Comma-separated preset geometry names to skip.",
    )
    return parser.parse_args()


def slide_paths(zip_file: zipfile.ZipFile) -> list[str]:
    return sorted(
        [name for name in zip_file.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
        key=lambda value: int(re.search(r"slide(\d+)\.xml$", value).group(1)),
    )


def shape_text(element: ET.Element) -> str:
    return "".join(node.text or "" for node in element.findall(".//a:t", NS)).strip()


def shape_kind(shape: ET.Element) -> str:
    sp_pr = shape.find("p:spPr", NS)
    if sp_pr is None:
        return ""
    prst = sp_pr.find("a:prstGeom", NS)
    if prst is not None:
        return prst.attrib.get("prst", "")
    if sp_pr.find("a:custGeom", NS) is not None:
        return "custGeom"
    return ""


def connector_kind(_: ET.Element) -> str:
    return "connector"


def visible_shape_render(shape: ET.Element, theme_colors: dict[str, str]) -> str:
    sp_pr = shape.find("p:spPr", NS)
    if sp_pr is None:
        return ""
    xfrm = sp_pr.find("a:xfrm", NS)
    if xfrm is None:
        return ""
    off = xfrm.find("a:off", NS)
    if off is None:
        return ""
    x = float(off.attrib.get("x", "0"))
    y = float(off.attrib.get("y", "0"))
    return base.render_shape_vector(shape, base.translate(-x, -y), theme_colors)


def visible_connector_render(connector: ET.Element, theme_colors: dict[str, str]) -> str:
    sp_pr = connector.find("p:spPr", NS)
    if sp_pr is None:
        return ""
    xfrm = sp_pr.find("a:xfrm", NS)
    if xfrm is None:
        return ""
    off = xfrm.find("a:off", NS)
    if off is None:
        return ""
    x = float(off.attrib.get("x", "0"))
    y = float(off.attrib.get("y", "0"))
    return base.render_connector(connector, base.translate(-x, -y), theme_colors)


def element_bbox(element: ET.Element) -> tuple[float, float]:
    sp_pr = element.find("p:spPr", NS)
    if sp_pr is None:
        return 0.0, 0.0
    xfrm = sp_pr.find("a:xfrm", NS)
    if xfrm is None:
        return 0.0, 0.0
    ext = xfrm.find("a:ext", NS)
    if ext is None:
        return 0.0, 0.0
    return float(ext.attrib.get("cx", "0")), float(ext.attrib.get("cy", "0"))


def element_name(element: ET.Element, local_name: str) -> str:
    if local_name == "cxnSp":
        c_nv_pr = element.find("p:nvCxnSpPr/p:cNvPr", NS)
    else:
        c_nv_pr = element.find("p:nvSpPr/p:cNvPr", NS)
    return c_nv_pr.attrib.get("name", local_name) if c_nv_pr is not None else local_name


def element_id(element: ET.Element, local_name: str) -> str:
    if local_name == "cxnSp":
        c_nv_pr = element.find("p:nvCxnSpPr/p:cNvPr", NS)
    else:
        c_nv_pr = element.find("p:nvSpPr/p:cNvPr", NS)
    return c_nv_pr.attrib.get("id", "0") if c_nv_pr is not None else "0"


def document_svg(width: float, height: float, inner_markup: str) -> str:
    width_px = max(width / base.EMU_PER_PT, 1.0)
    height_px = max(height / base.EMU_PER_PT, 1.0)
    return (
        f"{base.SVG_HEADER}\n"
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width_px:.3f}px" height="{height_px:.3f}px" '
        f'viewBox="0 0 {width:.3f} {height:.3f}">\n'
        f"{inner_markup}\n"
        f"</svg>\n"
    )


def should_export_shape(shape: ET.Element, excluded_geoms: set[str]) -> bool:
    kind = shape_kind(shape)
    if not kind or kind in excluded_geoms:
        return False
    if shape_text(shape):
        return False
    cx, cy = element_bbox(shape)
    if cx <= 0 and cy <= 0:
        return False
    if kind != "line" and (cx <= 0 or cy <= 0):
        return False
    return True


def should_export_connector(connector: ET.Element) -> bool:
    cx, cy = element_bbox(connector)
    return cx > 0 or cy > 0


def export_pptx(
    pptx_path: Path,
    output_root: Path,
    excluded_geoms: set[str],
) -> dict:
    deck_output = output_root / pptx_path.stem
    deck_output.mkdir(parents=True, exist_ok=True)

    manifest_entries = []
    duplicate_entries = []
    stats = {
        "slides": 0,
        "shape_candidates": 0,
        "connector_candidates": 0,
        "exported_assets": 0,
        "skipped_text_shapes": 0,
        "skipped_excluded_geom": 0,
        "skipped_empty_render": 0,
        "skipped_zero_size": 0,
        "skipped_duplicates": 0,
    }
    seen_hashes: dict[str, str] = {}

    with zipfile.ZipFile(pptx_path) as zip_file:
        theme_colors = base.parse_theme_colors(zip_file)
        for slide_path in slide_paths(zip_file):
            slide_no = int(re.search(r"slide(\d+)\.xml$", slide_path).group(1))
            stats["slides"] += 1
            slide_root = ET.fromstring(zip_file.read(slide_path))

            for shape in slide_root.findall(".//p:sp", NS):
                stats["shape_candidates"] += 1
                kind = shape_kind(shape)
                if shape_text(shape):
                    stats["skipped_text_shapes"] += 1
                    continue
                if not kind or kind in excluded_geoms:
                    stats["skipped_excluded_geom"] += 1
                    continue
                cx, cy = element_bbox(shape)
                if kind != "line" and (cx <= 0 or cy <= 0):
                    stats["skipped_zero_size"] += 1
                    continue
                if kind == "line" and cx <= 0 and cy <= 0:
                    stats["skipped_zero_size"] += 1
                    continue

                inner = visible_shape_render(shape, theme_colors)
                if not inner.strip():
                    stats["skipped_empty_render"] += 1
                    continue

                svg_text = document_svg(max(cx, 1.0), max(cy, 1.0), inner)
                digest = hashlib.sha256(svg_text.encode("utf-8")).hexdigest()
                if digest in seen_hashes:
                    stats["skipped_duplicates"] += 1
                    duplicate_entries.append(
                        {
                            "slide": slide_no,
                            "element_name": element_name(shape, "sp"),
                            "kind": kind,
                            "duplicate_of": seen_hashes[digest],
                        }
                    )
                    continue

                out_name = (
                    f"slide{slide_no:03d}_id{element_id(shape, 'sp')}_{kind}_{base.sanitize_filename(element_name(shape, 'sp'))}.svg"
                )
                out_path = deck_output / out_name
                out_path.write_text(svg_text, encoding="utf-8")
                seen_hashes[digest] = str(out_path.relative_to(output_root.parent))
                stats["exported_assets"] += 1
                manifest_entries.append(
                    {
                        "slide": slide_no,
                        "element_name": element_name(shape, "sp"),
                        "kind": kind,
                        "output_file": str(out_path.relative_to(output_root.parent)),
                    }
                )

            for connector in slide_root.findall(".//p:cxnSp", NS):
                stats["connector_candidates"] += 1
                if not should_export_connector(connector):
                    stats["skipped_zero_size"] += 1
                    continue

                inner = visible_connector_render(connector, theme_colors)
                if not inner.strip():
                    stats["skipped_empty_render"] += 1
                    continue

                cx, cy = element_bbox(connector)
                svg_text = document_svg(max(cx, 1.0), max(cy, 1.0), inner)
                digest = hashlib.sha256(svg_text.encode("utf-8")).hexdigest()
                if digest in seen_hashes:
                    stats["skipped_duplicates"] += 1
                    duplicate_entries.append(
                        {
                            "slide": slide_no,
                            "element_name": element_name(connector, "cxnSp"),
                            "kind": "connector",
                            "duplicate_of": seen_hashes[digest],
                        }
                    )
                    continue

                out_name = (
                    f"slide{slide_no:03d}_id{element_id(connector, 'cxnSp')}_connector_{base.sanitize_filename(element_name(connector, 'cxnSp'))}.svg"
                )
                out_path = deck_output / out_name
                out_path.write_text(svg_text, encoding="utf-8")
                seen_hashes[digest] = str(out_path.relative_to(output_root.parent))
                stats["exported_assets"] += 1
                manifest_entries.append(
                    {
                        "slide": slide_no,
                        "element_name": element_name(connector, "cxnSp"),
                        "kind": "connector",
                        "output_file": str(out_path.relative_to(output_root.parent)),
                    }
                )

    manifest_path = deck_output / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "pptx": str(pptx_path),
                "output_dir": str(deck_output),
                "stats": stats,
                "exports": manifest_entries,
                "duplicates": duplicate_entries,
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
        "stats": stats,
    }


def main() -> int:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    excluded_geoms = {
        item.strip() for item in args.exclude_geoms.split(",") if item.strip()
    }

    pptx_files = sorted(
        path for path in input_dir.glob("*.pptx") if not path.name.startswith("~$")
    )
    if not pptx_files:
        print(f"No .pptx files found in {input_dir}")
        return 1

    results = []
    totals = {
        "slides": 0,
        "shape_candidates": 0,
        "connector_candidates": 0,
        "exported_assets": 0,
        "skipped_text_shapes": 0,
        "skipped_excluded_geom": 0,
        "skipped_empty_render": 0,
        "skipped_zero_size": 0,
        "skipped_duplicates": 0,
    }

    for pptx_path in pptx_files:
        try:
            result = export_pptx(pptx_path, output_dir, excluded_geoms)
        except zipfile.BadZipFile as exc:
            print(f"{pptx_path.name}: skipped_bad_zip={exc}")
            continue

        results.append(result)
        for key, value in result["stats"].items():
            totals[key] = totals.get(key, 0) + value
        stats = result["stats"]
        print(
            f"{pptx_path.name}: exported={stats['exported_assets']} "
            f"duplicates={stats['skipped_duplicates']} "
            f"text_skipped={stats['skipped_text_shapes']}"
        )

    summary_path = output_dir / "summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "input_dir": str(input_dir),
                "output_dir": str(output_dir),
                "excluded_geoms": sorted(excluded_geoms),
                "totals": totals,
                "files": results,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"TOTAL: exported={totals['exported_assets']} "
        f"duplicates={totals['skipped_duplicates']} "
        f"shape_candidates={totals['shape_candidates']}"
    )
    print(f"Summary written to {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
