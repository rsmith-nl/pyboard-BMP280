# file: query.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-04-10 14:39:42 +0200
# Last modified: 2018-04-11 12:07:31 +0200
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to main.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/
"""
Create a BMP280 sensor object. When a line containing “?” is input over the
serial connection, query the sensor and report the result. (That goed out over
the serial connection.)

Copy this program to the pyboard as “main.py”.
"""
from pyb import delay
from BMP280 import BMP280_I2C

s = BMP280_I2C(2)  # Assuming the sensor is wired to the 2nd I²C bus.
delay(60000)  # Wait a minute after startup; give the sensor time to settle.

while True:
    if '?' in input():
        # Read and print the values.
        rv = s.read()
        print('{:.1f} °C, {:.0f} mbar'.format(s.temperature, s.mbar))
