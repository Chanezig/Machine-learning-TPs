"""Lecture et inspection du jeu de données Telco Customer Churn.

Ce module ne modifie JAMAIS les données : il lit et il mesure.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

TARGET = "Churn"
ID_COLUMN = "customerID"


def sha256_of_file(path: Path) -> str:
    """Hash SHA-256 des octets du fichier (preuve d'identité de la source)."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_raw(path: Path) -> pd.DataFrame:
    """Lit le CSV tel quel (aucun nettoyage, aucun cast)."""
    return pd.read_csv(path)


def missing_report(df: pd.DataFrame) -> dict:
    """Compte, par colonne, les NaN et les valeurs vides / espaces seulement."""
    report = {}
    for col in df.columns:
        as_text = df[col].astype("string")
        report[col] = {
            "isna": int(df[col].isna().sum()),
            "empty_or_whitespace": int(as_text.str.strip().eq("").sum()),
        }
    return report


def target_report(df: pd.DataFrame) -> dict:
    counts = df[TARGET].value_counts(dropna=False)
    proportions = df[TARGET].value_counts(normalize=True, dropna=False)
    return {
        "counts": {str(k): int(v) for k, v in counts.items()},
        "proportions": {str(k): round(float(v), 4) for k, v in proportions.items()},
    }


def environment_info() -> dict:
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "pandas_version": importlib.metadata.version("pandas"),
    }


def build_report(path: Path) -> dict:
    """Assemble le rapport d'inspection complet."""
    path = Path(path)
    df = load_raw(path)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "path": str(path),
            "sha256": sha256_of_file(path),
            "size_bytes": path.stat().st_size,
        },
        "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "target": target_report(df),
        "duplicate_customer_ids": int(df[ID_COLUMN].duplicated().sum()),
        "missing_values": missing_report(df),
        "environment": environment_info(),
    }