"""
Pytest common fixtures
"""

from __future__ import absolute_import, print_function
import os
import pytest

from pywbemtools._utils import CONNECTIONS_FILENAME, \
    DEFAULT_CONNECTIONS_DIR, DEFAULT_CONNECTIONS_FILE

SCRIPT_DIR = os.path.dirname(__file__)

# Backup file of the default connections file
BAK_SUFFIX = '.bak'
CONNECTIONS_BAK_FILENAME = CONNECTIONS_FILENAME + BAK_SUFFIX
CONNECTIONS_BAK_FILE = os.path.join(DEFAULT_CONNECTIONS_DIR,
                                    CONNECTIONS_BAK_FILENAME)

# Save files for the default connections file and its backup file
SAVE_SUFFIX = '.testsavepywbemclitests'
CONNECTIONS_SAVE_FILENAME = CONNECTIONS_FILENAME + SAVE_SUFFIX
CONNECTIONS_SAVE_FILE = os.path.join(DEFAULT_CONNECTIONS_DIR,
                                     CONNECTIONS_SAVE_FILENAME)
CONNECTIONS_BAK_SAVE_FILENAME = CONNECTIONS_BAK_FILENAME + SAVE_SUFFIX
CONNECTIONS_BAK_SAVE_FILE = os.path.join(DEFAULT_CONNECTIONS_DIR,
                                         CONNECTIONS_BAK_SAVE_FILENAME)


@pytest.fixture
def default_connections_file_path():
    """
    Fixture to return the path name of the default connections file.
    """
    return DEFAULT_CONNECTIONS_FILE


@pytest.fixture(scope='session', autouse=True)
def save_default_connections_file(request):
    """
    Fixture that saves away an existing default connections file and its backup
    file at the begin of a test session and restores them at the end of the
    test session.

    This function is called once per test session (i.e. execution of the pytest
    command) before the first test is executed.
    """

    # Save the default connections file and its backup file
    if os.path.isfile(DEFAULT_CONNECTIONS_FILE):
        os.rename(DEFAULT_CONNECTIONS_FILE, CONNECTIONS_SAVE_FILE)
    if os.path.isfile(CONNECTIONS_BAK_FILE):
        os.rename(CONNECTIONS_BAK_FILE, CONNECTIONS_BAK_SAVE_FILE)

    def teardown():
        """
        Restore the saved default connections file and its saved backup
        file.

        This function is called once per test session (i.e. execution of the
        pytest command) after the last test has been executed.
        """

        # Restore the saved default connections file
        if os.path.isfile(DEFAULT_CONNECTIONS_FILE):
            os.remove(DEFAULT_CONNECTIONS_FILE)
        if os.path.isfile(CONNECTIONS_SAVE_FILE):
            os.rename(CONNECTIONS_SAVE_FILE, DEFAULT_CONNECTIONS_FILE)

        # Restore the saved backup file of the default connections file
        if os.path.isfile(CONNECTIONS_BAK_FILE):
            os.remove(CONNECTIONS_BAK_FILE)
        if os.path.isfile(CONNECTIONS_BAK_SAVE_FILE):
            os.rename(CONNECTIONS_BAK_SAVE_FILE, CONNECTIONS_BAK_FILE)

    request.addfinalizer(teardown)
