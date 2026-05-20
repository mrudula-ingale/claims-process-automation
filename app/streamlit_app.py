import streamlit as st

from claims_automation.query_manager import execute_query_from_file

# --------------------------------------------------
# 1. Page configuration
# --------------------------------------------------
# This sets the browser tab title and makes the dashboard use full page width.

st.set_page_config(
    page_title="Claims Process Automation Dashboard",
    layout="wide",
)


# --------------------------------------------------
# 2. Dashboard title and description
# --------------------------------------------------

st.title("Claims Process Automation Dashboard")

st.write(
    """
    This dashboard analyzes synthetic insurance claims data using SQL and Python
    automation to monitor process workload, delayed claims, and operational KPIs.
    """
)


# --------------------------------------------------
# 3. Load data from SQL query files
# --------------------------------------------------
# Streamlit reruns the script whenever the page updates.
# @st.cache_data stores the query results temporarily, so the database is not
# queried again unnecessarily on every rerun.


@st.cache_data
def load_dashboard_data():
    """
    Load all dashboard datasets from SQL query files.

    Each key in the dictionary is a dataset name.
    Each value is a pandas DataFrame returned from a SQL file.
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
        "priority_distribution": execute_query_from_file("priority_distribution"),
    }


# Actually call the cached function and store all query results in `data`.
data = load_dashboard_data()


# --------------------------------------------------
# 4. Assign query results to readable DataFrame names
# --------------------------------------------------
# This makes the rest of the dashboard easier to read.

row_counts_df = data["row_counts"]
claims_by_status_df = data["claims_by_status"]
department_workload_df = data["department_workload"]
delayed_claims_df = data["delayed_claims"]
average_processing_time_df = data["average_processing_time"]
high_value_claims_df = data["high_value_claims"]
open_claims_df = data["open_claims"]
monthly_claim_volume_df = data["monthly_claim_volume"]
approval_rejection_rate_df = data["approval_rejection_rate"]
priority_distribution_df = data["priority_distribution"]


# --------------------------------------------------
# 5. Calculate KPI values
# --------------------------------------------------
# KPIs are single-number business metrics shown at the top of the dashboard.

# Total number of claims from the row_counts query.
total_claims = int(
    row_counts_df.loc[
        row_counts_df["table_name"] == "claims",
        "row_count",
    ].iloc[0]
)

# Total number of payment records.
payments = int(
    row_counts_df.loc[
        row_counts_df["table_name"] == "payments",
        "row_count",
    ].iloc[0]
)

# Number of open claims.
# Here, open_claims_df already contains only claims that are not rejected,
# paid, or closed. So len(open_claims_df) gives the open claim count.
open_claims = len(open_claims_df)

# Number of delayed claims.
# delayed_claims_df already contains only open claims older than the delay
# threshold defined in delayed_claims.sql.
delayed_claims = len(delayed_claims_df)

# Number of high-value claims.
# high_value_claims_df already contains only claims above the amount threshold
# defined in high_value_claims.sql.
high_value_claims = len(high_value_claims_df)

# Average processing time for completed claims.
average_processing_days = float(
    average_processing_time_df["average_processing_days"].iloc[0]
)

# Approval and rejection rates from approval_rejection_rate.sql.
approval_rate = float(approval_rejection_rate_df["approval_rate_percent"].iloc[0])

rejection_rate = float(approval_rejection_rate_df["rejection_rate_percent"].iloc[0])

# Percentage of open claims that are delayed.
# This is a useful business insight because it shows backlog severity.
delayed_rate = round((delayed_claims / open_claims) * 100, 1)


# --------------------------------------------------
# 6. KPI cards
# --------------------------------------------------
# This section displays the main dashboard numbers using st.metric().

st.subheader("Key Performance Indicators")

# First row of KPI cards.
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Claims", total_claims)
col2.metric("Open Claims", open_claims)
col3.metric("Delayed Claims", delayed_claims)
col4.metric("Avg Processing Days", average_processing_days)

# Second row of KPI cards.
col5, col6, col7, col8 = st.columns(4)

col5.metric("High-Value Claims", high_value_claims)
col6.metric("Payments", payments)
col7.metric("Approval Rate", f"{approval_rate}%")
col8.metric("Rejection Rate", f"{rejection_rate}%")


# --------------------------------------------------
# 7. Business insight summary
# --------------------------------------------------
# This text converts raw numbers into business interpretation.

st.info(
    f"""
    Key insight: {delayed_rate}% of open claims are delayed.
    This suggests a potential backlog in active claims processing.
    """
)


# --------------------------------------------------
# 8. Dashboard tabs
# --------------------------------------------------
# Tabs make the dashboard easier to navigate.

overview_tab, operations_tab, explorer_tab = st.tabs(
    ["Overview", "Operations", "Claims Explorer"]
)


# --------------------------------------------------
# 8.1 Overview tab
# --------------------------------------------------

with overview_tab:
    st.subheader("Operational Insights")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Claims by Status")
        st.bar_chart(
            claims_by_status_df,
            x="status",
            y="total_claims",
        )

    with chart_col2:
        st.subheader("Open Claims by Department")
        st.bar_chart(
            department_workload_df,
            x="department_name",
            y="open_claims",
        )

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        st.subheader("Monthly Claim Volume")
        st.line_chart(
            monthly_claim_volume_df,
            x="claim_month",
            y="total_claims",
        )

    with chart_col4:
        st.subheader("Priority Distribution")
        st.bar_chart(
            priority_distribution_df,
            x="priority",
            y="total_claims",
        )


# --------------------------------------------------
# 8.2 Operations tab
# --------------------------------------------------

with operations_tab:
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


# --------------------------------------------------
# 8.3 Claims Explorer tab
# --------------------------------------------------

with explorer_tab:
    st.subheader("Open Claims")

    st.dataframe(
        open_claims_df,
        width="stretch",
    )
