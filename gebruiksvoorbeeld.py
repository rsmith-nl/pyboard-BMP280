import BMP280
s = BMP280.BMP280_I2C(2)
s.read()

data = s._i2c.mem_read(24, s._address, BMP280.REG_COMP)

from ustruct import unpack
comp = unpack('<HhhHhhhhhhhh', data)
s._i2c.mem_read(2, s._address, BMP280.REG_COMP)
