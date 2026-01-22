from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import functions.db as db

STAT_ITEMS: List[Tuple[str, str, bool]] = [
    ("avg_grade", "Average grade", False),
    ("avg_attendance", "Average attendance", False),
    ("count_fails", "Number of fails (< 40)", False),
    ("count_passes", "Number of passes (>= 40)", False),
    ("count_A", "Count A Grade (>= 70)", False),
    ("count_B", "Count B Grade (60-69)", False),
    ("count_C", "Count C Grade (50-59)", False),
    ("record_count", "Total records", False),
    ("unique_students", "Unique students", False),
    ("count_missing", "Missing grades", False),
    ("pass_rate", "Pass rate (%)", True),
    ("fail_rate", "Fail rate (%)", True),
]


def safe_series(df: pd.DataFrame, col: str) -> Optional[pd.Series]:
    if df is None or col not in df.columns:
        return None
    return df[col]

def calculate_stats(df: Optional[pd.DataFrame]) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "record_count": 0,
        "unique_students": 0,
        "avg_grade": None,
        "median_grade": None,
        "grade_std": None,
        "avg_attendance": None,
        "count_missing": 0,
        "count_fails": 0,
        "count_passes": 0,
        "count_A": 0,
        "count_B": 0,
        "count_C": 0,
        "pass_rate": None,
        "fail_rate": None,
    }
    if df is None or df.empty:
        return out
    out["record_count"] = int(len(df))
    if "student_id" in df.columns:
        try:
            out["unique_students"] = int(df["student_id"].nunique(dropna=True))
        except Exception:
            out["unique_students"] = out["record_count"]
    else:
        out["unique_students"] = out["record_count"]

    grades =  safe_series(df,"grade")
    attendance = safe_series(df,"attendance")

    if grades is not None:
        grades_numeric = pd.to_numeric(grades, errors="coerce")
        non_na = grades_numeric.dropna()
        out["count_missing"] = int(grades_numeric.isna().sum())
        if not non_na.empty:
            out["avg_grade"] = float(non_na.mean())
            out["median_grade"] = float(non_na.median())
            # sample std (ddof=1) if at least 2 points, else 0.0
            out["grade_std"] = float(non_na.std(ddof=1)) if len(non_na) > 1 else 0.0

            out["count_fails"] = int((non_na < 40).sum())
            out["count_passes"] = int((non_na >= 40).sum())

            out["count_A"] = int((non_na >= 70).sum())
            out["count_B"] = int(((non_na >= 60) & (non_na < 70)).sum())
            out["count_C"] = int(((non_na >= 50) & (non_na < 60)).sum())

            total_scored = int(len(non_na))
            out["pass_rate"] = (out["count_passes"] / total_scored) * 100.0
            out["fail_rate"] = (out["count_fails"] / total_scored) * 100.0
        else:
            # no numeric grades present
            out["avg_grade"] = None
            out["median_grade"] = None
            out["grade_std"] = None
            out["count_fails"] = 0
            out["count_passes"] = 0
            out["count_A"] = 0
            out["count_B"] = 0
            out["count_C"] = 0
            out["pass_rate"] = None
            out["fail_rate"] = None
    else:
        out["count_missing"] = 0

    # Attendance
    if attendance is not None:
        att_numeric = pd.to_numeric(attendance, errors="coerce").dropna()
        out["avg_attendance"] = float(att_numeric.mean()) if not att_numeric.empty else None

    return out


def fetch_and_compute() -> Dict[str, Any]:
    try:
        df = db.fetch_all()
    except Exception:
        df = None
    return calculate_stats(df)