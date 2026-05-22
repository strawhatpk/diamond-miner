import streamlit as st
import plotly.express as px


def show_visualizations(df):

    if df.empty:

        st.warning(
            "No data available for visualization."
        )

        return

    st.subheader("📊 Analytics Dashboard")

    # ---------------------------------
    # STATUS DISTRIBUTION
    # ---------------------------------
    if "status" in df.columns:

        status_counts = (
            df["status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "status",
            "count"
        ]

        fig_status = px.bar(
            status_counts,
            x="status",
            y="count",
            title="HTTP Status Distribution",
            color="count",
            color_continuous_scale="Turbo"
        )

        fig_status.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font_color="#ffffff"
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True
        )

    # ---------------------------------
    # PRIORITY DISTRIBUTION
    # ---------------------------------
    if "priority" in df.columns:

        priority_counts = (
            df["priority"]
            .value_counts()
            .reset_index()
        )

        priority_counts.columns = [
            "priority",
            "count"
        ]

        fig_priority = px.pie(
            priority_counts,
            names="priority",
            values="count",
            title="Priority Distribution",
            color_discrete_sequence=[
                "#00ffff",
                "#8b5cf6",
                "#ec4899"
            ]
        )

        fig_priority.update_layout(
            paper_bgcolor="#0f172a",
            font_color="#ffffff"
        )

        st.plotly_chart(
            fig_priority,
            use_container_width=True
        )

    # ---------------------------------
    # TOP URLS
    # ---------------------------------
    if "url" in df.columns:

        top_urls = (
            df["url"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_urls.columns = [
            "url",
            "count"
        ]

        fig_urls = px.bar(
            top_urls,
            x="url",
            y="count",
            title="Top Requested URLs",
            color="count",
            color_continuous_scale="Plasma"
        )

        fig_urls.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font_color="#ffffff"
        )

        st.plotly_chart(
            fig_urls,
            use_container_width=True
        )