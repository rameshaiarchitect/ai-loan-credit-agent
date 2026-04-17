from app.agents import parse_agent, risk_agent, fraud_agent, compliance_agent
from app.decision import decision_agent


def process_message(message_value: str, test_mode: bool = False):

    # ✅ TEST MODE → deterministic pipeline (NO GRAPH)
    if test_mode:
        data = parse_agent(message_value)

        data.update(risk_agent(data))
        data.update(fraud_agent(data))
        data.update(compliance_agent(data))

        data["test_mode"] = True

        return decision_agent(data)

    # ✅ NORMAL FLOW (Graph)
    from app.graph import evaluate
    return evaluate(message_value)


def create_consumer():
    from kafka import KafkaConsumer

    return KafkaConsumer(
        "loan.application.submitted",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="credit-agent-group-v3",
        value_deserializer=lambda x: x.decode("utf-8")
    )


def consume_events():
    consumer = create_consumer()

    print("Credit Agent started listening...")

    consumer.poll(timeout_ms=1000)

    while True:
        records = consumer.poll(timeout_ms=2000)

        for _, msgs in records.items():
            for message in msgs:
                result = process_message(message.value)

                print(f"Received event: {message.value}")
                print(
                    f"Decision: {result['decision']}, "
                    f"Risk: {result.get('risk_score', 'NA')}, "
                    f"Reason: {result['reason']}"
                )