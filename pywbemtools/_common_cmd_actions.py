# (C) Copyright 2023 IBM Corp.
# (C) Copyright 2023 Inova Development Inc.
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
Pywbemtools command action functions that are common across multiple
tools.  The action method is called by the command processor defined by
a click command decorator.  These methods processing the parsed command.

"""

from __future__ import print_function, absolute_import

import webbrowser
import click

# pylint: disable=relative-beyond-top-level
from ._output_formatting import validate_output_format, format_table


def docs_cmd_action(docs_url):
    """
    Action processor for docs command.  This function just calls a web browser
    with the docs_url provided. It is common because it is used by multiple
    pywbemtools.
    """
    try:
        webbrowser.open_new(docs_url)
    except webbrowser.Error as we:
        raise click.ClickException("Web Browser failed {}".format(we))


def help_subjects_action(obj, subject, help_subjects_dict):
    """
    Common method for displaying help used by a help command in each
    pywbemtools executable.

    parameters:

      obj (:class:`ContextObj`)
         Executable Context which must contain output_format property

      subject (:term:`string` or None):
         String containing the subject to be displayed, the partial string
         to be displayed or None.

         If None, a table of all subjects is displayed.

         If the string equals a single key in the help_subjects table,
         that help subject is displayed.

         If the string matches (startswith(...)) multiple subjects in the
         help_subjects dictionary, a table listing all of the subjects
         is displayed along with a comment that multiple subjects match
         the input string.

         If the string does not match any subject, a click.ClickException
         is executed.

      help_subjects_dict(dictionary):
         A dictionary where the key is the full subject name and the value
         is a list with two entries 1. Summary of the subject, 2. variable
         defining the full string to be displayed as help for the subject.

    returns: Text to display or clicl,ClickException


    """
    minimum_subjects_table_title = "\nHelp Subjects:"

    def get_complete_subject(subject_name, subject_value):
        """Returnthe subject with key subject"""
        return "{0} - {1}\n{2}".format(subject_name,
                                       subject_value[0],
                                       subject_value[1])

    def get_subjects_summary_as_table(subject_names, obj, title=None):
        """get subjects in subjects list as table"""
        rows = [[name, help_subjects_dict[name][0]]
                for name in subject_names]
        if not title:
            title = minimum_subjects_table_title
        output_format = validate_output_format(obj.output_format, 'TABLE')

        return format_table(rows, ("Subject name", "Subject description"),
                            title=title, table_format=output_format)

    all_subjects = sorted(list(help_subjects_dict.keys()))

    # If there is no subject argument, output a table of all of the subjects
    # and short descriptions.
    if not subject:
        return get_subjects_summary_as_table(all_subjects, obj)

    # If a subject text exists, output the help for that subject
    if subject in help_subjects_dict:
        return get_complete_subject(subject, help_subjects_dict[subject])

    # Try search for single subject exists that matches startswith on subject
    partial_subjects = [subj for subj in all_subjects
                        if subj.startswith(subject)]

    # Return if startswith matches a single subject
    if len(partial_subjects) == 1:
        subject = partial_subjects[0]
        return get_complete_subject(subject, help_subjects_dict[subject])

    # If multiple matches, return summary of all that match
    if len(partial_subjects) > 1:
        title = "{0} Input: `{1}` matches multiple subjects:` `{2}`". \
            format(minimum_subjects_table_title,
                   subject, ', '.join(partial_subjects))

        return get_subjects_summary_as_table(partial_subjects, obj, title)

    raise click.ClickException("'{}' is not a valid help subject. "
                               "Try commandd:'help' for list of subjects.".
                               format(subject))
