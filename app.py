
import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Website Traffic Analysis",
    page_icon="📊",
    layout="wide"
)

# Consistent chart appearance
chart_template = "plotly_white"
chart_colors = px.colors.qualitative.Set2

# --------------------------------------------------
# 2. LOAD DATASET
# --------------------------------------------------

df = pd.read_csv("Dataset/Website_Traffic_Analysis_Dataset.csv")

df["Date"] = pd.to_datetime(df["Date"])

# --------------------------------------------------
# 3. DASHBOARD TITLE
# --------------------------------------------------

st.title("📊 Website Traffic Analysis Dashboard")

st.markdown(
    "Analyze website traffic, user engagement, "
    "conversion performance and page effectiveness."
)

st.divider()

# --------------------------------------------------
# 4. DATASET PREVIEW
# --------------------------------------------------

with st.expander("📁 Preview Original Dataset"):
    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.caption(f"Total records in dataset: {len(df):,}")

# --------------------------------------------------
# 5. INTERACTIVE FILTERS
# --------------------------------------------------

st.subheader("🔎 Dashboard Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

month_options = [
    calendar.month_name[m]
    for m in sorted(df["Date"].dt.month.unique())
]

with filter_col1:
    selected_source = st.selectbox(
        "Traffic Source",
        ["All"] + sorted(df["Traffic_Source"].unique().tolist())
    )

with filter_col2:
    selected_device = st.selectbox(
        "Device",
        ["All"] + sorted(df["Device"].unique().tolist())
    )

with filter_col3:
    selected_month = st.selectbox(
        "Month",
        ["All"] + month_options
    )

# --------------------------------------------------
# 6. APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

if selected_source != "All":
    filtered_df = filtered_df[
        filtered_df["Traffic_Source"] == selected_source
    ]

if selected_device != "All":
    filtered_df = filtered_df[
        filtered_df["Device"] == selected_device
    ]

if selected_month != "All":
    filtered_df = filtered_df[
        filtered_df["Date"].dt.month_name() == selected_month
    ]

st.caption(f"Showing {len(filtered_df):,} matching sessions.")

st.divider()

# --------------------------------------------------
# 7. CALCULATE KPIs
# --------------------------------------------------

total_sessions = len(filtered_df)

total_users = filtered_df["User_ID"].nunique()

if total_sessions > 0:
    bounce_rate = filtered_df["Bounce"].mean() * 100
    conversion_rate = filtered_df["Conversion"].mean() * 100
else:
    bounce_rate = 0
    conversion_rate = 0

# --------------------------------------------------
# 8. DISPLAY KPI CARDS
# --------------------------------------------------

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sessions", f"{total_sessions:,}")
col2.metric("Total Users", f"{total_users:,}")
col3.metric("Bounce Rate", f"{bounce_rate:.2f}%")
col4.metric("Conversion Rate", f"{conversion_rate:.2f}%")

st.divider()

# --------------------------------------------------
# 9. SHOW FILTERED DATA
# --------------------------------------------------

with st.expander("📋 View Filtered Website Data"):
    st.dataframe(
        filtered_df.head(100),
        use_container_width=True
    )

# --------------------------------------------------
# 10. CHECK FILTERED DATA
# --------------------------------------------------

if filtered_df.empty:

    st.warning(
        "No records found for the selected filters. "
        "Please select different filter options."
    )

else:

    # --------------------------------------------------
    # 11. WEBSITE TRAFFIC BY SOURCE
    # --------------------------------------------------

    st.subheader("🌐 Traffic Analysis")

    traffic_source = (
        filtered_df["Traffic_Source"]
        .value_counts()
        .reset_index()
    )

    traffic_source.columns = [
        "Traffic Source",
        "Total Sessions"
    ]

    fig1 = px.bar(
        traffic_source,
        x="Traffic Source",
        y="Total Sessions",
        color="Traffic Source",
        text="Total Sessions",
        color_discrete_sequence=chart_colors,
        template=chart_template,
        title="Website Traffic by Source"
    )

    fig1.update_traces(textposition="outside")
    fig1.update_layout(showlegend=False)

    # --------------------------------------------------
    # 12. WEBSITE TRAFFIC BY DEVICE
    # --------------------------------------------------

    device_data = (
        filtered_df["Device"]
        .value_counts()
        .reset_index()
    )

    device_data.columns = [
        "Device",
        "Total Sessions"
    ]

    fig2 = px.pie(
        device_data,
        names="Device",
        values="Total Sessions",
        hole=0.45,
        color_discrete_sequence=chart_colors,
        template=chart_template,
        title="Website Traffic by Device"
    )

    fig2.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    # Display first two charts side by side
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.plotly_chart(
            fig1,
            use_container_width=True,
            key="traffic_source_chart"
        )

    with chart_col2:
        st.plotly_chart(
            fig2,
            use_container_width=True,
            key="device_traffic_chart"
        )

    st.divider()

    # --------------------------------------------------
    # 13. CONVERSION RATE BY TRAFFIC SOURCE
    # --------------------------------------------------

    st.subheader("🎯 Conversion Analysis")

    source_conversion = filtered_df.groupby(
        "Traffic_Source"
    ).agg(
        Total_Sessions=("Session_ID", "count"),
        Total_Conversions=("Conversion", "sum")
    ).reset_index()

    source_conversion["Conversion_Rate"] = (
        source_conversion["Total_Conversions"] /
        source_conversion["Total_Sessions"] * 100
    )

    fig3 = px.bar(
        source_conversion,
        x="Traffic_Source",
        y="Conversion_Rate",
        color="Traffic_Source",
        text=source_conversion["Conversion_Rate"].round(2).astype(str) + "%",
        color_discrete_sequence=chart_colors,
        template=chart_template,
        title="Conversion Rate by Traffic Source",
        labels={
            "Traffic_Source": "Traffic Source",
            "Conversion_Rate": "Conversion Rate (%)"
        }
    )

    fig3.update_traces(textposition="outside")
    fig3.update_layout(showlegend=False)

    # --------------------------------------------------
    # 14. CONVERSION RATE BY DEVICE
    # --------------------------------------------------

    device_conversion = filtered_df.groupby(
        "Device"
    ).agg(
        Total_Sessions=("Session_ID", "count"),
        Total_Conversions=("Conversion", "sum")
    ).reset_index()

    device_conversion["Conversion_Rate"] = (
        device_conversion["Total_Conversions"] /
        device_conversion["Total_Sessions"] * 100
    )

    fig4 = px.bar(
        device_conversion,
        x="Device",
        y="Conversion_Rate",
        color="Device",
        text=device_conversion["Conversion_Rate"].round(2).astype(str) + "%",
        color_discrete_sequence=chart_colors,
        template=chart_template,
        title="Conversion Rate by Device",
        labels={
            "Device": "Device",
            "Conversion_Rate": "Conversion Rate (%)"
        }
    )

    fig4.update_traces(textposition="outside")
    fig4.update_layout(showlegend=False)

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        st.plotly_chart(
            fig3,
            use_container_width=True,
            key="source_conversion_chart"
        )

    with chart_col4:
        st.plotly_chart(
            fig4,
            use_container_width=True,
            key="device_conversion_chart"
        )

    # Optional conversion summary tables
    with st.expander("View Conversion Summary Tables"):
        st.write("Conversion by Traffic Source")
        st.dataframe(
            source_conversion.round(2),
            use_container_width=True
        )

        st.write("Conversion by Device")
        st.dataframe(
            device_conversion.round(2),
            use_container_width=True
        )

    st.divider()

    # --------------------------------------------------
    # 15. MONTHLY WEBSITE TRAFFIC
    # --------------------------------------------------

    st.subheader("📅 Monthly Performance Analysis")

    monthly_traffic = filtered_df.groupby(
        filtered_df["Date"].dt.month
    ).size().reset_index(name="Total_Sessions")

    monthly_traffic = monthly_traffic.rename(
        columns={"Date": "Month_Number"}
    )

    monthly_traffic["Month"] = pd.to_datetime(
        monthly_traffic["Month_Number"],
        format="%m"
    ).dt.month_name()

    monthly_traffic = monthly_traffic.sort_values("Month_Number")

    fig5 = px.line(
        monthly_traffic,
        x="Month",
        y="Total_Sessions",
        markers=True,
        color_discrete_sequence=["#2563EB"],
        template=chart_template,
        title="Monthly Website Traffic Trend",
        labels={
            "Month": "Month",
            "Total_Sessions": "Total Sessions"
        }
    )

    fig5.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )

    # --------------------------------------------------
    # 16. MONTHLY CONVERSIONS
    # --------------------------------------------------

    monthly_conversion = filtered_df.groupby(
        filtered_df["Date"].dt.month
    ).agg(
        Total_Conversions=("Conversion", "sum")
    ).reset_index()

    monthly_conversion = monthly_conversion.rename(
        columns={"Date": "Month_Number"}
    )

    monthly_conversion["Month"] = pd.to_datetime(
        monthly_conversion["Month_Number"],
        format="%m"
    ).dt.month_name()

    monthly_conversion = monthly_conversion.sort_values("Month_Number")

    fig6 = px.line(
        monthly_conversion,
        x="Month",
        y="Total_Conversions",
        markers=True,
        color_discrete_sequence=["#16A34A"],
        template=chart_template,
        title="Monthly Conversion Trend",
        labels={
            "Month": "Month",
            "Total_Conversions": "Total Conversions"
        }
    )

    fig6.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )

    chart_col5, chart_col6 = st.columns(2)

    with chart_col5:
        st.plotly_chart(
            fig5,
            use_container_width=True,
            key="monthly_traffic_chart"
        )

    with chart_col6:
        st.plotly_chart(
            fig6,
            use_container_width=True,
            key="monthly_conversion_chart"
        )

    with st.expander("View Monthly Summary Tables"):
        st.write("Monthly Website Traffic")
        st.dataframe(
            monthly_traffic,
            use_container_width=True
        )

        st.write("Monthly Conversions")
        st.dataframe(
            monthly_conversion,
            use_container_width=True
        )

    st.divider()

    # --------------------------------------------------
    # 17. WEBSITE PAGE PERFORMANCE
    # --------------------------------------------------

    st.subheader("📄 Website Page Performance")

    page_performance = filtered_df.groupby(
        "Page_Visited"
    ).agg(
        Total_Sessions=("Session_ID", "count"),
        Total_Conversions=("Conversion", "sum"),
        Total_Bounces=("Bounce", "sum")
    ).reset_index()

    page_performance["Conversion_Rate"] = (
        page_performance["Total_Conversions"] /
        page_performance["Total_Sessions"] * 100
    )

    page_performance["Bounce_Rate"] = (
        page_performance["Total_Bounces"] /
        page_performance["Total_Sessions"] * 100
    )

    fig7 = px.bar(
        page_performance,
        x="Page_Visited",
        y="Total_Sessions",
        color="Page_Visited",
        text="Total_Sessions",
        color_discrete_sequence=chart_colors,
        template=chart_template,
        title="Website Traffic by Page",
        labels={
            "Page_Visited": "Website Page",
            "Total_Sessions": "Total Sessions"
        }
    )

    fig7.update_layout(showlegend=False)

    fig8 = px.bar(
        page_performance,
        x="Page_Visited",
        y="Conversion_Rate",
        color="Page_Visited",
        text=page_performance["Conversion_Rate"].round(2).astype(str) + "%",
        color_discrete_sequence=chart_colors,
        template=chart_template,
        title="Conversion Rate by Website Page",
        labels={
            "Page_Visited": "Website Page",
            "Conversion_Rate": "Conversion Rate (%)"
        }
    )

    fig8.update_layout(showlegend=False)

    chart_col7, chart_col8 = st.columns(2)

    with chart_col7:
        st.plotly_chart(
            fig7,
            use_container_width=True,
            key="page_traffic_chart"
        )

    with chart_col8:
        st.plotly_chart(
            fig8,
            use_container_width=True,
            key="page_conversion_chart"
        )

    with st.expander("View Website Page Performance Table"):
        st.dataframe(
            page_performance.round(2),
            use_container_width=True
        )

# --------------------------------------------------
# 18. DASHBOARD FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <p><b>Website Traffic Analysis Dashboard</b></p>
        <p>Developed using Python, Pandas, Plotly and Streamlit</p>
        <p>Portfolio Data Analysis Project | 2026</p>
    </div>
    """,
    unsafe_allow_html=True
)

