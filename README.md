# Credit Agent – AI Loan Decision System

AI-powered microservice that evaluates loan applications using a hybrid architecture combining deterministic rules and LLM-based reasoning.

---

## Overview

This service is part of an event-driven system where loan applications are processed and evaluated using:

- Rule-based agents (risk, fraud, compliance)
- LangGraph orchestration
- LLM-based decision reasoning

---

## Architecture

Loan Service → Kafka → Credit Agent → Decision
                         ↓
                  LangGraph Flow
                         ↓
     Risk Agent | Fraud Agent | Compliance Agent
                         ↓
                 Decision Agent (LLM)
                         ↓
                    Final Decision

---

## Key Features

### Multi-Agent System (LangGraph)

- Parallel execution of:
  - Risk evaluation
  - Fraud detection
  - Compliance checks

### Hybrid AI Decision Engine

- Deterministic rules:
  - Fraud → immediate rejection
  - Compliance failure → immediate rejection

- LLM reasoning:
  - Final decision based on risk score
  - Structured output using Pydantic

### Production-Ready Design

- Separation of concerns:
  - agents.py → business logic
  - graph.py → orchestration
  - decision.py → LLM reasoning
- Deterministic testing (no LLM dependency)
- Structured LLM output

---

## Tech Stack

- Python 3.11+
- FastAPI
- Kafka (kafka-python)
- LangGraph
- LangChain
- OpenAI (GPT-4o-mini)
- Pydantic

---

## Setup & Run

### Install Dependencies

uv sync

### Run Application

uv run uvicorn app.main:app --reload

---

## Testing

uv run pytest

---

## Coverage

uv run pytest --cov=app

---

## Design Decisions

- Avoided tool-based agents for strict financial rules
- Used deterministic agents for reliability
- Used LLM only for reasoning

---

## Future Enhancements

- JSON-based Kafka messages
- Kafka decision publishing
- Database integration
- RAG integration
- Observability (metrics, tracing)
- SonarQube integration

---

## Summary

This project demonstrates:

- AI-native system design
- Multi-agent orchestration
- Hybrid decision systems
- Production-ready LLM usage
