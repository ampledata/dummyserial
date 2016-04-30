#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Dummy Serial Class Definitions"""

import logging
import logging.handlers
import sys
import time

from serial.serialutil import portNotOpenError

import dummyserial.constants

__author__ = 'Greg Albrecht <gba@orionlabs.io>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'


class Serial(object):
    """
    Dummy (mock) serial port for testing purposes.

    Mimics the behavior of a serial port as defined by the
    `pySerial <http://pyserial.sourceforge.net/>`_ module.

    Args:
        * port:
        * timeout:

    Note:
    As the portname argument not is used properly, only one port on
    :mod:`dummyserial` can be used simultaneously.
    """

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(dummyserial.constants.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(dummyserial.constants.LOG_LEVEL)
        _console_handler.setFormatter(dummyserial.constants.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def __init__(self, *args, **kwargs):
        self._logger.debug('args=%s', args)
        self._logger.debug('kwargs=%s', kwargs)

        self.is_open = True
        self._waiting_data = dummyserial.constants.NO_DATA_PRESENT

        self.port = kwargs['port']  # Serial port name.
        self.initial_port_name = self.port  # Initial name given to the port

        self.ds_responses = kwargs.get('ds_responses', {})
        self.timeout = kwargs.get(
            'timeout', dummyserial.constants.DEFAULT_TIMEOUT)
        self.baudrate = kwargs.get(
            'baudrate', dummyserial.constants.DEFAULT_BAUDRATE)

    def __repr__(self):
        """String representation of the DummySerial object."""
        return (
            "{0}.{1}<id=0x{2:x}, open={3}>(port={4!r}, timeout={5!r}, "
            "waiting_data={6!r})".format(
                self.__module__,
                self.__class__.__name__,
                id(self),
                self.is_open,
                self.port,
                self.timeout,
                self._waiting_data,
            )
        )

    def open(self):
        """Open a (previously initialized) port."""
        self._logger.debug('Opening port')

        if self.is_open:
            raise dummyserial.exceptions.DSIOError('Port already opened.')

        self.is_open = True
        self.port = self.initial_port_name

    def close(self):
        """Close a port on dummy_serial."""
        self._logger.debug('Closing port')

        if not self.is_open:
            raise dummyserial.exceptions.DSIOError('Port already closed.')

        self.is_open = False
        self.port = None

    def write(self, inputdata):
        """Write to a port on dummy_serial.

        Args:
            inputdata (string/bytes): data for sending to the port on
            dummy_serial. Will affect the response for subsequent read
            operations.

        Note that for Python2, the inputdata should be a **string**. For
        Python3 it should be of type **bytes**.
        """
        self._logger.debug('Writing "%s"', inputdata)

        if sys.version_info[0] > 2:
            if not isinstance(inputdata, bytes):
                raise dummyserial.exceptions.DSTypeError(
                    'The input must be type bytes. Given:' + repr(inputdata))
            inputstring = str(inputdata, encoding='latin1')
        else:
            inputstring = inputdata

        if not self.is_open:
            raise dummyserial.exceptions.DSIOError(
                'Trying to write, but the port is not open. Given:' +
                repr(inputdata))

        # Look up which data that should be waiting for subsequent read
        # commands.
        self._waiting_data = self.ds_responses.get(inputstring)

    def read(self, size=1):
        """
        Read size bytes from the Dummy Serial Responses.

        The response is dependent on what was written last to the port on
        dummyserial, and what is defined in the :data:`RESPONSES` dictionary.

        Args:
            size (int): For compability with the real function.

        Returns a **string** for Python2 and **bytes** for Python3.

        If the response is shorter than size, it will sleep for timeout.

        If the response is longer than size, it will return only size bytes.

        """
        self._logger.debug('Reading %s bytes.', size)

        if not self.is_open:
            raise portNotOpenError

        if size < 0:
            raise dummyserial.exceptions.DSIOError(
                'The size to read must not be negative. ' +
                'Given: {!r}'.format(size))

        # Do the actual reading from the waiting data, and simulate the
        # influence of size.

        if self._waiting_data == dummyserial.constants.DEFAULT_RESPONSE:
            returnstring = self._waiting_data
        elif size == len(self._waiting_data):
            returnstring = self._waiting_data
            self._waiting_data = dummyserial.constants.NO_DATA_PRESENT
        elif size < len(self._waiting_data):
            self._logger.debug(
                'The size to read is smaller than the available ' +
                'data. Some bytes will be kept for later. Available data: ' +
                '%s (length = %s), size: %s',
                self._waiting_data, len(self._waiting_data), size)

            returnstring = self._waiting_data[:size]
            self._waiting_data = self._waiting_data[size:]
        else:  # Wait for timeout - we asked for more data than available!
            self._logger.debug(
                'The size to read is larger than the available ' +
                'data. Will sleep until timeout. Available data: ' +
                '%s (length = %s), size: %s',
                self._waiting_data, len(self._waiting_data), size)

            time.sleep(self.timeout)
            returnstring = self._waiting_data
            self._waiting_data = dummyserial.constants.NO_DATA_PRESENT

        # TODO Adapt the behavior to better mimic the Windows behavior

        self._logger.debug(
            'Read return data: %s (has length %s)',
            returnstring, len(returnstring))

        if sys.version_info[0] > 2:  # Convert types to make it python3 compat.
            return bytes(returnstring, encoding='latin1')
        else:
            return returnstring

    def out_waiting(self):  # pylint: disable=C0103
        """Returns length of waiting output data."""
        return len(self._waiting_data)

    outWaiting = out_waiting  # pyserial 2.7 / 3.0 compat.
