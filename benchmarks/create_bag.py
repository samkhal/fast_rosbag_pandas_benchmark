#!/usr/bin/env python
""" Create bags for benchmarking """
from __future__ import print_function

import os
from contextlib import closing
import rosbag
import rospy
from geometry_msgs.msg import PointStamped, Point
from std_msgs.msg import Header
from tqdm import tqdm

BAG_DIR = os.path.dirname(os.path.abspath(__file__)) + "../bags"


def create_points_bag(name, count):

    bagpath = "{}/{}.bag".format(BAG_DIR, name)
    print("Writing to ", bagpath)
    with closing(rosbag.Bag(bagpath, "w")) as bag:
        for i in tqdm(range(int(count))):
            bag.write("points", PointStamped(Header(i, rospy.Time(i), "frame1"), Point(i, i + 1, i + 2)))


if __name__ == "__main__":
    create_points_bag("points_1k", 1000)
    create_points_bag("points_1m", 1e6)
    create_points_bag("points_10m", 1e7)
