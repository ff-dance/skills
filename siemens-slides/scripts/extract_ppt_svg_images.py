#!/usr/bin/env python3

import argparse
import json
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract original SVG-backed picture elements from PPTX files."
    )
    parser.add_argument(
        "--input-dir",
        default="assets/raw",
        help="Directory containing .pptx files.",
    )
    parser.add_argument(
        "--output-dir",
        default="tmp/exported-svg",
        help="Directory where exported SVGs will be written.",
    )
    return parser.parse_args()


def sanitize_filename(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    cleaned = cleaned.strip("._")
    return cleaned or "unnamed"


def part_label(path: str) -> str:
    match = re.search(
        r"ppt/(slides/slide|slideLayouts/slideLayout|slideMasters/slideMaster|handoutMasters/handoutMaster|notesMasters/notesMaster)(\d+)\.xml$",
        path,
    )
    if not match:
        return sanitize_filename(Path(path).stem)

    raw_kind, index = match.groups()
    kind_map = {
        "slides/slide": "slide",
        "slideLayouts/slideLayout": "layout",
        "slideMasters/slideMaster": "master",
        "handoutMasters/handoutMaster": "handout",
        "notesMasters/notesMaster": "notes-master",
    }
    return f"{kind_map[raw_kind]}{int(index):03d}"


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


def extract_svg_elements(pptx_path: Path, output_root: Path) -> dict:
    deck_output_dir = output_root / pptx_path.stem
    deck_output_dir.mkdir(parents=True, exist_ok=True)

    manifest_entries = []
    filename_counts: Counter[str] = Counter()
    stats = Counter()

    with zipfile.ZipFile(pptx_path) as zip_file:
        candidate_parts = sorted(
            [
                name
                for name in zip_file.namelist()
                if name.endswith(".xml")
                and (
                    name.startswith("ppt/slides/slide")
                    or name.startswith("ppt/slideLayouts/slideLayout")
                    or name.startswith("ppt/slideMasters/slideMaster")
                    or name.startswith("ppt/handoutMasters/handoutMaster")
                    or name.startswith("ppt/notesMasters/notesMaster")
                )
            ],
            key=slide_sort_key,
        )

        for part_path in candidate_parts:
            rels_path = (
                f"{posixpath.dirname(part_path)}/_rels/{posixpath.basename(part_path)}.rels"
            )
            relationships = load_relationships(zip_file, rels_path)
            part_root = ET.fromstring(zip_file.read(part_path))
            part_name = part_label(part_path)

            for pic in part_root.findall(".//p:pic", NS):
                stats["picture_elements"] += 1
                nv_props = pic.find("p:nvPicPr/p:cNvPr", NS)
                pic_name = nv_props.attrib.get("name", "") if nv_props is not None else ""
                pic_id = nv_props.attrib.get("id", "") if nv_props is not None else ""

                svg_blip = pic.find(".//asvg:svgBlip", NS)
                if svg_blip is None:
                    stats["skipped_non_svg"] += 1
                    continue

                rel_id = svg_blip.attrib.get(f"{{{NS['r']}}}embed")
                if not rel_id:
                    stats["skipped_missing_rel"] += 1
                    continue

                target = relationships.get(rel_id)
                if not target:
                    stats["skipped_missing_target"] += 1
                    continue

                svg_part = resolve_target(part_path, target)
                if not svg_part.endswith(".svg"):
                    stats["skipped_non_svg_target"] += 1
                    continue

                try:
                    svg_bytes = zip_file.read(svg_part)
                except KeyError:
                    stats["skipped_missing_part"] += 1
                    continue

                name_parts = [
                    part_name,
                    f"pic{pic_id or '0'}",
                    sanitize_filename(pic_name or "image"),
                ]
                base_name = "_".join(name_parts) + ".svg"
                filename_counts[base_name] += 1
                if filename_counts[base_name] > 1:
                    stem = base_name[:-4]
                    base_name = f"{stem}__{filename_counts[base_name]}.svg"

                out_path = deck_output_dir / base_name
                out_path.write_bytes(svg_bytes)
                stats["exported_svg_elements"] += 1

                manifest_entries.append(
                    {
                        "part": part_path,
                        "part_label": part_name,
                        "shape_id": pic_id,
                        "shape_name": pic_name,
                        "source_part": svg_part,
                        "output_file": str(out_path.relative_to(output_root.parent)),
                    }
                )

    manifest_path = deck_output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "pptx": str(pptx_path),
                "output_dir": str(deck_output_dir),
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
        "output_dir": str(deck_output_dir),
        "manifest": str(manifest_path),
        "stats": dict(stats),
    }


def main() -> int:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pptx_files = sorted(input_dir.glob("*.pptx"))
    if not pptx_files:
        print(f"No .pptx files found in {input_dir}")
        return 1

    summary = []
    totals = Counter()

    for pptx_path in pptx_files:
        result = extract_svg_elements(pptx_path, output_dir)
        summary.append(result)
        totals.update(result["stats"])

    summary_path = output_dir / "summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "input_dir": str(input_dir),
                "output_dir": str(output_dir),
                "totals": dict(totals),
                "files": summary,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    for item in summary:
        stats = item["stats"]
        print(
            f"{Path(item['pptx']).name}: "
            f"exported={stats.get('exported_svg_elements', 0)} "
            f"skipped_non_svg={stats.get('skipped_non_svg', 0)}"
        )

    print(
        f"TOTAL: exported={totals.get('exported_svg_elements', 0)} "
        f"skipped_non_svg={totals.get('skipped_non_svg', 0)}"
    )
    print(f"Summary written to {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
