#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import sys
import time

import dummyserial.constants
import dummyserial.exceptions

"""Dummy Serial Class Definitions"""

__author__ = 'Greg Albrecht <gba@orionlabs.io>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'


class DummySerial(object):
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

        self._isOpen = True
        self._waiting_data = dummyserial.constants.NO_DATA_PRESENT

        self.port = kwargs['port']  # Serial port name.
        self.initial_port_name = self.port  # Initial name given to the port

        self.ds_responses = kwargs.get('ds_responses', {})
        self.timeout = kwargs.get(
            'timeout', dummyserial.constants.DEFAULT_TIMEOUT)
        self.baudrate = kwargs.get(
            'baudrate', dummyserial.constants.DEFAULT_BAUDRATE)

    def __repr__(self):
        """String representation of the DummySerial object"""
        return (
            "{0}.{1}<id=0x{2:x}, open={3}>(port={4!r}, timeout={5!r}, "
            "waiting_data={6!r})".format(
                self.__module__,
                self.__class__.__name__,
                id(self),
                self._isOpen,
                self.port,
                self.timeout,
                self._waiting_data,
            )
        )

    def open(self):
        """Open a (previously initialized) port."""
        self._logger.debug('Opening port')

        if self._isOpen:
            raise dummyserial.exceptions.DSIOError('Port already opened.')

        self._isOpen = True
        self.port = self.initial_port_name

    def close(self):
        """Close a port on dummy_serial."""
        self._logger.debug('Closing port')

        if not self._isOpen:
            raise dummyserial.exceptions.DSIOError('Port already closed.')

        self._isOpen = False
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
            if not type(inputdata) == bytes:
                raise dummyserial.exceptions.DSTypeError(
                    'The input must be type bytes. Given:' + repr(inputdata))
            inputstring = str(inputdata, encoding='latin1')
        else:
            inputstring = inputdata

        if not self._isOpen:
            raise dummyserial.exceptions.DSIOError(
                'Trying to write, but the port is not open. Given:' +
                repr(inputdata))

        # Look up which data that should be waiting for subsequent read
        # commands.
        self._waiting_data = self.ds_responses.get(inputstring)

    def read(self, numberOfBytes):
        """
        Read from a port.

        The response is dependent on what was written last to the port on
        dummyserial, and what is defined in the :data:`RESPONSES` dictionary.

        Args:
            numberOfBytes (int): For compability with the real function.

        Returns a **string** for Python2 and **bytes** for Python3.

        If the response is shorter than numberOfBytes, it will sleep for
        timeout.

        If the response is longer than numberOfBytes, it will return only
        numberOfBytes bytes.

        """
        self._logger.debug(
            'Reading from port (max length %s bytes)', numberOfBytes)

        if numberOfBytes < 0:
            raise dummyserial.exceptions.DSIOError(
                'The numberOfBytes to read must not be negative. ' +
                'Given: {!r}'.format(numberOfBytes))

        if not self._isOpen:
            raise dummyserial.exceptions.DSIOError(
                'Trying to read, but the port is not open.')

        # Do the actual reading from the waiting data, and simulate the
        # influence of numberOfBytes.

        if self._waiting_data == dummyserial.constants.DEFAULT_RESPONSE:
            returnstring = self._waiting_data
        elif numberOfBytes == len(self._waiting_data):
            returnstring = self._waiting_data
            self._waiting_data = dummyserial.constants.NO_DATA_PRESENT
        elif numberOfBytes < len(self._waiting_data):
            self._logger.debug(
                'The numberOfBytes to read is smaller than the available ',
                'data. Some bytes will be kept for later. Available data: ',
                '%s (length = %s), numberOfBytes: %s',
                self._waiting_data, len(self._waiting_data), numberOfBytes)

            returnstring = self._waiting_data[:numberOfBytes]
            self._waiting_data = self._waiting_data[numberOfBytes:]
        else:  # Wait for timeout - we asked for more data than available!
            self._logger.debug(
                'The numberOfBytes to read is larger than the available ' +
                'data. Will sleep until timeout. Available data: ' +
                '%s (length = %s), numberOfBytes: %s',
                self._waiting_data, len(self._waiting_data), numberOfBytes)

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

    def outWaiting(self):
        return len(self._waiting_data)
