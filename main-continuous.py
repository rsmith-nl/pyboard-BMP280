# file: continuous-report.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-04-10 14:39:42 +0200
# Last modified: 2018-04-11 12:10:40 +0200
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to main.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/
"""
Create a BMP280 sensor object. Then query it every minute and print the results
over the serial connection.

Copy this program to the pyboard as “main.py”.
"""
from pyb import delay
from BMP280 import BMP280_I2C

s = BMP280_I2C(2)  # Assuming the chip is wired to the 2nd I²C bus.

print('Please wait one minute for the sensor to settle...')
delay(60000)
print('Ready')

while True:
    # Read and print the values, then wait.
    rv = s.read()
    print('{:.1f} °C, {:.0f} mbar'.format(s.temperature, s.mbar))
    delay(60000)
