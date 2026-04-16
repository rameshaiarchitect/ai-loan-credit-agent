from kafka import KafkaConsumer

def create_consumer():
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

    # Initial poll to trigger partition assignment
    consumer.poll(timeout_ms=1000)

    while True:
        records = consumer.poll(timeout_ms=2000)

        for tp, msgs in records.items():
            for message in msgs:
                print(f"Received event: {message.value}")

                decision = "APPROVED" if "amount" in message.value else "REJECTED"
                print(f"Decision: {decision}")