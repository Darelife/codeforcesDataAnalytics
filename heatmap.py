from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import json
import numpy as np
from datetime import datetime
import matplotlib.ticker as ticker
from matplotlib import colors as colors
import matplotlib
import time
import os
from dotenv import load_dotenv

load_dotenv()
FRIENDS = os.getenv("FRIENDS")

with open("./output/json/algoX.json", "r") as f:
    initialData = json.load(f)


def getData(initialData, closeFriendsOnly=False, algoOnly=True, maxCount=15):
    data = {}
    count = 0
    for user in initialData:
        if initialData[user]["algo"] == 0 and algoOnly:
            continue
        if user not in FRIENDS and closeFriendsOnly:
            continue
        count += 1
        if count > maxCount:
            break
        # data[user] = initialData[user]["ratingHistory"]
        # data[user] -> {month-year: ((monthEndRating- monthStartRating)*100)/monthStartRating, ...}
        data[user] = {}
        actualTime = []
        for x in initialData[user]["ratingHistory"]:
            x["time"] -= 19800
            actualTime.append(x["time"])
            time = datetime.fromtimestamp(int(x["time"])).strftime("%Y-%m")
            if time not in data[user]:
                data[user][time] = []
            data[user][time].append(x["rating"])
        for time in data[user]:
            if user == "darelife":
                print(data[user][time][0], data[user][time][-1])
            if len(data[user][time]) == 0:
                data[user][time] = np.nan
            # if len(data[user][time]) != 1:
            data[user][time] = (
                (data[user][time][-1] - data[user][time][0]) * 100
            ) / data[user][time][0]
            # elif len(data[user][time]) == 1:
            #     # the month has only one rating, so the rating%change is the rating - lastmonthRating/lastmonthRating

    return data


data = getData(initialData, closeFriendsOnly=True, algoOnly=True, maxCount=15)
# print(data["Naman_Agarwal_03"])


# Data:
# -> {user:[{month-year: ((monthEndRating- monthStartRating)*100)/monthStartRating, ...}, ...]}
# Heatmap of rating%change over time for each user (user -> Y-axis, time -> X-axis)
# Dataframe

# Now i need to plot user vs (month-year) with the value being the rating%change, which is the value in the cell, and is provided in the data itself

# Dataframe
dfs = []  # list to hold dataframes
for user in data:
    ratings = []
    times = []
    for x in data[user]:
        ratings.append(data[user][x])
        times.append(x)
    df = pd.DataFrame(
        {"time": times, "rating%change": ratings}
    )  # create a dataframe for each user
    df["user"] = user
    dfs.append(df)

df = pd.concat(dfs)  # combine all dataframes into one
# print(df)
df["time"] = pd.to_datetime(df["time"])  # convert time to datetime
df = df.pivot(
    index="user", columns="time", values="rating%change"
)  # pivot the dataframe
# df = df.fillna(0)  # fill NaN with 0
print(df)
# Plot
plt.figure(figsize=(20, 10))
# ax = sns.heatmap(df, cmap="coolwarm", annot=True, fmt=".2f", cbar=False, mask=df == 0)
# cmap = colors.LinearSegmentedColormap.from_list("", ["darkred", "blue"])

rd_bu = matplotlib.colormaps.get_cmap("RdBu")

# Create a custom colormap
# cmap = colors.LinearSegmentedColormap.from_list(
#     "", [(0, "darkred"), (0.5, rd_bu(0.5)), (1, rd_bu(0.9))], N=256
# )
# Get the blue colormap
blue_cmap = plt.cm.get_cmap("Blues")

# Create a custom colormap
# Find the range of the values in the dataframe
max_val = df.max().max()
min_val = df.min().min()
t = ((-1) * min_val) / (max_val - min_val)
N = int(max_val - min_val)
cmaplist = []
# tt = 0
for i in range(int(t * 100)):
    cmaplist.append((i / 100, "darkred"))
    # tt = i / 100
# cmaplist.append((t, "darkred"))
cmaplist.append((t - 0.001, "darkred"))
cmaplist.append((t, blue_cmap(0.6)))
cmaplist.append((1, blue_cmap(0.99)))
print(cmaplist)
print(max_val, min_val)
print(t, N)
cmap = colors.LinearSegmentedColormap.from_list(
    "",
    cmaplist,
    N=N,
)
ax = sns.heatmap(
    df,
    # cmap="BuGn_r",
    # cmap="Set1",
    # cmap="coolwarm",
    # cmap="RdBu",
    cmap=cmap,
    # center=0,
    # center=50,
    # cbar_kws={"label": "Percent Change"},
    annot=True,
    fmt=".1f",
    annot_kws={"size": 7},
    linewidths=0.5,
    # linecolor="white",
    cbar=True,
    mask=df == np.nan,
)

# Add lines to differentiate each user
ax.hlines(np.arange(len(df)), *ax.get_xlim(), colors="#e1e1e1", linewidths=0.5)
ax.vlines(np.arange(len(df.columns)), *ax.get_ylim(), colors="#e1e1e1", linewidths=0.5)

labels = [
    # datetime.strptime(item.get_text(), "%Y-%m-%dT%H:%M:%S.%f").strftime("%b %Y")
    datetime.fromtimestamp(
        int(time.mktime(datetime.strptime(item.get_text()[:7], "%Y-%m").timetuple()))
    ).strftime("%b %Y")
    for item in ax.get_xticklabels()
]
ax.set_xticklabels(labels)
ax.set_yticklabels(
    ax.get_yticklabels(), rotation=0, ha="right"
)  # Make y-axis labels horizontal
ax.set_xticklabels(ax.get_xticklabels(), ha="right", rotation=45)

# print only the first 10 characters of the x axis

plt.title(
    "Percent change in rating for every month (if you only gave 1 contest in a month, it will show 0)"
)
plt.xlabel("Time")
plt.ylabel("User")
plt.savefig("heatmap.png")
plt.show()
