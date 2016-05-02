Python Module for Dummy Serial
******************************

Emulates pyserial's write/read responses from a serial port.

Works by suppling a dictionary of responses to various paramters.

For example::

    ds_responses = {
        'taco': 'yum'
    }

Would `read()` *yum* for a `write()` of *taco*.

Derived from Jonas Berg's 'dummy_serial.py'.

Source
======
Github: https://github.com/ampledata/dummyserial

Authors
=======
* 'dummyserial' Stand-alone Python Module: Greg Albrecht <gba@orionlabs.io>
* 'dummy_serial.py' Mock Fixture: Jonas Berg <pyhys@users.sourceforge.net>

Copyright
=========
Copyright 2016 Orion Labs, Inc.

License
=======
Apache License, Version 2.0
