from pathlib import Path
import sqlite3
from typing import Dict, Any, Optional, List
import pandas as pd
from functions.fileIO import Expected_Columns

_DB_PATH = Path("student_grades.db")
_TABLE_NAME = "grades"

def _get_conn(db_path: Optional[Path] = None) -> sqlite3.Connection:
    path = db_path or _DB_PATH
    conn = sqlite3.connect(path)
    return conn

def init_db(db_path: Optional[Path] = None) -> None:
    conn = _get_conn(db_path)
    with conn:
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {_TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                first_name TEXT,
                last_name TEXT,
                age INTEGER,
                email TEXT,
                country TEXT,
                attendance REAL,
                assignment_completed INTEGER,
                grade REAL
            )
            """
        )
    conn.close()

def insert_grade(row: Dict[str, Any], db_path: Optional[Path] = None) -> int:
    values = [row.get(c) for c in Expected_Columns]
    placeholders = ", ".join("?" for _ in Expected_Columns)
    cols_sql = ", ".join(Expected_Columns)

    conn = _get_conn(db_path)
    with conn:
        cur = conn.execute(
            f"INSERT INTO {_TABLE_NAME} ({cols_sql}) VALUES ({placeholders})",
            values,
        )
        last_id = cur.lastrowid
    conn.close()
    return last_id

def insert_dataframe(df: pd.DataFrame, db_path: Optional[Path] = None) -> int:
    if df is None or df.empty:
        return 0

    # Keep only expected columns (if present) and in the expected order
    cols_in_df: List[str] = [c for c in Expected_Columns if c in df.columns]
    if not cols_in_df:
        return 0

    to_insert = df.loc[:, cols_in_df].where(pd.notnull(df.loc[:, cols_in_df]), None)
    rows = [tuple(r) for r in to_insert.to_numpy().tolist()]

    # Build SQL using the columns we actually have
    cols_sql = ", ".join(cols_in_df)
    placeholders = ", ".join("?" for _ in cols_in_df)

    conn = _get_conn(db_path)
    with conn:
        cur = conn.executemany(
            f"INSERT INTO {_TABLE_NAME} ({cols_sql}) VALUES ({placeholders})",
            rows,
        )
        inserted = len(rows)
    conn.close()
    return inserted

def delete_grade(record_id: int, db_path: Optional[Path] = None) -> int:
    """Delete a row by its primary key id.

    Returns the number of rows deleted (0 if not found, 1 if deleted).
    """
    conn = _get_conn(db_path)
    try:
        with conn:
            cur = conn.execute(f"DELETE FROM {_TABLE_NAME} WHERE id = ?", (record_id,))
            # cursor.rowcount should reflect rows affected for DELETE
            deleted = cur.rowcount
    finally:
        conn.close()
    return deleted

def fetch_all(db_path: Optional[Path] = None) -> pd.DataFrame:
    conn = _get_conn(db_path)
    try:
        cols_sql = ", ".join(Expected_Columns)
        df = pd.read_sql_query(f"SELECT * FROM {_TABLE_NAME}", conn)
    finally:
        conn.close()
    return df