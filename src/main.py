
from extract import fetched_data, extract_pr_fields, fetch_all_pages
from transform import dft_pt,transform_pr_df
from Load import load_to_postgres, pull_requests_data
url = "https://api.github.com/repos/microsoft/vscode/pulls?state=all&per_page=30"
# Complete  ETL pipline

def run_etl_pipline():
    print("Starting  ETL pipline....")

    fetched_data = fetch_all_pages(url)
    print("Starting  Extracting pr fields....")

    df_pr =  extract_pr_fields(fetched_data)

    print("Starting  transforming pr dataframe....")

    dft_pr = transform_pr_df(df_pr)

    print("Loading pr data to posgres....")

    load_to_postgres( dft_pr, pull_requests_data)
    
    print("ETL pipline completed")
