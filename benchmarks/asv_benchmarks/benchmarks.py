from __future__ import print_function
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def setup():
    with open(ROOT_DIR + "/installed_build") as f:
        sys.path = [f.read().strip() + "/workspace/devel/lib/python2.7/dist-packages"] + sys.path
    import fast_rosbag_pandas


def read_points(bagname):
    import fast_rosbag_pandas

    fast_rosbag_pandas.rosbag_to_dataframe("{}/bags/{}.bag".format(ROOT_DIR, bagname), "points")


def time_read_points_1k():
    read_points("points_1k")


def time_read_points_1m():
    read_points("points_1m")


def time_read_points_10m():
    read_points("points_10m")


time_read_points_10m.timeout = 240
