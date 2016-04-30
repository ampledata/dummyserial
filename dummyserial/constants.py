#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Dummy Serial Constants."""

import logging


__author__ = 'Greg Albrecht <gba@orionlabs.io>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'


LOG_LEVEL = logging.DEBUG
LOG_FORMAT = logging.Formatter(
    '%(asctime)s dummyserial %(levelname)s %(name)s.%(funcName)s:%(lineno)d'
    ' - %(message)s')


# The default timeout value in seconds.
DEFAULT_TIMEOUT = 2

# The default Baud Rate.
DEFAULT_BAUDRATE = 9600

# A dictionary of respones from the dummy serial port.
#
# The key is the message (string) sent to the dummy serial port, and the item
# is the response (string) from the dummy serial port.
#
# Intended to be monkey-patched in the calling test module.
#
# Example:
#    RESPONSES['EXAMPLEREQUEST'] = 'EXAMPLERESPONSE'


# Response when no matching message (key) is found in the look-up dictionary.
#
# Should not be an empty string, as that is interpreted as "no data available
# on port".
#
# Might be monkey-patched in the calling test module.
DEFAULT_RESPONSE = 'NONE'


NO_DATA_PRESENT = ''
