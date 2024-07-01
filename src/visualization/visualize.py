import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

from IPython import display

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df = pd.read_pickle("../../data/interim/01-processed-data.pkl")

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------

set_df = df[df["set"] == 1]
# drop=True -> drops the existing index and replace it with new index which is default
# integer index in this case
plt.plot(set_df["acc_y"].reset_index(drop=True))

# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------

for exc in df["exc"].unique():
    subset = df[df["exc"] == exc]
    fig, ax = plt.subplots()
    plt.plot(subset["acc_y"].reset_index(drop=True), label=exc)
    plt.legend()
    plt.show()


for exc in df["exc"].unique():
    subset = df[df["exc"] == exc]
    fig, ax = plt.subplots()
    plt.plot(subset[:100]["acc_y"].reset_index(drop=True), label=exc)
    plt.legend()
    plt.show()

# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------
# https://www.dunderdata.com/blog/view-all-available-matplotlib-styles
# https://www.dunderdata.com/blog/view-all-available-matplotlib-styles
# https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rcParams

plt.style.available
# plt.style.use("seaborn-whitegrid")
mpl.rcParams["figure.figsize"] = (20, 5)
mpl.rcParams["figure.dpi"] = 100

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------

trainee_a_squat_df = df.query("exc == 'squat'").query("pcpnt == 'A'").reset_index()
fig, ax = plt.subplots()
trainee_a_squat_df.groupby(["cat"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("categories")
plt.legend()


# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------

squats_df = df.query('exc == "bench"').sort_values("pcpnt").reset_index()

fix, ax = plt.subplots()
squats_df.groupby(["pcpnt"], group_keys=False)["acc_y"].plot()
plt.legend()

# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------
participant = "A"
excercise = "squat"

all_axes = (
    df.query(f"pcpnt == '{participant}'").query(f'exc == "{excercise}"').reset_index()
)

fig, ax = plt.subplots()
all_axes[["acc_x", "acc_y", "acc_z"]].plot(ax=ax)
plt.legend()


# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------
excercises = df["exc"].unique()
participants = df["pcpnt"].unique()


for exc in excercises:
    for participant in participants:
        all_axes_df = (
            df.query(f"exc == '{exc}'").query(f"pcpnt == '{participant}'").reset_index()
        )
        if len(all_axes_df):
            fig, ax = plt.subplots()
            all_axes_df[["acc_y", "acc_x", "acc_z"]].plot(ax=ax)
            plt.title(f"{exc} - {participant}")
            plt.legend()

# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------
exc = "bench"
participant = "B"

all_axes_df = (
    df.query(f"exc == '{exc}'").query(f"pcpnt == '{participant}'").reset_index()
)

fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 5))

all_axes_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
all_axes_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])
ax[0].legend(
    loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True
)
ax[1].legend(
    loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True
)

# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------


excercises = df["exc"].unique()
participants = df["pcpnt"].unique()


for exc in excercises:
    for participant in participants:
        all_axes_df = (
            df.query(f"exc == '{exc}'").query(f"pcpnt == '{participant}'").reset_index()
        )
        if len(all_axes_df):
            fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 5))

            all_axes_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
            all_axes_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])
            ax[0].legend(
                loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True
            )
            ax[1].legend(
                loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True
            )
            plt.savefig(f'../../reports/figures/{exc}-{participant}.png')
            plt.show()