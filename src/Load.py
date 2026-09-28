from sqlalchemy import create_engine
import psycopg2
from transform import dft_pt

print("psycopg2 works")

port = 5432
host = "localhost"
user = "postgres"
password = "umair777"
db_github_pr = "db_github_pr"

pull_requests_data = "pull_requests_data"


def load_to_postgres(dft_pt, pull_requests_data):

    engine = create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{db_github_pr}"
    )

    dft_pt.to_sql(
        pull_requests_data,
        engine,
        if_exists="append",
        index=False
    )

    print("PR data has been loaded successfully")
load_to_postgres(dft_pt, pull_requests_data)