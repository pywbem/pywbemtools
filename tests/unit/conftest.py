"""
Pytest common fixtures
"""

from __future__ import absolute_import, print_function
import os
import pytest

from pywbemtools.pywbemcli._connection_repository \
    import DEFAULT_CONNECTIONS_FILE

SCRIPT_DIR = os.path.dirname(__file__)

DEFAULT_CONNECTION_FILE_DIR = os.path.expanduser("~")
REPO_FILE_PATH = os.path.join(DEFAULT_CONNECTION_FILE_DIR,
                              DEFAULT_CONNECTIONS_FILE)
BACK_FILE = DEFAULT_CONNECTIONS_FILE + '.bak'
REPO_FILE_BACKUP_PATH = os.path.join(DEFAULT_CONNECTION_FILE_DIR,
                                     DEFAULT_CONNECTIONS_FILE)
# if there is a config file or backup, save to this name during tests
SAVE_FILE = DEFAULT_CONNECTIONS_FILE + '.testsave'
SAVE_FILE_PATH = os.path.join(DEFAULT_CONNECTION_FILE_DIR,
                              SAVE_FILE)

SAVE_BAK_FILE = BACK_FILE + '.testsave'
SAVE_BAK_FILE_PATH = os.path.join(DEFAULT_CONNECTION_FILE_DIR, SAVE_BAK_FILE)


@pytest.fixture
def repo_file_path():
    """
    Fixture to return the file path to the repository file
    """
    return REPO_FILE_PATH


@pytest.fixture(scope='session', autouse=True)
def set_connections_file(request):
    """
    Fixture to hide any existing connection repository at the beginning of a
    session and restore it at the end of the session.  This assumes that the
    connection repository is in the root directory of pywbemcli which is
    logical since that file is defined by the call to pywbemcli in tests.

    This saves and restores any connections file and backup connections file
    in the home directory.
    """
    if os.path.isfile(REPO_FILE_PATH):
        os.rename(REPO_FILE_PATH, SAVE_FILE_PATH)
    if os.path.isfile(REPO_FILE_BACKUP_PATH):
        os.rename(REPO_FILE_BACKUP_PATH, SAVE_BAK_FILE_PATH)

    def teardown():
        """
        Remove any created repository file and restore saved file. This
        should occur at session end.
        """
        if os.path.isfile(REPO_FILE_PATH):
            os.remove(REPO_FILE_PATH)
        if os.path.isfile(SAVE_FILE_PATH):
            os.rename(SAVE_FILE_PATH, REPO_FILE_PATH)

        if os.path.isfile(REPO_FILE_BACKUP_PATH):
            os.remove(REPO_FILE_BACKUP_PATH)
        if os.path.isfile(SAVE_BAK_FILE_PATH):
            os.rename(SAVE_BAK_FILE_PATH, REPO_FILE_BACKUP_PATH)

    request.addfinalizer(teardown)
