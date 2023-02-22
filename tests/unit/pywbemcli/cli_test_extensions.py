"""
The class in this file defines a common base for the pytests executed
through pywbemcli execution

"""

from __future__ import absolute_import, print_function
import re
import os
import io
from contextlib import contextmanager
import yaml
import pytest
import six

# import pkgs to determine pywbem version
import packaging.version
import pywbem
from pywbem_mock import FakedWBEMConnection

from ..utils import execute_command, assert_rc, assert_patterns, assert_lines

TEST_DIR = os.path.dirname(__file__)

# Boolean Variable that can be in individual tests to determine tests are to
# be executed.  Returns True if the pywbem >=1.0.0 is use. Otherwise returns
# False. These variables can be applied to tests that are specific to one
# version of pywbem or the other
PYWBEM_VERSION = packaging.version.parse(pywbem.__version__)
PYWBEM_1 = PYWBEM_VERSION.release >= (1, 0, 0)
PYWBEM_0 = not PYWBEM_1


# This variable defines the url returned from some of the commands.  Since it
# is changed with pywbem 1.0.0 to include the port number, we must dynamically
# create it for the tests depending on pywbem version
FAKEURL_STR = '//FakedUrl:5988' if PYWBEM_1 else '//FakedUrl'


class CLITestsBase(object):
    # pylint: disable=too-few-public-methods, useless-object-inheritance
    """
        Defines methods to execute tests on pywbemcli.

    """
    def command_test(self, desc, command_grp, inputs, exp_response, mock_files,
                     condition, verbose=False):
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

          command_grp (:term:`string` or None):
            Pywbemcli command group for this test. This is the first level of
            the command, e.g. 'class' or 'instance'.

          inputs (:term:`string` or tuple/list of :term:`string` or :class:`py:dict`):

            * If inputs is a string or a tuple/list of strings, it contains the
              command line arguments, without the command name or command group.

              Each single argument must be its own item in the iterable;
              combining the arguments into a string does not work, and the
              string is not split into words (anymore).

              The arguments may be binary strings encoded in UTF-8, or unicode
              strings.

            * If inputs is a dict it can contain the following optional items:

              - 'connections_file_args': tuple(conn_file, conn_content) that can
                specify a connections file to be prepared for the test.
                The tuple items are passed as arguments to the
                'connections_file()' context manager. See there for details.

              - 'args': String or tuple/list of strings with local
                (command-level) options that will be added to the command
                line after the command name.

                Each single argument (e.g. option name and option arguments)
                must be its own item in the iterable.

              - 'general': String or tuple/list of strings with general
                options that will be added to the command line before the
                command name.

                Each single argument (e.g. option name and option arguments)
                must be its own item in the iterable.

              - 'env': Dictionary of environment variables where key is the
                variable name; dict value is the variable value (without any
                shell escaping needed).

                If omitted, None, or empty, no environment variables will be
                set for the test.

              - 'stdin': A string or a tuple/list of strings, that contains the
                standard input for the command.

                This can be used for commands in interactive mode, and for
                responding to prompts.

                If present, the command group specified in the `command_grp`
                parameter is not added to the command line, but the local and
                global options are added.

                If specified as a tuple/list of strings, these strings are
                joined into a single string separated by an EOL char. Each line
                is processed as a separate repl line or prompt input by
                pybemcli.

                If omitted or None, no standard input will be provided to the
                pywbemcli command.

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

          condition (True, False, 'pdb', or 'verbose'):
            If True, the test is executed.
            If False, the test is skipped.
            If 'pdb', the test breaks in the debugger.
            If 'verbose', verbose mode is enabled for the test.

          verbose (:class:`py:bool`):
            If True, verbose mode is enabled for the test.

            In verbose mode, the assembled command line, the environment
            variables set by 'env', and other details will be displayed.
        """  # noqa: E501
        # pylint: enable=line-too-long

        if not condition:
            pytest.skip('Condition for test case {} not met'.format(desc))

        env = None
        stdin = None
        general_args = None
        connections_file_args = (None, None)
        if isinstance(inputs, dict):
            connections_file_args = inputs.get(
                "connections_file_args", (None, None))
            general_args = inputs.get("general", None)
            local_args = inputs.get("args", None)
            env = inputs.get("env", None)
            stdin = inputs.get('stdin', None)
            if stdin:
                if isinstance(stdin, (tuple, list)):
                    stdin = '\n'.join(stdin)
        elif isinstance(inputs, six.string_types):
            local_args = inputs
        elif isinstance(inputs, (list, tuple)):
            local_args = inputs
        else:
            assert False, 'Invalid inputs param to test {!r}. Allowed types ' \
                'are dict, string, list, tuple.'.format(inputs)

        if stdin and condition == 'pdb':
            assert False, "Condition 'pdb' cannot be used on testcases that " \
                "specify stdin"

        if isinstance(local_args, six.string_types):
            # Is not split into words anymore
            local_args = [local_args]

        if isinstance(general_args, six.string_types):
            # Is not split into words anymore
            general_args = [general_args]

        cmd_line = []

        if condition == 'pdb':
            capture = False
            cmd_line.append('--pdb')
        else:
            capture = True

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
                assert False, \
                    'CLI_TEST_EXTENSIONS mock_file {} invalid' \
                    .format(mock_files)

        if not stdin:
            if command_grp:
                cmd_line.append(command_grp)

        if local_args:
            cmd_line.extend(local_args)

        if not verbose:
            verbose = condition == 'verbose'

        with connections_file(*connections_file_args):
            rc, stdout, stderr = execute_command(
                'pywbemcli', cmd_line, env=env, stdin=stdin, verbose=verbose,
                capture=capture)

        exp_rc = exp_response['rc'] if 'rc' in exp_response else 0
        assert_rc(exp_rc, rc, stdout, stderr, desc)

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
                        assert isinstance(test_value, six.string_types)
                        assert_lines(test_value.splitlines(),
                                     rtn_value.splitlines(),
                                     rtn_type, desc)
                # compress test_value and rtn_value into whitespace single
                # strings and assert_lines.
                elif test_definition == 'linesnows':
                    assert_lines(remove_ws(test_value),
                                 remove_ws(rtn_value),
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
                        assert remove_ws(test_str, join=True) in \
                            remove_ws(rtn_value, join=True), \
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
                        assert remove_ws(test_str, join=True) not in \
                            remove_ws(rtn_value, join=True), \
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
                    raise AssertionError(
                        "Test validation {!r} is invalid in test:\n"
                        "{}\n".format(test_definition, desc))


def remove_ws(inputs, join=False):
    """
    Return the input with whitespace removed and empty lines removed.

    Whitespace is defined as spaces and tabs.

    Parameters:

      inputs: The input, which may be:
        * a single string representing one or more lines.
        * an iterable of strings, each representing one or more lines.

      join (bool): Controls whether the returned list is joined into one line.

    Returns:

      string or list of string: Non-empty lines from the input with whitespace
        removed, as one string if joined, or as a list of strings is not joined.
    """

    if isinstance(inputs, six.string_types):
        inputs = [inputs]

    input_lines = []
    for line in inputs:
        input_lines.extend(line.splitlines())

    ret_lines = []
    for line in input_lines:
        line = re.sub(r"\s", "", line)
        if line:
            ret_lines.append(line)
    if join:
        ret_lines = ''.join(ret_lines)
    return ret_lines


def setup_mock_connection(mock_items, namespace):
    """
    Return FakedWBEMConnection with the specified mock items in the specified
    namespace.

    Parameters:

      mock_items (iterable of mock items): List of mock items to be added
        to the mock environment.

        A mock item can be:
        * string: path name of MOF file to be compiled
        * string: MOF string to be compiled
        * list/tuple: List of CIM objects to be added

      namespace (string): CIM namespace

    Returns:
      FakedWBEMConnection: Mock environment that has been set up.
    """
    conn = FakedWBEMConnection()
    conn.add_namespace(namespace)
    for mock_item in mock_items:
        if isinstance(mock_item, six.string_types):
            if mock_item.endswith('.mof'):
                conn.compile_mof_file(mock_item, namespace=namespace)
            else:
                conn.compile_mof_string(mock_item, namespace=namespace)
        elif isinstance(mock_item, (list, tuple)):
            conn.add_cimobjects(mock_item, namespace=namespace)
    return conn


@contextmanager
def connections_file(conn_file, conn_content):
    """
    Context mannager that creates a connections file upon entry and removes
    it again, and also its backup file, upon exit.

    A previously existing connections file with the same name and its backup
    file will be saved away and restored.

    Parameters:

      conn_file (string or None): Path name of connections file. If None,
        the context manager does nothing on entry or exit.

      content_dict (dict or string or None): Connections file conn_content,
        either as a dictionary that will be converted to a YAML string before
        writing it, or as a YAML string that will be written directly, or None
        which will cause no connections file with the specified name to exist.

    Returns:
      None
    """

    if conn_file is not None:

        bak_suffix = '.bak'
        saved_suffix = '.saved'

        # The backup file of the connections file
        bak_file = conn_file + bak_suffix

        # File names for saving the connections file and its backup file
        saved_conn_file = conn_file + saved_suffix
        saved_bak_file = bak_file + saved_suffix

        # Save the original connections file and its backup file
        if os.path.isfile(conn_file):
            if os.path.isfile(saved_conn_file):
                os.remove(saved_conn_file)
            os.rename(conn_file, saved_conn_file)
        if os.path.isfile(bak_file):
            if os.path.isfile(saved_bak_file):
                os.remove(saved_bak_file)
            os.rename(bak_file, saved_bak_file)

        # Create the new connections file.
        if conn_content is not None:
            with io.open(conn_file, 'w', encoding='utf-8') as fp:
                if isinstance(conn_content, dict):
                    conn_content = yaml.dump(conn_content)
                if isinstance(conn_content, six.binary_type):
                    conn_content = conn_content.decode('utf-8')
                fp.write(conn_content)
                fp.write(u'\n')

    yield None

    if conn_file is not None:

        # Clean up the new connections file and its backup file
        if os.path.isfile(conn_file):
            os.remove(conn_file)
        if os.path.isfile(bak_file):
            os.remove(bak_file)

        # Restore the original connections file and its backup file
        if os.path.isfile(saved_conn_file):
            os.rename(saved_conn_file, conn_file)
        if os.path.isfile(saved_bak_file):
            os.rename(saved_bak_file, bak_file)
