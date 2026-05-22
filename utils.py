import pandas as pd


# -----------------------------------
# HEALTH SCORE
# -----------------------------------
def calculate_health_score(
    df_clean,
    df_trash
):

    total_records = (
        len(df_clean) + len(df_trash)
    )

    if total_records == 0:
        return 0

    return (
        len(df_clean) / total_records
    ) * 100


# -----------------------------------
# FILE SIZE FORMATTER
# -----------------------------------
def format_file_size(size_bytes):

    if size_bytes < 1024:
        return f"{size_bytes} B"

    elif size_bytes < 1024 * 1024:
        return (
            f"{size_bytes / 1024:.2f} KB"
        )

    else:
        return (
            f"{size_bytes / (1024 * 1024):.2f} MB"
        )


# -----------------------------------
# SAFE DATAFRAME CHECK
# -----------------------------------
def safe_dataframe(df):

    if df is None:
        return pd.DataFrame()

    return df