import pandas as pd


Expected_Columns = [
    "student_id",
    "first_name",
    "last_name",
    "age",
    "email",
    "country",
    "attendance",
    "assignment_completed",
    "grade"
]

def _validate_columns(df: pd.columns) -> bool:
    return set(Expected_Columns).issubset(set(df.columns))

## Coerce columns to expected types, returning a new DataFrame for database importing
def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    out = df.loc[:, Expected_Columns].copy()
    # IDs and textual fields -> pandas' string dtype (nullable)
    out["student_id"] = out["student_id"].astype("string")
    for col in ("first_name", "last_name", "email", "country"):
        out[col] = out[col].astype("string")

    # age -> nullable integer
    out["age"] = pd.to_numeric(out["age"], errors="coerce").astype("Int64")

    # attendance -> nullable float (percentage)
    out["attendance"] = pd.to_numeric(out["attendance"], errors="coerce").astype("Float64")

    # assignment_completed -> nullable integer
    out["assignment_completed"] = pd.to_numeric(out["assignment_completed"], errors="coerce").astype("Int64")

    # grade -> nullable float
    out["grade"] = pd.to_numeric(out["grade"], errors="coerce").astype("Float64")

    return out

def CSVImport(filePath):
    try:
        df = pd.read_csv(filePath)
    except:
        print("Error Importing File @ " + filePath)
        return None
    if not _validate_columns(df):
        print("Invalid Columns in CSV File @ " + filePath)
        return None

    return _coerce_types(df)

def JSONImport(filePath):
    try:
        df = pd.read_json(filePath, orient="records")
    except:
        print("Error Importing File @ " + filePath)
        return None
    if not isinstance(df, pd.DataFrame):
        try:
            df = pd.DataFrame(df)
        except:
            print("Error Converting JSON to DataFrame @ " + filePath)
            return None
    if not _validate_columns(df):
        print("Invalid Columns in JSON File @ " + filePath)
        return None
    return _coerce_types(df)
