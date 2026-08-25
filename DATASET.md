# CAPS Syllabus Pipeline — Dataset Factory

Runs on **Alfred** (the Linux host, `alfred`). Produces training pairs for the local 2B student model that runs on the Windows PC with the RTX 4050.

## Directory layout

```
/opt/ai-stack/SmartChalk/caps-dataset/
  raw_pdfs/       — source CAPS PDFs (download + store)
  extracted/      — one validated JSON per PDF (teacher output)
  dataset/        — consolidated JSONL training dataset
  schema/         — caps-schema.json (target contract for /api/curriculum-source)
  logs/           — per-doc run logs
```

## Flow

1. Download CAPS PDF(s) into `raw_pdfs/`
2. Extract text (pdftotext — PDFs are text-based, no OCR for these docs)
3. **Solar-4:free (teacher, cloud)** reads the cleaned text, emits schema-valid JSON → `extracted/`
4. Validate JSON against `caps-schema.json`
5. If valid: append one JSONL row (id, source_pdf, grade, subject, curriculum, prompt, completion, created_at) to `dataset/`
6. Log the run to `logs/`

After enough pairs accumulate, the Windows PC trains the local student via Unsloth QLoRA.

## Notes

- Telecoms: CAPS is SA public curriculum — low privacy risk to send to cloud API for extraction.
- The dataset lives on Alfred and is copied to the Windows PC when ready for training.
- The schema targets SmartChalk's `/api/curriculum-source` — when the endpoint is live, extracted JSON POSTs directly without a translation layer.
