# file: BMP280.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-04-08 22:38:40 +0200
# Last modified: 2018-04-10 14:38:43 +0200
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to BMP280.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

from utime import sleep_ms
from ustruct import unpack
from pyb import I2C
from micropython import const

# Constants
REG_ID = const(0xD0)  # id register
ID_VAL = const(0x58)  # id value
REG_STATUS = const(0xF3)  # status register
REG_CONFIG = const(0xF5)  # configuration register
REG_CONTROL = const(0xF4)  # configuration register
REG_PRESS = const(0xF7)  # Start of data registers.
# All registers F7 - F9 should be read in one go.
REG_TEMP = const(0xFA)
# Registers FA - FC should be read in one go.
REG_COMP = const(0x88)  # Start of compensation parameters.
# All registers 88 - A1 should be read in one go.


class BMP280_I2C:
    """Use the BMP280 over Ii²C using a pyboard."""

    def __init__(self, bus, address=0x76):
        """Create an BMP280_I2C object.

        Arguments:
            bus: which connections we use.
            address: I2C address. Defaults to 0x76
        """
        self._i2c = I2C(bus, I2C.MASTER)
        self._address = address
        self._temp = None
        self._press = None
        # Read the compensation coefficients.
        data = self._i2c.mem_read(24, self._address, REG_COMP)
        comp = unpack('<HhhHhhhhhhhh', data)
        comp = [float(j) for j in comp]
        self._tempcal = comp[:3]
        self._presscal = comp[3:]

    @property
    def ready(self):
        """Whether BMP280 is found and available."""
        # if not self._i2c.is_ready(self._address):
        #    return False
        if self._i2c.mem_read(1, self._address, REG_ID)[0] != ID_VAL:
            return False  # Not a BMP280!
        return True

    @property
    def temperature(self):
        """The last measured temperature in °C."""
        return self._temp

    @property
    def pressure(self):
        """The last measured pressure in Pascal."""
        return self._press

    @property
    def mbar(self):
        """The last measured pressure in mbar"""
        return 1000*(self._press/1.013e5)

    def read(self):
        """Read the sensor data from the chip."""
        # Do one measurement in high resolution, forced mode.
        self._i2c.mem_write(0xFE, self._address, REG_CONTROL)
        while self._i2c.mem_read(1, self._address, REG_STATUS)[0] & 0x08:
            sleep_ms(2)  # Busy measuring.
        # Temperature
        tempdata = self._i2c.mem_read(3, self._address, REG_TEMP)
        UT = float((tempdata[0] << 16 | tempdata[1] << 8 | tempdata[2]) >> 4)
        # print("DEBUG: UT = ", UT)
        var1 = (UT / 16384.0 - self._tempcal[0] / 1024.0) * self._tempcal[1]
        # print("DEBUG: var1 = ", var1)
        var2 = ((UT / 131072.0 - self._tempcal[0] / 8192.0) * (
            UT / 131072.0 - self._tempcal[0] / 8192.0)) * self._tempcal[2]
        # print("DEBUG: var2 = ", var2)
        t_fine = int(var1+var2)
        # print("DEBUG: t_fine = ", t_fine)
        self._temp = t_fine/5120.0
        # print("DEBUG: self._temp = ", self._temp)
        # Pressure
        pressdata = self._i2c.mem_read(3, self._address, REG_PRESS)
        UP = float((pressdata[0] << 16 | pressdata[1] << 8 | tempdata[2]) >> 4)
        # print("DEBUG: UP = ", UP)
        var1 = t_fine/2.0 - 64000.0
        # print("DEBUG: var1 = ", var1)
        var2 = var1 * var1 * self._presscal[5] / 32768.0
        # print("DEBUG: var2 = ", var2)
        var2 = var2 + var1 * self._presscal[4] * 2.0
        # print("DEBUG: var2 = ", var2)
        var2 = var2/4.0 + self._presscal[3] * 65536.0
        # print("DEBUG: var2 = ", var2)
        var1 = (self._presscal[2] * var1 * var1 / 534288.0 +
                self._presscal[1] * var1) / 534288.0
        # print("DEBUG: var1 = ", var1)
        var1 = (1.0 + var1/32768.0) * self._presscal[0]
        # print("DEBUG: var1 = ", var1)
        if var1 == 0.0:
            return 0
        p = 1048576.0 - UP
        # print("DEBUG: p = ", p)
        p = ((p - var2 / 4096.0) * 6250) / var1
        # print("DEBUG: p = ", p)
        var1 = self._presscal[8] * p * p / 2147483648.0
        # print("DEBUG: var1 = ", var1)
        var2 = p * self._presscal[7] / 32768.0
        # print("DEBUG: var2 = ", var2)
        p = p + (var1 + var2 + self._presscal[6]) / 16.0
        self._press = p
        # print("DEBUG: self._press = ", self._press)
        return (self._temp, self._press)
