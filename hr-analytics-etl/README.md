# 📊 HR Analytics ETL Pipeline

Pipeline ETL end-to-end qui ingère des données RH brutes, les nettoie,
calcule des KPIs métier et les charge dans PostgreSQL pour le reporting.

## Architecture

```
CSV (Kaggle) → Extract → Transform → KPIs → PostgreSQL → Dashboard
                  │          │                  │
               validation  nettoyage        export CSV
               colonnes    + enrichissement
```

## Stack technique

- Python 3.11 / Pandas / SQLAlchemy
- PostgreSQL 16
- Docker / Docker Compose

## Dataset

[IBM HR Analytics Employee Attrition](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) :
1 470 employés, 35 colonnes.

## KPIs calculés

| KPI | Description |
|-----|-------------|
| Taux d'attrition | % d'employés ayant quitté l'entreprise |
| Masse salariale | Somme des salaires annuels |
| Salaire moyen | Salaire mensuel moyen |
| Ancienneté moyenne | Années moyennes dans l'entreprise |
| Taux d'heures sup. | % d'employés faisant des heures supplémentaires |
| Satisfaction moyenne | Score moyen de satisfaction au travail (1-4) |

Chaque KPI est ventilé par **département**, **poste**, **tranche d'âge** et **ancienneté**.

## Lancer le projet

1. Télécharger le dataset depuis Kaggle et le placer dans `data/raw/`
2. Configurer l'environnement :
```bash
   cp .env.example .env
```
3. Lancer avec Docker :
```bash
   docker compose up --build
```

### Sans Docker (développement)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python -m src.pipeline
```

## Tables produites

| Table | Contenu |
|-------|---------|
| `employees` | Données employés nettoyées et enrichies |
| `kpi_global` | KPIs globaux de l'entreprise |
| `kpi_by_department` | KPIs par département |
| `kpi_by_job_role` | KPIs par poste |
| `kpi_by_age_band` | KPIs par tranche d'âge |
| `kpi_by_tenure_band` | KPIs par ancienneté |
