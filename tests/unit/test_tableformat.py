#!/usr/bin/env python


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
Tests for functions in smipyping/_common.py
"""
from __future__ import print_function, absolute_import

import os
import unittest
import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from pywbemtools.pywbemcli._common import format_table, fold_string

VERBOSE = False

# TODO ks rewrite this test for pytest.  Note that the capture IO
#      may be different in that they have fixtures such as capsys
#      to capture output that may replace StringIO used below.


class BaseTableTests(unittest.TestCase):
    """Base class for testing table output"""
    @staticmethod
    def create_simple_table(table_format=None, title=True):
        """Create a standard table"""
        headers = ['col1', 'col2', 'col3']
        rows = [['row1col1', 'row1col2', 'row1col3'],
                ['row2col1', 'row2col2', 'row2col3'],
                ['row3 col1', 'row3  col2', 'row3   col3'],
                [0, 999, 9999999],
                [1.1432, 1.2, 0]]
        title_txt = 'test simple table' if title else None
        table = format_table(rows, headers, title=title_txt,
                             table_format=table_format)
        return table

    @staticmethod
    def create_sortable_table(table_format=None, title=True, sort_columns=None):
        """Create a standard table"""
        headers = ['col1', 'col2', 'col3']
        rows = [['row1col1', 'row1col2', 1],
                ['row2col1', 'row2col2', 99],
                ['row3 col1', 'row3  col2', 0],
                ['anotherrow', 'middle', 9999999],
                ['xorerow', 'anuts', 0]]
        title_txt = 'test sortable table' if title else None
        table = format_table(rows, headers, title=title_txt,
                             table_format=table_format,
                             sort_columns=sort_columns)
        return table

    @staticmethod
    def create_folded_table(table_format, title=True):
        """Create a table with folded cells"""
        headers = ['col1', 'col2', 'col3']
        folded = fold_string('this is a folded cell', 10)
        rows = [['row1col1', 'row2col2', folded],
                [folded, 'row2col2', 'row2col3']]
        title_txt = 'test folded table' if title else None
        table = format_table(rows, headers, title=title_txt,
                             table_format=table_format)
        return table

    @staticmethod
    def compare_results(actual, expected):
        """Compare two multiline strings to find differences. Helpful to
           find minor errors in the actual/expected outputs
        """
        if actual == expected:
            return
        actual_lines = actual.split(os.linesep)
        expected_lines = expected.split(os.linesep)
        if len(actual_lines) != len(expected_lines):
            print('Different number of lines actual %s, expected %s' %
                  (len(actual_lines), len(expected_lines)))
        line = 0
        for line_a, line_e in zip(actual_lines, expected_lines):
            if line_a != line_e:
                print('Line %s: Difference\n%s\n%s' % (line, line_a, line_e))
                if len(line_a) != len(line_e):
                    print('Different lengths act %s exp %s' % (len(line_a),
                                                               len(line_e)))
            line += 1


class FormatTableTests(BaseTableTests):
    """Tests on the table_format function in _common.py"""

    def test_table_table_hdr(self):
        """Test a table output_format table with header"""

        captured_output = StringIO()          # Create StringIO object
        sys.stdout = captured_output                   # and redirect stdout.
        table = self.create_simple_table(table_format='table', title=True)
        print(table)
        sys.stdout = sys.__stdout__
        actual = captured_output.getvalue()
        if VERBOSE:
            print(actual)

        expected = ('test simple table\n'
                    '+-----------+------------+-------------+\n'
                    '| col1      | col2       | col3        |\n'
                    '|-----------+------------+-------------|\n'
                    '| row1col1  | row1col2   | row1col3    |\n'
                    '| row2col1  | row2col2   | row2col3    |\n'
                    '| row3 col1 | row3  col2 | row3   col3 |\n'
                    '| 0         | 999        | 9999999     |\n'
                    '| 1.1432    | 1.2        | 0           |\n'
                    '+-----------+------------+-------------+\n')

        self.compare_results(actual, expected)

        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_tpsql_table_hdr(self):
        """Test a table output_format table with header"""

        captured_output = StringIO()          # Create StringIO object
        sys.stdout = captured_output                   # and redirect stdout.
        table = self.create_simple_table(table_format='psql', title=True)
        print(table)
        sys.stdout = sys.__stdout__
        actual = captured_output.getvalue()
        if VERBOSE:
            print(actual)

        expected = ('test simple table\n'
                    '+-----------+------------+-------------+\n'
                    '| col1      | col2       | col3        |\n'
                    '|-----------+------------+-------------|\n'
                    '| row1col1  | row1col2   | row1col3    |\n'
                    '| row2col1  | row2col2   | row2col3    |\n'
                    '| row3 col1 | row3  col2 | row3   col3 |\n'
                    '| 0         | 999        | 9999999     |\n'
                    '| 1.1432    | 1.2        | 0           |\n'
                    '+-----------+------------+-------------+\n')

        self.compare_results(actual, expected)

        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_html_table_hdr(self):
        """Test a table output_format table with header"""

        captured_output = StringIO()          # Create StringIO object
        sys.stdout = captured_output                   # and redirect stdout.
        table = self.create_simple_table(table_format='html', title=True)
        print(table)
        sys.stdout = sys.__stdout__
        actual = captured_output.getvalue()
        if VERBOSE:
            print(actual)

        expected = (
            '<p>test simple table</p>\n'
            '<table>\n'
            '<thead>\n'
            '<tr><th>col1     </th><th>col2      </th><th>col3       '
            '</th></tr>\n'
            '</thead>\n'
            '<tbody>\n'
            '<tr><td>row1col1 </td><td>row1col2  </td><td>row1col3   '
            '</td></tr>\n'
            '<tr><td>row2col1 </td><td>row2col2  </td><td>row2col3   '
            '</td></tr>\n'
            '<tr><td>row3 col1</td><td>row3  col2</td><td>row3   '
            'col3</td></tr>\n'
            '<tr><td>0        </td><td>999       </td><td>9999999    '
            '</td></tr>\n'
            '<tr><td>1.1432   </td><td>1.2       </td><td>0          '
            '</td></tr>\n'
            '</tbody>\n'
            '</table>\n')

        self.compare_results(actual, expected)

        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_table_simple_hdr(self):
        """Test a simple table with header"""

        captured_output = StringIO()          # Create StringIO object
        sys.stdout = captured_output                   # and redirect stdout.
        table = self.create_simple_table(table_format='simple', title=True)
        print(table)
        sys.stdout = sys.__stdout__
        actual = captured_output.getvalue()
        if VERBOSE:
            print(actual)

        expected = ('test simple table\n'
                    'col1       col2        col3\n'
                    '---------  ----------  -----------\n'
                    'row1col1   row1col2    row1col3\n'
                    'row2col1   row2col2    row2col3\n'
                    'row3 col1  row3  col2  row3   col3\n'
                    '0          999         9999999\n'
                    '1.1432     1.2         0\n')

        self.compare_results(actual, expected)

        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_table_simple_hdr_sort1(self):
        """Test a simple table with header and the sort option"""

        captured_output = StringIO()          # Create StringIO object
        sys.stdout = captured_output                   # and redirect stdout.
        table = self.create_sortable_table(table_format='simple', title=True,
                                           sort_columns=0)
        print(table)
        sys.stdout = sys.__stdout__
        actual = captured_output.getvalue()
        if VERBOSE:
            print(actual)

        expected = ('test sortable table\n'
                    'col1        col2           col3\n'
                    '----------  ----------  -------\n'
                    'anotherrow  middle      9999999\n'
                    'row1col1    row1col2          1\n'
                    'row2col1    row2col2         99\n'
                    'row3 col1   row3  col2        0\n'
                    'xorerow     anuts             0\n')

        self.compare_results(actual, expected)

        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_table_simple_hdr_sort2(self):
        """Test a simple table with header and the sort option"""

        captured_output = StringIO()          # Create StringIO object
        sys.stdout = captured_output                   # and redirect stdout.
        table = self.create_sortable_table(table_format='simple', title=True,
                                           sort_columns=[1, 0])
        print(table)
        sys.stdout = sys.__stdout__
        actual = captured_output.getvalue()
        if VERBOSE:
            print(actual)

        expected = ('test sortable table\n'
                    'col1        col2           col3\n'
                    '----------  ----------  -------\n'
                    'xorerow     anuts             0\n'
                    'anotherrow  middle      9999999\n'
                    'row1col1    row1col2          1\n'
                    'row2col1    row2col2         99\n'
                    'row3 col1   row3  col2        0\n')

        self.compare_results(actual, expected)

        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_table_simple_hdr_sort3(self):
        """Test a simple table with header and the sort option"""

        captured_output = StringIO()          # Create StringIO object
        sys.stdout = captured_output                   # and redirect stdout.
        table = self.create_sortable_table(table_format='simple', title=True,
                                           sort_columns=2)
        print(table)
        sys.stdout = sys.__stdout__
        actual = captured_output.getvalue()
        if VERBOSE:
            print(actual)

        expected = ('test sortable table\n'
                    'col1        col2           col3\n'
                    '----------  ----------  -------\n'
                    'row3 col1   row3  col2        0\n'
                    'xorerow     anuts             0\n'
                    'row1col1    row1col2          1\n'
                    'row2col1    row2col2         99\n'
                    'anotherrow  middle      9999999\n')

        self.compare_results(actual, expected)

        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_table_simple_no_hdr(self):
        """Test print a simple table no header"""

        captured_output = StringIO()          # Create StringIO object
        sys.stdout = captured_output                   # and redirect stdout.
        table = self.create_simple_table(table_format='simple', title=False)
        print(table)
        sys.stdout = sys.__stdout__
        actual = captured_output.getvalue()
        if VERBOSE:
            print(actual)

        expected = ('col1       col2        col3\n'
                    '---------  ----------  -----------\n'
                    'row1col1   row1col2    row1col3\n'
                    'row2col1   row2col2    row2col3\n'
                    'row3 col1  row3  col2  row3   col3\n'
                    '0          999         9999999\n'
                    '1.1432     1.2         0\n')

        self.compare_results(actual, expected)

        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_table_plain_hdr(self):
        """Test a none table borders with header"""

        captured_output = StringIO()          # Create StringIO object
        sys.stdout = captured_output                   # and redirect stdout.

        table = self.create_simple_table(table_format='plain', title=True)
        print(table)

        sys.stdout = sys.__stdout__
        actual = captured_output.getvalue()
        if VERBOSE:
            print(actual)

        expected = ('test simple table\n'
                    'col1       col2        col3\n'
                    'row1col1   row1col2    row1col3\n'
                    'row2col1   row2col2    row2col3\n'
                    'row3 col1  row3  col2  row3   col3\n'
                    '0          999         9999999\n'
                    '1.1432     1.2         0\n')

        self.compare_results(actual, expected)
        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_table_grid(self):
        """Test printing a plain table with borders and header"""
        captured_output = StringIO()          # Create StringIO object
        sys.stdout = captured_output                   # and redirect stdout.

        table = self.create_simple_table(table_format='grid', title=True)
        print(table)

        sys.stdout = sys.__stdout__
        actual = captured_output.getvalue()
        if VERBOSE:
            print(actual)

        expected = ('test simple table\n'
                    '+-----------+------------+-------------+\n'
                    '| col1      | col2       | col3        |\n'
                    '+===========+============+=============+\n'
                    '| row1col1  | row1col2   | row1col3    |\n'
                    '+-----------+------------+-------------+\n'
                    '| row2col1  | row2col2   | row2col3    |\n'
                    '+-----------+------------+-------------+\n'
                    '| row3 col1 | row3  col2 | row3   col3 |\n'
                    '+-----------+------------+-------------+\n'
                    '| 0         | 999        | 9999999     |\n'
                    '+-----------+------------+-------------+\n'
                    '| 1.1432    | 1.2        | 0           |\n'
                    '+-----------+------------+-------------+\n')

        self.compare_results(actual, expected)
        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_table_rst_hdr(self):
        """Test a none table borders with header"""

        captured_output = StringIO()          # Create StringIO object
        sys.stdout = captured_output                   # and redirect stdout.

        table = self.create_simple_table(table_format='rst', title=True)
        print(table)

        sys.stdout = sys.__stdout__
        actual = captured_output.getvalue()
        if VERBOSE:
            print(actual)

        expected = ('test simple table\n'
                    '=========  ==========  ===========\n'
                    'col1       col2        col3\n'
                    '=========  ==========  ===========\n'
                    'row1col1   row1col2    row1col3\n'
                    'row2col1   row2col2    row2col3\n'
                    'row3 col1  row3  col2  row3   col3\n'
                    '0          999         9999999\n'
                    '1.1432     1.2         0\n'
                    '=========  ==========  ===========\n')

        self.compare_results(actual, expected)
        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_folded_cell_plain(self):
        """Test building a folded cell table plain with header"""
        actual = self.create_folded_table(table_format='plain', title=True)

        if VERBOSE:
            print(actual)

        expected = ('test folded table\n'
                    'col1       col2      col3\n'
                    'row1col1   row2col2  this is a\n'
                    '                     folded\n'
                    '                     cell\n'
                    'this is a  row2col2  row2col3\n'
                    'folded\n'
                    'cell')

        self.compare_results(actual, expected)
        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_folded_cell_simple(self):
        """Test a folded cell table simplewith header"""
        captured_output = StringIO()          # Create StringIO object
        sys.stdout = captured_output                   # and redirect stdout.

        table = self.create_folded_table(table_format='simple', title=True)
        print(table)

        sys.stdout = sys.__stdout__
        actual = captured_output.getvalue()
        if VERBOSE:
            print(actual)

        expected = ('test folded table\n'
                    'col1       col2      col3\n'
                    '---------  --------  ---------\n'
                    'row1col1   row2col2  this is a\n'
                    '                     folded\n'
                    '                     cell\n'
                    'this is a  row2col2  row2col3\n'
                    'folded\n'
                    'cell\n')

        self.compare_results(actual, expected)
        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))

    def test_folded_cell_grid(self):
        """Test a folded cell table with header"""
        actual = self.create_folded_table(table_format='grid', title=True)

        if VERBOSE:
            print(actual)

        expected = ('test folded table\n'
                    '+-----------+----------+-----------+\n'
                    '| col1      | col2     | col3      |\n'
                    '+===========+==========+===========+\n'
                    '| row1col1  | row2col2 | this is a |\n'
                    '|           |          | folded    |\n'
                    '|           |          | cell      |\n'
                    '+-----------+----------+-----------+\n'
                    '| this is a | row2col2 | row2col3  |\n'
                    '| folded    |          |           |\n'
                    '| cell      |          |           |\n'
                    '+-----------+----------+-----------+')

        self.compare_results(actual, expected)
        self.assertEqual(actual, expected,
                         'Actual:\n%s\nExpected:\n%s\n' % (actual, expected))


if __name__ == '__main__':
    unittest.main()
