# Technical Approach Report — Cynbit GrowthDesk Pro

## Architecture
Streamlit UI / FastAPI → Pydantic validation → service matching → requirement extraction → explainable scoring → discovery brief → human review.

## Stack
Python, Streamlit, FastAPI, Pydantic, Pandas and optional OpenAI-compatible LLM. Deterministic fallback supports offline operation.

## Processing
1. Validate lead fields.
2. Match enquiry text to AI Automation, Custom Software Development, Cloud & Infrastructure or Digital Marketing & CRM.
3. Extract requirements with optional structured LLM output; otherwise use deterministic sentence-level extraction.
4. Score service fit (30), clarity (20), timeline (15), budget signal (15), contact completeness (10) and urgency (10).
5. Assign High (75–100), Medium (50–74) or Low (0–49).
6. Detect missing website, budget, timeline, workload and business outcome.
7. Generate discovery questions and a next step.
8. Draft an email; do not send it.
9. Provide lead status, filters, CSV export and analytics.

The score is a heuristic prioritization signal, not a conversion probability. It requires validation against approved historical outcomes.

## API
- GET /health
- POST /analyze
- POST /analyze/batch (maximum 100 leads)

## Evaluation
Use anonymized human-labelled enquiries. Measure classification macro-F1 and per-class precision/recall; requirement extraction precision/recall; missing-field detection; reviewer acceptance; and median handling time. Keep a holdout set for final evaluation.

## Security and limitations
Lead records live in Streamlit session state only. There is no persistent database, CRM, inbox, external enrichment, authentication or email sending. Do not use sensitive data. Production needs TLS, authentication, authorization, rate limiting, audit logs, retention/deletion controls and monitoring.
