# file: BMP280.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
# Using the Adafruit BMP280 breakout board with micropython
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-04-08 22:38:40 +0200
# Last modified: 2018-04-09 16:11:47 +0200

from utime import sleep_ms
from ustruct import unpack
from pyb import I2C
from micropython import const

# Constants
REG_ID = const(0xD0)  # id register
ID_VAL = const(0x58)  # id value
REG_STATUS = const(0xF3)  # status register
REG_CONFIG = const(0xF5)  # configuration register
REG_PRESS = const(0xF7)  # Start of data registers.
# All registers F7 - F9 should be read in one go.
REG_TEMP = const(0xFA)
# Registers FA - FC should be read in one go.
REG_COMP = const(0x88)  # Start of compensation parameters.
# All registers 88 - A1 should be read in one go.


class BMP280_I2C:

    def __init__(self, bus, address=0x77):
        """Create an BMP280_I2C object.

        Arguments:
            bus: which connections we use.
            address: I2C address. Defaults to 0x76
        """
        self._i2c = I2c(bus, I2C.MASTER)
        self._address = address
        if self.ready:
            self._i2c.mem_write(0xF3, self._address, REG_CONFIG)
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
        if self._i2c.mem_read(1, self._address, REG_ID) != ID_VAL:
            return False  # Not a BMP280!
        return True

    @property
    def temperature(self):
        return self._temp

    @property
    def pressure(self):
        return self._press

    def update(self):
        """Read the sensor data from the chip."""
        if self._i2c.mem_read(1, self._address, REG_STATUS) & 0x08 == 1:
            sleep_ms(2)  # Busy measuring.
        # Temperature
        tempdata = self._i2c.mem_read(3, self._address, REG_TEMP)
        UT = float((tempdata[0] << 16 | tempdata[1] << 8 | tempdata[2]) >> 4)
        var1 = (UT / 16384.0 - self._tempcal[0] / 1024.0) * self._tempcal[1]
        var2 = ((UT / 131072.0 - self._tempcal[0] / 8192.0) * (
            UT / 131072.0 - self._tempcal[0] / 8192.0)) * self._tempcal[2]
        t_fine = int(var1+var2)
        self._temp = t_fine/5120.0
        # Pressure
        pressdata = self._i2c.mem_read(3, self._address, REG_PRESS)
        UP = float((pressdata[0] << 16 | pressdata[1] << 8 | tempdata[2]) >> 4)
        var1 = t_fine/2.0 - 64000.0
        var2 = var1 * var1 * self._presscal[5] / 32768.0
        var2 = var2 + var1 * self._presscal[4] * 2.0
        var2 = var2/4.0 + self._presscal[3] * 65536.0
        var1 = self._presscal[2] * var1 * var1 / 534288.0 + self._presscal[1] * var1 / 534288.0
        var1 = (1.0 + var1/32768.0) * self._presscal[0]
        if var1 == 0.0:
            return 0
        p = 1048576.0 - UP
        p = (p - var2 / 4096.0) * 6250 / var1
        var1 = self._presscal[8] * p * p / 2147483648.0
        var2 = p * self._presscal[7] / 32768.0
        self._press = p + (var1 + var2 + self._presscal[6]) / 16.0
