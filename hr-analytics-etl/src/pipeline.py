import logging
import time

from src.extract import extract
from src.kpis import compute_all_kpis
from src.load import load
from src.transform import transform

logger = logging.getLogger(__name__)


def run() -> None:
    start = time.perf_counter()
    logger.info("=== Démarrage du pipeline HR Analytics ===")

    raw = extract()
    clean = transform(raw)
    kpis = compute_all_kpis(clean)
    load(clean, kpis)

    logger.info("=== Pipeline terminé en %.2f s ===", time.perf_counter() - start)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    run()