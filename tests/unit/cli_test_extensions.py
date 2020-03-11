"""
The class in this file defines a common base for the pytests executed
through pywbemcli execution

"""

from __future__ import absolute_import, print_function
import re
import os
import pytest
import six

from .utils import execute_pywbemcli, assert_rc, assert_patterns, assert_lines

TEST_DIR = os.path.dirname(__file__)


class CLITestsBase(object):
    # pylint: disable=too-few-public-methods, useless-object-inheritance
    """
        Defines methods to execute tests on pywbemcli.

    """
    def command_test(self, desc, command_grp, inputs, exp_response, mock_files,
                     condition, verbose=None):
        # pylint: disable=line-too-long, no-self-use
        """
        Test method to execute test on pywbemcli by calling the executable
        pywbemcli for the command defined by command with arguments defined
        by args. This can execute pywbemcli either with a mock environment
        by using the mock_files variable or without mock if the mock_files
        parameter is None. The method tests the results of the execution
        of pywbemcli using the exp_response parameter.

        Parameters:
          desc (:term:`string`):
            Description of the test

          command_grp (:term:`string`):
            pywbemcli command_grp definedfor this test.  This is the first
            level of the command(the command group) (ex. class).

          inputs (:class:`py:dict` or :class:`py:list` of :term:`string` or :term:`string`):

            If inputs is a list of strings, it contains the command
            line arguments, without the command name.

            Each single argument must be its own item in the iterable; combining
            the arguments into a string does not work.
            The arguments may be binary strings encoded in UTF-8, or unicode
            strings.

            If inputs is a dict it can contain the following possible keys:

              * 'args': defines local arguments to append to the command after
                  the command name. Each single argument must be its own
                  item in the iterable.

              * 'general': defines general arguments that will be inserted
                  into the command line before the command name. Each
                  single argument must be its own item in the iterable.

              * 'env': Dictionary of environment variables where  key is the
                variable name as a :term:`string`; dict value is the variable
                value as a :term:`string` (without any shell escaping needed).
                If None, no environment variables are set for the test.

              * 'stdin': If the key is `stdin`, the value is either a string or
                list of strings. If `stdin` is a list or tuple of strings, each
                string defines a line of text that will be included as stdin to
                the call to pywbemcli. The iterable is mapped to a single string
                with each line separated by an EOL char. This becomes the stdin
                parameter for the call to pywbemcli. Each line is processed
                as a separate repl line by the pybemcli executable.
                If `stdin` is a single string it is passed  to the stdin
                parameter for the call to pywbemcli. If `stdin` is defined, the
                parameters defining a command to be executed are ignored and
                the full command must be in the `stdin` iterable.

                If None, no stdin input is defined for the test.

          exp_response (:class:`py:dict`)

            Keyword arguments for expected response.

            Includes the following possible keys:

               'stdout' or 'stderr' - Defines which return is expected (the
               expected response). The value is a string or iterable defining
               the data expected in the response. The data definition in
               this dictionary entry must be compatible with the definition
               of expected data for the test selected.
               Only one of these keys may exist.

               'test' - If it exists defines the test used to compare the
               returned data with the expected returned data defined as the
               value of 'stdout'/'stderr'.

               The tests define are:

                 'startswith' - Expected Response must be a single string
                 The returned text defined starts with the defined string

                 'lines' -  Expected response may be either a list of strings or
                 single string

                 Compares for exact match between the expected response and the
                 returned data line by line. The number of lines and the data
                 in each line must match.  If the expected response is a single
                 string it is split into lines separated at each new line
                 before the match

                 'linesnows' - Expected response may be either list of strings
                 or single string. Compares as with lines except that all
                 whitespace is removed from the strings before the compare.

                 'patterns' - Expected response must be same as lines test
                 except that each line in the expected response is treated as
                 a regex expression and a regex match is executed for each line.

                 'regex' - Expected response is a single string or list of
                 strings. Each string is considered a regex expression. The
                 regex expression is tested against each line in the output
                 using regex search. All strings in the expected response must
                 be found in actual response to pass the test

                 'in' - Expected response is string or list of strings.
                 Tests the complete response line by line to determine if each
                 entry in expected response is in the response data as a single
                 test.

                 'innows' - Like 'in, except that differences in whitespace are
                 ignored.

                 Executes a single regex search of the entire
                 response data to match with each entry in the expected
                 response

               'rc' expected exit_code from pywbemcli.  If None, code 0
               is expected.

          mock_files (:term:`string` or list of string or None):
            If this is a string, this test will be executed using the
            --mock-server pywbemcl option with this file as the name of the
            objects to be compiled or executed. This should be just a file name
            and this method assumes the file is in the tests/unit directory.

            If it is a list, the same rules apply to each entry in the list.

            If None, test is executed without the --mock-server input parameter
            and defines an artificial server name  Used to test commands
            and options that do not communicate with a server.  It is faster
            than installing the mock repository

          condition (True, False, or 'pdb'):
            If True, the test is executed.
            If False, the test is skipped.
            If 'pdb', the test breaks in the debugger.

          verbose (:class:`py:bool`):
            If `True` the assembled command line will be displayed
        """  # noqa: E501
        # pylint: enable=line-too-long

        if not condition:
            pytest.skip("Condition for test case %s not met" % desc)

        env = None
        stdin = None
        if isinstance(inputs, dict):
            general_args = inputs.get("general", None)
            local_args = inputs.get("args", None)
            env = inputs.get("env", None)
            stdin = inputs.get('stdin', None)
            if stdin:
                if isinstance(stdin, (tuple, list)):
                    stdin = '\n'.join(stdin)
        elif isinstance(inputs, six.string_types):
            local_args = inputs.split(" ")
            general_args = None
        elif isinstance(inputs, (list, tuple)):
            local_args = inputs
            general_args = None
        else:
            assert 'Invalid inputs param to test %r . Allowed types are ' \
                   'dict, string, list, tuple.' % inputs

        if isinstance(local_args, six.string_types):
            local_args = local_args.split(" ")

        if isinstance(general_args, six.string_types):
            general_args = general_args.split(" ")

        cmd_line = []
        if general_args:
            cmd_line.extend(general_args)

        if mock_files:
            if isinstance(mock_files, (list, tuple)):
                for item in mock_files:
                    cmd_line.extend(['--mock-server',
                                     os.path.join(TEST_DIR, item)])
            elif isinstance(mock_files, six.string_types):
                cmd_line.extend(['--mock-server',
                                 os.path.join(TEST_DIR, mock_files)])
            else:
                assert("CLI_TEST_EXTENSIONS mock_file %s invalid" % mock_files)

        if not stdin:
            cmd_line.append(command_grp)

        if local_args:
            cmd_line.extend(local_args)

        if condition == 'pdb':
            cmd_line.append('--pdb')

        if verbose:
            print('\nCMDLINE: %s' % cmd_line)

        if verbose and env:
            print('ENV: %s' % env)

        rc, stdout, stderr = execute_pywbemcli(cmd_line, env=env, stdin=stdin,
                                               verbose=verbose)

        exp_rc = exp_response['rc'] if 'rc' in exp_response else 0
        assert_rc(exp_rc, rc, stdout, stderr, desc)

        if verbose:
            print('RC=%s\nSTDOUT=%s\nSTDERR=%s' % (rc, stdout, stderr))

        if exp_response['test']:
            test_definition = exp_response['test']
        else:
            test_definition = None

        if 'stdout' in exp_response:
            test_value = exp_response['stdout']
            rtn_value = stdout
            rtn_type = 'stdout'
        elif 'stderr' in exp_response:
            test_value = exp_response['stderr']
            rtn_value = stderr
            rtn_type = 'stderr'
        else:
            assert False, 'Expected "stdout" or "stderr" key. One of these ' \
                          'keys required in exp_response.'

        if test_definition:
            if 'test' in exp_response:
                test_definition = exp_response['test']
                # test that rtn_value starts with test_value
                if test_definition == 'startswith':
                    assert isinstance(test_value, six.string_types)
                    assert rtn_value.startswith(test_value), \
                        "Unexpected start of line on {} in test:\n" \
                        "{}\n" \
                        "Expected start of line:\n" \
                        "------------\n" \
                        "{}\n" \
                        "------------\n" \
                        "Actual output line(s):\n" \
                        "------------\n" \
                        "{}\n" \
                        "------------\n". \
                        format(rtn_type, desc, test_value, rtn_value)
                # test that lines match between test_value and rtn_value
                # base on regex match
                elif test_definition == 'patterns':
                    if isinstance(test_value, six.string_types):
                        test_value = test_value.splitlines()
                    assert isinstance(test_value, (list, tuple))
                    assert_patterns(test_value, rtn_value.splitlines(),
                                    rtn_type, desc)
                # test that each line in the test value matches the
                # corresponding line in the rtn_value exactly
                elif test_definition == 'lines':
                    if isinstance(test_value, six.string_types):
                        test_value = test_value.splitlines()
                    if isinstance(test_value, (list, tuple)):
                        assert_lines(test_value, rtn_value.splitlines(),
                                     rtn_type, desc)
                    else:
                        assert(isinstance(test_value, six.string_types))
                        assert_lines(test_value.splitlines(),
                                     rtn_value.splitlines(),
                                     rtn_type, desc)
                # compress test_value and rtn_value into whitespace single
                # strings and assert_lines.
                elif test_definition == 'linesnows':
                    assert_lines([remove_ws(test_value)],
                                 [remove_ws(rtn_value)],
                                 rtn_type, desc)

                # test with a regex search that all values in list exist in
                # the return. Build rtn_value into single string and do
                # re.search against it for each test_value
                elif test_definition == 'regex':
                    assert isinstance(rtn_value, six.string_types)
                    if isinstance(test_value, six.string_types):
                        test_value = [test_value]
                    for regex in test_value:
                        assert isinstance(regex, six.string_types)
                        match_result = re.search(regex, rtn_value, re.MULTILINE)
                        assert match_result, \
                            "Missing pattern on {} in test:\n" \
                            "{}\n" \
                            "Expected pattern in any line:\n" \
                            "------------\n" \
                            "{}\n" \
                            "------------\n" \
                            "Actual output line(s):\n" \
                            "------------\n" \
                            "{}\n" \
                            "------------\n". \
                            format(rtn_type, desc, regex, rtn_value)
                elif test_definition == 'in':
                    if isinstance(test_value, six.string_types):
                        test_value = [test_value]
                    for test_str in test_value:
                        assert test_str in rtn_value, \
                            "Missing in-string on {} in test:\n" \
                            "{}\n" \
                            "Expected in-string in any line:\n" \
                            "------------\n" \
                            "{}\n" \
                            "------------\n" \
                            "Actual output line(s):\n" \
                            "------------\n" \
                            "{}\n" \
                            "------------\n". \
                            format(rtn_type, desc, test_str, rtn_value)
                elif test_definition == 'innows':
                    if isinstance(test_value, six.string_types):
                        test_value = [test_value]
                    for test_str in test_value:
                        assert remove_ws(test_str) in remove_ws(rtn_value), \
                            "Missing ws-agnostic in-string on {} in test:\n" \
                            "{}\n" \
                            "Expected ws-agnostic in-string in any line:\n" \
                            "------------\n" \
                            "{}\n" \
                            "------------\n" \
                            "Actual output line(s):\n" \
                            "------------\n" \
                            "{}\n" \
                            "------------\n". \
                            format(rtn_type, desc, test_str, rtn_value)
                elif test_definition == 'not-innows':
                    if isinstance(test_value, six.string_types):
                        test_value = [test_value]
                    for test_str in test_value:
                        assert remove_ws(test_str) not in \
                            remove_ws(rtn_value), \
                            "Unexpected ws-agnostic in-string on {} in test:\n"\
                            "{}\n" \
                            "Unexpected ws-agnostic in-string in any line:\n" \
                            "------------\n" \
                            "{}\n" \
                            "------------\n" \
                            "Actual output line(s):\n" \
                            "------------\n" \
                            "{}\n" \
                            "------------\n". \
                            format(rtn_type, desc, test_str, rtn_value)
                else:
                    assert 'test %s is invalid. Skipped' % test_definition


def remove_ws(inputs):
    """
    Remove all whitespace from a tuple or list of strings or a single
    string and return the result as a single string. Whitespace is
    defined as spaces, tabs, newlines
    """
    if isinstance(inputs, (tuple, list)):
        inputs = "".join(inputs)

    # return inputs.replace(" ", "").replace("\t", "").replace("\n", "")
    return re.sub(r"\s", "", inputs)
