from fastapi import FastAPI
from app.core import LeadInput, analyze_lead
app=FastAPI(title="Cynbit GrowthDesk Pro API",version="1.0.0")
@app.get("/health")
def health(): return {"status":"ok","service":"Cynbit GrowthDesk Pro"}
@app.post("/analyze")
def analyze(payload:LeadInput): return analyze_lead(payload)
@app.post("/analyze/batch")
def analyze_batch(payload:list[LeadInput]):
    if len(payload)>100: return {"error":"Batch limit is 100 leads"}
    return [analyze_lead(x) for x in payload]
