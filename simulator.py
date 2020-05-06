#!/usr/bin/env python3
import time
import sys

# this is a simulator of ./dmr-brandmeister to test
#  the pipeline without having to connect to the
#  BrandMeister network

# amount of frames per second
FRAMERATE = 18 / 300

with open("data/recording_long.txt") as infile:
    for frame in infile.readlines():
        sys.stdout.write(frame)
        sys.stdout.flush()
        time.sleep(FRAMERATE)
