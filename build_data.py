#!/usr/bin/env python3
"""
Regenerate data/consolidated.jsonl from the source CAPS syllabus dataset.

The viewer (index.html) parses each row of the consolidated file and reads
the `completion` field, which is a CAPS syllabus JSON object
(documentMeta -> contentAreas -> topics -> subtopics -> assessment). It builds
the knowledge graph from that structure.

The source rows are the per-subject files in source-dataset/ (each extracted
from a DBE CAPS PDF via the pipeline described in DATASET.md). This script just
concatenates them in a stable order and writes data/consolidated.jsonl.

Usage:
    python3 build_data.py
"""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(HERE, "source-dataset")
OUT = os.path.join(HERE, "data", "consolidated.jsonl")

# Stable, human-meaningful ordering (subject phase, then grade band).
ORDER = [
    "CAPS_MATHS_GR-R",
    "CAPS_MATHS_GR1-3_FS",
    "CAPS_MATHS_GR4-6_IP",
    "CAPS_MATHS_GR7-9_SP",
    "CAPS_MATHS_GR10-12_FET",
    "CAPS_MATH-LIT-GR10-12",
    "CAPS_TECH-MATHS-GR10-12",
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    rows = []
    for name in ORDER:
        path = os.path.join(SRC_DIR, name + ".jsonl")
        if not os.path.exists(path):
            print(f"! missing {path} — skipped")
            continue
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                # basic validation: every row must carry an id + completion
                if "id" not in obj or "completion" not in obj:
                    raise SystemExit(f"Bad row in {path}: missing id/completion")
                rows.append(obj)

    if not rows:
        raise SystemExit("No source rows found in source-dataset/")

    with open(OUT, "w", encoding="utf-8") as f:
        for obj in rows:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    print(f"Wrote {len(rows)} rows -> {OUT}")


if __name__ == "__main__":
    main()
