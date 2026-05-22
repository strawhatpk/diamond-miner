import hashlib

def curate_data(df_clean):

    # If dataframe is empty, return safely
    if df_clean.empty:
        return df_clean

    # Check required columns
    required_columns = ["ip", "status"]

    for col in required_columns:
        if col not in df_clean.columns:
            return df_clean

    # Create masked IP column
    df_clean["masked_ip"] = df_clean["ip"].apply(
        lambda x: hashlib.sha256(x.encode()).hexdigest()[:12]
    )

    # Convert status to integer
    df_clean["status"] = df_clean["status"].astype(int)

    # Assign priority
    def assign_priority(status):

        if status >= 500:
            return "Critical"

        elif status >= 400:
            return "High"

        else:
            return "Low"

    df_clean["priority"] = df_clean["status"].apply(assign_priority)

    return df_clean