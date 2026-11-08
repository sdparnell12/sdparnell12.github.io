# DIGGIT Beta 0.2 — browser-first starter

This package includes:
- `frontend/index.html`: current DIGGIT HTML interface plus provisional horticulture screening and carbonate-sculpture concept calculators.
- `backend/main.py`: FastAPI starter endpoints.
- `database/schema.sql`: PostgreSQL/PostGIS starter schema.
- `openapi.yaml`: API contract starter.
- `design/biochemical_kinetic_sculpture.md`: concept brief and chemistry boundaries.

## Run the browser interface
Open `frontend/index.html` in a modern browser. The existing map and Sentinel-2 features require internet access to their public data services.

## Run the API (developer deployment)
Python 3.10+:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
API docs then appear at `/docs`.

## Important limitations
The horticulture score is an illustrative weighted heuristic, not a calibrated plant response model. It does not predict contaminant uptake, degradation, safe planting, yield or field performance. Replace it with species- and substrate-specific models calibrated against replicated experiments.

The carbonate calculator is a stoichiometric upper bound for CO2-to-CaCO3 conversion. It does not model gas transfer, saturation indices, kinetics, crystal polymorphs, scaling, microbial ecology, energy use or lifecycle emissions. Particulate carbon is a separate capture stream.

The API currently uses permissive CORS for local development and has no authentication, database connection, user management, secrets management or production deployment configuration. Restrict origins and implement authentication before deployment. Never put provider API keys in frontend JavaScript.

This is research decision-support scaffolding, not field authorization or a substitute for site-specific risk assessment.
