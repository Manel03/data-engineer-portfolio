import logging
from pathlib import Path

import pandas as pd

from src.config import RAW_DATA_PATH

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
    "EmployeeNumber", "Attrition", "Department",
    "JobRole", "MonthlyIncome", "YearsAtCompany", "OverTime",
}


def extract(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Lit le CSV brut et vérifie la présence des colonnes essentielles."""
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset introuvable : {path}\n"
            "Télécharge-le depuis Kaggle (IBM HR Analytics Attrition Dataset)."
        )

    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes dans le dataset : {missing}")

    logger.info("Extraction : %d lignes, %d colonnes", *df.shape)
    return df