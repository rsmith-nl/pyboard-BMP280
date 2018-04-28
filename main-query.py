# file: main-query.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2018-04-10T17:33:01+0200
# Last modified: 2018-04-29T01:27:22+0200
"""
Create a BMP280 sensor object. When a line containing “?” is input over the
serial connection, query the sensor and report the result. (That goed out over
the serial connection.)

Copy this program to the pyboard as “main.py”.
"""
from pyb import delay
from bmp280 import Bmp280_i2c

s = Bmp280_i2c(2)  # Assuming the sensor is wired to the 2nd I²C bus.
delay(60000)  # Wait a minute after startup; give the sensor time to settle.

while True:
    if '?' in input():
        # Read and print the values.
        rv = s.read()
        print('{:.1f} °C, {:.0f} mbar'.format(s.temperature, s.mbar))
