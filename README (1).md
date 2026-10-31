# Cynbit GrowthDesk Pro

**AI-assisted Lead Intelligence & Sales Discovery Workspace**

Cynbit GrowthDesk Pro is a prototype designed to help a sales or presales team turn unstructured customer enquiries into structured, reviewable lead briefs. It combines lead intake, service categorization, requirement extraction, explainable prioritization, discovery-question generation, and follow-up email drafting in one workspace.

> **Assessment prototype:** This repository demonstrates a proposed AI opportunity for Cynbit. It is not represented as an existing Cynbit product, and its scores and recommendations should be reviewed by a human.

## Overview

The application helps a team:

- Capture a prospect's contact details and business enquiry.
- Categorize the enquiry into a likely service area.
- Extract requirements stated in the enquiry.
- Identify missing information that may be needed before a discovery call.
- Calculate a transparent lead-priority score.
- Generate relevant discovery questions and a recommended next step.
- Prepare a follow-up email draft for human review.
- Review lead activity, filter records, and export lead data as CSV.

## Key Features

### 1. Lead intelligence
- Service classification across AI Automation, Custom Software Development, Cloud & Infrastructure, and Digital Marketing & CRM.
- Requirement extraction using an optional LLM integration, with a deterministic fallback.
- Missing-information detection and discovery-question suggestions.
- Explainable heuristic scoring with a visible category breakdown.

### 2. Lead workspace
- Overview dashboard with lead and priority metrics.
- Lead analysis form with sample scenarios.
- Searchable and filterable lead pipeline.
- Lead review statuses: New, In review, Qualified, Nurture, and Closed.
- CSV export for filtered lead records.

### 3. Follow-up assistance
- Contextual follow-up email draft.
- Editable draft and text-file export.
- No email is sent automatically; a team member must review and send it.

### 4. API
- FastAPI backend.
- Single-lead and batch-analysis endpoints.
- Interactive API documentation through Swagger UI.

## Application Screens / Sections

| Section | Purpose |
|---|---|
| Overview | Workspace KPIs, recent activity, and priority distribution |
| Analyze a Lead | Intake, analysis, score explanation, gaps, and follow-up draft |
| Lead Pipeline | Search, filter, review status, and CSV export |
| Insights & Reports | Service demand, priority mix, score trends, and pilot KPIs |

## Technology Stack

- **Language:** Python
- **Frontend:** Streamlit
- **Backend API:** FastAPI
- **Validation:** Pydantic
- **Data analysis and export:** Pandas
- **Optional LLM:** OpenAI-compatible chat completions API
- **Local development:** Python virtual environment

## Architecture

```text
                ┌──────────────────────────┐
                │      Streamlit UI        │
                │ Overview / Intake / CRM  │
                └────────────┬─────────────┘
                             │
                ┌────────────▼─────────────┐
                │     Lead Validation      │
                │         Pydantic         │
                └────────────┬─────────────┘
                             │
                ┌────────────▼─────────────┐
                │    Service Matching      │
                └────────────┬─────────────┘
                             │
                ┌────────────▼─────────────┐
                │ Requirement Extraction   │
                │ Optional LLM / Fallback  │
                └────────────┬─────────────┘
                             │
                ┌────────────▼─────────────┐
                │ Explainable Lead Scoring │
                └────────────┬─────────────┘
                             │
                ┌────────────▼─────────────┐
                │ Discovery Brief & Draft  │
                │       Human Review       │
                └──────────────────────────┘

                FastAPI exposes the analysis
                functionality as REST endpoints.
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- `pip`
- Git (optional, for version control)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Cynbit-GrowthDesk-Pro.git
cd Cynbit-GrowthDesk-Pro
```

Replace `<your-username>` with your GitHub username.

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run app/streamlit_app.py
```

Open the local URL printed in the terminal. Streamlit commonly uses:

```text
http://localhost:8501
```

Use **Load sample leads** on the Overview page to explore the dashboard with demonstration data.

## Optional LLM Configuration

The application can run without an API key. Without one, it uses the built-in deterministic extraction fallback.

To enable LLM-assisted requirement extraction, copy `.env.example` to `.env` and configure the values in your shell or through your preferred environment-variable manager:

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_MODEL="gpt-4o-mini"
# Optional for an OpenAI-compatible provider:
export OPENAI_BASE_URL="https://api.openai.com/v1"
```

Restart the Streamlit application after setting the environment variables.

**Security:** Never commit `.env`, API keys, passwords, or customer secrets to GitHub. Use synthetic data for demonstrations.

## Run the FastAPI Backend

Start the API from the project root:

```bash
uvicorn app.api:app --reload
```

Useful endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/analyze` | Analyze one lead |
| `POST` | `/analyze/batch` | Analyze a batch of up to 100 leads |

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### Example API request

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aarav Sharma",
    "company": "Northstar Retail",
    "email": "aarav@example.com",
    "website": "https://example.com",
    "message": "We need an AI-powered support solution to classify tickets, summarize conversations and route urgent issues. We also need CRM integration.",
    "budget": "high",
    "timeline": "within_1_month",
    "region": "India"
  }'
```

Accepted budget values: `not_shared`, `low`, `medium`, `high`.

Accepted timeline values: `not_shared`, `urgent`, `within_1_month`, `within_3_months`, `more_than_3_months`.

## Lead Priority Scoring

The prototype calculates a heuristic score using the following weighted dimensions:

| Dimension | Maximum points |
|---|---:|
| Service fit | 30 |
| Requirement clarity | 20 |
| Timeline | 15 |
| Budget signal | 15 |
| Contact completeness | 10 |
| Urgency signal | 10 |
| **Total** | **100** |

Priority bands:

- **High:** 75–100
- **Medium:** 50–74
- **Low:** 0–49

The score is an explainable triage aid. It is **not** a machine-learned conversion probability, and the weights should be calibrated using approved, representative historical data before operational use.

## Repository Structure

```text
Cynbit_GrowthDesk_Pro/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── core.py
│   └── streamlit_app.py
├── data/
│   └── sample_leads.json
├── reports/
│   ├── ai_opportunity_report.md
│   └── technical_approach_report.md
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Reports and Deliverables

The `reports/` directory contains:

- **AI Opportunity Report:** Business opportunity hypothesis, alternatives, proposed workflow, pilot KPIs, and risks.
- **Technical Approach Report:** Architecture, processing pipeline, API endpoints, evaluation approach, and limitations.

## Current Scope and Limitations

This version is a functional proof of concept, not a production CRM.

- Lead records are stored in Streamlit session state and are not persisted in a database.
- There is no authentication, role-based access control, or audit trail.
- CRM, email inbox, calendar, and external company-enrichment integrations are not implemented.
- Follow-up emails are drafts only; the application does not send messages.
- LLM extraction is optional and depends on valid provider configuration.
- Classification and priority scoring require evaluation and calibration with representative, appropriately approved data.

## Suggested Next Steps

1. Add PostgreSQL persistence and database migrations.
2. Implement authentication, authorization, and role-based access.
3. Add CRM integration after confirming the target workflow and permissions.
4. Create a labelled evaluation dataset and measure classification and extraction quality.
5. Track reviewer overrides and calibrate the priority score against agreed business outcomes.
6. Add audit logging, data-retention controls, monitoring, rate limiting, and deployment security.
7. Conduct a pilot with sales/presales users and compare handling time and qualification quality against a baseline.

## Responsible Use

Use synthetic or approved test data in this prototype. Minimize personal information, obtain appropriate authorization before processing prospect data, and have a human review AI-generated classifications, scores, questions, and email drafts before acting on them.

---

**Cynbit GrowthDesk Pro** · AI-assisted decision support · Human review required
