import sys, uuid
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))

import pandas as pd
import streamlit as st
from app.core import LeadInput, analyze_lead, SERVICE_CATALOG

st.set_page_config(page_title="GrowthDesk Pro | Cynbit",page_icon="✳",layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root{--ink:#142b35;--muted:#71838b;--teal:#087e80;--line:#e5ecec}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:#f4f8f8;color:var(--ink)}
.block-container{max-width:1450px;padding-top:1.5rem}
[data-testid="stSidebar"]{background:#102b35}
[data-testid="stSidebar"] *{color:#eaf4f3!important}
.brand{display:flex;gap:11px;align-items:center;padding:7px 0 24px}
.brandmark{width:40px;height:40px;border-radius:13px;background:linear-gradient(135deg,#14a39a,#0b5963);display:grid;place-items:center;color:white;font-size:22px;font-weight:800}
.brandname{font:800 18px Manrope;color:white}.brandsub{font-size:10px;letter-spacing:1.7px;color:#9ab6b9;text-transform:uppercase}
.eyebrow{color:#087e80;font-size:11px;font-weight:800;letter-spacing:1.8px;text-transform:uppercase}
.hero{background:linear-gradient(115deg,#103d48,#087e80 70%,#18a59a);padding:28px 30px;border-radius:22px;color:white;margin:10px 0 22px;box-shadow:0 16px 40px #0a59601c}
.hero h1{color:white!important;font:800 29px Manrope;margin:8px 0}.hero p{color:#d5eeeb;margin:0}
.tag{display:inline-block;background:#ffffff20;border:1px solid #ffffff35;border-radius:50px;padding:5px 10px;font-size:10px;letter-spacing:1px}
.metric{background:white;border:1px solid #e5ecec;border-radius:17px;padding:17px;min-height:112px}
.mlabel{font-size:12px;color:#71838b;font-weight:600}.mvalue{font:800 29px Manrope;color:#142b35;margin:5px 0}.mfoot{font-size:11px;color:#8a9a9e}
.panel{background:white;border:1px solid #e5ecec;border-radius:18px;padding:20px;margin-bottom:15px;box-shadow:0 3px 12px #193a4207}
.ptitle{font:800 16px Manrope;color:#142b35}.psub{font-size:12px;color:#71838b;margin:3px 0 14px}
.pill{display:inline-block;padding:5px 10px;border-radius:30px;font-size:11px;font-weight:700}
.high{background:#e5f6ee;color:#16734b}.medium{background:#fff3dd;color:#9b6711}.low{background:#eef1f3;color:#65747b}.teal{background:#e5f4f2;color:#087e80}
.info{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid #edf1f1;font-size:13px}
.stButton>button[kind="primary"]{background:linear-gradient(100deg,#087e80,#0b6268);border:0;border-radius:11px;color:white;font-weight:700}
.stButton>button{border-radius:10px;font-weight:600}
footer{visibility:hidden}
</style>
""",unsafe_allow_html=True)

if "leads" not in st.session_state: st.session_state.leads=[]
if "active" not in st.session_state: st.session_state.active=None

SAMPLES=[
{"name":"Aarav Sharma","company":"Northstar Retail","email":"aarav@example.com","website":"https://example.com","message":"We need an AI-powered customer support automation system. It should classify incoming customer support tickets, summarize conversations, identify urgent issues and route them to the right department. We want CRM integration and a pilot within six weeks.","budget":"high","timeline":"within_1_month","region":"India"},
{"name":"Meera Kapoor","company":"Urban Spaces","email":"meera@example.com","website":"https://example.com","message":"We are looking to build a web platform to manage tenant records, rental payments, property availability and maintenance requests. We need an admin dashboard and REST API for our operations team.","budget":"medium","timeline":"within_3_months","region":"India"},
{"name":"Rohan Verma","company":"BrightPath","email":"rohan@example.com","website":"","message":"We want to improve our website organic traffic through technical SEO and content optimization. We also need CRM automation, lead generation and better conversion tracking.","budget":"low","timeline":"not_shared","region":"India"},
{"name":"Nisha Rao","company":"CloudNine Labs","email":"nisha@example.com","website":"https://example.com","message":"Our application is hosted on AWS. We need help with Docker, Kubernetes deployment, CI/CD pipelines, cloud migration planning and infrastructure scaling as traffic grows.","budget":"high","timeline":"urgent","region":"India"}
]
def add_lead(data):
    lead=LeadInput(**data); result=analyze_lead(lead)
    rec={"id":str(uuid.uuid4())[:8],"created":datetime.now().strftime("%d %b %Y %H:%M"),"status":"New","input":lead.model_dump(mode="json"),"analysis":result}
    st.session_state.leads.insert(0,rec);st.session_state.active=rec["id"];return rec
def metric(label,value,foot,icon):
    st.markdown(f'<div class="metric"><div class="mlabel">{icon} &nbsp; {label}</div><div class="mvalue">{value}</div><div class="mfoot">{foot}</div></div>',unsafe_allow_html=True)
def heading(t,s=""):
    st.markdown(f'<div class="ptitle">{t}</div><div class="psub">{s}</div>',unsafe_allow_html=True)
def pill(s):
    return f'<span class="pill {s.lower()}">{s}</span>' if s in ["High","Medium","Low"] else f'<span class="pill teal">{s}</span>'

with st.sidebar:
    st.markdown('<div class="brand"><div class="brandmark">✳</div><div><div class="brandname">GrowthDesk</div><div class="brandsub">Cynbit intelligence</div></div></div>',unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;letter-spacing:1.6px;color:#80c9c3;font-weight:800;margin:5px 0 10px">WORKSPACE</div>',unsafe_allow_html=True)
    page=st.radio("Navigation",["Overview","Analyze a Lead","Lead Pipeline","Insights & Reports"],label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<div style="font-size:10px;letter-spacing:1.6px;color:#80c9c3;font-weight:800">SYSTEM STATUS</div><p style="font-size:12px;color:#d4e8e6">● Analysis engine ready</p><p style="font-size:12px;color:#d4e8e6">● Human review enabled</p><p style="font-size:11px;color:#9ab6b9">Prototype v1.0 · Session storage</p>',unsafe_allow_html=True)

leads=st.session_state.leads
total=len(leads); high=sum(x["analysis"]["priority_band"]=="High" for x in leads)
med=sum(x["analysis"]["priority_band"]=="Medium" for x in leads)
avg=round(sum(x["analysis"]["priority_score"] for x in leads)/total) if total else 0
st.markdown(f'<div style="display:flex;justify-content:space-between;margin-bottom:16px"><div><div class="eyebrow">CYNBIT TECHNOLOGIES / SALES INTELLIGENCE</div><div style="font-size:13px;color:#71838b">AI-assisted lead qualification workspace</div></div><div style="text-align:right;font-size:12px;color:#71838b">{datetime.now().strftime("%A, %d %B %Y")}<br><b style="color:#087e80">● Workspace active</b></div></div>',unsafe_allow_html=True)

if page=="Overview":
    st.markdown('<div class="hero"><span class="tag">✦ AI-POWERED SALES INTELLIGENCE</span><h1>Turn every enquiry into an opportunity.</h1><p>Understand intent, qualify leads and prepare smarter discovery conversations — all in one workspace.</p></div>',unsafe_allow_html=True)
    cols=st.columns(4)
    for col,args in zip(cols,[("Total leads",total,"Captured in this session","◉"),("High priority",high,"Require prompt review","↗"),("Medium priority",med,"Need qualification","◎"),("Average score",f"{avg}/100" if total else "—","Heuristic priority index","✳")]):
        with col: metric(*args)
    left,right=st.columns([1.4,1])
    with left:
        st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Recent lead activity","Latest enquiries analyzed in this workspace")
        if leads:
            st.dataframe(pd.DataFrame([{"Company":x["input"]["company"],"Contact":x["input"]["name"],"Service":x["analysis"]["recommended_service"],"Score":x["analysis"]["priority_score"],"Priority":x["analysis"]["priority_band"],"Added":x["created"]} for x in leads[:7]]),use_container_width=True,hide_index=True)
        else: st.info("No leads yet. Load demo data or analyze your first enquiry.")
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Priority distribution","Current lead qualification mix")
        if leads: st.bar_chart(pd.Series({"High":high,"Medium":med,"Low":total-high-med}))
        else: st.caption("Analytics will appear when leads are analyzed.")
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Quick actions","Get started with a realistic demo or a new enquiry")
    a,b,c=st.columns(3)
    with a:
        if st.button("＋ Analyze a new lead",type="primary",use_container_width=True): st.info("Choose Analyze a Lead from the sidebar.")
    with b:
        if st.button("Load sample leads",use_container_width=True):
            existing={x["input"]["email"] for x in leads};n=0
            for s in SAMPLES:
                if s["email"] not in existing: add_lead(s);n+=1
            st.success(f"Added {n} sample leads.");st.rerun()
    with c:
        if st.button("Clear session leads",use_container_width=True):
            st.session_state.leads=[];st.session_state.active=None;st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)

elif page=="Analyze a Lead":
    st.markdown('<div class="eyebrow">INTELLIGENCE WORKSPACE</div>',unsafe_allow_html=True);st.title("Analyze a lead")
    st.caption("Convert an unstructured enquiry into an actionable discovery brief.")
    st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Lead information","Enter a prospect's details or select a sample scenario.")
    options=["Start with a blank form"]+[f'{x["company"]} — {x["name"]}' for x in SAMPLES]
    choice=st.selectbox("Quick-fill a demo scenario",options);idx=options.index(choice)-1;preset=SAMPLES[idx] if idx>=0 else {}
    with st.form("leadform"):
        x,y=st.columns(2)
        with x:
            name=st.text_input("Contact name *",preset.get("name",""));company=st.text_input("Company *",preset.get("company",""))
            email=st.text_input("Work email *",preset.get("email",""));website=st.text_input("Company website",preset.get("website",""))
        with y:
            region=st.text_input("Region",preset.get("region","India"))
            budgets=["not_shared","low","medium","high"];budget=st.selectbox("Indicative budget",budgets,index=budgets.index(preset.get("budget","not_shared")),format_func=lambda v:{"not_shared":"Not shared","low":"Low","medium":"Medium","high":"High"}[v])
            timelines=["not_shared","urgent","within_1_month","within_3_months","more_than_3_months"];timeline=st.selectbox("Expected timeline",timelines,index=timelines.index(preset.get("timeline","not_shared")),format_func=lambda v:{"not_shared":"Not shared","urgent":"Urgent","within_1_month":"Within 1 month","within_3_months":"Within 3 months","more_than_3_months":"More than 3 months"}[v])
        message=st.text_area("Enquiry / business requirement *",preset.get("message",""),height=160,placeholder="Describe the prospect's business problem, desired solution, constraints and expected outcome...")
        submit=st.form_submit_button("✦  Analyze enquiry",type="primary",use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)
    if submit:
        try: add_lead({"name":name,"company":company,"email":email,"website":website or None,"message":message,"budget":budget,"timeline":timeline,"region":region or None});st.rerun()
        except Exception as e: st.error(f"Please review the required fields: {e}")
    active=next((x for x in leads if x["id"]==st.session_state.active),None)
    if active:
        a=active["analysis"];i=active["input"];st.markdown('<div class="eyebrow">LATEST ANALYSIS</div>',unsafe_allow_html=True)
        c1,c2,c3=st.columns([1,1,1.5])
        with c1:
            st.markdown('<div class="panel">',unsafe_allow_html=True);st.caption("PRIORITY SCORE");st.markdown(f'<div style="font:800 38px Manrope;color:#087e80">{a["priority_score"]}<span style="font-size:15px;color:#91a2a5"> / 100</span></div>{pill(a["priority_band"])}',unsafe_allow_html=True);st.markdown('</div>',unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="panel">',unsafe_allow_html=True);st.caption("RECOMMENDED SERVICE");st.markdown(f'<div style="font:800 17px Manrope;margin:12px 0">{a["recommended_service"]}</div><span class="pill teal">Intent matched</span>',unsafe_allow_html=True);st.markdown('</div>',unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Recommended next step");st.write(a["recommended_next_step"]);st.markdown('</div>',unsafe_allow_html=True)
        l,r=st.columns(2)
        with l:
            st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Extracted requirements")
            for v in a["requirements"]: st.markdown("✓ "+v)
            st.markdown('</div><div class="panel">',unsafe_allow_html=True);heading("Missing information")
            for v in a["missing_information"]: st.markdown("⚠️ "+v)
            if not a["missing_information"]: st.success("No major information gaps detected.")
            st.markdown('</div>',unsafe_allow_html=True)
        with r:
            st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Explainable score","Heuristic breakdown — not a conversion probability")
            st.bar_chart(pd.Series(a["score_breakdown"]))
            for k,v in a["score_breakdown"].items(): st.markdown(f'<div class="info"><span>{k}</span><b>{v} pts</b></div>',unsafe_allow_html=True)
            st.markdown('</div><div class="panel">',unsafe_allow_html=True);heading("Discovery questions")
            for q in a["discovery_questions"]: st.markdown("• "+q)
            st.markdown('</div>',unsafe_allow_html=True)
        st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Follow-up email draft","Review and personalize before sending — no email is sent by this prototype.")
        st.text_area("Editable draft",a["follow_up_email"],height=230,key="email_"+active["id"])
        st.download_button("Download email draft",a["follow_up_email"],file_name=i["company"].replace(" ","_")+"_followup.txt")
        st.markdown('</div>',unsafe_allow_html=True)

elif page=="Lead Pipeline":
    st.markdown('<div class="eyebrow">RELATIONSHIP WORKSPACE</div>',unsafe_allow_html=True);st.title("Lead pipeline")
    st.caption("Search, filter, inspect and export leads analyzed in this browser session.")
    if not leads: st.info("No leads yet. Load sample leads from Overview or analyze a new lead.")
    else:
        f1,f2,f3=st.columns([2,1,1])
        query=f1.text_input("Search leads",placeholder="Company, contact or email")
        services=["All"]+sorted({x["analysis"]["recommended_service"] for x in leads});sf=f2.selectbox("Service",services);pf=f3.selectbox("Priority",["All","High","Medium","Low"])
        filtered=[x for x in leads if (not query or query.lower() in (x["input"]["company"]+" "+x["input"]["name"]+" "+x["input"]["email"]).lower()) and (sf=="All" or x["analysis"]["recommended_service"]==sf) and (pf=="All" or x["analysis"]["priority_band"]==pf)]
        rows=[{"Company":x["input"]["company"],"Contact":x["input"]["name"],"Email":x["input"]["email"],"Service":x["analysis"]["recommended_service"],"Score":x["analysis"]["priority_score"],"Priority":x["analysis"]["priority_band"],"Status":x["status"],"Added":x["created"]} for x in filtered]
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        st.download_button("↓ Export filtered leads (CSV)",pd.DataFrame(rows).to_csv(index=False).encode(),"growthdesk_leads.csv","text/csv")
        st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Lead detail","Inspect qualification and update review status.")
        selected=st.selectbox("Choose lead",filtered,format_func=lambda x:f'{x["input"]["company"]} · {x["input"]["name"]} · {x["analysis"]["priority_band"]}')
        if selected:
            st.write("**Service:**",selected["analysis"]["recommended_service"]," · **Score:**",selected["analysis"]["priority_score"])
            selected["status"]=st.selectbox("Review status",["New","In review","Qualified","Nurture","Closed"],index=["New","In review","Qualified","Nurture","Closed"].index(selected["status"]),key="status_"+selected["id"])
            if st.button("Show this lead's full analysis"): st.session_state.active=selected["id"];st.info("Open Analyze a Lead from the sidebar to see its full brief.")
        st.markdown('</div>',unsafe_allow_html=True)

else:
    st.markdown('<div class="eyebrow">PERFORMANCE INTELLIGENCE</div>',unsafe_allow_html=True);st.title("Insights & reports")
    st.caption("Service demand, priority mix and operational evaluation guidance.")
    if not leads: st.info("Analyze or load sample leads to generate insights.")
    else:
        df=pd.DataFrame([{"Company":x["input"]["company"],"Service":x["analysis"]["recommended_service"],"Priority":x["analysis"]["priority_band"],"Score":x["analysis"]["priority_score"]} for x in leads])
        l,r=st.columns(2)
        with l:
            st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Service demand");st.bar_chart(df["Service"].value_counts());st.markdown('</div>',unsafe_allow_html=True)
        with r:
            st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Priority mix");st.bar_chart(df["Priority"].value_counts());st.markdown('</div>',unsafe_allow_html=True)
        st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Score distribution","Triage indicator, not a sales forecast");st.line_chart(df["Score"].reset_index(drop=True));st.markdown('</div>',unsafe_allow_html=True)
        st.markdown('<div class="panel">',unsafe_allow_html=True);heading("Pilot evaluation KPIs")
        st.markdown("- Median time from enquiry to first reviewed triage.\n- Qualification completeness and missing-field detection.\n- Staff acceptance/override rate for service and priority suggestions.\n- Human rating of discovery brief factuality and relevance.\n- Qualified-lead-to-meeting and meeting-to-proposal rates against baseline.")
        st.markdown('</div>',unsafe_allow_html=True)

st.markdown('<div style="text-align:center;color:#9aabad;font-size:11px;padding:28px 0">CYNBIT GROWTHDESK PRO · AI-ASSISTED DECISION SUPPORT · HUMAN REVIEW REQUIRED</div>',unsafe_allow_html=True)
