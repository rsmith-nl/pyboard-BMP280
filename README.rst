Using the Adafruit BMP280 with the pyboard
##########################################

:date: 2018-04-11
:tags: pyboard, BMP280
:author: Roland Smith

.. Last modified: 2018-04-17T00:27:54+0200

Introduction
------------

This code was written to get the Adafruit BMP280 breakout board to work with
the pyboard.

The pyboard_ runs micropython_, while Adafruit uses a variant of micropython called
circuitpython_ on their boards.

.. _micropython: https://micropython.org/
.. _pyboard: https://store.micropython.org/product/PYBv1.1
.. _circuitpython: https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython

Adafruit's Python code is generally not compatible with micropython because of
API differences.

But using the datasheet of the BMP280_ and the `Adafruit code`_ as guides, it
was not difficult to create a working version for the pyboard.

.. _Adafruit code: https://github.com/adafruit/Adafruit_CircuitPython_BMP280
.. _BMP280: https://www.bosch-sensortec.com/bst/products/all_products/bmp280


Wiring the BMP280 to the pyboard
--------------------------------

This module only supports an I²C connection.

The code in the examples assumes that the BMP280 is connected to the 2nd I²C
channel on the pyboard. That is, Y9 on the byboard is connected to SCK on the
BMP280 and Y10 on the pyboard is connected to SDI on the BMP280.

The 3V3 pin of the pyboard is connected to VIN on the BMP280. The GND pin of
the pyboard is connected to the GND pin of the BMP280. Additionally, the SDO
pin of the BMP280 is also connected to GND, to select I²C address ``0x76``.


Using the code
--------------

Copy the file ``BMP280.py`` to the pyboard. Then you can use it from either
the REPL or from ``main.py``.


Examples
--------

There are two examples that you can use or study.

* ``main-continuous.py`` reports the sensor reading every minute over the
  serial connection.
* ``main-query.py`` reports the sensor reading whenever it receives a line
  containing ``?``.

Both examples can be used by copying one of them to the pyboard as ``main.py``
and rebooting the pyboard.

If you use ``main-query.py`` on the pyboard, you can use ``listener.py`` on
your computer to retrieve the sensor values periodically and store them in a
file.


License
-------

MIT. See LICENSE.txt

.. PELICAN_END_SUMMARY


