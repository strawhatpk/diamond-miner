import re
import pandas as pd
import json

# Apache/Nginx regex
log_pattern = r'(?P<ip>\S+) \S+ \S+ \[(?P<date>.*?)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d+) (?P<size>\S+)'


# -----------------------------
# APACHE / NGINX LOG PARSER
# -----------------------------
def parse_log_file(file, limit=10000):

    structured_data = []
    quarantine_data = []

    for i, line in enumerate(file):

        if i >= limit:
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

    return build_dataframes(structured_data, quarantine_data)


# -----------------------------
# CSV PARSER
# -----------------------------
def parse_csv_file(file):

    try:
        df = pd.read_csv(file)

        quarantine = pd.DataFrame(
            columns=["raw_line", "issue"]
        )

        return df, quarantine

    except Exception as e:

        quarantine = pd.DataFrame([
            {
                "raw_line": "CSV Parsing Failed",
                "issue": str(e)
            }
        ])

        return pd.DataFrame(), quarantine


# -----------------------------
# JSON PARSER
# -----------------------------
def parse_json_file(file):

    try:

        data = json.load(file)

        df = pd.json_normalize(data)

        quarantine = pd.DataFrame(
            columns=["raw_line", "issue"]
        )

        return df, quarantine

    except Exception as e:

        quarantine = pd.DataFrame([
            {
                "raw_line": "JSON Parsing Failed",
                "issue": str(e)
            }
        ])

        return pd.DataFrame(), quarantine


# -----------------------------
# GENERIC TEXT PARSER
# -----------------------------
def parse_text_file(file, limit=10000):

    lines = []

    for i, line in enumerate(file):

        if i >= limit:
            break

        lines.append({
            "text": line.decode(
                "utf-8",
                errors="ignore"
            ).strip()
        })

    df = pd.DataFrame(lines)

    quarantine = pd.DataFrame(
        columns=["raw_line", "issue"]
    )

    return df, quarantine


# -----------------------------
# HELPER
# -----------------------------
def build_dataframes(
    structured_data,
    quarantine_data
):

    df_clean = pd.DataFrame(structured_data)

    if quarantine_data:
        df_trash = pd.DataFrame(quarantine_data)

    else:
        df_trash = pd.DataFrame(
            columns=["raw_line", "issue"]
        )

    return df_clean, df_trash


# -----------------------------
# AUTO DETECTION ROUTER
# -----------------------------
def auto_parse(file, filename):

    filename = filename.lower()

    if filename.endswith(".csv"):
        return parse_csv_file(file)

    elif filename.endswith(".json"):
        return parse_json_file(file)

    elif filename.endswith(".log"):
        return parse_log_file(file)

    else:
        return parse_text_file(file)