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
Utilities to exercise pywbemcli both as a separate executable and in line with
a direct call.
"""

from __future__ import absolute_import, print_function

import os
import sys
import re
try:
    from StringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO  # Python 3
from copy import copy
from subprocess import Popen, PIPE
import packaging.version
import click
import six

# Click issue #1231:
# On Windows, the Click package has the issue that it writes '\n' at the Python
# level as '\r\r\n' at the level of the Windows shell, and Popen() with
# universal_newlines=True does not handle this case.
# To circumvent that issue, pywbemtools specifies universal_newlines=False and
# performs the universal newline conversions itself (it does what Popen() does,
# and in addition replaces the incorrectly created '\r\r\n' sequence).
# That issue has been fixed in Click 7.1 on Python 3, but Click 7.1 has also
# removed support for Python 3.4 so pywbemtools now requires Click 7.1 where
# possible and still needs the circumvention code for Python 2.7 and 3.4 on
# Windows.
# The CLICK_ISSUE_1231 boolean indicates that the Click issue is present.
CLICK_VERSION = packaging.version.parse(click.__version__)
CLICK_ISSUE_1231 = sys.version_info[0:2] <= (3, 4) and sys.platform == 'win32'


def execute_pywbemcli(args, env=None, stdin=None, verbose=None, condition=True):
    """
    Invoke the 'pywbemcli' command as a child process.

    This requires that the 'pywbemcli' command is installed in the current
    Python environment.

    Parameters:

      args (iterable of :term:`string`): Command line arguments and subcommand,
        without the command name.
        Each single argument must be its own item in the iterable; combining
        the arguments into a string does not work.
        The arguments may be binary strings, encoded in UTF-8, or unicode
        strings.

      env (dict): Environment variables to be put into the environment when
        calling the command. May be `None`. Dict key is the variable name as a
        :term:`string`; dict value is the variable value as a :term:`string`
        (without any shell escaping needed).

      stdin (:term:`string` or None):
        Passed to the executable as stdin.

      verbose (bool):
        If True, display args, env, and stdin before executing the command

      condition ('pdb', other values):
        If 'pdb', the test breaks in the debugger before invoking the command.

    Returns:

      tuple(rc, stdout, stderr): Output of the command, where:

        * rc(int): Exit code of the command.
        * stdout(:term:`unicode string`): Standard output of the command,
          as a unicode string with newlines represented as '\\n'.
          Returns empty string, if there was no data.
        * stderr(:term:`unicode string`): Standard error of the command,
          as a unicode string with newlines represented as '\\n'.
          Returns empty string, if there was no data.
    """
    cli_cmd = u'pywbemcli'

    if env is None:
        env = {}
    else:
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

    if verbose:
        display_envvars = '\n'.join(
            ['{}={}'.format(var, os.environ[var])
             for var in os.environ if 'PYWBEMCLI' in var])
        print('PYWBEMCLI env vars:\n{}'.format(display_envvars))

    assert isinstance(args, (list, tuple))
    cmd_args = [cli_cmd]
    for arg in args:
        if not isinstance(arg, six.text_type):
            arg = arg.decode('utf-8')
        cmd_args.append(arg)

    if verbose:
        print('\nexecute_pywbemcli CMD_ARGS {}'.format(cmd_args))

    if verbose and stdin:
        print('stdin {}'.format(stdin))

    if condition == 'pdb':
        stdin_stream = None
        stdout_stream = None
        stderr_stream = None
    else:
        stdin_stream = PIPE
        stdout_stream = PIPE
        stderr_stream = PIPE

    if CLICK_ISSUE_1231:
        universal_newlines = False
        if stdin and six.PY3:
            stdin = stdin.encode('utf-8')
    else:
        universal_newlines = True

    # pylint: disable=consider-using-with
    proc = Popen(cmd_args, shell=False, stdin=stdin_stream,
                 stdout=stdout_stream, stderr=stderr_stream,
                 universal_newlines=universal_newlines)

    stdout_str, stderr_str = proc.communicate(input=stdin)
    rc = proc.returncode

    # Restore environment of current process
    for name, value in saved_env.items():
        if value is None:
            del os.environ[name]
        else:
            os.environ[name] = value

    if verbose:
        print('output type {}\nstdout:{!r}\nstderr:{!r}'
              .format(type(stdout_str), stdout_str, stderr_str))

    if isinstance(stdout_str, six.binary_type):
        stdout_str = stdout_str.decode('utf-8')
    if isinstance(stderr_str, six.binary_type):
        stderr_str = stderr_str.decode('utf-8')

    if CLICK_ISSUE_1231:
        stdout_str = stdout_str.replace('\r\r\n', '\n')  \
                               .replace('\r\n', '\n')  \
                               .replace('\r', '')
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
        "{}\n" \
        "Expected rc: {}\n" \
        "Actual rc: {}\n" \
        "Stdout:\n" \
        "------------\n" \
        "{}\n" \
        "------------\n" \
        "Stderr:\n" \
        "------------\n" \
        "{}\n" \
        "------------\n". \
        format(desc, exp_rc, rc, stdout, stderr)


def assert_patterns(exp_patterns, act_lines, source, desc):
    """
    Assert that the specified lines match the specified patterns.

    The patterns are matched against the complete line from begin to end,
    even if no begin and end markers are specified in the patterns.

    Parameters:

      exp_patterns (iterable of string): regexp patterns defining the expected
        value for each line.

      act_lines (iterable of string): the lines to be matched.

      source (string): Source from where the lines were obtained, e.g.
        'stdout' or 'stderr'.

      desc (string): Testcase description.
    """
    assert len(act_lines) == len(exp_patterns), \
        "Unexpected number of lines on {} in test:\n" \
        "{}\n" \
        "Expected lines (cnt={}):\n" \
        "------------\n" \
        "{}\n" \
        "------------\n" \
        "Actual lines (cnt={}):\n" \
        "------------\n" \
        "{}\n" \
        "------------\n". \
        format(source, desc, len(act_lines), '\n'.join(act_lines),
               len(exp_patterns), '\n'.join(exp_patterns))

    for i, act_line in enumerate(act_lines):
        exp_line = exp_patterns[i]
        # if not exp_line.endswith('$'):
        #    exp_line += '$'
        assert re.match(exp_line, act_line), \
            "Unexpected line #{} on {} in test:\n" \
            "{}\n" \
            "Expected line:\n" \
            "------------\n" \
            "{}\n" \
            "------------\n" \
            "Actual line:\n" \
            "------------\n" \
            "{}\n" \
            "------------\n". \
            format(i, source, desc, exp_line, act_line)


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
        "Unexpected number of lines on {} in test:\n" \
        "{}\n" \
        "Expected lines cnt={}:\n" \
        "------------\n" \
        "{}\n" \
        "------------\n" \
        "Actual lines cnt={}:\n" \
        "------------\n" \
        "{}\n" \
        "------------\n". \
        format(source, desc, len(exp_lines), '\n'.join(exp_lines),
               len(act_lines), '\n'.join(act_lines))

    for i, act_line in enumerate(act_lines):
        exp_line = exp_lines[i]
        assert exp_line == act_line, \
            "Unexpected line #{} on {} in test:\n" \
            "{}\n" \
            "Expected line:\n" \
            "------------\n" \
            "{}\n" \
            "------------\n" \
            "Actual line:\n" \
            "------------\n" \
            "{}\n" \
            "------------\n". \
            format(i, source, desc, exp_line, act_line)


class captured_output(object):
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
