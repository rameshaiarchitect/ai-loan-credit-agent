from langgraph.graph import StateGraph
from typing import TypedDict

from app.decision import parse_agent, risk_agent, fraud_agent, decision_agent, compliance_agent

class LoanState(TypedDict, total=False):
    message: str
    amount: float
    salary: float
    risk_score: float
    fraud_flag: bool
    decision: str
    reason: str
    test_mode: bool


# --- Nodes ---

def parse_node(state: LoanState):
    message = state.get("message")
    if not message:
        return {}

    return parse_agent(message)


def risk_node(state: LoanState):
    return risk_agent(state)


def fraud_node(state: LoanState):
    return fraud_agent(state)


def decision_node(state: LoanState):
    return decision_agent(state)

def merge_node(state: LoanState):
    # just pass state forward (ensures synchronization)
    return {}

def compliance_node(state: LoanState):
    return compliance_agent(state)


# --- Graph ---

def build_graph():
    graph = StateGraph(LoanState)

    graph.add_node("parse", parse_node)
    graph.add_node("risk", risk_node)
    graph.add_node("fraud", fraud_node)
    graph.add_node("decision", decision_node)
    graph.add_node("merge", merge_node)
    graph.add_node("compliance", compliance_node)

    graph.set_entry_point("parse")

    # Parallel execution
    graph.add_edge("parse", "risk")
    graph.add_edge("parse", "fraud")
    graph.add_edge("parse", "compliance")

    # Merge into decision
    graph.add_edge("risk", "merge")
    graph.add_edge("fraud", "merge")
    graph.add_edge("compliance", "merge")

    graph.add_edge("merge", "decision")

    return graph.compile()


# --- Public API ---

def evaluate(message: str, test_mode: bool = False):
    graph = build_graph()

    result = graph.invoke({
        "message": message,
        "test_mode": test_mode   # 👈 ADD THIS
    })

    return {
        "decision": result.get("decision", "REJECTED"),
        "risk_score": result.get("risk_score", 1.0),
        "reason": result.get("reason", "Unknown")
    }