import pandas as pd

url_base = "http://api:8000/process/"


def create_file(data_dict):
    return pd.DataFrame([data_dict])


def concat_csv_files(csv_files):
    if len(csv_files) == 1:
        csv_data = csv_files[0]
    else:
        concat_df = pd.concat(csv_files, ignore_index=True)
        csv_data = concat_df.to_csv(index=False)
    return csv_data
