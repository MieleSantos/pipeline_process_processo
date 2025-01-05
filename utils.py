import pandas as pd


def create_file(data_dict):
    return pd.DataFrame([data_dict])


def concat_csv_files(csv_files):
    if len(csv_files) == 1:
        csv_data = csv_files[0]
        csv_data = csv_data.to_csv(index=False)
    else:
        concat_df = pd.concat(csv_files, ignore_index=True)
        csv_data = concat_df.to_csv(index=False)
    return csv_data
