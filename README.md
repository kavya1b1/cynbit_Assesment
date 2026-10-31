# Cynbit GrowthDesk Pro

AI-assisted Lead Intelligence & Sales Discovery Workspace.

## Features
- Modern Streamlit workspace with Overview, Analyze a Lead, Lead Pipeline, and Insights & Reports.
- KPI cards, service mix, priority distribution and lead activity.
- Guided lead intake with sample scenarios.
- Service classification, requirement extraction and explainable priority scoring.
- Missing-information detection, discovery questions and human-reviewed email drafts.
- Session-level lead history, status updates, search, filters and CSV export.
- FastAPI health, single-analysis and batch-analysis endpoints.
- Optional OpenAI-compatible LLM extraction with deterministic offline fallback.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```
Open the local URL shown by Streamlit (usually http://localhost:8501).

## Run API
```bash
uvicorn app.api:app --reload
```
Swagger docs: http://127.0.0.1:8000/docs

## Optional LLM
Set `OPENAI_API_KEY`, `OPENAI_BASE_URL` (optional), and `OPENAI_MODEL` in your environment. The app works without a key.

## Architecture
Lead intake → validation → service matching → requirement extraction → explainable scoring → discovery brief → human review.

## Important limitations
Lead records are held in Streamlit session state only and disappear when the session resets. There is no persistent database, live CRM, inbox integration, external enrichment or email sending. Priority scores are heuristic signals, not conversion probabilities. Use synthetic data only; do not enter confidential or sensitive customer information. Review all generated content.

## Production roadmap
Validate service categories and score weights with sales staff; connect an approved CRM; evaluate on anonymized labelled data; add authentication, authorization, audit logs, retention controls, monitoring and security testing.
