#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for RS-UV3 Classes."""

import random
import unittest
import logging
import logging.handlers

from serial.serialutil import SerialException

from . import constants
from .context import dummyserial

__author__ = 'Greg Albrecht <gba@orionlabs.io>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'


class DummySerialTest(unittest.TestCase):  # pylint: disable=R0904
    """Tests for Dummy Serial."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(dummyserial.constants.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(dummyserial.constants.LOG_LEVEL)
        _console_handler.setFormatter(dummyserial.constants.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    @classmethod
    def random(cls, length=8, alphabet=None):
        """
        Generates a random string for test cases.

        :param length: Length of string to generate.
        :param alphabet: Alphabet to use to create string.
        :type length: int
        :type alphabet: str
        """
        alphabet = alphabet or constants.ALPHANUM
        return ''.join(random.choice(alphabet) for _ in xrange(length))

    def setUp(self):  # pylint: disable=C0103
        """
        Sets up test environment:

        1) Creates a random serial port name.
        2) Creates a random baud rate.
        """
        self.random_serial_port = self.random()
        self.random_baudrate = self.random(5, constants.NUMBERS)
        self._logger.debug(
            'random_serial_port=%s random_baudrate=%s',
            self.random_serial_port,
            self.random_baudrate
        )

    def test_write_and_read(self):
        """Tests writing-to and reading-from a Dummy Serial port."""
        rand_write_len1 = random.randint(0, 1024)
        rand_write_len2 = random.randint(0, 1024)
        rand_write_str1 = self.random(rand_write_len1)
        rand_write_str2 = self.random(rand_write_len2)

        ds_instance = dummyserial.Serial(
            port=self.random_serial_port,
            baudrate=self.random_baudrate,
            ds_responses={rand_write_str1: rand_write_str2}
        )

        ds_instance.write(rand_write_str1)

        read_data = ''
        while 1:
            read_data = ''.join([read_data, ds_instance.read(rand_write_len2)])
            waiting_data = ds_instance.outWaiting()
            if not waiting_data:
                break

        self.assertEqual(read_data, rand_write_str2)

    def test_open_port(self):
        """Tests opening an already-open Dummy Serial port."""
        rand_write_len1 = random.randint(0, 1024)
        rand_write_len2 = random.randint(0, 1024)
        rand_write_str1 = self.random(rand_write_len1)
        rand_write_str2 = self.random(rand_write_len2)

        ds_instance = dummyserial.Serial(
            port=self.random_serial_port,
            baudrate=self.random_baudrate,
            ds_responses={rand_write_str1: rand_write_str2}
        )

        self.assertTrue(ds_instance._isOpen)  # pylint: disable=W0212
        with self.assertRaises(SerialException):
            ds_instance.open()

    def test_close(self):
        """Tests closing a Dummy Serial port."""
        rand_write_len1 = random.randint(0, 1024)
        rand_write_len2 = random.randint(0, 1024)
        rand_write_str1 = self.random(rand_write_len1)
        rand_write_str2 = self.random(rand_write_len2)

        ds_instance = dummyserial.Serial(
            port=self.random_serial_port,
            baudrate=self.random_baudrate,
            ds_responses={rand_write_str1: rand_write_str2}
        )

        self.assertTrue(ds_instance._isOpen)  # pylint: disable=W0212
        self.assertFalse(ds_instance.close())
        self.assertFalse(ds_instance._isOpen)  # pylint: disable=W0212

    def test_write_and_read_no_data_present(self):  # pylint: disable=C0103
        """Tests writing and reading with an unspecified response."""
        rand_write_len1 = random.randint(0, 1024)
        rand_write_len2 = random.randint(0, 1024)
        rand_write_str1 = self.random(rand_write_len1)

        ds_instance = dummyserial.Serial(
            port=self.random_serial_port,
            baudrate=self.random_baudrate
        )

        ds_instance.write(rand_write_str1)

        read_data = ''
        while 1:
            read_data = ''.join([read_data, ds_instance.read(rand_write_len2)])
            waiting_data = ds_instance.outWaiting()
            if not waiting_data:
                break

        self.assertEqual(
            dummyserial.constants.NO_DATA_PRESENT, read_data)

if __name__ == '__main__':
    unittest.main()
