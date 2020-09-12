"""
Pytest common fixtures
"""

from __future__ import absolute_import, print_function
import os
import pytest

from pywbemtools.pywbemcli._utils import CONNECTIONS_FILENAME, \
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
    Fixture to return the path name of the connections file.
    """
    return DEFAULT_CONNECTIONS_FILE


@pytest.fixture(scope='session', autouse=True)
def set_connections_file(request):
    """
    Fixture to hide any existing connection repository at the beginning of a
    session and restore it at the end of the session.  This assumes that the
    connection repository is in the root directory of pywbemcli which is
    logical since that file is defined by the call to pywbemcli in tests.

    This saves and restores any connections file and backup connections file
    in the home directory.

    This fixture should execute once per session (execution of one of the
    test_*.py files) so the load of creating backups and restoring them is
    very low.  In case the fixture fails to restore the backed up connections
    files are saved  with with their full names and the suffix `.testsave`.
    """
    # Save the default connections file and its backup file
    if os.path.isfile(DEFAULT_CONNECTIONS_FILE):
        os.rename(DEFAULT_CONNECTIONS_FILE, CONNECTIONS_SAVE_FILE)
    if os.path.isfile(CONNECTIONS_BAK_FILE):
        os.rename(CONNECTIONS_BAK_FILE, CONNECTIONS_BAK_SAVE_FILE)

    def teardown():
        """
        Remove any created repository file and restore saved file. This
        should occur at session end.
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
