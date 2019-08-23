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
Defines those cmd line options that apply arross multiple command groups.
"""

CMD_OPTION_NAMES_ONLY_HELP_LINE = \
    '-o, --names-only Retrieve only the returned object names.'

CMD_OPTION_HELP_HELP_LINE = \
    '-h, --help Show this message and exit.'

CMD_OPTION_SUMMARY_HELP_LINE = \
    '-S, --summary Return only summary of objects'

CMD_OPTION_NAMESPACE_HELP_LINE = \
    '-n, --namespace <name> Namespace to use for this operation'

CMD_OPTION_PROPERTYLIST_HELP_LINE = \
    '-p, --propertylist <property name> Define a propertylist'

CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE = \
    '-c, --include-classorigin Request that server include classorigin'

CMD_VERIFY_OPTION_HELP_LINE = \
    '-V, --verify If set, The change is displayed'
