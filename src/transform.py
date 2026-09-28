
# 2 Transform  pr redords,   change columns,  date formating in month, year, hour, data type if any

import pandas as pd
from extract import df_pr


def transform_pr_df(df_pr):

    if df_pr.empty:
        return None

    df_pr = df_pr.rename(columns={"pr_id": "pr_unique_id"})

    df_pr = df_pr.drop(columns=["author_login"])

    # Convert strings → datetime
    datetime_columns = [
        "created_at",
        "updated_at",
        "closed_at",
        "merged_at"
    ]

    for col in datetime_columns:
        df_pr[col] = pd.to_datetime(
            df_pr[col],
            errors="coerce",
            utc=True
        )

    # Derived date fields
    df_pr["created_year"] = df_pr["created_at"].dt.year
    df_pr["created_month"] = df_pr["created_at"].dt.month
    df_pr["created_hour"] = df_pr["created_at"].dt.hour

    df_pr["updated_year"] = df_pr["updated_at"].dt.year
    df_pr["updated_month"] = df_pr["updated_at"].dt.month
    df_pr["updated_hour"] = df_pr["updated_at"].dt.hour

    df_pr["closed_year"] = df_pr["closed_at"].dt.year
    df_pr["closed_month"] = df_pr["closed_at"].dt.month
    df_pr["closed_hour"] = df_pr["closed_at"].dt.hour

    df_pr["merged_year"] = df_pr["merged_at"].dt.year
    df_pr["merged_month"] = df_pr["merged_at"].dt.month
    df_pr["merged_hour"] = df_pr["merged_at"].dt.hour

    return df_pr

dft_pt = transform_pr_df(df_pr)
