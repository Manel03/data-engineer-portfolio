import pandas as pd


def pct(series: pd.Series) -> float:
    return round(series.mean() * 100, 2)


def compute_global_kpis(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([{
        "headcount": len(df),
        "attrition_count": int(df["attrition"].sum()),
        "attrition_rate_pct": pct(df["attrition"]),
        "annual_payroll": int(df["annual_income"].sum()),
        "avg_monthly_income": round(df["monthly_income"].mean(), 2),
        "avg_tenure_years": round(df["years_at_company"].mean(), 2),
        "overtime_rate_pct": pct(df["over_time"]),
        "avg_job_satisfaction": round(df["job_satisfaction"].mean(), 2),
    }])


def compute_kpis_by(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    return (
        df.groupby(dimension)
        .agg(
            headcount=("employee_number", "count"),
            attrition_rate_pct=("attrition", pct),
            annual_payroll=("annual_income", "sum"),
            avg_monthly_income=("monthly_income", "mean"),
            avg_tenure_years=("years_at_company", "mean"),
            overtime_rate_pct=("over_time", pct),
        )
        .round(2)
        .reset_index()
        .sort_values("attrition_rate_pct", ascending=False)
    )


def compute_all_kpis(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        "kpi_global": compute_global_kpis(df),
        "kpi_by_department": compute_kpis_by(df, "department"),
        "kpi_by_job_role": compute_kpis_by(df, "job_role"),
        "kpi_by_age_band": compute_kpis_by(df, "age_band"),
        "kpi_by_tenure_band": compute_kpis_by(df, "tenure_band"),
    }