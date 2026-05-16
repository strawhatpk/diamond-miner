import streamlit as st
import re
import pandas as pd

st.title("💎 Diamond Miner")

# Upload option
uploaded_file = st.file_uploader(
    "Upload your log / txt / csv file",
    type=["log", "txt", "csv"]
)

# Local file option
use_local = st.checkbox("Use local file (for large files)")
file_path = st.text_input("Enter file path (for large file)")

# Process condition
if uploaded_file or (use_local and file_path):

    # Decide file source
    if use_local and file_path:
        file = open(file_path, "rb")
        st.success(f"Using local file: {file_path}")
    else:
        file = uploaded_file
        st.success(f"File uploaded: {uploaded_file.name}")

    # Regex pattern
    log_pattern = r'(?P<ip>\S+) \S+ \S+ \[(?P<date>.*?)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d+) (?P<size>\S+)'

    structured_data = []
    quarantine_data = []

    # Parse logs (limit for testing)
    for i, line in enumerate(file):
        if i >= 10000:
            break

        line = line.decode("utf-8", errors="ignore").strip()

        if not line:
            continue

        match = re.search(log_pattern, line)

        if match:
            structured_data.append(match.groupdict())
        else:
            quarantine_data.append({
                "raw_line": line,
                "issue": "Format Mismatch"
            })

    # Convert to DataFrame
    df_clean = pd.DataFrame(structured_data)

    if quarantine_data:
        df_trash = pd.DataFrame(quarantine_data)
    else:
        df_trash = pd.DataFrame(columns=["raw_line", "issue"])

    # Display results
    rows_to_show = st.slider("Select number of rows to display", 10, 500, 50)
    st.subheader("💎 Diamonds (Parsed Data)")
    st.dataframe(df_clean.head(rows_to_show))

    st.subheader("🌑 Quarantine (Bad Data)")
    st.dataframe(df_trash.head(rows_to_show))

    st.success(f"Parsed {len(df_clean)} clean records, {len(df_trash)} quarantined")