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

CMD_OPTION_HELP_HELP_LINE = \
    '-h, --help Show this message and exit.'

CMD_OPTION_INTERACTIVE_HELP_LINE = \
    "-i, --interactive If set, `INSTANCENAME` argument must"

CMD_OPTION_VERIFY_HELP_LINE = \
    '-V, --verify If set, The change is displayed'

CMD_OPTION_NAMESPACE_HELP_LINE = \
    '-n, --namespace <name> Namespace to use for this operation'

CMD_OPTION_NAMES_ONLY_HELP_LINE = \
    '-o, --names-only Retrieve only the returned object names.'

CMD_OPTION_SUMMARY_HELP_LINE = \
    '-S, --summary Return only summary of objects'

CMD_OPTION_LOCAL_ONLY_HELP_LINE = \
    '-l, --local-only Show only local properties'

CMD_OPTION_PROPERTYLIST_HELP_LINE = \
    '-p, --propertylist <property name> Define a propertylist'

CMD_OPTION_FILTER_QUERY_LINE = \
    '-f, --filter-query TEXT A filter query to be passed to the server'

CMD_OPTION_FILTER_QUERY_LANGUAGE_LINE = \
    '--filter-query-language TEXT A filter-query language to be used'

CMD_OPTION_NO_QUALIFIERS_HELP_LINE = \
    '--no-qualifiers If set, request server to not include qualifiers'

CMD_OPTION_INCLUDE_QUALIFIERS_HELP_LINE = \
    '-q, --include-qualifiers If set, requests server to include'

CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE = \
    '-c, --include-classorigin Request that server include classorigin'
