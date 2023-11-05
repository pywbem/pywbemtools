# (C) Copyright 2021 Inova Development Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The class in this file defines a common base for the pytests executed
through pywbemlistener execution.
"""

from __future__ import absolute_import, print_function

import sys
import os
import io
import glob
import pytest
import six

try:
    from collections.abc import Sequence
except ImportError:
    # pylint: disable=deprecated-class
    from collections import Sequence

if os.name == 'posix' and six.PY2:
    # pylint: disable=import-error
    import subprocess32 as subprocess
else:
    import subprocess  # pylint: disable=reimport

# pylint: disable=wrong-import-position
from ..utils import execute_command, assert_rc, assert_patterns, \
    assert_patterns_in_lines
# pylint: enable=wrong-import-position

# The boolean conditions, for better readability
RUN = True
SKIP = False
RUN_NOWIN = sys.platform != 'win32'
# See issue #1327 Disable all tests that fail because of this issue
RUN_NO_PY27 = six.PY3

# Do not run tests that use either windows or python 2.7
RUN_NO_WIN_NO_PY27 = RUN_NOWIN and RUN_NO_PY27


def pywbemlistener_test(desc, inputs, exp_results, condition):
    """
    Execute a testcase on the pywbemlistener command.

    This function executes the pywbemlistener command with inputs defined in a
    testcase and checks the actual results against expected results defined in
    the testcase.

    Parameters:

      desc (string): Description of the testcase.

      inputs (dict): Input dictionary with the following items:

        - args (sequence of string): Mandatory.
          The command line arguments for the pywbemlistener command,
          starting with the first argument after the command name.

        - env (dict of string/string): Optional.
          Environment variables to be set before executing the
          pywbemlistener command. The dict key is the variable name, and
          the dict value is the variable value as a string (without any
          shell escaping needed).

        - listeners (sequence of sequence of string): Optional.
          Listeners to have running before the pywbemlistener command is
          executed. Each outer sequence item is a listener. Each inner
          sequence item are the command line arguments for the pywbemlistener
          start command, starting with the first argument after 'start'.

      exp_results (dict): Expected result dictionary with the following items:

        - rc (int): Optional, default: 0.
          Expected command exit code.

        - stdout (sequence of string): Optional, default: not checked.
          Expected stdout of the command, in format defined by 'test' item.

        - stderr (sequence of string): Optional, default: not checked.
          Expected stderr of the command, in format defined by 'test' item.

        - log (tuple(filename, sequence of string)): Optional, default: not
          checked.
          Expected log file name and content, in format defined by 'test' item.

        - test (string): Mandatory if stdout or stderr is specified.
          Test applied to the expected output in stdout and stderr:
          - 'all': Expected output has one regex pattern for each expected
            output line, in the same order, and all must match.
          - 'contains': Expected output has regex patterns where each
            of them must match one (or more) output lines.

      condition (bool or 'pdb' or 'verbose'): Condition for running the testcase
        and how to run it:
        - True: Run the testcase.
        - False: Skip the testcase.
        - 'pdb': Break in debugger by adding the '--pdb' option.
        - 'verbose': Display command line, environment, stdin, rc, stdout
          and stderr for the command.
    """

    if not condition:
        pytest.skip('Condition not met for running the testcase')

    assert isinstance(inputs, dict)
    assert isinstance(exp_results, dict)

    input_args = inputs['args']
    input_env = inputs.get('env', {})
    input_listeners = inputs.get('listeners', [])

    assert isinstance(input_args, Sequence)
    assert isinstance(input_env, dict)
    assert isinstance(input_listeners, Sequence)

    verbose = (condition == 'verbose')
    capture = not (condition == 'pdb')

    args = []
    if condition == 'pdb':
        args.append('--pdb')
    args.extend(input_args)

    if verbose:
        print("\nExecuting testcase: {}".format(desc))
        sys.stdout.flush()

    ensure_no_listeners(verbose, 'test setup')
    start_listeners(input_listeners, verbose, 'test setup')

    if 'log' in exp_results:
        exp_log_file, exp_log_lines = exp_results['log']
        assert isinstance(exp_log_file, six.string_types)
        assert isinstance(exp_log_lines, (list, tuple))
        if os.path.isfile(exp_log_file):
            os.remove(exp_log_file)

    rc, stdout, stderr = execute_command(
        'pywbemlistener', args=args, env=input_env,
        verbose=verbose, capture=capture)

    ensure_no_listeners(verbose, 'test teardown')

    exp_rc = exp_results.get('rc', 0)
    assert_rc(exp_rc, rc, stdout, stderr, desc)

    if 'stdout' in exp_results and capture:
        assert stdout is not None
        exp_stdout = exp_results['stdout']
        stdout_lines = stdout.rstrip('\n').split('\n')
        assert 'test' in exp_results
        test = exp_results['test']
        assert_output(test, exp_stdout, stdout_lines, 'stdout', desc)

    if 'stderr' in exp_results and capture:
        assert stderr is not None
        exp_stderr = exp_results['stderr']
        stderr_lines = stderr.rstrip('\n').split('\n')
        assert 'test' in exp_results
        test = exp_results['test']
        assert_output(test, exp_stderr, stderr_lines, 'stderr', desc)

    if 'log' in exp_results:
        assert os.path.isfile(exp_log_file)
        with io.open(exp_log_file, 'r', encoding='utf-8') as log_fp:
            log_lines = log_fp.readlines()
        assert 'test' in exp_results
        test = exp_results['test']
        assert_output(test, exp_log_lines, log_lines, 'log', desc)


def ensure_no_listeners(verbose, situation):
    """
    Ensure that no listener is running.

    This function relies on the 'pywbemlistener list' and 'stop' commands
    working.
    """
    cmd_args = 'pywbemlistener -o plain list'
    if verbose:
        print("{}: Listing listeners: {}".format(situation, cmd_args))
        sys.stdout.flush()
    out = check_output(cmd_args, situation, "Listing listeners failed", verbose)
    lis_lines = out.decode('utf-8').rstrip('\n').split('\n')
    for lis_line in lis_lines[1:]:
        lis_name = lis_line.split(' ')[0]
        cmd_args = 'pywbemlistener stop {}'.format(lis_name)
        if verbose:
            print("{}: Stopping listener: {}".format(situation, cmd_args))
            sys.stdout.flush()
        check_output(cmd_args, situation, "Stopping listener failed", verbose)


def start_listeners(input_listeners, verbose, situation):
    """
    Start the specified listeners.

    This function relies on the 'pywbemlistener start' command working.

    Parameters:
      input_listeners (sequence of sequence of string):
        Listeners to have running before the pywbemlistener command is
        executed. Each outer sequence item is a listener. Each inner
        sequence item are the command line arguments for the pywbemlistener
        start command, starting with the first argument after 'start'.
    """
    for lis_args in input_listeners:
        assert isinstance(lis_args, Sequence)
        verbose_opts = '-vv' if verbose else ''
        cmd_args = 'pywbemlistener {} start {}'. \
            format(verbose_opts, ' '.join(lis_args))
        if verbose:
            print("{}: Starting listener: {}".format(situation, cmd_args))
        check_output(cmd_args, situation, "Starting listener failed", verbose)


def check_output(cmd_args, situation, msg, verbose):
    """
    Improved replacement for subprocess.check_output() with a reduced interface.

    The improvements are:
    - Prints command output (stdout+stderr) in case the command fails.
    - Circumvents a unicode encoding issue on Windows with Python 2 that happens
      on GitHub Actions, where cp65001 (Windows speak for UTF-8) is used,
      causing "LookupError: unknown encoding: cp65001", by setting
      the PYTHONIOENCODING environment variable.
    """
    if sys.platform == 'win32' and six.PY2:
        os.putenv('PYTHONIOENCODING', 'UTF-8')
    try:
        # pylint: disable=consider-using-with
        p = subprocess.Popen(cmd_args, shell=True, stdout=subprocess.PIPE)
        if six.PY2:
            try:
                out, _ = p.communicate(timeout=15)
            except Exception:
                p.kill()
                p.wait()
                raise
            rc = p.poll()
            if rc:
                raise subprocess.CalledProcessError(
                    rc, cmd_args, output=out)
        else:
            try:
                out, err = p.communicate(timeout=30)
            except subprocess.TimeoutExpired:
                p.kill()
                p.wait()
                raise
            rc = p.poll()
            if rc:
                raise subprocess.CalledProcessError(
                    rc, cmd_args, output=out, stderr=err)
    except Exception as exc:
        # Note: The exception message contains the command line
        print("{}: Error: {}: {}".format(situation, msg, exc))
        sys.stdout.flush()
        if hasattr(exc, 'output'):
            out = exc.output
            if isinstance(out, six.binary_type):
                out = out.decode('utf-8')
            print("Begin of command output (stdout):")
            print(out)
            print("End of command output")
            sys.stdout.flush()
        if hasattr(exc, 'stderr'):
            err = exc.stderr
            if isinstance(err, six.binary_type):
                err = err.decode('utf-8')
            print("Begin of command output (stderr):")
            print(err)
            print("End of command output")
            sys.stdout.flush()
        if verbose:
            # We do not have the listener name at this point, but there
            # should be only one log file, if any.
            log_files = 'pywbemlistener_*.log'
            for log_file in glob.glob(log_files):
                with io.open(log_file, 'r', encoding='utf-8') as log_fp:
                    log_data = log_fp.read()
                if isinstance(log_data, six.binary_type):
                    log_data = log_data.decode('utf-8')
                print("Begin of log file {}:".format(log_file))
                print(log_data)
                print("End of log file")
                sys.stdout.flush()
        raise
    return out


def assert_output(test, exp_patterns, act_lines, source, desc):
    """
    Assert the output depending on the type of test.
    """
    if test == 'all':
        assert_patterns(exp_patterns, act_lines, source, desc)
    elif test == 'contains':
        assert_patterns_in_lines(exp_patterns, act_lines, source, desc)
