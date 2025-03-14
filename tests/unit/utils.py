# Copyright 2017 IBM Corp. All Rights Reserved.
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
Utilities to execute a pywbemtools command and for comparing expected results.
"""


import os
import sys
import re
from collections.abc import Mapping, Sequence
from io import StringIO
from copy import copy
from subprocess import Popen, PIPE, TimeoutExpired
import shlex

import packaging.version
import click


# Click version as a tuple
CLICK_VERSION = packaging.version.parse(click.__version__).release

EOL = '\n'  # Replace "\n" f-strings. "\" not fails in {} with python lt 3.12


def execute_command(cmdname, args, env=None, stdin=None, verbose=False,
                    capture=True):
    """
    Invoke a command as a child process.

    The command must be accessible in the PATH, i.e. installed in the current
    Python environment.

    Parameters:

      cmdname (string): Command name (e.g. pywbemcli). The command name may be
        a binary string encoded in UTF-8, or a unicode string.

      args (sequence of string): Command line arguments, starting with the first
        argument after the command name. Each single argument must be its own
        item in the sequence; combining the arguments into a string does not
        work. The arguments may be binary strings encoded in UTF-8, or unicode
        strings.

      env (dict or None): Environment variables to be put into the environment
        before executing the command. None means to not set any variables. Dict
        key is the variable name as a string; dict value is the variable value
        as a string (without any shell escaping needed), or None to unset the
        variable. The environment of the current process is saved and restored.

      stdin (string or None):
        Passed to the executable as stdin, if not None. Lines are separated
        with NL. May be binary a string encoded in UTF-8, or a unicode string.

      verbose (bool):
        Display args, env, and stdin before executing the command and rc,
        stdout, stderr afterwards.

      capture (bool):
        Capture stdout and stderr of the command. Not capturing that is useful
        when invoking the commands with the --pdb option that breaks in the
        built-in pdb debugger.

    Returns:

      tuple(rc, stdout, stderr): Output of the command, where:

        * rc (int): Exit code of the command.

        * stdout (unicode string): Standard output of the command. Lines are
          separated with NL. Empty string if there was no output. None if
          output was not captured.

        * stderr (unicode string): Standard error of the command. Lines are
          separated with NL. Empty string if there was no output. None if
          output was not captured.
    """

    if env is None:
        env = {}
    else:
        assert isinstance(env, Mapping)
        env = copy(env)

    env['PYTHONPATH'] = '.'  # Use local files
    env['PYTHONWARNINGS'] = ''  # Disable for parsing output

    saved_env = {}  # Saved env vars that were changed for this test case

    # Put the env vars into the environment of the current Python process,
    # from where they will be inherited into its child processes (-> shell ->
    # cli command).
    for name in env:
        value = env[name]
        if value is None:
            if name in os.environ:
                saved_env[name] = os.getenv(name)
                del os.environ[name]
        else:
            saved_env[name] = os.getenv(name)  # None if not set
            os.environ[name] = value

    assert isinstance(args, Sequence)
    if not isinstance(cmdname, str):
        cmdname = cmdname.decode('utf-8')
    cmd_args = [cmdname]
    for arg in args:
        if not isinstance(arg, str):
            arg = arg.decode('utf-8')
        cmd_args.append(arg)

    if stdin is not None and not isinstance(stdin, str):
        stdin = stdin.decode('utf-8')

    if verbose:
        display_envvars = ', '.join(
            [f'{var}={os.environ[var]}'
             for var in os.environ if 'PYWBEM' in var])
        print(f'\nEnvironment: {display_envvars}')
        if stdin is not None:
            print(f'Stdin: {stdin!r}')
        sys.stdout.flush()

    if capture:
        stdin_stream = PIPE
        stdout_stream = PIPE
        stderr_stream = PIPE
    else:
        stdin_stream = None
        stdout_stream = None
        stderr_stream = None
        if stdin is not None:
            if verbose:
                print('Suppressing stdin because not capturing')
                sys.stdout.flush()
            stdin = None

    universal_newlines = True

    # Time in seconds allowed for command before the test considers it to have
    # timed out. With 60 seconds, we got occasional timeouts in GitHub tests.
    cmd_timeout = 120

    # Note: Popen.communicate() and Popen.wait() wait not only for the child
    # process to finish, but for all grandchild processes in addition. In case
    # of the 'pywbemlistener start' command, the grandchild 'run' process
    # however is supposed to continue running after the 'start' process has
    # finished. Therefore, using Popen.communicate() and Popen.wait() does not
    # work for this case. See https://stackoverflow.com/q/55160319/1424462.
    # We use shell redirection in this case.

    if capture and cmd_args[0] == 'pywbemlistener':
        assert stdin is None
        out_log = 'out.log'
        err_log = 'err.log'
        redirect = f' >{out_log} 2>{err_log}'
        cmd_args = ' '.join([shlex.quote(a) for a in cmd_args]) + redirect

        if verbose:
            print(f'Command (shell): {cmd_args}')
            sys.stdout.flush()

        # pylint: disable=consider-using-with
        proc = Popen(cmd_args, shell=True, stdin=None,
                     stdout=None, stderr=None,
                     universal_newlines=universal_newlines)

        try:
            proc.wait(timeout=cmd_timeout)
            rc = proc.returncode
        except TimeoutExpired:
            proc.kill()
            rc = 255
            print(f"Error: Timeout ({cmd_timeout} sec) when waiting for "
                  f"command to complete; Killed process and setting {rc=}")
            sys.stdout.flush()

        with open(out_log, 'rb') as fp:
            stdout_str = fp.read()
        with open(err_log, 'rb') as fp:
            stderr_str = fp.read()

    else:
        if verbose:
            print(f'Command (direct): {cmd_args}')
            sys.stdout.flush()

        # pylint: disable=consider-using-with
        proc = Popen(cmd_args, shell=False, stdin=stdin_stream,
                     stdout=stdout_stream, stderr=stderr_stream,
                     universal_newlines=universal_newlines)

        try:
            stdout_str, stderr_str = proc.communicate(
                input=stdin, timeout=cmd_timeout)
            rc = proc.returncode
        except TimeoutExpired:
            proc.kill()
            rc = 255
            try:
                stdout_str, stderr_str = proc.communicate(timeout=10)
            except TimeoutExpired:
                stdout_str = stderr_str = None
            print(f"Error: Timeout ({cmd_timeout} sec) when waiting for "
                  f"command to complete; Killed process and setting {rc=};"
                  f" Stdout produced so far: {stdout_str!r}; Stderr produced "
                  f"so far: {stderr_str!r}")
            sys.stdout.flush()

    # Restore environment of current process
    for name, value in saved_env.items():
        if value is None:
            del os.environ[name]
        else:
            os.environ[name] = value

    if verbose:
        print(f'Exit code: {rc}')
        if capture:
            print(f'Stdout: {stdout_str!r}')
            print(f'Stderr: {stderr_str!r}')
        sys.stdout.flush()

    if stdout_str is not None:
        if isinstance(stdout_str, bytes):
            stdout_str = stdout_str.decode('utf-8')
        # Note: The CRs were originally only fixed for Click issue #1231, but
        # with the pywbemlistener testing, it became necessary on all Python
        # versions on Windows.
        if sys.platform == 'win32':
            stdout_str = stdout_str.replace('\r\r\n', '\n')  \
                                   .replace('\r\n', '\n')  \
                                   .replace('\r', '')

    if stderr_str is not None:
        if isinstance(stderr_str, bytes):
            stderr_str = stderr_str.decode('utf-8')
        # Note: The CRs were originally only fixed for Click issue #1231, but
        # with the pywbemlistener testing, it became necessary on all Python
        # versions on Windows.
        if sys.platform == 'win32':
            stderr_str = stderr_str.replace('\r\r\n', '\n')  \
                                   .replace('\r\n', '\n')  \
                                   .replace('\r', '')

    return rc, stdout_str, stderr_str


def assert_rc(exp_rc, rc, stdout, stderr, desc):
    """
    Assert that the specified return code is as expected.

    The actual return code is compared with the expected return code,
    and if they don't match, stdout and stderr are displayed as a means
    to help debugging the issue.

    Parameters:

      exp_rc (int): expected return code.

      rc (int): actual return code.

      stdout (string): stdout of the command, for debugging purposes.

      stderr (string): stderr of the command, for debugging purposes.

      desc (string): Testcase description.
    """

    assert exp_rc == rc, \
        "Unexpected exit code in test:\n" \
        f"{desc}\n" \
        f"Expected rc: {exp_rc}\n" \
        f"Actual rc: {rc}\n" \
        "Stdout:\n" \
        "------------\n" \
        f"{stdout}\n" \
        "------------\n" \
        "Stderr:\n" \
        "------------\n" \
        f"{stderr}\n" \
        "------------\n"


def assert_patterns(exp_patterns, act_lines, source, desc):
    """
    Assert that the specified lines match the specified patterns.

    The patterns are searched in the lines. If a pattern is supposed to match
    a line from start to end, it must contain '^' and '$'.

    Parameters:

      exp_patterns (iterable of string): regexp patterns defining the expected
        value for each line.

      act_lines (iterable of string): the lines to be matched.

      source (string): Source from where the lines were obtained, e.g.
        'stdout' or 'stderr'.

      desc (string): Testcase description.
    """
    assert len(act_lines) == len(exp_patterns), \
        f"Unexpected number of lines on {source} in test:\n" \
        f"{desc}\n" \
        f"Expected patterns (cnt={len(exp_patterns)}):\n" \
        "------------\n" \
        f"{EOL.join(exp_patterns)}\n" \
        "------------\n" \
        f"Actual lines (cnt={len(act_lines)}):\n" \
        "------------\n" \
        f"{EOL.join(act_lines)}\n" \
        "------------\n"

    for i, act_line in enumerate(act_lines):
        exp_pattern = exp_patterns[i]
        assert re.search(exp_pattern, act_line), \
            f"Unexpected line #{i} on {source} in test:\n" \
            f"{desc}\n" \
            "Expected pattern:\n" \
            "------------\n" \
            f"{exp_pattern}\n" \
            "------------\n" \
            "Actual line:\n" \
            "------------\n" \
            f"{act_line}\n" \
            "------------\n"


def assert_patterns_in_lines(exp_patterns, act_lines, source, desc):
    """
    Assert that for each pattern there is a matching line, in order of the
    patterns

    The patterns are searched in the lines. If a pattern is supposed to match
    a line from start to end, it must contain '^' and '$'.

    Parameters:

      exp_patterns (iterable of string): regexp patterns defining the expected
        value for a line.

      act_lines (iterable of string): the lines to be matched.

      source (string): Source from where the lines were obtained, e.g.
        'stdout' or 'stderr'.

      desc (string): Testcase description.
    """
    act_lines_iter = iter(act_lines)
    start_line = '<begin>'
    i = 0  # avoids pylint warning used-before-assignment
    try:
        act_line = next(act_lines_iter)
        for i, exp_pattern in enumerate(exp_patterns):
            start_line = act_line
            found = False
            while not found:
                if re.search(exp_pattern, act_line):
                    found = True
                    break
                act_line = next(act_lines_iter)
    except StopIteration:
        raise AssertionError(
            f"Pattern #{i} not found in order on {source} in test:\n"
            f"{desc}\n"
            "Expected pattern:\n"
            "------------\n"
            f"{exp_pattern!r}\n"
            "------------\n"
            "Start line for search:\n"
            "------------\n"
            f"{start_line!r}\n"
            "------------\n"
            "Actual lines:\n"
            "------------\n"
            f"{EOL.join(act_lines)}\n"
            "------------\n")


def assert_lines(exp_lines, act_lines, source, desc):
    """
    Assert that the specified lines match exactly the lines specified in
    exp_lines. This does not require that the pattern lines escape any
    special characters, etc.

    The exp_lines are matched against the complete line from begin to end. The
    test stops at the first difference

    Parameters:

      exp_lines (iterable of string): the expected string for each line.

      act_lines (iterable of string): the lines to be matched.

      source (string): Source from where the lines were obtained, e.g.
        'stdout' or 'stderr'.

      desc (string): Testcase description.
    """
    assert len(act_lines) == len(exp_lines), \
        f"Unexpected number of lines on {source} in test:\n" \
        f"{desc}\n" \
        f"Expected lines cnt={len(exp_lines)}:\n" \
        "------------\n" \
        f"{EOL.join(exp_lines)}\n" \
        "------------\n" \
        f"Actual lines cnt={len(act_lines)}:\n" \
        "------------\n" \
        f"{EOL.join(act_lines)}\n" \
        "------------\n"

    for i, act_line in enumerate(act_lines):
        exp_line = exp_lines[i]
        assert exp_line == act_line, \
            f"Unexpected line #{i} on {source} in test:\n" \
            f"{desc}\n" \
            "Expected line:\n" \
            "------------\n" \
            f"{exp_line}\n" \
            "------------\n" \
            "Actual line:\n" \
            "------------\n" \
            f"{act_line}\n" \
            "------------\n"


class captured_output:
    # pylint: disable=invalid-name
    """
    Context manager that captures any data written to sys.stdout and sys.stderr
    during execution of its body. The data can be obtained via the attributes
    'stdout' and 'stderr'.

    Example:

        with captured_output() as captured:
            print("Hello stdout")
            print("Hello stderr", file=sys.stderr)
        print(captured.stdout)  # Prints 'Hello stdout'
        print(captured.stderr)  # Prints 'Hello stderr'
    """

    # pylint: disable=attribute-defined-outside-init

    def __enter__(self):
        self._saved_stdout = sys.stdout
        sys.stdout = self._iobuf_stdout = StringIO()
        self.stdout = None
        self._saved_stderr = sys.stderr
        sys.stderr = self._iobuf_stderr = StringIO()
        self.stderr = None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stdout = self._iobuf_stdout.getvalue()
        self._iobuf_stdout.close()
        sys.stdout = self._saved_stdout
        self.stderr = self._iobuf_stderr.getvalue()
        self._iobuf_stderr.close()
        sys.stderr = self._saved_stderr
        return False  # re-raise any exceptions

    # pylint: enable=attribute-defined-outside-init
