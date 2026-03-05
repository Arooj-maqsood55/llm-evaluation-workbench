import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORER = ROOT / "src" / "scorer.py"
SAMPLE = ROOT / "samples" / "pairs.json"


def test_cli_generates_reports():
    with tempfile.TemporaryDirectory() as tmp:
        out_json = Path(tmp) / "report.json"
        out_csv = Path(tmp) / "report.csv"
        result = subprocess.run(
            [sys.executable, str(SCORER), str(SAMPLE), "--out-json", str(out_json), "--out-csv", str(out_csv)],
            check=True,
            capture_output=True,
            text=True,
        )
        assert out_json.exists()
        assert out_csv.exists()
        rows = json.loads(out_json.read_text(encoding="utf-8"))
        assert rows[0]["preferred"] == "response_a"
        assert rows[1]["preferred"] == "tie"
        assert "Wrote" in result.stdout
