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


import sys
import os
import glob
from collections.abc import Sequence
import subprocess
import tempfile
import pathlib

import pytest

# pylint: disable=wrong-import-position
from ..utils import execute_command, assert_rc, assert_patterns, \
    assert_patterns_in_lines
# pylint: enable=wrong-import-position

# The boolean conditions, for better readability
RUN = True
SKIP = False
RUN_NO_WIN = sys.platform != 'win32'


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
        print(f"\nExecuting testcase: {desc}", flush=True)

    ensure_no_listeners(verbose, 'test setup')
    start_listeners(input_listeners, verbose, 'test setup')

    if 'log' in exp_results:
        exp_log_file, exp_log_lines = exp_results['log']
        assert isinstance(exp_log_file, str)
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
        with open(exp_log_file, encoding='utf-8') as log_fp:
            log = log_fp.read()
        log_lines = log.rstrip('\n').split('\n')
        assert 'test' in exp_results
        test = exp_results['test']
        assert_output(test, exp_log_lines, log_lines, 'log', desc)


def ensure_no_listeners(verbose, situation):
    """
    Ensure that no listener is running.

    This function relies on the 'pywbemlistener list' and 'stop' commands
    working.
    """
    cmd_args = ["pywbemlistener", "-o", "plain", "list"]
    if verbose:
        print(f"{situation}: Listing listeners: {cmd_args!r}", flush=True)
    out = check_output(cmd_args, situation, "Listing listeners failed", verbose)
    lis_lines = out.rstrip('\n').split('\n')
    for lis_line in lis_lines[1:]:
        lis_name = lis_line.split(' ')[0]
        cmd_args = ["pywbemlistener", "stop", lis_name]
        if verbose:
            cmd_args.insert(1, "-vv")
        if verbose:
            print(f"{situation}: Stopping listener: {cmd_args!r}", flush=True)
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
        cmd_args = ["pywbemlistener", "start"]
        if verbose:
            cmd_args.insert(1, "-vv")
        cmd_args.extend(lis_args)
        if verbose:
            print(f"{situation}: Starting listener: {cmd_args!r}", flush=True)
        check_output(cmd_args, situation, "Starting listener failed", verbose)


def check_output(cmd_args, situation, msg, verbose):
    """
    Execute a pywbemlistener command and capture its stdout/stderr.

    If the command succeeds, its stdout is returned.
    If the command fails (rc!=0) or a timeout happens, AssertionError is raised.

    A pywbemlistener 'start' command is executed by capturing its stdout/stderr
    via files, by using its hidden options --stdout-file and --stderr-file.
    This avoids the use of pipes and that is one element in
    avoiding (short-lived) pywbemlistener 'start' command timeouts
    when launching the (long-lived) pywbemlistener 'run' command.

    Any other pywbemlistener command is executed by capturing its stdout/stderr
    via pipes.

    Parameters:
      cmd_args (list of str): List of complete command line args, including
        the pywbemlistener command name.
      situation (str): Short text describing the situation (eg. test setup).
      msg (str): Error message to be used if the command fails.
      verbose (bool): Print listener log files, if they exist.

    Returns:
      str: Standard output of the command, as a Unicode string.

    Raises:
      AssertionError: The command failed or timed out.
    """
    timeout = 30  # seconds

    try:
        start_pos = cmd_args.index("start")  # 0-based index
    except ValueError:
        start_pos = None

    tmp_dir = None
    try:
        if start_pos is not None:
            # This is the start command. That is the only command where we
            # need to make sure that no file handles are inherited by the
            # run command launched by the start command. If file handles
            # from the (short-lived) start command are inherited into the
            # (long-lived) run command, the start command hangs when exiting,
            # and the subprocess.run() call below times out.
            # To achieve that, the capturing of stdout/stderr of the start
            # command is implemented via files rather than pipes by
            # specifying the --stdout-file / --stderr-file options so that the
            # start command writes its stdout/stderr to these files.

            # pylint: disable=consider-using-with
            tmp_dir = tempfile.TemporaryDirectory()
            stdout_file = pathlib.Path(tmp_dir.name) / "stdout.log"
            stderr_file = pathlib.Path(tmp_dir.name) / "stderr.log"

            cmd_args_pt1 = cmd_args[:start_pos + 1]  # including "start"
            cmd_args_pt2 = cmd_args[start_pos + 1:]  # after "start"
            cmd_args = cmd_args_pt1
            cmd_args.extend([
                "--stdout-file", str(stdout_file),
                "--stderr-file", str(stderr_file)])
            cmd_args.extend(cmd_args_pt2)

            cmd_stdin = subprocess.DEVNULL
            cmd_stdout = subprocess.DEVNULL
            cmd_stderr = subprocess.DEVNULL

        else:
            # This is any other command but the start command.
            # In that case, we can use pipes to capture its stdout/stderr,
            # because none of the other commands starts a long-lived process.
            cmd_stdin = subprocess.PIPE
            cmd_stdout = subprocess.PIPE
            cmd_stderr = subprocess.PIPE

        try:
            cp = subprocess.run(
                cmd_args, shell=False, text=True, check=False, close_fds=True,
                stdin=cmd_stdin, stdout=cmd_stdout, stderr=cmd_stderr,
                timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            if start_pos is not None:
                out, err = get_out_err(stdout_file, stderr_file)
            else:
                out = ""
                err = ""
            exc_out, exc_err = get_exc_out_err(exc)
            if verbose:
                log_data = get_listener_logdata()
            else:
                log_data = None

            raise AssertionError(
                f"{msg}: The command {cmd_args!r} timed out after "
                f"{timeout} s.\n"
                f"Situation: {situation}\n"
                f"Standard output:\n{out}\n"
                f"Standard error:\n{err}\n"
                f"Exception standard output:\n{exc_out}\n"
                f"Exception standard error:\n{exc_err}\n"
                f"{log_data}") from exc

        if start_pos is not None:
            out, err = get_out_err(stdout_file, stderr_file)
        else:
            out = cp.stdout
            err = cp.stderr
        rc = cp.returncode
        if rc != 0:
            if verbose:
                log_data = get_listener_logdata()
            else:
                log_data = None
            raise AssertionError(
                f"{msg}: The command {cmd_args!r} failed with rc={rc}.\n"
                f"Situation: {situation}\n"
                f"Standard output:\n{out}\n"
                f"Standard error:\n{err}\n"
                f"{log_data}")
    finally:
        if tmp_dir:
            tmp_dir.cleanup()

    return out


def get_out_err(stdout_file, stderr_file):
    """
    Return stdout and stderr from the stdout/stderr files.
    """
    try:
        out = stdout_file.read_text()
    except FileNotFoundError:
        out = ""
    try:
        err = stderr_file.read_text()
    except FileNotFoundError:
        err = ""
    return out, err


def get_exc_out_err(exc):
    """
    Return stdout/stderr attached to a subprocess.TimeoutExpired exception.
    """
    exc_out = exc.output
    if isinstance(exc_out, bytes):
        exc_out = exc_out.decode('utf-8')
    exc_err = exc.stderr
    if isinstance(exc_err, bytes):
        exc_err = exc_err.decode('utf-8')
    return exc_out, exc_err


def get_listener_logdata():
    """
    Return the data in the listener log files.

    We do not have the listener name at this point, but there
    should be only one log file, if any.
    """
    log_files = 'pywbemlistener_*.log'
    result = []
    for log_file in glob.glob(log_files):
        with open(log_file, encoding='utf-8') as log_fp:
            log_data = log_fp.read()
        if isinstance(log_data, bytes):
            log_data = log_data.decode('utf-8')
        result.append(f"Log file {log_file}:")
        result.append(log_data)
    return "\n".join(result)


def assert_output(test, exp_patterns, act_lines, source, desc):
    """
    Assert the output depending on the type of test.
    """
    if test == 'all':
        assert_patterns(exp_patterns, act_lines, source, desc)
    elif test == 'contains':
        assert_patterns_in_lines(exp_patterns, act_lines, source, desc)
