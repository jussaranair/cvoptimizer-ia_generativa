"""SQLite helper module for CV Optimizer.

Provides functions to create tables and perform basic CRUD operations
for `resumes` and `analyses` tables.

Usage:
    from src import cv_database
    cv_database.create_tables()
    resume_id = cv_database.insert_resume('Name', 'email@example.com', '/path/to/file')
    analysis_id = cv_database.insert_analysis(resume_id, 8.5, 9.0, 7.0, 8.0, ['python', 'sql'])
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "cvoptimizer.db"


def _get_db_path(db_path: Optional[str | Path]) -> Path:
    return Path(db_path) if db_path else DEFAULT_DB_PATH


def _get_connection(db_path: Optional[str | Path] = None) -> sqlite3.Connection:
    path = _get_db_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {k: row[k] for k in row.keys()}


def create_tables(db_path: Optional[str | Path] = None) -> None:
    """Create `resumes` and `analyses` tables if they don't exist."""
    with _get_connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            upload_date TEXT NOT NULL,
            file_path TEXT NOT NULL
        );
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER NOT NULL,
            summary_score REAL,
            experience_score REAL,
            skills_score REAL,
            education_score REAL,
            keywords_missing TEXT,
            analysis_date TEXT NOT NULL,
            FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
        );
        """
        )
        conn.commit()


def insert_resume(name: str, email: Optional[str], file_path: str, db_path: Optional[str | Path] = None) -> int:
    """Insert a resume and return the new resume id."""
    upload_date = datetime.utcnow().isoformat()
    with _get_connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO resumes (name, email, upload_date, file_path) VALUES (?, ?, ?, ?)",
            (name, email, upload_date, file_path),
        )
        conn.commit()
        return cur.lastrowid


def insert_analysis(
    resume_id: int,
    summary_score: Optional[float],
    experience_score: Optional[float],
    skills_score: Optional[float],
    education_score: Optional[float],
    keywords_missing: Optional[List[str] | str],
    db_path: Optional[str | Path] = None,
) -> int:
    """Insert an analysis row and return the new analysis id.

    `keywords_missing` may be a list of strings or a pre-serialized JSON string.
    """
    if isinstance(keywords_missing, list):
        km_serialized = json.dumps(keywords_missing)
    else:
        km_serialized = keywords_missing if keywords_missing is not None else None

    analysis_date = datetime.utcnow().isoformat()
    with _get_connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
        INSERT INTO analyses (
            resume_id, summary_score, experience_score, skills_score, education_score, keywords_missing, analysis_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                resume_id,
                summary_score,
                experience_score,
                skills_score,
                education_score,
                km_serialized,
                analysis_date,
            ),
        )
        conn.commit()
        return cur.lastrowid


def get_all_resumes(db_path: Optional[str | Path] = None) -> List[Dict[str, Any]]:
    """Return a list of all resumes as dictionaries, newest first."""
    with _get_connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM resumes ORDER BY upload_date DESC")
        rows = cur.fetchall()
        return [_row_to_dict(r) for r in rows]


def get_analyses_for_resume(resume_id: int, db_path: Optional[str | Path] = None) -> List[Dict[str, Any]]:
    """Return all analyses for the given `resume_id` as dictionaries, newest first.

    `keywords_missing` will be returned as a Python list if it was stored as JSON.
    """
    with _get_connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM analyses WHERE resume_id = ? ORDER BY analysis_date DESC", (resume_id,)
        )
        rows = cur.fetchall()
        results: List[Dict[str, Any]] = []
        for r in rows:
            d = _row_to_dict(r)
            km = d.get("keywords_missing")
            if isinstance(km, str) and km:
                try:
                    d["keywords_missing"] = json.loads(km)
                except json.JSONDecodeError:
                    d["keywords_missing"] = km
            results.append(d)
        return results


if __name__ == "__main__":
    # Quick sanity check when run as a script
    create_tables()
    print("Tables ensured. DB:", DEFAULT_DB_PATH)
