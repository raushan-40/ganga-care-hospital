# Ganga Care Hospital: containerized OPD booking on AWS
Flask + SQLite app: public pages (Home, Doctors, Facilities, Contact) and OPD appointment booking with double-booking protection.
Cloud features: Docker, `restart: always`, container HEALTHCHECK, `/health` endpoint, crash and TTR scripts, SLA and cost docs.

## Run locally
    docker compose up -d --build     # open http://localhost
    ./scripts/ttr_test.sh            # crash + measure recovery time (needs curl, bc)
    ./scripts/loadtest.sh            # latency and throughput (needs ab)
Without Docker: `cd app && pip install -r requirements.txt && DB_PATH=./h.db python -m flask --app app run`

## Demo crash (also via UI/curl): `curl -X POST http://localhost/crash` (only when ENABLE_CRASH=1)
## Docs: docs/AWS_DEPLOY.md, docs/SLA_AND_COST.md
Endpoints: `/`, `/doctors`, `/facilities`, `/contact`, `/book`, `/appointment/<ref>`, `/health`, `/api/appointments`.
Notes: SQLite on a Docker volume is fine for a demo; use RDS for production. Remove ENABLE_CRASH in production.
