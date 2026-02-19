# Multi-Agent Manufacturing System

A role-based multi-agent system that automates supplier sourcing and generates structured comparison reports using LLM-powered agents.

This project demonstrates agent specialization, controlled hand-offs, schema validation, state management, and workflow orchestration using **Python + CrewAI + LLM APIs**.

---

## Problem Statement

Design and implement a collaborative Manufacturing Agent architecture featuring specialization and structured hand-off protocols.

The system consists of:

* **Researcher Agent** → Collects supplier information
* **Writer Agent** → Synthesizes and formats structured comparison reports
* **Orchestrator** → Controls execution flow and state management

The goal is to produce high-quality, structured outputs from complex sourcing queries.

---

## System Overview

The system follows a layered architecture:

```
User → Streamlit UI → Orchestrator
                   → Researcher Agent → LLM API
                   → Writer Agent     → LLM API
                   → Storage + Schema Validation
```

### Agent Roles

#### Researcher Agent

* Interprets supplier sourcing queries
* Identifies potential suppliers
* Extracts supplier attributes
* Outputs structured raw JSON

#### Writer Agent

* Cleans and normalizes supplier data
* Generates structured comparison tables
* Ranks suppliers
* Produces executive summary report

#### Orchestrator

* Creates session/run ID
* Executes agents sequentially
* Validates schema between stages
* Stores artifacts
* Returns final results to UI

---

## Architecture Diagram

![Architecture Diagram](images/Architecture_Diagram_1.png)

---

## Workflow

1. User submits manufacturing query
2. Orchestrator initializes session
3. Researcher Agent generates raw supplier dataset
4. Schema validation occurs
5. Writer Agent generates structured report
6. Artifacts stored
7. UI displays final output

---

## Project Structure

```
Multi-agent-system/
│
├── agents.py          # Agent definitions
├── orchestrator.py    # Workflow controller
├── tasks.py           # Task definitions
├── schemas.py         # JSON validation models
├── storage.py         # File-based persistence
├── frontend.py        # Streamlit UI
├── requirements.txt
└── artifacts/         # Generated run outputs
```

---

## Sample Output Artifacts

Each run generates:

```
artifacts/
  run_YYYYMMDD_HHMMSS/
    raw_suppliers.json
    structured_suppliers.json
    report.md
    state.json
```

---

## Tech Stack

* Python 3.10+
* CrewAI
* Gemini / LLM API
* Streamlit
* Pydantic (Schema Validation)

---

## 🛠 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/omtiwari17/Multi-agent-system.git
cd Multi-agent-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
CREWAI_DISABLE_TELEMETRY=true
```

---

## Running the Application

```bash
streamlit run frontend.py
```

Open the browser at:

```
http://localhost:8501
```

---

## Example Query

```
Find aluminum die casting suppliers in India for automotive parts.
```

Output:

* Ranked supplier list
* Comparison table
* Risk and gap analysis
* Executive summary

---

## Design Highlights

✔ Role-based agent specialization
✔ JSON-based structured handoffs
✔ Schema validation between stages
✔ Run-based artifact storage
✔ Clear separation of concerns
✔ Extensible architecture for additional agents

---

## Future Enhancements

* Add Compliance Agent
* Add RFQ Generator Agent
* Add Negotiation Strategy Agent
* Integrate vector database (RAG)
* Deploy backend as REST API
* Add Docker containerization
* Add caching layer
* Add rate-limit fallback logic

---

## Non-Functional Considerations

* Session isolation
* Controlled retries for LLM errors
* No API key persistence
* Deterministic workflow states
* Structured artifact logging

---

## Development Goals

This project demonstrates:

* Multi-agent orchestration
* LLM workflow engineering
* State management
* Structured output enforcement
* Practical AI system design

---

## Authors

* Om Tiwari 
* Paridhi Shirwalkar 
* Nitesh Chourasiya 
* Mradul Jain 
