"""
Test global options that can be tested without a subcommand
"""
from __future__ import absolute_import, print_function

import os
import re
import pytest

from .utils import execute_pywbemcli, assert_rc

TEST_DIR = os.path.dirname(__file__)


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

    # TODO remap this to use the same test_funct decorator as pywbem when
    # that code is committed.
    @pytest.mark.parametrize(
        "desc, tst_files, exp_result_start, exp_result_end, exp_rc, exp_stderr",
        [
            [
                ["Single good mof file"],
                ['simple_mock_model.mof'],
                None,
                None,
                0,
                ""
            ],
            [
                ["Mof file does not exist. Test for rc = 1"],
                ['blah.mof'],
                None,
                None,
                1,
                None,
            ],
            [
                ["Python file as mock setup script"],
                ['simple_python_mock_script.py'],
                None,
                None,
                0,
                None,
            ],
            [
                ["Install mof and python file into repo"],
                ['simple_mock_model.mof', 'simple_python_mock_script.py'],
                None,
                None,
                0,
                None,
            ]
        ]
    )
    def test_mock_server(self, desc, tst_files, exp_result_start,
                         exp_result_end, exp_rc, exp_stderr):
        """
        Test 'pywbemcli -s http://blah --mock-server <filename>.mof.
        Tests that the option is accepted. Does not test that the mof
        file is compiled.
        """
        cmd_line = []
        for tst_file in tst_files:
            cmd_line.append('--mock-server')
            cmd_line.append(os.path.join(TEST_DIR, tst_file))
        # Because there is no quit subcommand, some command must be issued
        # to avoid going into repl mode.
        # TODO add a subcommand quit.
        cmd_line.extend(['class', 'enumerate'])

        rc, stdout, stderr = execute_pywbemcli(cmd_line)

        assert_rc(exp_rc, rc, stdout, stderr)
        if exp_stderr:
            assert stderr == exp_stderr
        if exp_result_start:
            assert stdout.startswith(
                "Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]...\n"), \
                "stdout={!r}".format(stdout)
