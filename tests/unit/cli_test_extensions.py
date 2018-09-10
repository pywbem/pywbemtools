"""
The class in this file defines a common base for the pytests executed
through pywbemcli execution

"""

from __future__ import absolute_import, print_function
import re
import pytest
import os
import six

from .utils import execute_pywbemcli, assert_rc, assert_patterns, assert_lines

TEST_DIR = os.path.dirname(__file__)


class CLITestsBase(object):
    """
        Defines methods to execute tests on pywbemcli

    """
    def mock_subcmd_test(self, desc, subcmd, args, env, exp_response,
                         mock_file, condition):
        # pylint: disable=line-too-long
        """
        Test method to execute test on pywbemcli by calling the executable
        pywbemcli for the command defined by subcmd with arguments defined
        by args. This can execute pywbemcli either with a mock environment
        by using the mock_file variable or without mock if the mock_file
        parameter is None. The method tests the results of the execution
        of pywbemcli using the exp_response parameter.

        Parameters:
          desc (:term:`string`):
            Description of the test

          subcmd (:term:`string`):
            pywbemcli subcommand inserted for this test.  This is the first
            level subcommand (ex. class).

          args (:class:`py:dict` or :class:`py:list` of :term:`string` or :term:`string`):

            If it is a dictionary, arguments to be inserted into the command
            line both as local (after the subcommand name) and global (before
            the subcommand name) options may be defined. The dictionary may
            contain two possible key keys:

              * args: defines local aruments to append to the command after
                    the subcommand name

              * globals: defines global arguments that will be inserted
                  into the command line before the subcommand name.

            If args is a list or string it is the set of arguments to append
            after the subcommand name

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
                 string is is split into lines separated at each new line
                 before the match

                 'patterns' - Expected response must be same as lines test
                 except that each line in the expected response is treated as
                 a regex expression and a regex match is executed for each line.

                 'regex' - Expected response is a single string or list of
                 strings. Each string is considered a regex expression.

                 'in' - Expected response is string or list of strings.
                 Tests the complete response to determine if each entry
                 in expected response is in the response data as a single test.

                 Executes a single regex search of the entire
                 response data to match with each entry in the expected
                 response

               'rc' expected exit_code from pywbemcli.  If None, code 0
               is expected.

          mock_file (:term:`string` or None):
            If this is a string, this test will be executed using the
            --mock-server pywbemcl option with this file as the name of the
            objects to be compiled or executed. This should be just a file name
            and this method assumes the file is in the tests/unit directory.

            If it is a list, the same rules apply to each entry in the list.


            If None, test is executed without the --mock-server input parameter
            and defines an artificial server name  Used to test subcommands
            and options that do not communicate with a server.  It is faster
            than installing the mock repository

          condition (None or False):
            If False, the test is skipped
        """  # noqa: E501
        # pylint: enable=line-too-long

        if not condition:
            pytest.skip("Condition for test case %s not met" % desc)

        global_args = []
        local_args = []
        if isinstance(args, dict):
            global_args = args.get("global", None)
            local_args = args.get("args", None)
        elif isinstance(args, six.string_types):
            local_args = args.split(" ")
        elif isinstance(args, (list, tuple)):
            local_args = args
        else:
            assert 'Invalid args input to test %r . Allowed types are dict, ' \
                   'string, list, tuple.' % args

        if isinstance(local_args, six.string_types):
            local_args = local_args.split(" ")

        if isinstance(global_args, six.string_types):
            global_args = global_args.split(" ")

        cmd_line = ['-s', 'http:/blah']
        if global_args:
            cmd_line.extend(global_args)

        if mock_file:
            if isinstance(mock_file, (list, tuple)):
                for item in mock_file:
                    cmd_line.extend(['--mock-server',
                                     os.path.join(TEST_DIR, item)])
            elif isinstance(mock_file, six.string_types):
                cmd_line.extend(['--mock-server',
                                 os.path.join(TEST_DIR, mock_file)])
            else:
                assert("CLI_TEST_EXTENSIONS mock_file %s invalid" % mock_file)

        cmd_line.append(subcmd)

        if local_args:
            cmd_line.extend(local_args)

        # print('\nCMDLINE %s' % cmd_line)

        rc, stdout, stderr = execute_pywbemcli(cmd_line)

        exp_rc = exp_response['rc'] if 'rc' in exp_response else 0
        assert_rc(exp_rc, rc, stdout, stderr)

        test_value = None
        component = None
        if 'stdout' in exp_response:
            test_value = exp_response['stdout']
            rtn_value = stdout
            component = 'stdout'
        elif 'stderr' in exp_response:
            test_value = exp_response['stderr']
            rtn_value = stderr
            component = 'stderr'
        else:
            assert False, 'Expected "stdout" or "stderr" key. One of these ' \
                          'keys required in exp_response.'

        if test_value:
            if 'test' in exp_response:
                test = exp_response['test']
                # test that rtn_value starts with test_value
                if test == 'startswith':
                    assert isinstance(test_value, six.string_types)
                    assert rtn_value.startswith(test_value), \
                        "{}\n{}={!r}".format(desc, component, rtn_value)
                # test that lines match between test_value and rtn_value
                # base on regex match
                elif test == 'patterns':
                    if isinstance(test_value, six.string_types):
                        test_value = test_value.splitlines()
                    assert isinstance(test_value, (list, tuple))
                    assert_patterns(test_value, rtn_value.splitlines(),
                                    "{}\n{}={!r}".format(desc, component,
                                                         rtn_value))
                # test that each line in the test value matches the
                # corresponding line in the rtn_value exactly
                elif test == 'lines':
                    if isinstance(test_value, six.string_types):
                        test_value = test_value.splitlines()
                    if isinstance(test_value, (list, tuple)):
                        assert_lines(test_value, rtn_value.splitlines(),
                                     "{}\n{}={!r}".format(desc, component,
                                                          rtn_value))
                    else:
                        assert(isinstance(test_value, six.string_types))
                        assert_lines(test_value.splitlines(),
                                     rtn_value.splitlines(),
                                     "{}\n{}={!r}".format(desc, component,
                                                          rtn_value))
                # test with a regex search that all values in list exist in
                # the return
                elif test == 'regex':
                    if isinstance(test_value, (tuple, list)):
                        rtn_value = rtn_value.join("\n")
                    elif isinstance(test_value, six.string_types):
                        rtn_value = [rtn_value]
                    else:
                        assert False, "regex expected response must be string" \
                                      "or list of strings. %s found" % \
                                      type(rtn_value)

                    for regex in test_value:
                        assert isinstance(regex, six.string_types)
                        match_result = re.search(regex, rtn_value)
                        assert not match_result, \
                            "{}\n{}={!r}".format(desc, re, rtn_value)
                elif test == 'in':
                    if isinstance(test_value, six.string_types):
                        test_value = [test_value]
                    for test_str in test_value:
                        assert test_str in rtn_value, \
                            "{}\n{}={!r}".format(desc, test_str, rtn_value)
                else:
                    assert 'test %s is invalid. Skipped' % test
