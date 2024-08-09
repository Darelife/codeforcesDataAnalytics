from matplotlib import pyplot as plt
import json
from datetime import datetime
import seaborn as sns
import os
from dotenv import load_dotenv

load_dotenv()
FRIENDS = os.getenv("FRIENDS")

with open("./output/json/algoX.json", "r") as f:
    initialData = json.load(f)

data = {}

# TODO: check if u want only friends or not, (same for algoOnly)
friendsOnly = True
algoOnly = True


for user in initialData:
    if algoOnly and initialData[user]["algo"] == 0:
        continue
    if friendsOnly and user not in FRIENDS:
        continue
    # if user in ["darelife", "harshb", "acsde", "garam_icecream", "Centelle", "Aashman", "LightHouse1"]:
    data[user] = initialData[user]["ratingHistory"]

"""
Data:
-> {user:[{rating, time(unix), rank},...], ...}

We need to plot a multi-line graph (rating vs time) with the following data:
"""


def plot_graph(data):
    # sns.set_theme()
    sns.set_theme(style="darkgrid")
    for user in data:
        ratings = []
        times = []
        for x in data[user]:
            # 1640975401
            # 1672511401
            if x["time"] < 1640975401:
                continue
            ratings.append(x["rating"])
            times.append(datetime.fromtimestamp(int(x["time"])))
        # ratings = [x["rating"] for x in data[user]]
        # times = [datetime.fromtimestamp(int(x["time"])) for x in data[user]]
        plt.plot(times, ratings, label=user)
    plt.xlabel("Timeee")
    plt.ylabel("Rating")
    plt.legend()
    # increase the pixel size of the graph
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    # plt.xticks(rotation=45)
    plt.savefig("ratingVsTime.png")
    plt.show()


plot_graph(data)
