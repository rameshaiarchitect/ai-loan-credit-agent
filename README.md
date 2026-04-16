# Credit Agent

AI-based microservice responsible for evaluating loan applications and
determining credit decisions.

------------------------------------------------------------------------

## Responsibilities

-   Consume loan application events from Kafka
-   Evaluate credit risk based on incoming data
-   Generate decision (APPROVED / REJECTED)
-   Print or publish results for downstream processing

------------------------------------------------------------------------

## Flow

Loan Service → Kafka → Credit Agent → Decision

------------------------------------------------------------------------

## Tech Stack

-   Python 3.11+
-   FastAPI
-   Kafka (kafka-python)
-   Uvicorn

------------------------------------------------------------------------

## Kafka Integration

-   Topic Consumed: `loan.application.submitted`
-   Consumer Group: `credit-agent-group`
-   Message Format: String (LoanRequest)

------------------------------------------------------------------------

## ▶️ Setup & Run Application

### 1. Install Dependencies

Ensure `uv` is installed, then run:

```bash
uv sync

### 2. Run Application

``` bash
uv run uvicorn app.main:app --reload
```

------------------------------------------------------------------------

## Logs

On successful consumption:

    Credit Agent started listening...
    Received event: LoanRequest(applicationId=..., amount=..., salary=...)
    Decision: APPROVED

------------------------------------------------------------------------

## 🧪 Testing

The service includes unit tests for core logic.

### Test Coverage

-   Decision logic (approval/rejection)
-   Consumer message processing
-   API health endpoint
-   Model validation

------------------------------------------------------------------------

## ▶️ Run Tests

``` bash
PYTHONPATH=. uv run pytest
```

------------------------------------------------------------------------

## 📊 Code Coverage

``` bash
PYTHONPATH=. uv run pytest --cov=app
```

Optional HTML report:

``` bash
PYTHONPATH=. uv run pytest --cov=app --cov-report=html
```

------------------------------------------------------------------------

## Notes

-   Uses event-driven architecture
-   Consumer runs in background thread using FastAPI lifespan
-   Kafka connectivity supports local Docker setup
-   Designed for scalability and extension with AI/ML models

------------------------------------------------------------------------

## Future Enhancements

-   Replace string parsing with JSON payload
-   Implement real credit scoring logic
-   Publish decision to Kafka (new topic)
-   Store decisions in database
-   Add retry and error handling
