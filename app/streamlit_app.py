import streamlit as st

from claims_automation.query_manager import execute_query_from_file

st.set_page_config(
    page_title="Claims Process Automation Dashboard",
    layout="wide",
)

st.title("Claims Process Automation Dashboard")

st.write(
    """
    This dashboard analyzes synthetic insurance claims data using SQL and Python
    automation to monitor process workload, delayed claims, and operational KPIs.
    """
)


@st.cache_data
def load_dashboard_data():
    """
    Load all dashboard datasets from SQL query files.

    Streamlit reruns the script after interactions.
    Caching prevents unnecessary repeated database reads.
    """
    return {
        "row_counts": execute_query_from_file("row_counts"),
        "claims_by_status": execute_query_from_file("claims_by_status"),
        "department_workload": execute_query_from_file("department_workload"),
        "delayed_claims": execute_query_from_file("delayed_claims"),
        "average_processing_time": execute_query_from_file("average_processing_time"),
        "high_value_claims": execute_query_from_file("high_value_claims"),
        "open_claims": execute_query_from_file("open_claims"),
        "monthly_claim_volume": execute_query_from_file("monthly_claim_volume"),
        "approval_rejection_rate": execute_query_from_file("approval_rejection_rate"),
    }


data = load_dashboard_data()

row_counts_df = data["row_counts"]
claims_by_status_df = data["claims_by_status"]
department_workload_df = data["department_workload"]
delayed_claims_df = data["delayed_claims"]
average_processing_time_df = data["average_processing_time"]
high_value_claims_df = data["high_value_claims"]
open_claims_df = data["open_claims"]
monthly_claim_volume_df = data["monthly_claim_volume"]
approval_rejection_rate_df = data["approval_rejection_rate"]


total_claims = int(
    row_counts_df.loc[
        row_counts_df["table_name"] == "claims",
        "row_count",
    ].iloc[0]
)

payments = int(
    row_counts_df.loc[
        row_counts_df["table_name"] == "payments",
        "row_count",
    ].iloc[0]
)

open_claims = len(open_claims_df)
delayed_claims = len(delayed_claims_df)
high_value_claims = len(high_value_claims_df)

average_processing_days = float(
    average_processing_time_df["average_processing_days"].iloc[0]
)

approval_rate = float(approval_rejection_rate_df["approval_rate_percent"].iloc[0])

rejection_rate = float(approval_rejection_rate_df["rejection_rate_percent"].iloc[0])


st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Claims", total_claims)
col2.metric("Open Claims", open_claims)
col3.metric("Delayed Claims", delayed_claims)
col4.metric("Avg Processing Days", average_processing_days)

col5, col6, col7, col8 = st.columns(4)

col5.metric("High-Value Claims", high_value_claims)
col6.metric("Payments", payments)
col7.metric("Approval Rate", f"{approval_rate}%")
col8.metric("Rejection Rate", f"{rejection_rate}%")


# --------------------------------------------------
# Dashboard charts
# --------------------------------------------------

st.subheader("Operational Insights")

# Create 2 columns for side-by-side charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Claims by Status")

    st.bar_chart(
        claims_by_status_df,
        x="status",
        y="total_claims",
    )

with col2:
    st.subheader("Open Claims by Department")

    st.bar_chart(
        department_workload_df,
        x="department_name",
        y="open_claims",
    )


# Second row of charts
col3, col4 = st.columns(2)

with col3:
    st.subheader("Monthly Claim Volume")

    st.line_chart(
        monthly_claim_volume_df,
        x="claim_month",
        y="total_claims",
    )

with col4:
    st.subheader("Claims Status Distribution")

    st.bar_chart(
        claims_by_status_df,
        x="status",
        y="total_claims",
    )

st.subheader("Open Claims")

st.dataframe(
    open_claims_df,
    width="stretch",
)


st.subheader("Delayed Claims")

st.dataframe(
    delayed_claims_df,
    width="stretch",
)


st.subheader("High-Value Claims")

st.dataframe(
    high_value_claims_df,
    width="stretch",
)
