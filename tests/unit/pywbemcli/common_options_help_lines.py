# Copyright 2018 IBM Corp. All Rights Reserved.
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
Defines the expected help text for command specific options that apply across
multiple command groups.

The expected help text strings are used with the 'innows' test, which is a
whitespace-tolerant test for whether the expected text is in the actual text.
"""

# NOTE: A number of the options use double-dash as the short form.  In those
# cases, a third definition of the options without the double-dash defines
# the corresponding option name, ex. 'include_qualifiers'. It should be
# defined with underscore and not dash

CMD_OPTION_HELP_HELP_LINE = \
    '-h, --help Show this help message.'

CMD_OPTION_VERIFY_HELP_LINE = \
    '-V, --verify Prompt for confirmation before performing a change'

CMD_OPTION_NAMESPACE_HELP_LINE = \
    '-n, --namespace NAMESPACE Namespace to use for this command'

CMD_OPTION_NAMES_ONLY_HELP_LINE = \
    '--no, --names-only Retrieve only the object paths (names).'

CMD_OPTION_SUMMARY_HELP_LINE = \
    '-s, --summary Show only a summary (count) of the objects.'

CMD_OPTION_LOCAL_ONLY_CLASS_HELP_LINE = \
    '--lo, --local-only Do not include superclass properties and methods in ' \
    'the returned'

CMD_OPTION_LOCAL_ONLY_INSTANCE_GET_HELP_LINE = \
    '--lo, --local-only Do not include superclass properties in the returned'

CMD_OPTION_LOCAL_ONLY_INSTANCE_LIST_HELP_LINE = \
    '--lo, --local-only When traditional operations are used, do not include ' \
    'superclass properties'

CMD_OPTION_PROPERTYLIST_HELP_LINE = \
    '--pl, --propertylist PROPERTYLIST Filter the properties included in'

CMD_OPTION_FILTER_QUERY_LINE = \
    '--fq, --filter-query QUERY-STRING When pull operations are used, filter ' \
    'the instances in the result'

CMD_OPTION_FILTER_QUERY_LANGUAGE_LINE = \
    '--filter-query-language QUERY-LANGUAGE The filter query language to be ' \
    'used'

CMD_OPTION_NO_QUALIFIERS_HELP_LINE = \
    '--nq, --no-qualifiers Do not include qualifiers in the returned'

CMD_OPTION_INCLUDE_QUALIFIERS_GET_HELP_LINE = \
    '--iq, --include-qualifiers Include qualifiers in the returned'

CMD_OPTION_INCLUDE_QUALIFIERS_LIST_HELP_LINE = \
    '--iq, --include-qualifiers When traditional operations are used, ' \
    'include qualifiers in the returned'

CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE = \
    '--ico, --include-classorigin Include class origin information in the ' \
    'returned'

CMD_OPTION_MULTIPLE_NAMESPACE_ALL_HELP_LINE = \
    '-n, --namespace NAMESPACE(s) Namespace(s) for search scope. May be ' \
    'specified '

CMD_OPTION_KEYS_HELP_LINE = \
    '-k, --key KEYNAME=VALUE   Value for a key in keybinding of'

# NOTE: The FILTER help lines below should exist as a group wherever used.

CMD_OPTION_ASSOCIATION_FILTER_HELP_LINE = \
    '--association / --no-association'

CMD_OPTION_INDICATION_FILTER_HELP_LINE = \
    '--indication / --no-indication'

CMD_OPTION_EXPERIMENTAL_FILTER_HELP_LINE = \
    '--experimental / --no-experimental'

CMD_OPTION_DEPRECATED_FILTER_HELP_LINE = \
    '--deprecated / --no-deprecated'

CMD_OPTION_SINCE_FILTER_HELP_LINE = \
    '--since VERSION Filter the returned classes to return only'

CMD_OPTION_SCHEMA_FILTER_HELP_LINE = \
    "--schema SCHEMA Filter the returned classes to return only classes"

CMD_OPTION_SUBCLASSOF_FILTER_HELP_LINE = \
    "--subclass-of CLASSNAME Filter the returned classes to return only"

CMD_OPTION_LEAFCLASSES_FILTER_HELP_LINE = \
    "--leaf-classes Filter the returned classes to return only"

CMD_OPTION_HELP_INSTANCENAME_HELP_LINE = \
    '--hi, --help-instancename Show help message for specifying INSTANCENAME'

CMD_OPTION_SHOW_NULL_HELP_LINE = \
    '--show-null In the TABLE output formats, show properties with no '

CMD_OPTION_MULTIPLE_NAMESPACE_DFLT_CONN_HELP_LINE = \
    'Namespace(s) to use for this command, instead of the'
