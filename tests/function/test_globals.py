"""
Test global options that can be tested without a subcommand
"""
from __future__ import absolute_import, print_function

import re

from .utils import execute_pywbemcli, assert_rc


class TestGlobalOptions(object):
    """
    All tests for the 'pywbmecl' command with global options that can be tested
    without a subcommand.
    """

    def test_global_help(self):
        """Test 'pywbemcli --help'"""

        rc, stdout, stderr = execute_pywbemcli(['--help'])

        assert_rc(0, rc, stdout, stderr)
        assert stdout.startswith(
            "Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]...\n"), \
            "stdout={!r}".format(stdout)
        assert stderr == ""

    def test_global_version(self):
        """Test 'pywbemcli --version'"""

        rc, stdout, stderr = execute_pywbemcli(['--version'])

        assert_rc(0, rc, stdout, stderr)
        assert re.match(r'^pywbemcli, version [0-9]+\.[0-9]+\.[0-9]+', stdout)
        assert stderr == ""
