import random
import sqlite3
from datetime import timedelta

import pandas as pd
from faker import Faker

from claims_automation.config import DATABASE_PATH

fake = Faker()


DEPARTMENTS = [
    "Auto Claims",
    "Health Claims",
    "Property Claims",
    "Travel Claims",
    "Fraud Investigation",
]

CLAIM_TYPES = [
    "Car Accident",
    "Medical Expense",
    "Water Damage",
    "Flight Cancellation",
    "Theft",
]

STATUSES = [
    "submitted",
    "under_review",
    "documents_requested",
    "approved",
    "rejected",
    "paid",
    "closed",
]

PRIORITIES = [
    "low",
    "medium",
    "high",
]


def create_customers(num_customers: int = 200) -> pd.DataFrame:
    """Generate synthetic customer data."""
    customers = []

    for customer_id in range(1, num_customers + 1):
        customers.append(
            {
                "customer_id": customer_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.unique.email(),
                "city": fake.city(),
                "customer_since": fake.date_between(
                    start_date="-5y",
                    end_date="today",
                ),
            }
        )
    return pd.DataFrame(customers)


def create_departments() -> pd.DataFrame:
    """Generate synthetic department data."""
    departments = []

    for department_id, department_name in enumerate(DEPARTMENTS, start=1):
        departments.append(
            {
                "department_id": department_id,
                "department_name": department_name,
            }
        )

    return pd.DataFrame(departments)


def create_claims(num_claims: int = 1000) -> pd.DataFrame:
    """Generate synthetic insurance claims."""
    claims = []

    for claim_id in range(1, num_claims + 1):
        submitted_date = fake.date_between(
            start_date="-1y",
            end_date="today",
        )

        status = random.choices(
            population=[
                "submitted",
                "under_review",
                "documents_requested",
                "approved",
                "rejected",
                "paid",
                "closed",
            ],
            weights=[5, 10, 10, 20, 15, 20, 20],
            k=1,
        )[0]

        closed_date = None

        if status in ["paid", "closed", "rejected"]:
            closed_date = submitted_date + timedelta(days=random.randint(1, 30))

        claims.append(
            {
                "claim_id": claim_id,
                "customer_id": random.randint(1, 200),
                "department_id": random.randint(1, 5),
                "claim_type": random.choice(CLAIM_TYPES),
                "claim_amount": round(
                    random.uniform(100, 15000),
                    2,
                ),
                "status": status,
                "submitted_date": submitted_date,
                "closed_date": closed_date,
                "priority": random.choice(PRIORITIES),
            }
        )

    return pd.DataFrame(claims)


def create_claim_events(claims_df: pd.DataFrame) -> pd.DataFrame:
    """Generate claim status history events"""
    events = []

    event_id = 1

    for _, claim in claims_df.iterrows():
        submitted_date = pd.to_datetime(claim["submitted_date"])

        workflow = ["submitted", "under_review"]

        if random.random() < 0.3:
            workflow.append("documents_requested")
            workflow.append("under_review")

        final_status = claim["status"]

        if final_status not in workflow:
            workflow.append(final_status)

        current_date = submitted_date

        for status in workflow:
            current_date += timedelta(days=random.randint(1, 5))

            events.append(
                {
                    "event_id": event_id,
                    "claim_id": claim["claim_id"],
                    "event_status": status,
                    "event_date": current_date.date(),
                    "notes": fake.sentence(nb_words=6),
                }
            )

            event_id += 1

        return pd.DataFrame(events)


def create_payments(claims_df: pd.DataFrame) -> pd.DataFrame:
    """Generate payment records for paid/closed claims."""

    payments = []

    payment_id = 1

    eligible_claims = claims_df[claims_df["status"].isin(["paid", "closed"])]

    for _, claim in eligible_claims.iterrows():
        submitted_date = pd.to_datetime(claim["submitted_date"])

        payment_date = submitted_date + timedelta(days=random.randint(5, 20))

        payments.append(
            {
                "payment_id": payment_id,
                "claim_id": claim["claim_id"],
                "payment_amount": claim["claim_amount"],
                "payment_date": payment_date.date(),
                "payment_method": random.choice(
                    [
                        "Bank Transfer",
                        "Credit Card",
                        "PayPal",
                    ]
                ),
            }
        )

        payment_id += 1

    return pd.DataFrame(payments)


def load_dataframe_to_sqlite(
    customers_df: pd.DataFrame,
    departments_df: pd.DataFrame,
    claims_df: pd.DataFrame,
    events_df: pd.DataFrame,
    payments_df: pd.DataFrame,
) -> None:
    """Load generated DataFrames into SQLite database."""

    with sqlite3.connect(database=DATABASE_PATH) as connection:
        customers_df.to_sql(
            name="customers",
            con=connection,
            if_exists="append",
            index=False,
        )

        departments_df.to_sql(
            name="departments",
            con=connection,
            if_exists="append",
            index=False,
        )

        claims_df.to_sql(
            name="claims",
            con=connection,
            if_exists="append",
            index=False,
        )

        events_df.to_sql(
            name="claim_events",
            con=connection,
            if_exists="append",
            index=False,
        )

        payments_df.to_sql(
            name="payments",
            con=connection,
            if_exists="append",
            index=False,
        )

    print("Synthetic data loaded successfully.")


def main() -> None:
    """Generate and load synthetic data."""

    customers_df = create_customers()
    departments_df = create_departments()
    claims_df = create_claims()

    events_df = create_claim_events(claims_df=claims_df)
    payments_df = create_payments(claims_df=claims_df)

    load_dataframe_to_sqlite(
        customers_df=customers_df,
        departments_df=departments_df,
        claims_df=claims_df,
        events_df=events_df,
        payments_df=payments_df,
    )

    print("Data generation complete.")


if __name__ == "__main__":
    main()
