"""Génère reports/data_overview.json à partir du CSV brut.

Usage : uv run python scripts/inspect_data.py
"""
import argparse
import json
from pathlib import Path

from telco_churn.dataset import build_report

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspecte le CSV Telco.")
    parser.add_argument("--input", type=Path, default=ROOT / "data" / "raw" / "telco.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "reports" / "data_overview.json")
    args = parser.parse_args()

    report = build_report(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Rapport écrit : {args.output}")


if __name__ == "__main__":
    main()