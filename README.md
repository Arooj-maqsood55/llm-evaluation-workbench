# LLM Evaluation Workbench

Python CLI for rubric scoring of paired model answers with structured JSON/CSV reports.

**Timeline:** Freelance LLM evaluation work — 2026

## Usage

```bash
python3 src/scorer.py samples/pairs.json --out-json report.json --out-csv report.csv
python3 -m unittest tests/test_scorer.py
```
