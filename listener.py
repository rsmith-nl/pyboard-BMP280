#!/usr/bin/env python3
# file: listener.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2018-04-10T18:10:29+0200
# Last modified: 2018-04-17T00:26:15+0200
"""
Program to receive data from the BMP280 sensor connected to the pyboard,
which is running the main-query.py program.
"""

from datetime import datetime
import time
import serial


def nexthour():
    sleeptime = 3600 - int(round(time.time())) % 3600
    time.sleep(sleeptime)


# assuming the pyboard connects to /dev/cuaU0
pyboard = serial.Serial("/dev/cuaU0", 115200, timeout=1)
datafile = open("/tmp/monitor.d", "w")

now = datetime.utcnow().strftime("%FT%TZ")
datafile.write("# BMP280 data.\n# Started monitoring at {}.\n".format(now))
datafile.flush()

while True:
    nexthour()
    now = datetime.utcnow().strftime("%FT%TZ")
    # print('Datetime is', now)
    pyboard.write("?\r\n".encode("utf-8"))
    pyboard.readline().decode("utf-8")  # read and discard echo
    degC, _, mbar, _ = pyboard.readline().decode("utf-8").split()
    # print('Received {} °C {} mbar'.format(degC, mbar))
    datafile.write("{} {} {}\n".format(now, degC, mbar))
    datafile.flush()
