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
Internal module with utility code to print out terminal a table from
a data structure

This code uses the python terminaltables library

"""

from __future__ import print_function, absolute_import

from textwrap import wrap
import six
from terminaltables import SingleTable, AsciiTable


# TODO account for max width of table and columns.
def print_ascii_table(table_data, title=None, inner=False, outer=False,
                      ascii=True):
    """ Print table data as an ascii table. The input is a dictionary
        of table data in the format used by terminaltable package.

        Parameters:
           table_data (iterable of list of :term:`string`)
               Each list in the iterable is a line in the table
               Each String in the list is data for a cell

           title (:class:`py:list` of :term:`unicode string`)
              Strings representing the title row of the table

           inner (:class:`py:bool`): if True an inner border is printed
             between cells

           outer (:class:`py:bool`): If True an outer border is printed
            around the table

           ascii (:class:`py:bool`): If True, the borders are printed with ascii
            characters. Otherwise they are printed with box drawing
            characters which might lead to more variation in different
            platforms.


        The remaining lines are the table lines each as a list of entries
    """

    table_instance = AsciiTable(table_data) if ascii else \
        SingleTable(table_data)
    table_instance.inner_column_border = inner
    table_instance.outer_border = outer
    table_instance.title = title

    print(table_instance.table)
    print()


def fold_line(line_string, max_line_width):
    """ Fold a line within a maximum width to fit within a table entry
    """
    new_line = line_string
    if isinstance(line_string, six.string_types):
        if max_line_width < len(line_string):
            new_line = '\n'.join(wrap(line_string, max_line_width))

    return new_line
