import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bar_chart_race as bcr
from datetime import datetime
import os
from dotenv import load_dotenv
import time

load_dotenv()

FRIENDS = os.getenv("FRIENDS")

with open("./output/json/algoX.json", "r") as f:
    initialData = json.load(f)


def getData(initialData, closeFriendsOnly=False, algoOnly=True, minRating=1000):
    data = {}
    for user in initialData:
        if initialData[user]["algo"] == 0 and algoOnly:
            continue
        if user not in FRIENDS and closeFriendsOnly:
            continue
        if initialData[user]["maxRating"] < minRating:
            pass
        data[user] = initialData[user]["ratingHistory"]
    return data


# Data:
# -> {user:[{rating, time(unix), rank},...], ...}

"""
A bar chart race video with the top users with the highest rating at any given time.
"""


def doIt(
    data,
    startTime=None,
    endTime=None,
    bars=10,
    periodLength=200,
    filename="bar_chart_race.mp4",
    root="output/barChartRace",
    dpi=144,
):
    time1 = time.time()
    # Dataframe
    dfs = []  # list to hold dataframes
    for user in data:
        ratings = []
        times = []
        for x in data[user]:
            # if x["time"] < 1640975401:
            if startTime is not None and x["time"] < startTime:
                continue
            if endTime is not None and x["time"] > endTime:
                continue
            # if x["time"] < 1672511401:
            #     continue
            ratings.append(x["rating"])
            # times.append(x["time"])
            times.append(datetime.fromtimestamp(int(x["time"])))
        temp_df = pd.DataFrame({user: ratings, "time": times})
        temp_df = temp_df.set_index("time")
        dfs.append(temp_df)

    # Concatenate all the dataframes
    df = pd.concat(dfs, axis=1)

    df = df.sort_index()

    # Top 10 users with the highest rating at any given time
    # top10 = df.apply(lambda x: x.sort_values(ascending=False).head(10).index, axis=1)

    # Convert the index to a DatetimeIndex
    df.index = pd.to_datetime(df.index)

    # Now you can resample
    df_daily = df.resample("D").mean()

    # Interpolate missing values
    df_interpolated = df_daily.interpolate()

    # Create the bar chart race
    print(f"Number of users: {len(df_interpolated.columns)}")
    bcr.bar_chart_race(
        df=df_interpolated,
        filename=f"{root}/{filename}",
        title=f"Top {bars} Users with Highest Rating",
        n_bars=bars,
        # period_length=100,
        period_length=periodLength,
        dpi=dpi,
        # period_length=500,
    )
    time2 = time.time()
    print(f"Time taken: {time2-time1}")


doIt(
    getData(initialData, closeFriendsOnly=True, algoOnly=True),
    startTime=1640975401,
    # endTime=1672511401, # 1 jan 2023 (31536000 seconds in a year)
    bars=10,
    periodLength=200,
    filename="firstiePupils_200paceAlgoX.mp4",
    root="./output/barChartRace",
)


# doIt(
#     getData(initialData, closeFriendsOnly=False, algoOnly=True, minRating=1200),
#     startTime=1640975401,
#     # endTime=1672511401, # 1 jan 2023 (31536000 seconds in a year)
#     bars=20,
#     periodLength=200,
#     filename="algoX_20bars_200Pace.mp4",
#     root="./output/barChartRace",
#     dpi=300,
# )

# doIt(
#     getData(initialData, closeFriendsOnly=False, algoOnly=True, minRating=1000),
#     startTime=1640975401,
#     # endTime=1672511401, # 1 jan 2023 (31536000 seconds in a year)
#     bars=30,
#     periodLength=200,
#     filename="algoX_30bars_200Pace.mp4",
#     root="./output/barChartRace",
#     dpi=300,
# )
