#
#   Pytest common fixtures
#

import os
import pytest

from pywbemtools.pywbemcli._connection_repository \
    import DEFAULT_CONNECTIONS_FILE

SCRIPT_DIR = os.path.dirname(__file__)
TEST_DIR = os.getcwd()
REPO_FILE_PATH = os.path.join(TEST_DIR, DEFAULT_CONNECTIONS_FILE)
# if there is a config file, save to this name during tests
SAVE_FILE = DEFAULT_CONNECTIONS_FILE + '.testsave'
SAVE_FILE_PATH = os.path.join(SCRIPT_DIR, SAVE_FILE)


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
    """
    if os.path.isfile(REPO_FILE_PATH):
        os.rename(REPO_FILE_PATH, SAVE_FILE_PATH)

    def teardown():
        """
        Remove any created repository file and restore saved file. This
        should occur as session end.
        """
        if os.path.isfile(REPO_FILE_PATH):
            os.remove(REPO_FILE_PATH)
        if os.path.isfile(SAVE_FILE_PATH):
            os.rename(SAVE_FILE_PATH, REPO_FILE_PATH)

    request.addfinalizer(teardown)
