#!/usr/bin/env python

import timeit
from tqdm import tqdm
import pandas as pd
from asv_benchmarks import benchmarks
import os
import rosbag_pandas
from tabulate import tabulate
import fast_rosbag_pandas

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../"


def timeit_auto(stmt="pass", setup="pass", repeat=True):
    t = timeit.Timer(stmt, setup)

    # determine number so that 0.2 <= total time
    for i in range(10):
        number = 10 ** i
        time = t.timeit(number)  # seconds
        if time >= 0.2:
            break

    if repeat:
        time = min(time, t.timeit(number))
        time = min(time, t.timeit(number))

    return time / number


def print_benchmark_table(include_rosbag_pandas=True, repeat=True):
    benchmarks.setup()

    bagnames = ["points_1k.bag", "points_1m.bag", "points_10m.bag"]

    df = pd.DataFrame(columns=bagnames)
    if include_rosbag_pandas:
        rosbag_pandas_times = []
        for bagname in tqdm(bagnames):
            rosbag_pandas_times.append(
                timeit_auto(lambda: rosbag_pandas.bag_to_dataframe(ROOT_DIR + "/bags/" + bagname), repeat=repeat)
            )
        df = df.append(pd.Series(rosbag_pandas_times, index=bagnames, name="rosbag_pandas"))

    fast_rosbag_pandas_times = []
    for bagname in tqdm(bagnames):
        fast_rosbag_pandas_times.append(
            timeit_auto(
                lambda: fast_rosbag_pandas.rosbag_to_dataframe(ROOT_DIR + "/bags/" + bagname, "points"), repeat=repeat
            )
        )
    df = df.append(pd.Series(fast_rosbag_pandas_times, index=bagnames, name="fast_rosbag_pandas"))

    df = df.transpose()

    # Add comparison
    if include_rosbag_pandas:
        df["Speedup"] = df["rosbag_pandas"] / df["fast_rosbag_pandas"]

    print(
        tabulate(
            df,
            tablefmt="pipe",
            headers=["rosbag_pandas (s)", "fast_rosbag_pandas (s)", "speedup factor"],
            floatfmt=(".4f", ".4f", ".4f", ".1f"),
        )
    )


if __name__ == "__main__":
    print_benchmark_table(include_rosbag_pandas=True, repeat=True)
    # print_benchmark_table(include_rosbag_pandas=True, repeat=False)
