# CAPS Syllabus Knowledge Graph

An interactive, self-contained knowledge-graph viewer for the **South African CAPS Mathematics syllabus** (Grades R–12: Mathematics, Technical Mathematics, Mathematical Literacy).

Built from the ground up with **zero external dependencies** — a single `index.html` that renders a Canvas-2D force-directed graph with a from-scratch physics simulation. No Three.js, no `force-graph`, no CDN. It runs on any modern browser, including mobile Firefox with **no WebGL**.

## Features

- **Progressive drill-down**: loads only the top tiers (documents + content areas), then *tap a node* to expand one level of children and focus it. Already-open nodes stay open, so you build the tree as deep as you like.
- **Auto-reflow**: every time you expand a node, the layout engine re-energizes so newly revealed nodes push apart instead of overlapping.
- **Click-to-focus**: tapping a node highlights it + its neighbors and opens a side panel listing every attached node (grouped by type), each clickable to drill further.
- **Drag to pin**: drag a node to reposition it; it sticks where you drop it. Right-click (desktop) or the **Pin** button pins it in place permanently.
- **2D / 3D toggle**: a pseudo-3D mode (perspective projection on the same Canvas2D — no WebGL) you can orbit by dragging empty space. Works on phones that can't do real WebGL.
- **Pan / zoom**: drag empty space to pan, scroll/pinch to zoom.
- **Per-subject + localStorage**: build a subject's graph on demand and cache it in the browser so reloads are instant.
- **Self-hosted or Vercel**: pure static files — drop it behind any web server or point Vercel at the repo.

## Quick start (local)

Open `index.html` from a static server (it fetches `data/consolidated.jsonl` relative to the page):

```bash
# from the repo root
python3 -m http.server 8080
# then visit http://localhost:8080/   (note the trailing slash)
```

Or just open `index.html` in a browser if your server serves it at a path ending in `/`.

## The dataset

The graph is derived entirely from the **CAPS syllabus dataset** (`source-dataset/*.jsonl`). Each row is a structured extraction of a DBE CAPS PDF:

```
{ id, source_pdf, grade, subject, curriculum, standard, prompt, completion, created_at }
```

The viewer parses each row's `completion` field (a CAPS syllabus JSON: `documentMeta` → `contentAreas` → `topics` → `subtopics` → `assessment`) and turns it into graph nodes and links. Nothing is hand-authored — the graph *is* the dataset.

The pipeline that produced it (raw PDFs → text → schema-valid JSON → consolidated JSONL) is documented in [`DATASET.md`](./DATASET.md); the target schema is in [`schema/caps-schema.json`](./schema/caps-schema.json).

### Regenerating the data file

`data/consolidated.jsonl` is the concatenation of the per-subject files in `source-dataset/`, in a stable order. To regenerate (e.g. after adding a new subject):

```bash
python3 build_data.py
```

This is deterministic: regenerating from the committed `source-dataset/` always produces an identical `data/consolidated.jsonl`.

> **Provenance / licensing**: CAPS is the South African national curriculum, published by the Department of Basic Education. The extracted syllabus text is public curriculum content. The structured dataset here is released for educational and non-commercial use under [CC BY 4.0](./LICENSE) — attribute the Department of Basic Education, Republic of South Africa. The viewer code (this repo, excluding the dataset) is MIT.

## Deploy to Vercel

This is a static site. Two ways:

1. **Import on Vercel**: link your GitHub account, import this repository. Vercel auto-detects it as a static site (see `vercel.json`) and builds with no framework.
2. **Vercel CLI**:
   ```bash
   npm i -g vercel
   vercel
   ```

The build output is the repo root served as-is. No build step is required (the `vercel.json` has an empty build command and serves the directory).

## Controls

| Action | Mouse (desktop) | Touch (mobile) |
| --- | --- | --- |
| Expand node + focus | Click | Tap |
| Collapse node's children | Double-click | Double-tap |
| Drag / reposition node | Drag | Tap-hold + drag |
| Pin/unpin node | Right-click | Select node → **Pin** button |
| Pan canvas | Drag empty space | Drag empty space |
| Orbit (3D mode) | Drag empty space | Drag empty space |
| Zoom | Scroll | Pinch |
| Clear focus | Click empty space | Tap empty space |

Toolbar (top-left): **2D/3D** toggle · **Expand all** · **Collapse** · **Pin** · **Fit**.

## Technical notes

- Force simulation: velocity-Verlet with O(n²) repulsion + Hooke-spring links + centering force, alpha decay to rest. For the full ~647-node graph this is fine on desktop; on mobile, drill down progressively (the default) to keep node counts small and the layout snappy.
- Rendering: `canvas.getContext('2d')`, DPR-aware, requestAnimationFrame loop.
- No analytics, no network calls except fetching `data/consolidated.jsonl`.
