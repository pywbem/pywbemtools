"""
Tests for Python tell() behavior.

This test exists because certain uses of tell() behave differently between
Windows and Unix-like platforms on Python 2.7.

They document these differences, and verify that the approach used in
test_build_mockenv() works on all platforms.
"""

from __future__ import absolute_import, print_function

import sys
import os
import pytest


@pytest.fixture()
def file_path():
    """
    Create a text file with one line, and remove it after the test.

    Returns the file path of the text file.
    """

    _file_path = 'tmp_file.txt'
    with open(_file_path, 'w') as fp:
        fp.write('first line\n')

    # The yield causes the remainder of this fixture to be executed at the
    # end of the test.
    yield _file_path

    os.remove(_file_path)


def test_tell_append_diff(file_path):
    # pylint: disable=redefined-outer-name
    """
    Test the different behavior of tell() after opening for appending on
    Python 2 on Windows.
    """

    size = os.stat(file_path).st_size

    # Get the stream position via tell() and append a line
    with open(file_path, 'a') as fp:
        pos = fp.tell()
        fp.write('second line\n')

    # Remove the line again by truncating the file to the previous stream
    # position.
    with open(file_path, 'a') as fp:
        fp.seek(pos)
        fp.truncate()

    new_size = os.stat(file_path).st_size
    if sys.platform == 'win32' and sys.version_info[0] == 2:
        exp_size = 0
    else:
        exp_size = size
    assert new_size == exp_size, \
        "original size: {}, tell() result: {}, actual new size: {}, " \
        "expected new size: {}". \
        format(size, pos, new_size, exp_size)


def test_truncate_append_same(file_path):
    # pylint: disable=redefined-outer-name
    """
    Test the behavior of truncate(size) after opening for appending.

    This is the approach used in test_build_mockenv().
    """

    size = os.stat(file_path).st_size

    # Append a line
    with open(file_path, 'a') as fp:
        fp.write('second line\n')

    # Remove the line again by truncating the file using truncate() with size.
    with open(file_path, 'a') as fp:
        fp.truncate(size)

    new_size = os.stat(file_path).st_size
    exp_size = size
    assert new_size == exp_size, \
        "original size: {}, actual new size: {}, expected new size: {}". \
        format(size, new_size, exp_size)
