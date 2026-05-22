import sqlite3
import pandas as pd


# -----------------------------------
# CLEAN COLUMN NAMES
# -----------------------------------
def clean_columns(df):

    df.columns = [
        str(col)
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "_")
        .replace("/", "_")
        .replace(":", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("[", "")
        .replace("]", "")
        for col in df.columns
    ]

    return df


# -----------------------------------
# SAVE DATABASE
# -----------------------------------
def save_to_database(
    df_clean,
    df_trash,
    db_name="diamond_miner.db"
):

    conn = sqlite3.connect(db_name)

    # -----------------------------
    # CLEAN DATA
    # -----------------------------
    if not df_clean.empty:

        df_clean = clean_columns(df_clean)

        df_clean.to_sql(
            "cleansed_data",
            conn,
            if_exists="replace",
            index=False
        )

    # -----------------------------
    # QUARANTINE DATA
    # -----------------------------
    if not df_trash.empty:

        df_trash = clean_columns(df_trash)

        df_trash.to_sql(
            "quarantine_data",
            conn,
            if_exists="replace",
            index=False
        )

    conn.close()

    return db_name