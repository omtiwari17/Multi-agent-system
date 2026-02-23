import os
os.environ["CREWAI_TRACING_ENABLED"] = "false"
os.environ["CREWAI_TELEMETRY_ENABLED"] = "false"
os.environ["CREWAI_TELEMETRY_DISABLED"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import json
import streamlit as st

from backend.agents import build_researcher, build_writer
from backend.tasks import research_task, write_task
from backend.orchestrator import Orchestrator

# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(
    page_title="Multi-Agent Manufacturing System",
    layout="wide"
)

st.title("Multi-Agent Manufacturing System")
st.caption("Research Agent → Writer Agent → Structured Output")


# ----------------------------
# Sidebar: LLM Settings (Simple + Safe)
# ----------------------------
with st.sidebar:
    st.markdown("## LLM Settings")

    provider = st.selectbox("Provider", ["Gemini"], index=0)

    api_key = st.text_input("API Key", type="password", help="Stored only for this session.")

    model = st.text_input("Model", value="gemini/gemini-2.5-flash")
    verbose = st.checkbox("Verbose logs", value=False)

    st.caption("Tip: If output is too long, keep Verbose off.")

if not api_key.strip():
    st.warning("Please enter your API key to use the system.")
    st.stop()


# ----------------------------
# Query Form
# ----------------------------
st.subheader("Manufacturing Sourcing Query")

with st.form("query_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        process = st.text_input("Process", value="Injection Molding")
        capacity = st.number_input("Monthly Capacity Min", value=50000)

    with col2:
        materials = st.text_input("Materials (comma separated)", value="ABS")
        certifications = st.text_input("Certifications (comma separated)", value="ISO 9001")

    with col3:
        location = st.text_input("Location Preference", value="India")

    submitted = st.form_submit_button("Run Agents")


# ----------------------------
# Helpers
# ----------------------------
def parse_csv(text):
    return [x.strip() for x in text.split(",") if x.strip()]


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ----------------------------
# Run Orchestrator
# ----------------------------
if submitted:

    if not api_key:
        st.error("Please enter your Gemini API key.")
        st.stop()

    # Inject key for agents.py
    os.environ["GOOGLE_API_KEY"] = api_key

    query = {
        "process": process,
        "material": parse_csv(materials),
        "location_preference": parse_csv(location),
        "certifications": parse_csv(certifications),
        "monthly_capacity_min": int(capacity),
    }

    try:
        with st.spinner("Running multi-agent workflow..."):

            researcher = build_researcher(api_key=api_key, model=model)
            writer = build_writer(api_key=api_key, model=model)


            orch = Orchestrator(
                researcher,
                writer,
                research_task(researcher),
                write_task(writer)
            )

            result = orch.run(query)

        st.success(f"Run completed: {result['run_id']}")

        raw_json = load_json(result["raw_dataset_path"])
        final_json = load_json(result["final_suppliers_path"])
        report_md = load_text(result["report_path"])

        tabs = st.tabs(["Report", "Ranked Suppliers", "Raw Research", "⬇ Download"])

        # ----------------------------
        # REPORT TAB
        # ----------------------------
        with tabs[0]:
            st.markdown("### Final Supplier Report")
            st.markdown(report_md)

        # ----------------------------
        # FINAL JSON TAB
        # ----------------------------
        with tabs[1]:
            st.markdown("### Ranked Supplier Output")
            st.json(final_json)

        # ----------------------------
        # RAW TAB
        # ----------------------------
        with tabs[2]:
            st.markdown("### Raw Research Dataset")
            st.json(raw_json)

        # ----------------------------
        # DOWNLOAD TAB
        # ----------------------------
        with tabs[3]:
            st.download_button(
                "Download Report (.md)",
                data=report_md,
                file_name=f"{result['run_id']}_report.md",
            )

            st.download_button(
                "Download Final Suppliers (.json)",
                data=json.dumps(final_json, indent=2),
                file_name=f"{result['run_id']}_final.json",
            )

            st.download_button(
                "Download Raw Research (.json)",
                data=json.dumps(raw_json, indent=2),
                file_name=f"{result['run_id']}_raw.json",
            )

    except Exception as e:
        st.exception(e)
