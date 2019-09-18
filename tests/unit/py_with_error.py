"""
    Test script to be loaded with pywbemcli --mock-server general option to test
    capability to execute python code as part of startup.
    This script should generate an exception because of python syntax error.
"""

# pylint: disable=undefined-variable
assert "CONN" in globalsx()  # noqa: F821
