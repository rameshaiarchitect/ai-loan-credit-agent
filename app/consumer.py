from kafka import KafkaConsumer
from app.decision import decide

def process_message(message_value: str) -> str:
    return decide(message_value)

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

    consumer.poll(timeout_ms=1000)

    while True:
        records = consumer.poll(timeout_ms=2000)

        for _, msgs in records.items():
            for message in msgs:
                print(f"Received event: {message.value}")
                decision = process_message(message.value)
                print(f"Decision: {decision}")