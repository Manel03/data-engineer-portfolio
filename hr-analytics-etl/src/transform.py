import logging
import re

import pandas as pd

logger = logging.getLogger(__name__)

# Colonnes ayant la même valeur pour tous les employés : aucune information utile
CONSTANT_COLUMNS = ["EmployeeCount", "Over18", "StandardHours"]

EDUCATION_LABELS = {
    1: "Below College", 2: "College", 3: "Bachelor", 4: "Master", 5: "Doctor",
}


def to_snake_case(name: str) -> str:
    """MonthlyIncome -> monthly_income"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    initial_rows = len(df)

    # 1. Nettoyage
    df = df.drop_duplicates(subset="EmployeeNumber")
    if len(df) < initial_rows:
        logger.warning("%d doublons supprimés", initial_rows - len(df))

    df = df.drop(columns=CONSTANT_COLUMNS, errors="ignore")
    df.columns = [to_snake_case(c) for c in df.columns]

    # 2. Conversion des Yes/No en booléens
    for col in ["attrition", "over_time"]:
        df[col] = df[col].map({"Yes": True, "No": False})

    # 3. Colonnes dérivées
    df["annual_income"] = df["monthly_income"] * 12
    df["education_level"] = df["education"].map(EDUCATION_LABELS)

    df["age_band"] = pd.cut(
        df["age"],
        bins=[17, 25, 35, 45, 55, 100],
        labels=["18-25", "26-35", "36-45", "46-55", "56+"],
    ).astype(str)

    df["tenure_band"] = pd.cut(
        df["years_at_company"],
        bins=[-1, 2, 5, 10, 100],
        labels=["0-2 ans", "3-5 ans", "6-10 ans", "11+ ans"],
    ).astype(str)

    logger.info("Transformation : %d lignes, %d colonnes", *df.shape)
    return df