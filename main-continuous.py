# file: main-continuous.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2018-04-10T14:39:42+0200
# Last modified: 2018-04-29T01:27:14+0200
"""
Create a BMP280 sensor object. Then query it every minute and print the results
over the serial connection.

Copy this program to the pyboard as “main.py”.
"""
from pyb import delay
from bmp280 import Bmp280_i2c

s = Bmp280_i2c(2)  # Assuming the chip is wired to the 2nd I²C bus.

print('Please wait one minute for the sensor to settle...')
delay(60000)
print('Ready')

while True:
    # Read and print the values, then wait.
    rv = s.read()
    print('{:.1f} °C, {:.0f} mbar'.format(s.temperature, s.mbar))
    delay(60000)
