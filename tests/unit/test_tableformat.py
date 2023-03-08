# (C) Copyright 2017 IBM Corp.
# (C) Copyright 2017 Inova Development Inc.
# All Rights Reserved
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
Tests for table formatting.
"""

from __future__ import print_function, absolute_import

import sys
try:
    from StringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO  # Python 3
import pytest

from pywbemtools._output_formatting import format_table, fold_strings

# pylint: disable=use-dict-literal

# A simple table
TABLE1_HEADERS = ['col1', 'col2', 'col3']
TABLE1_ROWS = [
    ['row1col1', 'row1col2', 'row1col3'],
    ['row2col1', 'row2col2', 'row2col3'],
    ['row3 col1', 'row3  col2', 'row3   col3'],
    [0, 999, 9999999],
    [1.1432, 1.2, 0],
]

# A table used for sorting tests
TABLE2_HEADERS = ['col1', 'col2', 'col3']
TABLE2_ROWS = [
    ['row1col1', 'row1col2', 1],
    ['row2col1', 'row2col2', 99],
    ['row3 col1', 'row3  col2', 0],
    ['anotherrow', 'middle', 9999999],
    ['xorerow', 'anuts', 0],
]

# A table with folded cells
TABLE3_HEADERS = ['col1', 'col2', 'col3']
_TABLE3_FOLDED = fold_strings('this is a folded cell', 10)
TABLE3_ROWS = [
    ['row1col1', 'row2col2', _TABLE3_FOLDED],
    [_TABLE3_FOLDED, 'row2col2', 'row2col3'],
]


TESTCASES_FORMAT_TABLE = [
    # Testcases for format_table().
    #
    # Each testcase is a tuple with the following items:
    # * desc: Description of testcase.
    # * kwargs: Dict with input keyword arguments for format_table():
    #     rows, headers, title=None, table_format='simple',
    #     sort_columns=None, hide_empty_cols=None, float_fmt=None
    # * exp_table: Expected formatted table as tuple of single line strings.
    # * exp_exc_type: Expected exception type, or None.
    # * condition: If True the test is executed, if 'pdb' the test breaks in the
    #     the debugger, if 'verbose' print verbose messages, if False the test
    #     is skipped.

    (
        "Table 1 without title, default format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
        ),
        (
            'col1       col2        col3',
            '---------  ----------  -----------',
            'row1col1   row1col2    row1col3',
            'row2col1   row2col2    row2col3',
            'row3 col1  row3  col2  row3   col3',
            '0          999         9999999',
            '1.1432     1.2         0',
        ),
        None, True
    ),
    (
        "Table 1 with title, default format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            title='simple table',
        ),
        (
            'simple table',
            'col1       col2        col3',
            '---------  ----------  -----------',
            'row1col1   row1col2    row1col3',
            'row2col1   row2col2    row2col3',
            'row3 col1  row3  col2  row3   col3',
            '0          999         9999999',
            '1.1432     1.2         0',
        ),
        None, True
    ),
    (
        "Table 1 without title, simple format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            table_format='simple',
        ),
        (
            'col1       col2        col3',
            '---------  ----------  -----------',
            'row1col1   row1col2    row1col3',
            'row2col1   row2col2    row2col3',
            'row3 col1  row3  col2  row3   col3',
            '0          999         9999999',
            '1.1432     1.2         0',
        ),
        None, True
    ),
    (
        "Table 1 with title, simple format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            title='simple table',
            table_format='simple',
        ),
        (
            'simple table',
            'col1       col2        col3',
            '---------  ----------  -----------',
            'row1col1   row1col2    row1col3',
            'row2col1   row2col2    row2col3',
            'row3 col1  row3  col2  row3   col3',
            '0          999         9999999',
            '1.1432     1.2         0',
        ),
        None, True
    ),
    (
        "Table 1 without title, plain format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            table_format='plain',
        ),
        (
            'col1       col2        col3',
            'row1col1   row1col2    row1col3',
            'row2col1   row2col2    row2col3',
            'row3 col1  row3  col2  row3   col3',
            '0          999         9999999',
            '1.1432     1.2         0',
        ),
        None, True
    ),
    (
        "Table 1 with title, plain format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            title='simple table',
            table_format='plain',
        ),
        (
            'simple table',
            'col1       col2        col3',
            'row1col1   row1col2    row1col3',
            'row2col1   row2col2    row2col3',
            'row3 col1  row3  col2  row3   col3',
            '0          999         9999999',
            '1.1432     1.2         0',
        ),
        None, True
    ),
    (
        "Table 1 without title, table format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            table_format='table',
        ),
        (
            '+-----------+------------+-------------+',
            '| col1      | col2       | col3        |',
            '|-----------+------------+-------------|',
            '| row1col1  | row1col2   | row1col3    |',
            '| row2col1  | row2col2   | row2col3    |',
            '| row3 col1 | row3  col2 | row3   col3 |',
            '| 0         | 999        | 9999999     |',
            '| 1.1432    | 1.2        | 0           |',
            '+-----------+------------+-------------+',
        ),
        None, True
    ),
    (
        "Table 1 with title, table format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            title='simple table',
            table_format='table',
        ),
        (
            'simple table',
            '+-----------+------------+-------------+',
            '| col1      | col2       | col3        |',
            '|-----------+------------+-------------|',
            '| row1col1  | row1col2   | row1col3    |',
            '| row2col1  | row2col2   | row2col3    |',
            '| row3 col1 | row3  col2 | row3   col3 |',
            '| 0         | 999        | 9999999     |',
            '| 1.1432    | 1.2        | 0           |',
            '+-----------+------------+-------------+',
        ),
        None, True
    ),
    (
        "Table 1 without title, psql format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            table_format='psql',
        ),
        (
            '+-----------+------------+-------------+',
            '| col1      | col2       | col3        |',
            '|-----------+------------+-------------|',
            '| row1col1  | row1col2   | row1col3    |',
            '| row2col1  | row2col2   | row2col3    |',
            '| row3 col1 | row3  col2 | row3   col3 |',
            '| 0         | 999        | 9999999     |',
            '| 1.1432    | 1.2        | 0           |',
            '+-----------+------------+-------------+',
        ),
        None, True
    ),
    (
        "Table 1 with title, psql format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            title='simple table',
            table_format='psql',
        ),
        (
            'simple table',
            '+-----------+------------+-------------+',
            '| col1      | col2       | col3        |',
            '|-----------+------------+-------------|',
            '| row1col1  | row1col2   | row1col3    |',
            '| row2col1  | row2col2   | row2col3    |',
            '| row3 col1 | row3  col2 | row3   col3 |',
            '| 0         | 999        | 9999999     |',
            '| 1.1432    | 1.2        | 0           |',
            '+-----------+------------+-------------+',
        ),
        None, True
    ),
    (
        "Table 1 without title, grid format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            table_format='grid',
        ),
        (
            '+-----------+------------+-------------+',
            '| col1      | col2       | col3        |',
            '+===========+============+=============+',
            '| row1col1  | row1col2   | row1col3    |',
            '+-----------+------------+-------------+',
            '| row2col1  | row2col2   | row2col3    |',
            '+-----------+------------+-------------+',
            '| row3 col1 | row3  col2 | row3   col3 |',
            '+-----------+------------+-------------+',
            '| 0         | 999        | 9999999     |',
            '+-----------+------------+-------------+',
            '| 1.1432    | 1.2        | 0           |',
            '+-----------+------------+-------------+',
        ),
        None, True
    ),
    (
        "Table 1 with title, grid format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            title='simple table',
            table_format='grid',
        ),
        (
            'simple table',
            '+-----------+------------+-------------+',
            '| col1      | col2       | col3        |',
            '+===========+============+=============+',
            '| row1col1  | row1col2   | row1col3    |',
            '+-----------+------------+-------------+',
            '| row2col1  | row2col2   | row2col3    |',
            '+-----------+------------+-------------+',
            '| row3 col1 | row3  col2 | row3   col3 |',
            '+-----------+------------+-------------+',
            '| 0         | 999        | 9999999     |',
            '+-----------+------------+-------------+',
            '| 1.1432    | 1.2        | 0           |',
            '+-----------+------------+-------------+',
        ),
        None, True
    ),
    (
        "Table 1 without title, rst format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            table_format='rst',
        ),
        (
            '=========  ==========  ===========',
            'col1       col2        col3',
            '=========  ==========  ===========',
            'row1col1   row1col2    row1col3',
            'row2col1   row2col2    row2col3',
            'row3 col1  row3  col2  row3   col3',
            '0          999         9999999',
            '1.1432     1.2         0',
            '=========  ==========  ===========',
        ),
        None, True
    ),
    (
        "Table 1 with title, rst format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            title='simple table',
            table_format='rst',
        ),
        (
            'simple table',
            '=========  ==========  ===========',
            'col1       col2        col3',
            '=========  ==========  ===========',
            'row1col1   row1col2    row1col3',
            'row2col1   row2col2    row2col3',
            'row3 col1  row3  col2  row3   col3',
            '0          999         9999999',
            '1.1432     1.2         0',
            '=========  ==========  ===========',
        ),
        None, True
    ),
    (
        "Table 1 without title, html format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            table_format='html',
        ),
        (
            '<table>',
            '<thead>',
            '<tr><th>col1     </th><th>col2      </th><th>col3       '
            '</th></tr>',
            '</thead>',
            '<tbody>',
            '<tr><td>row1col1 </td><td>row1col2  </td><td>row1col3   '
            '</td></tr>',
            '<tr><td>row2col1 </td><td>row2col2  </td><td>row2col3   '
            '</td></tr>',
            '<tr><td>row3 col1</td><td>row3  col2</td><td>row3   col3'
            '</td></tr>',
            '<tr><td>0        </td><td>999       </td><td>9999999    '
            '</td></tr>',
            '<tr><td>1.1432   </td><td>1.2       </td><td>0          '
            '</td></tr>',
            '</tbody>',
            '</table>',
        ),
        None, True
    ),
    (
        "Table 1 with title, html format",
        dict(
            rows=TABLE1_ROWS,
            headers=TABLE1_HEADERS,
            title='simple table',
            table_format='html',
        ),
        (
            '<table>',
            '<caption>simple table</caption>',
            '<thead>',
            '<tr><th>col1     </th><th>col2      </th><th>col3       '
            '</th></tr>',
            '</thead>',
            '<tbody>',
            '<tr><td>row1col1 </td><td>row1col2  </td><td>row1col3   '
            '</td></tr>',
            '<tr><td>row2col1 </td><td>row2col2  </td><td>row2col3   '
            '</td></tr>',
            '<tr><td>row3 col1</td><td>row3  col2</td><td>row3   col3'
            '</td></tr>',
            '<tr><td>0        </td><td>999       </td><td>9999999    '
            '</td></tr>',
            '<tr><td>1.1432   </td><td>1.2       </td><td>0          '
            '</td></tr>',
            '</tbody>',
            '</table>',
        ),
        None, True
    ),

    (
        "Table 2 with title, simple format, sorted by column 0",
        dict(
            rows=TABLE2_ROWS,
            headers=TABLE2_HEADERS,
            title='sortable table',
            table_format='simple',
            sort_columns=0,
        ),
        (
            'sortable table',
            'col1        col2           col3',
            '----------  ----------  -------',
            'anotherrow  middle      9999999',
            'row1col1    row1col2          1',
            'row2col1    row2col2         99',
            'row3 col1   row3  col2        0',
            'xorerow     anuts             0',
        ),
        None, True
    ),
    (
        "Table 2 with title, simple format, sorted by columns 1,0",
        dict(
            rows=TABLE2_ROWS,
            headers=TABLE2_HEADERS,
            title='sortable table',
            table_format='simple',
            sort_columns=[1, 0],
        ),
        (
            'sortable table',
            'col1        col2           col3',
            '----------  ----------  -------',
            'xorerow     anuts             0',
            'anotherrow  middle      9999999',
            'row1col1    row1col2          1',
            'row2col1    row2col2         99',
            'row3 col1   row3  col2        0',
        ),
        None, True
    ),
    (
        "Table 2 with title, simple format, sorted by column 2",
        dict(
            rows=TABLE2_ROWS,
            headers=TABLE2_HEADERS,
            title='sortable table',
            table_format='simple',
            sort_columns=2,
        ),
        (
            'sortable table',
            'col1        col2           col3',
            '----------  ----------  -------',
            'row3 col1   row3  col2        0',
            'xorerow     anuts             0',
            'row1col1    row1col2          1',
            'row2col1    row2col2         99',
            'anotherrow  middle      9999999',
        ),
        None, True
    ),

    (
        "Table 3 (folded) with title, plain format",
        dict(
            rows=TABLE3_ROWS,
            headers=TABLE3_HEADERS,
            title='folded table',
            table_format='plain',
        ),
        (
            'folded table',
            'col1       col2      col3',
            'row1col1   row2col2  this is a',
            '                     folded',
            '                     cell',
            'this is a  row2col2  row2col3',
            'folded',
            'cell',
        ),
        None, True
    ),
    (
        "Table 3 (folded) with title, simple format",
        dict(
            rows=TABLE3_ROWS,
            headers=TABLE3_HEADERS,
            title='folded table',
            table_format='simple',
        ),
        (
            'folded table',
            'col1       col2      col3',
            '---------  --------  ---------',
            'row1col1   row2col2  this is a',
            '                     folded',
            '                     cell',
            'this is a  row2col2  row2col3',
            'folded',
            'cell',
        ),
        None, True
    ),
    (
        "Table 3 (folded) with title, grid format",
        dict(
            rows=TABLE3_ROWS,
            headers=TABLE3_HEADERS,
            title='folded table',
            table_format='grid',
        ),
        (
            'folded table',
            '+-----------+----------+-----------+',
            '| col1      | col2     | col3      |',
            '+===========+==========+===========+',
            '| row1col1  | row2col2 | this is a |',
            '|           |          | folded    |',
            '|           |          | cell      |',
            '+-----------+----------+-----------+',
            '| this is a | row2col2 | row2col3  |',
            '| folded    |          |           |',
            '| cell      |          |           |',
            '+-----------+----------+-----------+',
        ),
        None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_table, exp_exc_type, condition",
    TESTCASES_FORMAT_TABLE)
def test_format_table(desc, kwargs, exp_table, exp_exc_type, condition):
    # pylint: disable=unused-argument
    """
    Test function for format_table() tests, using direct comparison.
    """

    if not condition:
        pytest.skip("Condition for test case not met")

    if exp_exc_type:
        with pytest.raises(exp_exc_type):

            if condition == 'pdb':
                pytest.set_trace()

            # The code to be tested
            format_table(**kwargs)
    else:

        if condition == 'pdb':
            pytest.set_trace()

        # The code to be tested
        act_table = format_table(**kwargs)

        exp_table = '\n'.join(exp_table)
        assert act_table == exp_table


@pytest.mark.parametrize(
    "desc, kwargs, exp_table, exp_exc_type, condition",
    TESTCASES_FORMAT_TABLE)
def test_format_table_cap(desc, kwargs, exp_table, exp_exc_type, condition):
    # pylint: disable=unused-argument
    """
    Test function for format_table() tests, using IO capturing.
    """

    if not condition:
        pytest.skip("Condition for test case not met")

    if exp_exc_type:
        with pytest.raises(exp_exc_type):

            if condition == 'pdb':
                pytest.set_trace()

            # The code to be tested
            format_table(**kwargs)
    else:

        # Redirect stdout into capture buffer
        captured_output = StringIO()
        sys.stdout = captured_output

        if condition == 'pdb':
            pytest.set_trace()

        # The code to be tested
        act_table = format_table(**kwargs)

        # Restore stdout and get captured output
        print(act_table)
        sys.stdout = sys.__stdout__
        act_table = captured_output.getvalue()

        exp_table = '\n'.join(exp_table) + '\n'  # print() adds NL
        assert act_table == exp_table
