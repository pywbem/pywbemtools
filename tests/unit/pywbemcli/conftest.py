"""
Pytest common fixtures
"""

import os
import shutil
import pytest

# from pywbemtools._utils import debug_log
from pywbemtools.pywbemcli._connection_file_names import \
    DEFAULT_CONNECTIONS_DIR, PYWBEMCLI_ALT_HOME_DIR_ENVVAR


@pytest.fixture(scope='session', autouse=True)
def cleanup_connections_dirs(request):
    """
    Fixture that removes existing default connections file, its backup and
    the mock cache at beginning of module test and removes the complete
    test connections file directory at end of session test.

    This function is called once per test session (i.e. execution of the pytest
    command on a file) before the first test is executed.
    """
    # validate that test env var exists and get connection files directory
    test_dir_path = os.getenv(PYWBEMCLI_ALT_HOME_DIR_ENVVAR)
    if test_dir_path is None:
        pytest.fail(f"Env var {PYWBEMCLI_ALT_HOME_DIR_ENVVAR} not set.")

    # remove any files in the this directory before test
    if os.path.exists(test_dir_path):
        shutil.rmtree(DEFAULT_CONNECTIONS_DIR)
        os.mkdir(DEFAULT_CONNECTIONS_DIR)

    def cleanup():
        """
        Remove the test connections directory and files at end of the test.
        """
        if os.path.exists(test_dir_path):
            shutil.rmtree(DEFAULT_CONNECTIONS_DIR)

    request.addfinalizer(cleanup)


@pytest.fixture(scope='module', autouse=True)
def cleanup_connections_files(request):
    """
    Removes existing default connections file its backup file and mock cache at
    the begining of a module test and at the end of the module test.

    Called once per test module (i.e. execution of the pytest
    command on a file) before the first test of the sessuib is executed.
    """

    test_dir_path = os.getenv(PYWBEMCLI_ALT_HOME_DIR_ENVVAR)

    if test_dir_path is None:
        pytest.fail(f"Env var {PYWBEMCLI_ALT_HOME_DIR_ENVVAR} not set.")

    # remove any files in the this directory before test
    if os.path.exists(test_dir_path):
        shutil.rmtree(DEFAULT_CONNECTIONS_DIR)
        os.mkdir(DEFAULT_CONNECTIONS_DIR)

    def cleanup():
        """
        Remove the test connections files at end of the test.  Called at end
        of tests for each module
        """
        if os.path.exists(test_dir_path):
            shutil.rmtree(DEFAULT_CONNECTIONS_DIR)
            os.mkdir(DEFAULT_CONNECTIONS_DIR)

    request.addfinalizer(cleanup)
