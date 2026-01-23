import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def _group_mean_top(df: pd.DataFrame, group_col: str, value_col: str, top_n: int = 20) -> pd.Series:
    if df is None or group_col not in df.columns or value_col not in df.columns:
        return pd.Series(dtype=float)
    s = df[[group_col, value_col]].dropna()
    if s.empty:
        return pd.Series(dtype=float)
    grouped = s.groupby(group_col)[value_col].mean()
    return grouped.sort_values(ascending=False).head(top_n)

def _bar_plot_series(series: pd.Series, title: str, xlabel: str = "", ylabel: str = "", figsize=(10, 6)) -> plt.Figure:
    fig, ax = plt.subplots(figsize=figsize)
    series_sorted = series.sort_values()
    ax.barh(series_sorted.index.astype(str), series_sorted.values, color="#4C72B0")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    return fig

def plot_avg_grade_by_country(df: pd.DataFrame, top_n: int = 20) -> plt.Figure:
    series = _group_mean_top(df, "country", "grade", top_n=top_n)
    return _bar_plot_series(series, title=f"Average Grade by Country (top {len(series)})",
                            xlabel="Average Grade", ylabel="Country")

def plot_avg_attendance_by_country(df: pd.DataFrame, top_n: int = 20) -> plt.Figure:
    series = _group_mean_top(df, "country", "attendance", top_n=top_n)
    return _bar_plot_series(series, title=f"Average Attendance by Country (top {len(series)})",
                            xlabel="Average Attendance (%)", ylabel="Country")

def plot_grade_vs_attendance_scatter(df: pd.DataFrame) -> plt.Figure:
    if df is None or "grade" not in df.columns or "attendance" not in df.columns:
        return plt.Figure()
    s = df[["grade", "attendance"]].dropna()
    if s.empty:
        return plt.Figure()
    # ensure numeric
    x = pd.to_numeric(s["attendance"], errors="coerce").dropna().astype(float)
    y = pd.to_numeric(s["grade"], errors="coerce").dropna().astype(float)
    # align indices after coercion
    common_idx = x.index.intersection(y.index)
    x = x.loc[common_idx]
    y = y.loc[common_idx]
    if x.empty or y.empty:
        return plt.Figure()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y, alpha=0.6, s=30, color="#4C72B0", label="Data")

    # Fit a linear model if we have at least two points
    if len(x) >= 2:
        try:
            coeffs = np.polyfit(x.values, y.values, 1)
            slope, intercept = coeffs[0], coeffs[1]
            x_line = np.linspace(x.min(), x.max(), 100)
            y_line = slope * x_line + intercept
            ax.plot(x_line, y_line, color="red", linestyle="--", linewidth=1.5, label="Best fit")

            # compute R^2
            y_pred = slope * x.values + intercept
            ss_res = ((y.values - y_pred) ** 2).sum()
            ss_tot = ((y.values - y.values.mean()) ** 2).sum()
            r2 = 1.0 - ss_res / ss_tot if ss_tot != 0 else 1.0
            ax.text(0.02, 0.98, f"R² = {r2:.3f}", transform=ax.transAxes,
                    verticalalignment="top", bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))
        except Exception:
            # silently skip fit if something goes wrong
            pass

    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Grade")
    ax.set_title("Grade vs Attendance")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend()
    plt.tight_layout()
    return fig

def plot_grade_histogram(df: pd.DataFrame, bins: int = 20) -> plt.Figure:
    if df is None or "grade" not in df.columns:
        return plt.Figure()
    grades = pd.to_numeric(df["grade"], errors="coerce").dropna()
    if grades.empty:
        return plt.Figure()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(grades, bins=bins, color="#4C72B0", edgecolor="white")
    ax.set_xlabel("Grade")
    ax.set_ylabel("Count")
    ax.set_title("Grade Distribution")
    plt.tight_layout()
    return fig

def plot_grade_box_by_country(df: pd.DataFrame, top_n: int = 10) -> plt.Figure:
    if df is None or "country" not in df.columns or "grade" not in df.columns:
        return plt.Figure()
    tmp = df[["country", "grade"]].dropna()
    if tmp.empty:
        return plt.Figure()
    medians = tmp.groupby("country")["grade"].median().sort_values(ascending=False).head(top_n)
    countries = medians.index.tolist()
    data = [pd.to_numeric(tmp.loc[tmp["country"] == c, "grade"], errors="coerce").dropna() for c in countries]
    if not any(len(d) for d in data):
        return plt.Figure()
    fig, ax = plt.subplots(figsize=(max(6, len(countries) * 0.8), 6))
    ax.boxplot(data, labels=countries, vert=False, patch_artist=True,
               boxprops=dict(facecolor="#4C72B0", color="#4C72B0"))
    ax.set_xlabel("Grade")
    ax.set_title(f"Grade Distribution by Country (top {len(countries)})")
    plt.tight_layout()
    return fig

def plot_grade_band_stacked_by_country(df: pd.DataFrame, top_n: int = 10) -> plt.Figure:
    if df is None or "country" not in df.columns or "grade" not in df.columns:
        return plt.Figure()
    tmp = df[["country", "grade"]].copy()
    if tmp.empty:
        return plt.Figure()
    bins = [-float("inf"), 40, 50, 60, 70, float("inf")]
    labels = ["Fail (<40)", "C (50-59)", "B (60-69)", "A (>=70)"]
    tmp["band"] = pd.cut(tmp["grade"], bins=[-float("inf"), 40, 50, 60, 70, float("inf")],
                         labels=["Fail (<40)", "C (50-59)", "B (60-69)", "A (>=70)", "A+(>=70)"],
                         include_lowest=True)
    tmp["band"] = tmp["grade"].apply(lambda g: "Missing" if pd.isna(g)
                                     else ("Fail (<40)" if g < 40
                                           else ("C (50-59)" if 50 <= g < 60
                                                 else ("B (60-69)" if 60 <= g < 70
                                                       else "A (>=70)"))))
    counts = tmp.groupby(["country", "band"]).size().unstack(fill_value=0)
    top_countries = counts.sum(axis=1).sort_values(ascending=False).head(top_n).index
    counts = counts.loc[top_countries]
    if counts.empty:
        return plt.Figure()
    cols = [c for c in ["A (>=70)", "B (60-69)", "C (50-59)", "Fail (<40)", "Missing"] if c in counts.columns]
    fig, ax = plt.subplots(figsize=(max(8, len(top_countries) * 0.6), 6))
    bottom = None
    colors = {"A (>=70)": "#2ca02c", "B (60-69)": "#1f77b4", "C (50-59)": "#9467bd",
              "Fail (<40)": "#d62728", "Missing": "#7f7f7f"}
    for col in cols:
        vals = counts[col]
        if bottom is None:
            p = ax.bar(counts.index.astype(str), vals, label=col, color=colors.get(col))
            bottom = vals.values
        else:
            p = ax.bar(counts.index.astype(str), vals, bottom=bottom, label=col, color=colors.get(col))
            bottom = bottom + vals.values
    ax.set_ylabel("Count")
    ax.set_title(f"Grade Band Counts by Country (top {len(top_countries)})")
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig

def save_figure(fig: plt.Figure, path: str, dpi: int = 150) -> None:
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)