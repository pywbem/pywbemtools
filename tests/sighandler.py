#!/usr/bin/env python

"""
Demonstrate signal handling in Python.

Usage:
- run this script, it will show the process ID
- send OS-level signals to the process ID of the script (e.g. 'kill -n 2 PID')
"""

# pylint: disable=missing-function-docstring,missing-class-docstring

import sys
import os
import platform
import signal
import time

SLEEP_TIME = 300

EOL = '\n'  # Replace "\n" f-strings. "\" not fails in {} with python lt 3.12


def sigstr(signal_number):
    try:
        return signal.strsignal(signal_number)
    except AttributeError:
        return '?'


class SignalIndication(Exception):
    pass


def signal_handler(signal_number, frame):
    # pylint: disable=unused-argument
    print(f"handler: Received signal {signal_number} ({sigstr(signal_number)}")
    raise SignalIndication(
        f"signal {signal_number} ({sigstr(signal_number)})")


def register_handler(signal_name, condition=True):
    if condition:
        signal_number = getattr(signal, signal_name)
        print(f"main: Registering handler for signal {signal_number} "
              f"({signal_name}, {sigstr(signal_number)})")
        signal.signal(signal_number, signal_handler)


print(f"main: Python: {sys.version.replace(EOL, '')}")
print(f"main: Platform: {sys.platform} / {platform.platform()}")
print(f"main: Process: {os.getpid()}")
register_handler('SIGINT')
register_handler('SIGILL')
register_handler('SIGABRT')
register_handler('SIGFPE')
register_handler('SIGSEGV')
register_handler('SIGTERM')
register_handler('SIGBREAK', sys.platform == 'win32')
while True:
    print(f"main: Sleeping for {SLEEP_TIME} sec")
    try:
        time.sleep(SLEEP_TIME)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"main: Caught {exc.__class__.__name__}: {exc}")
