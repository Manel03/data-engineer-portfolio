import logging

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.config import DATABASE_URL, PROCESSED_DIR

logger = logging.getLogger(__name__)


def get_engine() -> Engine:
    return create_engine(DATABASE_URL)


def load(employees: pd.DataFrame, kpis: dict[str, pd.DataFrame],
         engine: Engine | None = None) -> None:
    """Charge les données dans PostgreSQL et exporte des CSV pour le dashboard."""
    engine = engine or get_engine()

    # Transaction unique : tout est chargé, ou rien
    with engine.begin() as conn:
        employees.to_sql("employees", conn, if_exists="replace", index=False)
        logger.info("Table 'employees' chargée (%d lignes)", len(employees))

        for table_name, table in kpis.items():
            table.to_sql(table_name, conn, if_exists="replace", index=False)
            logger.info("Table '%s' chargée (%d lignes)", table_name, len(table))

    # Export CSV (utile pour Power BI ou pour inspecter rapidement)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    employees.to_csv(PROCESSED_DIR / "employees_clean.csv", index=False)
    for table_name, table in kpis.items():
        table.to_csv(PROCESSED_DIR / f"{table_name}.csv", index=False)