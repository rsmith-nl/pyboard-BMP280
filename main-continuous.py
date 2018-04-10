# file: continuous-report.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-04-10 14:39:42 +0200
# Last modified: 2018-04-10 17:34:47 +0200
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to main.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/
"""
Create a BMP280 sensor object. Then query it every minute and print the results
over the serial connection.

copy this program to the pyboard as “main.py”.
"""

from BMP280 import BMP280_I2C

DELAY = const(60000)  # One minute in ms.

s = BMP280_I2C(2)  # Assuming the chip is wired to the 2nd I²C bus.

print('Please wait...')
pyb.delay(DELAY)  # Wait a minute after startup.
print('Ready')

while True:
    # Read and print the values.
    rv = s.read()
    print('{:.1f} °C, {:.0f} mbar'.format(s.temperature, s.mbar))
    # Wait 60 seconds
    pyb.delay(DELAY)
