import pandas as pd
from glob import glob


files = glob("../../data/raw/MetaMotion/*.csv")


def extract_csv_data() -> tuple:

    data_path = "../../data/raw/MetaMotion/"

    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    def file_generator():
        global files
        for file in files:
            yield file

    acc_set = 1
    gyr_set = 1

    for f in file_generator():

        participant = f.split("-")[0].replace(data_path, "")
        exercise = f.split("-")[1]
        category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

        df = pd.read_csv(f)
        df["participant"] = participant
        df["exercise"] = exercise
        df["category"] = category

        if f.lower().__contains__("accelerometer"):
            df["set"] = acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df, df])

        if f.lower().__contains__("gyroscope"):
            df["set"] = gyr_set
            gyr_set += 1
            gyr_df = pd.concat([gyr_df, df])

    acc_df.set_index(pd.to_datetime(acc_df["epoch (ms)"], unit="ms"), inplace=True)
    gyr_df.set_index(pd.to_datetime(gyr_df["epoch (ms)"], unit="ms"), inplace=True)

    del acc_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del acc_df["elapsed (s)"]

    del gyr_df["epoch (ms)"]
    del gyr_df["time (01:00)"]
    del gyr_df["elapsed (s)"]

    return acc_df, gyr_df


acc_df, gyr_df = extract_csv_data()


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------


merged_data = pd.concat([acc_df.iloc[:, :3], gyr_df], axis=1)
# merged_data.dropna()

merged_data.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyr_x",
    "gyr_y",
    "gyr_z",
    "pcpnt",
    "exc",
    "cat",
    "set",
]  # type: ignore


# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz

agg_funcs_on_columns = {
    "acc_x": "mean",
    "acc_y": "mean",
    "acc_z": "mean",
    "gyr_x": "mean",
    "gyr_y": "mean",
    "gyr_z": "mean",
    "pcpnt": "last",
    "exc": "last",
    "cat": "last",
    "set": "last",
}

merged_data.resample(rule="200ms").apply(agg_funcs_on_columns)  # type: ignore

# above code is not efficient, other workaround is to break dataset into
# smaller parts and then apply the aggregation and resampling
daily_data = [g for n, g in merged_data.groupby(pd.Grouper(freq="D"))]

resampled_data = pd.concat(
    [grp.resample(rule="200ms").apply(agg_funcs_on_columns).dropna() for grp in daily_data]  # type: ignore
)

resampled_data.info()

resampled_data['set'] = resampled_data['set'].astype('int')

# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------

# smaller size
# faster to load
# don't need any conversion
resampled_data.to_pickle('../../data/interim/01-processed-data.pkl')