#!/usr/bin/env python
import sys
import os
import subprocess

if __name__ == "__main__":
    build_dir = sys.argv[1]
    build_cache_dir = sys.argv[2]
    print "Build dir", build_dir
    print "cache dir", build_cache_dir

    os.chdir(build_cache_dir)
    os.makedirs("workspace/src")
    os.chdir("workspace")
    print os.getcwd()
    env = os.environ
    env.update({"PYTHONPATH":"/opt/ros/melodic/lib/python2.7/dist-packages", "PWD":os.getcwd()})
    subprocess.call("/opt/ros/melodic/bin/catkin_make", env=env)

    os.symlink(build_dir, "src/fast_rosbag_pandas")
    subprocess.call("/opt/ros/melodic/bin/catkin_make", env=env)