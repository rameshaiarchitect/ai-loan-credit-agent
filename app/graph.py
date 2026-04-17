from langgraph.graph import StateGraph
from typing import TypedDict

from app.agents import parse_agent, risk_agent, fraud_agent, compliance_agent
from app.decision import decision_agent


class LoanState(TypedDict, total=False):
    message: str
    amount: float
    salary: float
    risk_score: float
    fraud_flag: bool
    compliance_flag: bool
    decision: str
    reason: str
    test_mode: bool


def parse_node(state: LoanState):
    return parse_agent(state.get("message", ""))


def risk_node(state: LoanState):
    return risk_agent(state)


def fraud_node(state: LoanState):
    return fraud_agent(state)


def compliance_node(state: LoanState):
    return compliance_agent(state)


def merge_node(state: LoanState):
    return {}


def decision_node(state: LoanState):
    return decision_agent(state)


def build_graph():
    graph = StateGraph(LoanState)

    graph.add_node("parse", parse_node)
    graph.add_node("risk", risk_node)
    graph.add_node("fraud", fraud_node)
    graph.add_node("compliance", compliance_node)
    graph.add_node("merge", merge_node)
    graph.add_node("decision", decision_node)

    graph.set_entry_point("parse")

    graph.add_edge("parse", "risk")
    graph.add_edge("parse", "fraud")
    graph.add_edge("parse", "compliance")

    graph.add_edge("risk", "merge")
    graph.add_edge("fraud", "merge")
    graph.add_edge("compliance", "merge")

    graph.add_edge("merge", "decision")

    return graph.compile()


def evaluate(message: str):
    graph = build_graph()

    result = graph.invoke({"message": message})

    return {
        "decision": result.get("decision", "REJECTED"),
        "risk_score": result.get("risk_score", 1.0),
        "reason": result.get("reason", "Unknown")
    }