import streamlit as st
import pandas as pd

from log_parser import auto_parse
from curator import curate_data
from visualizer import show_visualizations
from database import save_to_database

from utils import (
    calculate_health_score,
    format_file_size,
    safe_dataframe
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Diamond Miner",
    layout="wide"
)

# -----------------------------------
# LOAD CSS
# -----------------------------------
def load_css():

    with open("style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# -----------------------------------
# TITLE
# -----------------------------------
st.title("💎 Diamond Miner")

st.caption(
    "Turning Raw Data into Structured Intelligence"
)

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.title("💎 Diamond Miner")

st.sidebar.markdown(
    """
    Supported Formats:
    - LOG
    - CSV
    - JSON
    - TXT
    """
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Data Tables",
        "Quarantine",
        "Downloads",
        "About"
    ]
)

# -----------------------------------
# ABOUT PAGE
# -----------------------------------
if page == "About":

    st.markdown(
        "<h2><u>About Diamond Miner :</u></h2>",
        unsafe_allow_html=True
    )

    st.write(
        """
        Diamond Miner is a lightweight
        multi-format data curation platform
        designed to transform messy raw
        datasets into structured,
        analyzable intelligence.
        """
    )

    st.markdown(
        "<h3><u>Features :</u></h3>",
        unsafe_allow_html=True
    )

    st.write("- Multi-format parsing")
    st.write("- Automatic parser routing")
    st.write("- Quarantine architecture")
    st.write("- Privacy-safe curation")
    st.write("- Interactive analytics")
    st.write("- SQL database export")

    st.markdown(
        "<h3><u>Current Scope :</u></h3>",
        unsafe_allow_html=True
    )

    st.write(
        """
        Optimized for lightweight and
        medium-scale datasets on
        low-end hardware systems.
        """
    )

    st.markdown(
        "<h3><u>Future Scope :</u></h3>",
        unsafe_allow_html=True
    )

    st.write("- Android log parser")
    st.write("- Excel support")
    st.write("- XML support")
    st.write("- Chunk-based processing")
    st.write("- AI-assisted anomaly detection")

# -----------------------------------
# MAIN APP
# -----------------------------------
else:

    # -----------------------------------
    # FILE UPLOAD
    # -----------------------------------
    uploaded_file = st.file_uploader(
        "Upload log / csv / json / txt file",
        type=["log", "csv", "json", "txt"]
    )

    # -----------------------------------
    # NO FILE MESSAGE
    # -----------------------------------
    if not uploaded_file:

        st.info(
            "Upload a supported file to begin data curation."
        )

    else:

        # --------------------------------
        # FILE INFO
        # --------------------------------
        filename = uploaded_file.name

        file_size = format_file_size(
            uploaded_file.size
        )

        st.success(
            f"File uploaded: {filename}"
        )

        st.write(
            f"File Size: {file_size}"
        )

        # --------------------------------
        # AUTO PARSING
        # --------------------------------
        with st.spinner(
            "Parsing and curating data..."
        ):

            df_clean, df_trash = auto_parse(
                uploaded_file,
                filename
            )

            df_clean = safe_dataframe(
                df_clean
            )

            df_trash = safe_dataframe(
                df_trash
            )

            # Curate data
            df_clean = curate_data(
                df_clean
            )

        # --------------------------------
        # METRICS
        # --------------------------------
        total_records = (
            len(df_clean) + len(df_trash)
        )

        health_score = calculate_health_score(
            df_clean,
            df_trash
        )

        # --------------------------------
        # DASHBOARD PAGE
        # --------------------------------
        if page == "Dashboard":

            st.header("📊 Dashboard")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Total Records",
                total_records
            )

            col2.metric(
                "Diamonds",
                len(df_clean)
            )

            col3.metric(
                "Quarantined",
                len(df_trash)
            )

            col4.metric(
                "Health Score",
                f"{health_score:.2f}%"
            )

            show_visualizations(df_clean)
            # --------------------------------
            # PARSER CONFIDENCE
            # --------------------------------
            confidence = health_score

            st.subheader("🧠 Parser Confidence")

            st.progress(
                int(confidence)
            )

            st.write(
                f"Confidence Score: {confidence:.2f}%"
            )

        # --------------------------------
        # DATA TABLES PAGE
        # --------------------------------
        elif page == "Data Tables":

            st.header("💎 Curated Data")

            rows_to_show = st.slider(
                "Rows to display",
                10,
                500,
                50
            )

            st.dataframe(
                df_clean.head(rows_to_show),
                use_container_width=True
            )

            st.write(
                f"Showing {min(rows_to_show, len(df_clean))} rows"
            )
        # --------------------------------
        # QUARANTINE PAGE
        # --------------------------------
        elif page == "Quarantine":

            st.header("🌑 Quarantine Data")

            rows_to_show = st.slider(
                "Rows to display",
                10,
                500,
                50
            )

            st.dataframe(
                df_trash.head(rows_to_show),
                use_container_width=True
            )

        # --------------------------------
        # DOWNLOADS PAGE
        # --------------------------------
        elif page == "Downloads":

            st.header("⬇ Downloads")

            # -----------------------------
            # SAVE DATABASE
            # -----------------------------
            db_file = save_to_database(
                df_clean,
                df_trash
            )

            # -----------------------------
            # CLEAN DATA DOWNLOAD
            # -----------------------------
            if not df_clean.empty:

                csv_data = df_clean.to_csv(
                    index=False
                )

                st.download_button(
                    label="⬇ Download Curated CSV",
                    data=csv_data,
                    file_name="diamond_dataset.csv",
                    mime="text/csv"
                )

            else:

                st.warning(
                    "No curated data available."
                )

            # -----------------------------
            # QUARANTINE DOWNLOAD
            # -----------------------------
            if not df_trash.empty:

                quarantine_csv = df_trash.to_csv(
                    index=False
                )

                st.download_button(
                    label="⬇ Download Quarantine Data",
                    data=quarantine_csv,
                    file_name="quarantine_data.csv",
                    mime="text/csv"
                )

            else:

                st.info(
                    "No quarantine data available."
                )

            # -----------------------------
            # SQL DATABASE DOWNLOAD
            # -----------------------------
            try:

                with open(db_file, "rb") as db:

                    st.download_button(
                        label="⬇ Download SQL Database",
                        data=db,
                        file_name="diamond_miner.db",
                        mime="application/octet-stream"
                    )

            except Exception as e:

                st.error(
                    f"Database export failed: {e}"
                )

        # --------------------------------
        # FINAL STATUS
        # --------------------------------
        st.success(
            f"Processed {total_records} records successfully."
        )
        # -----------------------------------
        # CUSTOM FOOTER
        # -----------------------------------
        st.markdown(
            """
            <div class="custom-footer">
                💎 Diamond Miner |
                Intelligent Data Curation Platform
            </div>
            """,
            unsafe_allow_html=True
        )