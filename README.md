# 🧠 S.I.M.T.E.A.M

![https://simteam.danielpham.com.au/](docs/hero.png)

https://simteam.danielpham.com.au/

> **"Simulate. Predict. Explain. Optimise."**
> A full-stack analytics & AI platform for organisational design, built with commercial-grade technologies and shaped by real enterprise experience.

---

## 📌 Project Summary

**SimTeam** is a full-stack, end-to-end platform for:

* Simulating organisational dynamics: hiring, promotions, attrition
* Generating predictive insights through surrogate models
* Enabling natural language analytics using LLM-style SQL agents
* Visualising evolving org structures through interactive charts

It blends modern software engineering, machine learning, simulation logic, and cloud-native deployment—offering a complete demonstration of **full-stack data science and engineering**.

---

## 🔧 Features

### 🏢 Organisational Simulator

* Agent-based simulator using modular, object-oriented Pydantic models
* Role-based life cycle: `HIRE`, `PROMOTE`, `LEFT`, `REORG`
* Logic split across Hiring, Promotion, Vacancy, Manager Reassignment modules
* Simulates daily organisational state transitions

### 📊 Streamlit Interface + Custom Org Chart

* Streamlit dashboard with:

  * Time series views
  * Daily snapshot filtering
  * Console-style logs
* Custom **React-based org chart** using `d3-org-chart`:

  * Neon-aerospace theme
  * Metadata-rich nodes: salary, position, reports, contact

### 🤖 Surrogate Modelling with AutoML

* Batch simulations exported to train predictive models
* FLAML AutoML used to estimate final outcomes (e.g. team size, churn)
* Fast scenario prototyping and counterfactual exploration without re-simulation

### 💬 PydanticAI SQL Agent (LLM-style interface)

* Secure, schema-aware natural language queries
* Connects to live Postgres via SQLAlchemy ORM
* Business logic prompt engineering (e.g. “current employee” defined via last event)
* Powered by PydanticAI (drop-in LangChain alternative)

### 🌐 FastAPI Backend

* Modular API exposing:

  * `/simulate` → Run simulation with parameters
  * `/model/predict` → Use trained surrogate model
  * `/event-log` and `/employees` → View current and past org state
* All endpoints are typed with Pydantic and backed by ORM

---

## 🧱 Tech Stack

| Layer               | Technologies Used                                                      |
| ------------------- | ---------------------------------------------------------------------- |
| **Frontend**        | Streamlit, Custom React Component (`d3-org-chart`)                     |
| **Backend**         | FastAPI, Pydantic, SQLAlchemy ORM, PostgreSQL                          |
| **Simulation**      | OOP with Pydantic under `simteam/core`, modular simulation logic       |
| **AutoML**          | FLAML (Fast Lightweight AutoML)                                        |
| **LLM Integration** | PydanticAI + custom prompt templates                                   |
| **Deployment**      | Docker, NGINX, hosted on **Google Cloud Platform (GCP)** via Cloud Run |

---

## 🧩 Project Structure

```
simteam/
├── core/                  # Simulation logic (Pydantic + OOP modules)
│   ├── models/            # EmployeeState, EventLog, Organisation logic
│   └── simulator/         # Modular rule logic: hire, promote, etc.
│
├── server/                # FastAPI app and routers
│   └── db/                # SQLAlchemy engine, session, base models
│
├── ui/
│   ├── main.py            # Streamlit interface
│   ├── pydanticai/        # SQL agent logic with prompt templates
│   └── components/        # Custom React org chart
│       └── org_chart_component/
│           └── streamlit_register.py
│
├── automl/                # FLAML surrogate model training/inference
├── training_data/         # Data exports from simulations
├── Dockerfile             # Containerized setup
└── .env                   # GCP/DB configuration
```

---

## 🌍 Deployment (GCP Cloud Run + Docker)

Each service (Streamlit, API) is deployable independently using Docker, GCP Cloud Run, and optional Cloudflare Load Balancer. `nginx.conf` is dynamically generated using `envsubst`.

### 🚀 Local Setup

```bash
# FastAPI backend
uvicorn simteam.server.main:app --reload

# Streamlit frontend
streamlit run simteam/ui/main.py

# React org chart component
cd simteam/ui/components/org_chart_component
npm install
npm run build
```

---

## 💡 Why This Demonstrates Full-Stack Data Science & Engineering

| Layer                   | Description                                                  |
| ----------------------- | ------------------------------------------------------------ |
| **Data Engineering**    | PostgreSQL, SQLAlchemy ORM, secure live DB access            |
| **Simulation Science**  | Daily lifecycle simulation with rules-based agent modelling  |
| **Machine Learning**    | Surrogate modelling pipeline using FLAML                     |
| **AI/LLM Integration**  | Prompt-tuned SQL agent with live Pydantic schema binding     |
| **Web App Development** | Streamlit dashboard + React component embedding              |
| **API Design**          | FastAPI endpoints with typed I/O and extensible architecture |
| **DevOps & Hosting**    | Docker + GCP Cloud Run + NGINX reverse proxy                 |

---

## ✅ Use Cases

* Forecast team growth under different attrition/promotion strategies
* Predict organisational KPIs without running full simulations
* Explore historical promotion or attrition patterns with natural language
* Visualise team structure and succession chains interactively

---

## 🔒 Security & Guardrails

* Read-only DB access for agents
* SQL injection resistant via ORM
* Prompt templates use enforced business logic (e.g. filtering for current employees)
* Clear separation between data access, model, and UI layers

---

## 🙋 Author

**Daniel Pham**
PhD (Data Science) | CSL Ltd
Full-Stack Data Scientist & Simulation Optimiser
