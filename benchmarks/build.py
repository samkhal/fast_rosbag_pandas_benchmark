#!/usr/bin/env python

import sys
import os
import subprocess

if __name__ == "__main__":
    build_dir = sys.argv[1]
    build_cache_dir = sys.argv[2]

    os.chdir(build_cache_dir)
    os.makedirs("workspace/src")
    os.chdir("workspace")

    env = os.environ
    env.update({"PYTHONPATH": "/opt/ros/melodic/lib/python2.7/dist-packages", "PWD": os.getcwd()})

    os.symlink(build_dir, "src/fast_rosbag_pandas")
    subprocess.check_call(
        ["/opt/ros/melodic/bin/catkin_make", "-DCMAKE_CXX_FLAGS=-O3 -g -DNDEBUG", "-DCMAKE_BUILD_TYPE="], env=env
    )
