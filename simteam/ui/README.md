## Overview

A full-stack interactive platform that demonstrates **end-to-end data science, machine learning, and modern backend engineering** in a real-world setting.

* 🧠 **A simulation engine** modelling workforce dynamics (hiring, promotion, attrition)
* 🗂 **A live database backend** with a fully normalised schema and API access
* 🤖 **An LLM-powered AI assistant** that translates natural language into executable SQL
* 📈 **A machine learning meta-model** that predicts simulation outcomes using AutoML
* 💻 **A clean interactive frontend** built with Streamlit + custom React components

This project shows how to move from **code-based modelling and simulation** to a **production-style AI & analytics tool**, complete with cloud deployment, custom UI, and API interfaces.

---

## 🧩 System Overview

![GitHub](https://img.shields.io/badge/-black?logo=github)
![PydanticAI](https://img.shields.io/badge/-black?logo=pydantic&logoColor=E520E9)
![LangChain](https://img.shields.io/badge/-black?logo=langchain&logoColor=white)
![FastAPI](https://img.shields.io/badge/-black?logo=fastapi&logoColor=05998B)
![Streamlit](https://img.shields.io/badge/-black?logo=streamlit&logoColor=FF4B4B)
![PostgreSQL](https://img.shields.io/badge/-black?logo=postgresql&logoColor=336791)
![Google Cloud](https://img.shields.io/badge/-black?logo=google-cloud&logoColor=4285F4)
![Docker](https://img.shields.io/badge/-black?logo=docker&logoColor=2496ED)
![React](https://img.shields.io/badge/-black?logo=react&logoColor=)
![OpenAI](https://img.shields.io/badge/-black?logo=openai&logoColor=white)

| Component      | Role                                                                  |
| -------------- | --------------------------------------------------------------------- |
| **Simulator**  | OOP Python logic simulating employee events over time                 |
| **API Layer**  | FastAPI app exposing schema-validated endpoints at `/api/v1/docs`     |
| **Database**   | PostgreSQL + SQLAlchemy ORM, supporting historical event storage      |
| **LLM Agent**  | PydanticAI prompt engine with SQL validation & execution              |
| **Meta Model** | AutoML (via FLAML) to evaluate simulation outputs                     |
| **Frontend**   | Streamlit UI + React org chart for time-aware structure visualisation |
| **Deployment** | Docker + GCP Cloud Run, behind Cloudflare reverse proxy               |

---

## 🧭 Features in the Interface

* **ORG CHART**: Explore the company structure at any date; sidebar shows that day’s event stream.
* **AI CHATBOT**: Ask org-related questions in plain English (e.g. “Who was promoted last week?”).
* **META MODEL**: Run a full simulation and see how well a predictive model matches the outcome.

---

## 💡 Tips for Use

* Use the sidebar to select a date and observe personnel events.
* Hover `ℹ️` icons throughout the interface for help.
* Use the chatbot to query your organisation.
* Run "what-if" experiments using the meta model.

---

## 🔮 Future Features / Backlog

* [ ] Time-lapse visualisation of org chart
* [ ] Simulation scenario comparison and ranking
* [ ] Export functionality (CSV / PDF)
* [ ] AI query intent classification (HR, team, performance, etc.)
* [ ] Role-based access control (admin/user modes)
* [ ] Dashboard for key org metrics over time