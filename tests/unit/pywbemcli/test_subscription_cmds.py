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
Tests the subscription command group.

Many of the tests in of the subscription group use stdin because multiple
pywbemcli commands must be used to add and test the various subscriptions.
A single command can be used only  to test the add... commands. Since the
requests sent to the mock server have a lifecycle of one interactive command
session, stdin servers to test these commands.  Also, the mockwbemserver
mock definition is used in a local namespace and therefore, does not get
pickled making the time to execute each test significantly longer (ex. 5
seconds rather than LT a second) so a number of commands were combined into
a single test to test the create, list, and removal commands.

NOTE: We used long lines in the test definitions to make the tests more
readable.
"""

from __future__ import absolute_import, print_function
import os
import sys
import pytest

from .cli_test_extensions import CLITestsBase
from .common_options_help_lines import CMD_OPTION_HELP_HELP_LINE

# pylint: disable=use-dict-literal

TEST_DIR = os.path.dirname(__file__)
TEST_DIR_REL = os.path.relpath(TEST_DIR)


def GET_TEST_PATH_STR(filename):  # pylint: disable=invalid-name
    """
    Return the string representing the relative path of the file name provided.
    """
    return (str(os.path.join(TEST_DIR_REL, filename)))

#
# Definition of files that mock selected pywbemcli calls for tests
# These are installed in pywbemcli through a special env variable set
# before the test that is NOT one of the externally defined environment
# variables
#


TEST_INTEROP_MOCK_FILE = 'simple_interop_mock_script.py'
TEST_USER_MOCK_FILE = 'simple_mock_model.mof'

# MOF with supplementary classes/instances for some subscription tests
SUBSCRIPTION_MOF_FILE = 'mock_subscriptiontest.mof'
SUBSCRIPTIONTEST_MOF_FILEPATH = os.path.join(TEST_DIR, SUBSCRIPTION_MOF_FILE)

MOCK_SERVER_MODEL_PATH = os.path.join(TEST_DIR, 'testmock',
                                      'wbemserver_mock_script.py')

MOCK_SERVER_MODEL_FILE = os.path.join('testmock', 'wbemserver_mock_script.py')

STARTUP_SCRIPT_ENVVAR = 'PYWBEMCLI_STARTUP_SCRIPT'
MOCK_PROMPT_0_FILE = "mock_prompt_0.py"
MOCK_PROMPT_1_FILE = "mock_prompt_pick_response_1.py"
MOCK_CONFIRM_Y_FILE = "mock_confirm_y.py"
MOCK_CONFIRM_N_FILE = "mock_confirm_n.py"

# Test connections file used in some testcases
TEST_SUBSCRIPTIONS_FILE_PATH = 'tmp_subscription_options.yaml'
TEST_SUBSCRIPTIONS_FILE_DICT = {
    'connection_definitions': {
        'blah': {
            'name': 'blah',
            'server': None,
            'user': None,
            'password': None,
            'default-namespace': 'root/cimv2',
            'timeout': 30,
            'use_pull': None,
            'pull_max_cnt': 1000,
            'verify': True,
            'certfile': None,
            'keyfile': None,
            'ca-certs': None,
            'mock-server': [
                os.path.join(TEST_DIR, 'simple_mock_model.mof'),
            ],
        },
    },
    'default_connection_name': None,
}


SUBSCRIPTION_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] subscription COMMAND [ARGS]  '
    '[COMMAND-OPTIONS]',
    'Command group to manage WBEM indication subscriptions.',
    CMD_OPTION_HELP_HELP_LINE,
    'add-destination      Add new listener destination.',
    'add-filter           Add new indication filter.',
    'add-subscription     Add new indication subscription.',
    'list                 Display indication subscriptions overview.',
    'list-destinations    Display indication listeners on the WBEM server.',
    'list-filters         Display indication filters on the WBEM server.',
    'list-subscriptions   Display indication subscriptions on the WBEM server.',
    'remove-destination   Remove a listener destination from the WBEM server.',
    'remove-filter        Remove an indication filter from the WBEM server.',
    'remove-subscription  Remove indication subscription from the WBEM '
    'server.',
    'remove-server        Remove current WBEM server from the '
    'SubscriptionManager.',
]

CMD_OPTION_OWNED_LINE = '--owned / --permanent   Defines whether an owned ' \
    'or permanent filter, destination, or subscription is to be'

OWNEDADD_FLAG_OPTION = '--owned / --permanent  Defines whether an owned or'

SELECT_OPTION = '--select Prompt user to select from multiple objects that ' \
    'match the IDENTITY'

VERIFY_REMOVE_OPTION = '-v, --verify Prompt user to verify instances to be ' \
    'removed before request is'

NAMES_ONLY_OPTION = '--names-only, --no Show the CIMInstanceName elements  ' \
    'of the'

SUMMARY_OPTION = '-s, --summary Show only summary count of instances'

DETAIL_OPTION = '--detail Show more detailed information.'

TYPE_OPTION = '--type [owned|permanent|all]  Defines whether the command ' \
    'filters owned, permanent'

SUBSCRIPTION_ADD_DESTINATION_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] subscription add-destination '
    'IDENTITY [COMMAND-OPTIONS]',
    '-l, --listener-url URL  Defines the URL of the target listener in the '
    'format:',
    OWNEDADD_FLAG_OPTION,
    CMD_OPTION_HELP_HELP_LINE,
]

SUBSCRIPTION_ADD_FILTER_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] subscription add-filter IDENTITY '
    '[COMMAND-OPTIONS]',
    '-q, --query FILTER  Filter query definition. This is a SELECT ',
    '--source-namespaces TEXT The namespace(s) for which the query is defined',
    '--query-language TEXT Filter query language for this subscription',
    CMD_OPTION_HELP_HELP_LINE,
    OWNEDADD_FLAG_OPTION,
]

SUBSCRIPTION_ADD_SUBSCRIPTION_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] subscription add-subscription '
    'DESTINATIONID FILTERID [COMMAND-OPTIONS]',
    CMD_OPTION_HELP_HELP_LINE,
    OWNEDADD_FLAG_OPTION,
    SELECT_OPTION,
]

# TODO : The list of options for each command is incomplete
SUBSCRIPTION_LIST_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] subscription list',
    'Display indication subscriptions overview.',
    SUMMARY_OPTION,
    DETAIL_OPTION,
    CMD_OPTION_HELP_HELP_LINE,
]

SUBSCRIPTION_LIST_DESTINATIONS_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] subscription list-destinations',
    'Display indication listeners on the WBEM server.',
    TYPE_OPTION,
    SUMMARY_OPTION,
    DETAIL_OPTION,
    NAMES_ONLY_OPTION,
    CMD_OPTION_HELP_HELP_LINE,
]

SUBSCRIPTION_LIST_FILTERS_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] subscription list-filters',
    'Display indication filters on the WBEM server.',
    TYPE_OPTION,
    SUMMARY_OPTION,
    DETAIL_OPTION,
    NAMES_ONLY_OPTION,
    CMD_OPTION_HELP_HELP_LINE,
]

SUBSCRIPTION_LIST_SUBSCRIPTIONS_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] subscription list-subscriptions',
    'Display indication subscriptions on the WBEM server.',
    TYPE_OPTION,
    SUMMARY_OPTION,
    '--detail Show more detailed information including MOF of referenced ',
    NAMES_ONLY_OPTION,
    CMD_OPTION_HELP_HELP_LINE,
]

SUBSCRIPTION_REMOVE_DESTINATION_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] subscription remove-destination',
    'Remove a listener destination from the WBEM server.',
    CMD_OPTION_HELP_HELP_LINE,
    VERIFY_REMOVE_OPTION,
    SELECT_OPTION,
    CMD_OPTION_OWNED_LINE,
]

SUBSCRIPTION_REMOVE_FILTER_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] subscription remove-filter',
    'Remove an indication filter from the WBEM server.',
    CMD_OPTION_HELP_HELP_LINE,
    VERIFY_REMOVE_OPTION,
    SELECT_OPTION,
    CMD_OPTION_OWNED_LINE,
]

SUBSCRIPTION_REMOVE_SUBSCRIPTION_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] subscription remove-subscription '
    'DESTINATIONID FILTERID [COMMAND-OPTIONS]',
    'Remove indication subscription from the WBEM server.',
    CMD_OPTION_HELP_HELP_LINE,
    VERIFY_REMOVE_OPTION,
    SELECT_OPTION,
    # CMD_OPTION_OWNED_LINE, TODO: Should we include the owned option.
    '--remove-associated-instances Attempt to remove the instances associated '
]


OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet

# pylint: disable=line-too-long
# Long lines for test cases are more readable.
TEST_CASES = [

    # List of testcases.
    # Each testcase is a list with the following items:
    # * desc: Description of testcase.
    # * inputs: String, or tuple/list of strings, or dict of 'env', 'args',
    #     'general', and 'stdin'. See the 'inputs' parameter of
    #     CLITestsBase.command_test() in cli_test_extensions.py for detailed
    #     documentation.
    # * exp_response: Dictionary of expected responses (stdout, stderr, rc) and
    #     test definition (test: <testname>). See the 'exp_response' parameter
    #     of CLITestsBase.command_test() in cli_test_extensions.py for
    #     detailed documentation.
    # * mock: None, name of file (.mof or .py), or list thereof.
    # * condition: If True the test is executed, if 'pdb' the test breaks in the
    #     the debugger, if 'verbose' print verbose messages, if False the test
    #     is skipped.

    ['Verify subscription command --help response',
     ['--help'],
     {'stdout': SUBSCRIPTION_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify subscription command -h response',
     ['-h'],
     {'stdout': SUBSCRIPTION_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify subscription command --help command order',
     ['--help'],
     {'stdout': r'Commands:'
                '.*\n  add-destination'
                '.*\n  add-filter'
                '.*\n  add-subscription'
                '.*\n  list'
                '.*\n  list-destinations'
                '.*\n  list-filters'
                '.*\n  list-subscriptions'
                '.*\n  remove-destination'
                '.*\n  remove-filter'
                '.*\n  remove-subscription'
                '.*\n  remove-server',
      'test': 'regex'},
     None, OK],

    #
    # Test help commands
    #
    ['Verify subscription command add-destination --help response',
     ['add-destination', '--help'],
     {'stdout': SUBSCRIPTION_ADD_DESTINATION_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify subscription command add-filter --help response',
     ['add-filter', '--help'],
     {'stdout': SUBSCRIPTION_ADD_FILTER_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify subscription command add-subscription --help response',
     ['add-subscription', '--help'],
     {'stdout': SUBSCRIPTION_ADD_SUBSCRIPTION_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify subscription command list --help response',
     ['list', '--help'],
     {'stdout': SUBSCRIPTION_LIST_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify subscription command list-destinations --help response',
     ['list-destinations', '--help'],
     {'stdout': SUBSCRIPTION_LIST_DESTINATIONS_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify subscription command list-filters --help response',
     ['list-filters', '--help'],
     {'stdout': SUBSCRIPTION_LIST_FILTERS_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify subscription command list-subscriptions --help response',
     ['list-subscriptions', '--help'],
     {'stdout': SUBSCRIPTION_LIST_SUBSCRIPTIONS_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify subscription command remove-destination --help response',
     ['remove-destination', '--help'],
     {'stdout': SUBSCRIPTION_REMOVE_DESTINATION_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify subscription command remove-filter --help response',
     ['remove-filter', '--help'],
     {'stdout': SUBSCRIPTION_REMOVE_FILTER_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify subscription command remove-subscription --help response',
     ['remove-subscription', '--help'],
     {'stdout': SUBSCRIPTION_REMOVE_SUBSCRIPTION_HELP_LINES,
      'test': 'innows'},
     None, OK],

    #
    #  Create a destination and list the connection in the next command
    #
    ['Verify add-destination succeeds and list.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ["subscription add-destination x1 -l http://someone:50000 ",
                "-o simple subscription list"]},
     {'stdout': ["CIM_class                     owned    permanent    all",
                 "--------------------------  -------  -----------  -----",
                 "CIM_IndicationSubscription        0            0      0",
                 "CIM_IndicationFilter              0            0      0",
                 "CIM_ListenerDestinationCIMXML     1            0      1",
                 "TOTAL INSTANCES                   1            0      1"],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-destination tests of list cmd with --type options.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://blah:5000',
                '-o mof subscription list-destinations --type permanent --summary',  # noqa: E501
                '-o mof subscription list-destinations --type owned --summary',
                '-o simple subscription list'
                ]},
     {'stdout': ['Added owned destination: '
                 # test no permanents returned
                 'Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',
                 '0 objects returned',
                 '1 CIMInstance(s) returned',
                 'CIM_ListenerDestinationCIMXML  1  0  1'
                 ],
      'test': 'innows'},
     None, OK],

    ['Verify add-destination duplicate --permanent fails.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ["subscription add-destination x1 -l http://someone:50000 --permanent",  # noqa: E501
                "subscription add-destination x1 -l http://someone:50000 --permanent",  # noqa: E501
                "-o simple subscription list"]},
     {'stdout': ["CIM_class                     owned    permanent    all",
                 "--------------------------  -------  -----------  -----",
                 "CIM_IndicationSubscription        0            0      0",
                 "CIM_IndicationFilter              0            0      0",
                 "CIM_ListenerDestinationCIMXML     0            1      1",
                 "TOTAL INSTANCES                   0            1      1"],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-destination duplicate --owned fails.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ["subscription add-destination x1 -l http://someone:50000 --owned",  # noqa: E501
                "subscription add-destination x1 -l http://someone:50000 --owned",  # noqa: E501
                "-o simple subscription list"]},
     {'stdout': ["CIM_class                     owned    permanent    all",
                 "--------------------------  -------  -----------  -----",
                 "CIM_IndicationSubscription        0            0      0",
                 "CIM_IndicationFilter              0            0      0",
                 "CIM_ListenerDestinationCIMXML     1            0      1",
                 "TOTAL INSTANCES                   1            0      1"],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-destination list-destinations, remove destinations succeeds.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination dest1 -l http://blah:50000 ',
                'subscription add-destination dest2  -l https://blah:50001 '
                '--owned ',
                'subscription add-destination perm1 '
                '-l http://perm1:50002 --permanent',
                '-o simple subscription list',
                '-o simple subscription list-destinations',
                '-o mof subscription list-destinations',
                # TODO: Test of the list features should be in its own test
                '-o mof subscription list-destinations --owned',
                '-o mof subscription list-destinations --permanent',
                '-o mof subscription list-destinations --names-only',
                '-v subscription remove-destination dest1',
                '-v subscription remove-destination dest2 --owned',
                '-v subscription remove-destination perm1 --permanent',
                '-o simple subscription list']},
     {'stdout': ['Added owned destination: '
                 'Name=pywbemdestination:defaultpywbemcliSubMgr:dest1',
                 'Added owned destination: '
                 'Name=pywbemdestination:defaultpywbemcliSubMgr:dest2',
                 'Added permanent destination: Name=perm1',
                 'scription instance counts: '
                 'submgr-id=defaultpywbemcliSubMgr, '
                 'svr-id=http://FakedUrl:5988',
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        0            0      0',
                 'CIM_IndicationFilter              0            0      0',
                 'CIM_ListenerDestinationCIMXML     2            1      3',
                 'Indication Destinations: submgr-id=defaultpywbemcliSubMgr,',
                 'Ownership Identity Name Destination Persistence Protocol '
                 'Subscription',
                 # NOTE: Cannot test complete line because Name folds
                 'owned  dest1 pywbemdestination:defaultpywbe '
                 'http://blah:50000 3 2 0',
                 'owned  dest2 pywbemdestination:defaultpywbe '
                 'https://blah:50001 3 2 0',
                 'permanent perm1 perm1 http://perm1:50002  2  2  0',
                 'instance of CIM_ListenerDestinationCIMXML {',
                 # names-only
                 'interop:CIM_ListenerDestinationCIMXML.CreationClassName="CIM_ListenerDestinationCIMXML",'  # noqa: E501
                 'Name="perm1",SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest"',  # noqa: E501
                 'Destination = "http://blah:50000"',
                 'Destination = "https://blah:50001"',
                 'Destination = "http://perm1:50002"',
                 'Removed owned indication destination:',
                 'Removed permanent indication destination',
                 # Should be no destinations after the remove statements
                 'CIM_ListenerDestinationCIMXML  0     0  0'
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-destination list-destinations, remove/verify "y" works.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_CONFIRM_Y_FILE)},
      'stdin': ['subscription add-destination odest1 -l http://blah:50000 ',
                '-o simple subscription list',
                '-o simple subscription list-destinations',
                '-v subscription remove-destination odest1 --verify',
                '-o simple subscription list']},
     {'stdout': ['Added owned destination: '
                 'Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',
                 'CIM_ListenerDestinationCIMXML     1            0      1',
                 'Verify destination instance(s) to be removed:',
                 'MOCK_CLICK_CONFIRM(y):',
                 'CIM_ListenerDestinationCIMXML.CreationClassName="CIM_ListenerDestinationCIMXML",'  # noqa: E501
                 'Name="pywbemdestination:defaultpywbemcliSubMgr:odest1",'
                 'SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest"'  # noqa: E501
                 'Removed owned indication destination:',
                 # Should be no destinations after the remove statements
                 'CIM_ListenerDestinationCIMXML  0     0  0'
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-destination list-destinations, remove/verify "n" works.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_CONFIRM_N_FILE)},
      'stdin': ['subscription add-destination odest1 -l http://blah:50000 ',
                '-o simple subscription list-destinations',
                '-v subscription remove-destination odest1 --verify',
                # List to show destination not remvoved.
                '-o simple subscription list']},
     {'stdout': ['Added owned destination: '
                 'Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',
                 'Verify destination instance(s) to be removed:',
                 'MOCK_CLICK_CONFIRM(n):',
                 'CIM_ListenerDestinationCIMXML.CreationClassName="CIM_ListenerDestinationCIMXML",'  # noqa: E501
                 'Name="pywbemdestination:defaultpywbemcliSubMgr:odest1",'
                 'SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest"',  # noqa: E501
                 # Should be no destinations after the remove statements
                 'CIM_ListenerDestinationCIMXML  1     0  1'
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-destination owned twice same destination does not add second.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://blah:50000',
                'subscription add-destination odest2 -l http://blah:50000',
                # List to show 2nd destination not added
                '-o simple subscription list']},
     {'stdout': ['Added owned destination: '
                 'Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',
                 'CIM_ListenerDestinationCIMXML  1     0  1'
                 ],
      'stderr': ['owned destination: Name=odest2 Not added. Duplicates URL of'],
      'test': 'innows'},
     None, OK],

    ['Verify add-filter tests of list cmd with --type options.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-filter ofilter1 --query "SELECT from blah1"',
                '-o mof subscription list-filters --type permanent --summary',
                '-o mof subscription list-filters --type owned --summary',

                '-o simple subscription list'
                ]},
     {'stdout': ['Added owned filter: '
                 # test no permanents returned
                 'Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',
                 '0 objects returned',
                 '1 CIMInstance(s) returned',
                 'CIM_IndicationFilter  1     0  1'
                 ],
      'test': 'innows'},
     None, OK],

    ['Verify add-filters add, list, remove multiple filters succeeds .',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-filter filter1 --query "SELECT from blah1" --query-language WQL',  # noqa: E501
                'subscription add-filter filter2 --query "SELECT from blah2" --query-language DMTF:CQL --owned ',  # noqa: E501
                'subscription add-filter perm1 --query "SELECT from blah3" --query-language DMTF:CQL --permanent ',  # noqa: E501
                'subscription add-filter perm2 --query "SELECT from blah4" --query-language WQL --permanent ',  # noqa: E501
                '-o simple subscription list',
                # TODO the list tests should be separate. this is add/remove
                '-o simple subscription list-filters',
                '-o simple subscription list-filters --type owned',
                '-o simple subscription list-filters --type permanent',
                '-o simple subscription list-filters --detail',
                '-o simple subscription list-filters --summary',
                '-o mof subscription list-filters',
                '-o mof subscription list-filters --names-only',
                '-v subscription remove-filter filter1',
                '-v subscription remove-filter filter2 --owned',
                '-v subscription remove-filter perm1 --permanent',
                '-v subscription remove-filter perm2 --permanent',
                '-o simple subscription list']},
     {'stdout': ['Subscription instance counts: '
                 'submgr-id=defaultpywbemcliSubMgr, '
                 'svr-id=http://FakedUrl:5988',
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        0            0      0',
                 'CIM_IndicationFilter              2            2      4',
                 'CIM_ListenerDestinationCIMXML     0            0      0',
                 'Ownership  Identity Name Query  Query Source Subscription',
                 'owned filter1 pywbemfilter:defaultpywbemcliS SELECT from blah1  WQL root/cimv2  0',  # noqa: E501
                 'owned filter2 pywbemfilter:defaultpywbemcliS  SELECT from blah2  DMTF:CQL root/cimv2  0',  # noqa: E501
                 'permanent perm1 perm1 SELECT from blah3 DMTF:CQL root/cimv2  0',  # noqa: E501
                 'permanent perm2 perm2 SELECT from blah4  WQL root/cimv2  0',
                 'interop:CIM_IndicationFilter.CreationClassName="CIM_IndicationFilter",Name="pywbemfilter:defaultpywbemcliSubMgr:filter1",SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest"',  # noqa: E501
                 'Name = "perm1";',
                 'Name = "perm2";',
                 'Name = "pywbemfilter:defaultpywbemcliSubMgr:filter1";',
                 'Name = "pywbemfilter:defaultpywbemcliSubMgr:filter2";',
                 # No filters after removal
                 'CIM_IndicationFilter              0            0      0',
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-filters with source_namespaces succeeds.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-filter filter1 --query "xx" --permanent --source-namespaces interop --source-namespaces root/cimv2',  # noqa: E501
                'subscription add-filter filter2 --query "xx2" --permanent --source-namespaces root/cimv3,root/cimv4',  # noqa: E501
                '-o simple subscription list',
                '-o simple subscription list --summary',
                '-o text subscription list --summary',
                '-o simple subscription list-filters',
                '-o mof subscription list-filters',
                'subscription remove-filter filter1 --permanent',
                'subscription remove-filter filter2 --permanent',
                '-o simple subscription list']},
     {'stdout': ['Added permanent filter: Name=filter1',
                 'Added permanent filter: Name=filter2',
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        0            0      0',
                 'CIM_IndicationFilter              0            2      2',
                 'CIM_ListenerDestinationCIMXML     0            0      0',
                 'Ownership  Identity  Name  Query Query Source Subscription',
                 '        Property  Language  Namespaces     Count',
                 'permanent  filter1  filter1  xx  WQL   interop       0',
                 '                  root/cimv2',
                 'permanent  filter2   filter2 xx2  WQL   root/cimv3      0',
                 '                  root/cimv4',
                 # Validate property in MOF
                 'Removed permanent indication filter: identity=filter1, Name=filter1',   # noqa: E501
                 'Removed permanent indication filter: identity=filter2, Name=filter2',   # noqa: E501
                 'SourceNamespaces = { "interop", "root/cimv2" };',
                 'SourceNamespaces = { "root/cimv3", "root/cimv4" };',
                 # Test filters removed
                 'CIM_IndicationFilter              0            0      0',
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-filter list-filters, remove/verify "y" works.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_CONFIRM_Y_FILE)},
      'stdin': ['subscription add-filter ofilter1 --query "blah"',
                '-o simple subscription list',
                '-o simple subscription list-filters',
                '-v subscription remove-filter ofilter1 --verify',
                '-o simple subscription list']},
     {'stdout': ['Added owned filter: '
                 'Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',
                 'CIM_IndicationFilter     1            0      1',
                 'Verify filter instance(s) to be removed:',
                 'MOCK_CLICK_CONFIRM(y):',
                 'CIM_IndicationFilter.CreationClassName="CIM_IndicationFilter",'  # noqa: E501
                 'Name="pywbemfilter:defaultpywbemcliSubMgr:ofilter1",'
                 'SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest"'  # noqa: E501
                 'Removed owned indication filter:',
                 # Should be no destinations after the remove statements
                 'CIM_IndicationFilter  0     0  0'
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-filter list-filter, remove-filter/verify "n" works.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_CONFIRM_N_FILE)},
      'stdin': ['subscription add-filter ofilter1 --query "blah"',
                '-o simple subscription list',
                '-o simple subscription list-filters',
                '-v subscription remove-filter ofilter1 --verify',
                '-o simple subscription list']},
     {'stdout': ['Added owned filter: '
                 'Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',
                 'CIM_IndicationFilter     1            0      1',
                 'MOCK_CLICK_CONFIRM(n):',
                 'CIM_IndicationFilter.CreationClassName="CIM_IndicationFilter",'  # noqa: E501
                 'Name="pywbemfilter:defaultpywbemcliSubMgr:ofilter1",'
                 'SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest"',  # noqa: E501
                 # Should be no filters after the remove statements
                 'CIM_IndicationFilter  1     0  1'
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add owned dest, filter, subscription OK.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://someone:50000',
                'subscription add-filter ofilter1 -q "SELECT * from CIM_Indication" --owned',  # noqa: E501
                'subscription add-subscription  pywbemdestination:defaultpywbemcliSubMgr:odest1  pywbemfilter:defaultpywbemcliSubMgr:ofilter1 --owned',  # noqa: E501
                '-o simple subscription list']},
     {'stdout': ['Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',  # noqa: E501
                 'Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'Added owned subscription: DestinationName=pywbemdestination:defaultpywbemcliSubMgr:odest1, FilterName=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',   # noqa: E501
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        1            0      1',
                 'CIM_IndicationFilter              1            0      1',
                 'CIM_ListenerDestinationCIMXML     1            0      1'],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add owned dest, filter, subscription , verify list options.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://someone:50000',
                'subscription add-filter ofilter1 -q "SELECT * from CIM_Indication" --owned',  # noqa: E501
                'subscription add-subscription odest1 ofilter1 --owned',  # noqa: E501
                # subscription list
                '-o simple subscription list',
                '-o text subscription list',
                '-o simple subscription list --summary',
                '-o text subscription list --summary',
                # list-destinations
                '-o plain subscription list-destinations',
                '-o plain subscription list-destinations --names-only',
                '-o plain subscription list-destinations --detail',
                '-o mof=- subscription list-destinations --detail',
                '-o plain subscription list-destinations --summary',
                'subscription list-destinations --summary',
                # list-filters
                '-o plain subscription list-filters',
                '-o mof subscription list-filters --detail',
                '-o plain subscription list-filters --summary',
                # list-subscriptions
                'subscription list-subscriptions --summary',
                '-o plain subscription list-subscriptions',
                '-o plain subscription list-subscriptions --type owned',
                '-o plain subscription list-subscriptions --type permanent',
                '-o mof subscription list-subscriptions --detail',
                '-o mof subscription list-subscriptions --names-only',
                '-o plain subscription list-subscriptions --summary',
                'subscription list-subscriptions --summary']},
     {'stdout': ['Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',  # noqa: E501
                 'Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'Added owned subscription: DestinationName=pywbemdestination:defaultpywbemcliSubMgr:odest1, FilterName=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',   # noqa: E501
                 # Valid subscription list table (default) output
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        1            0      1',
                 'CIM_IndicationFilter              1            0      1',
                 'CIM_ListenerDestinationCIMXML     1            0      1',
                 # Valid -o text subscription list output
                 'CIM_IndicationSubscription: 1, 0, 1',
                 'CIM_IndicationFilter: 1, 0, 1',
                 'CIM_ListenerDestinationCIMXML: 1, 0, 1',
                 'TOTAL INSTANCES: 3, 0, 3',
                 # Valid -o text subscription list --summary  output
                 '1 subscriptions, 1 filters, 1 destinations'],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add owned dest, filter, subscription , verify list-destination options.',  # noqa: E501
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://someone:50000',
                'subscription add-filter ofilter1 -q "SELECT * from CIM_Indication" --owned',  # noqa: E501
                'subscription add-subscription  odest1  ofilter1 --owned',  # noqa: E501
                '-o plain subscription list-destinations',
                '-o plain subscription list-destinations --names-only',
                '-o plain subscription list-destinations --detail',
                '-o mof subscription list-destinations --detail',
                '-o plain subscription list-destinations --summary',
                '-o mof subscription list-destinations --summary',
                ]},
     {'stdout': ['Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',  # noqa: E501
                 'Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'Added owned subscription: DestinationName=pywbemdestination:defaultpywbemcliSubMgr:odest1, FilterName=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',   # noqa: E501
                 'Indication Destinations: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988, type=all',  # noqa: E501
                 'Ownership    Identity    Name       Destination      Persistence    Protocol    Subscription',  # noqa: E501
                 '                         Type         Count',
                 'owned        odest1      pywbemdestination:defaultpywbe  http://someone:50000       3    2        1',  # noqa: E501
                 '           mcliSubMgr:odest1',
                 'instance of CIM_ListenerDestinationCIMXML {',
                 '   CreationClassName = "CIM_ListenerDestinationCIMXML";',
                 '   SystemCreationClassName = "CIM_ComputerSystem";',
                 '   SystemName = "MockSystem_WBEMServerTest";',
                 '   PersistenceType = 3;',
                 '   Name = "pywbemdestination:defaultpywbemcliSubMgr:odest1";',
                 '   Destination = "http://someone:50000";',
                 '   Protocol = 2;',
                 '};',
                 'instance of CIM_ListenerDestinationCIMXML {',
                 '   CreationClassName = "CIM_ListenerDestinationCIMXML";',
                 '   SystemCreationClassName = "CIM_ComputerSystem";',
                 '   SystemName = "MockSystem_WBEMServerTest";',
                 '   PersistenceType = 3;',
                 '   Name = "pywbemdestination:defaultpywbemcliSubMgr:odest1";',
                 '   Destination = "http://someone:50000";',
                 '   Protocol = 2;',
                 # Result -o plain subscription list-destinations --names-only
                 'host    namespace    class   key=  key=  key=',
                 'interop CIM_ListenerDestinationCIMXML  CIM_ListenerDestinationCIMXML  pywbemdestination:defaultpywbemcliSubMgr:odest1  CIM_ComputerSystem   MockSystem_WBEMServerTest',   # noqa: E501
                 # Result list
                 '1 CIMInstance(s) returned',
                 '};'],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add owned dest, filter, subscription , verify list-filter options.',  # noqa: E501
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://someone:50000',
                'subscription add-filter ofilter1 -q "SELECT * from CIM_Indication" --owned',  # noqa: E501
                'subscription add-subscription  pywbemdestination:defaultpywbemcliSubMgr:odest1  pywbemfilter:defaultpywbemcliSubMgr:ofilter1 --owned',  # noqa: E501
                '-o plain subscription list-filters',
                '-o mof subscription list-filters --detail',
                '-o plain subscription list-filters --summary',
                '-o plain subscription list-filters --names-only',
                '-o mof subscription list-filters --summary',
                ]},
     {'stdout': ['Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',  # noqa: E501
                 'Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'Added owned subscription: DestinationName=pywbemdestination:defaultpywbemcliSubMgr:odest1, FilterName=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',   # noqa: E501
                 'Indication Filters: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988 type=all',  # noqa: E501
                 'Ownership    Identity Name  Query Query Source Subscription',
                 ' Property    Language    Namespaces      Count',
                 'owned        ofilter1    pywbemfilter:defaultpywbemcliS  SELECT * from   WQL  root/cimv2          1',  # noqa: E501
                 '           ubMgr:ofilter1    CIM_Indication',
                 'instance of CIM_IndicationFilter {',
                 '   CreationClassName = "CIM_IndicationFilter";',
                 '   SystemCreationClassName = "CIM_ComputerSystem";',
                 '   SystemName = "MockSystem_WBEMServerTest";',
                 '   Name = "pywbemfilter:defaultpywbemcliSubMgr:ofilter1";',
                 '   SourceNamespaces = { "root/cimv2" };',
                 '   Query = "SELECT * from CIM_Indication";',
                 '   QueryLanguage = "WQL";',
                 '   IndividualSubscriptionSupported = true;',
                 '};',
                 'instance of CIM_IndicationFilter {',
                 '   CreationClassName = "CIM_IndicationFilter";',
                 '   SystemCreationClassName = "CIM_ComputerSystem";',
                 '   SystemName = "MockSystem_WBEMServerTest";',
                 '   Name = "pywbemfilter:defaultpywbemcliSubMgr:ofilter1";',
                 '   SourceNamespaces = { "root/cimv2" };',
                 '   Query = "SELECT * from CIM_Indication";',
                 '   QueryLanguage = "WQL";',
                 '   IndividualSubscriptionSupported = true;',
                 '};',
                 '1 CIMInstance(s) returned',
                 # Result from -o plain subscription list-filters --names-only
                 'host  namespace  class key=  key=  key=  key=',
                 'interop   CIM_IndicationFilter  CIM_IndicationFilter  pywbemfilter:defaultpywbemcliSubMgr:ofilter1  CIM_ComputerSystem  MockSystem_WBEMServerTest', ],  # noqa: E501
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add owned dest, filter, subscription , verify list-subscription options.',  # noqa: E501
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://someone:50000',
                'subscription add-filter ofilter1 -q "SELECT * from CIM_Indication" --owned',  # noqa: E501
                'subscription add-subscription  pywbemdestination:defaultpywbemcliSubMgr:odest1  pywbemfilter:defaultpywbemcliSubMgr:ofilter1 --owned',  # noqa: E501
                'subscription list-subscriptions --summary',
                '-o plain subscription list-subscriptions',
                '-o plain subscription list-subscriptions --type owned',
                '-o plain subscription list-subscriptions --type permanent',
                '-o plain subscription list-subscriptions --summary',
                '-o plain subscription list-subscriptions --names-only',
                '-o mof subscription list-subscriptions',
                '-o mof subscription list --names-only',
                '-o mof subscription list-subscriptions --detail',
                '-o mof subscription list-subscriptions --summary']},
     {'stdout': ['Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',  # noqa: E501
                 'Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'Added owned subscription: DestinationName=pywbemdestination:defaultpywbemcliSubMgr:odest1, FilterName=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',   # noqa: E501
                 # plain table list
                 'Indication Subscriptions: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988, type=all',  # noqa: E501
                 'Ownership    Handler        Filter    Handler        Filter          Filter Query    Subscription',  # noqa: E501
                 '      Identity       Identity  Destination    Query           language        StartTime',  # noqa: E501
                 'owned        odest1(owned)  ofilter1(owned)  http://someone:50000  SELECT * from CIM_Indication  WQL',  # noqa: E501
                 'instance of CIM_IndicationSubscription {',
                 '   Filter =',
                 'interop:CIM_IndicationFilter.CreationClassName=', 'CIM_IndicationFilter',  # noqa: E501
                 'pywbemfilter:defaultpywbemcliSubMgr:ofilter1',
                 'SystemCreationClassName=', 'CIM_ComputerSystem', 'SystemName=',  # noqa: E501
                 'MockSystem_WBEMServerTest',
                 ' Handler =',
                 '  OnFatalErrorPolicy = 2;',
                 '   RepeatNotificationPolicy = 2;',
                 '   SubscriptionState = 2;',
                 '};',
                 # Limited result  -o plain ... list-subscriptions --name-only
                 'host    namespace    class   key=',
                 'Filter Handler',
                 'interop CIM_IndicationSubscription  /interop:CIM_IndicationFilter.SystemCreationClassName=  /interop:CIM_ListenerDestinationCIMXML.',  # noqa: E501
                 '};'],
      'stderr': [],
      'test': 'innows'},
     None, RUN],

    ['Verify add dest, filter, subscription and remove --permanent OK.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination pdest1 -l http://someone:50000 --permanent',  # noqa: E501
                'subscription add-filter pfilter1 -q "SELECT * from CIM_Indication" --permanent',  # noqa: E501
                'subscription add-subscription pdest1 pfilter1 --permanent',
                '-o simple subscription list',

                'subscription remove-subscription pdest1 pfilter1',  # noqa: E501
                'subscription remove-filter pfilter1 --permanent',
                'subscription remove-destination pdest1 --permanent',
                '-o simple subscription list'], },
     {'stdout': ['CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        0            1      1',
                 'CIM_IndicationFilter              0            1      1',
                 'CIM_ListenerDestinationCIMXML     0            1      1',
                 'CIM_IndicationSubscription        0            0      0',
                 'CIM_IndicationFilter              0            0      0',
                 'CIM_ListenerDestinationCIMXML     0            0      0'
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],


    ['Verify add dest, filter, subscription and remove --permanent errs with undefined remove',  # noqa: E501
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination pdest1 -l http://someone:50000 --permanent',  # noqa: E501
                'subscription add-destination pdest2 -l http://someone:50001 --permanent',  # noqa: E501
                'subscription add-filter pfilter1 -q "SELECT * from CIM_Indication" --permanent',  # noqa: E501
                'subscription add-subscription pdest1 pfilter1 --permanent',
                '-o simple subscription list',

                'subscription remove-subscription pdest1 pfilter1',  # noqa: E501
                'subscription remove-filter pfilter1 --permanent',
                'subscription remove-destination pdest1 --permanent',
                # Try to remove non-existent subscription
                'subscription remove-subscription pdest2 pfilter1',  # noqa: E501
                'subscription remove-destination pdest2 --permanent',
                '-o simple subscription list'], },
     {'stdout': ['CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        0            1      1',
                 'CIM_IndicationFilter              0            1      1',
                 'CIM_ListenerDestinationCIMXML     0            2      2',
                 'CIM_IndicationSubscription        0            0      0',
                 'CIM_IndicationFilter              0            0      0',
                 'CIM_ListenerDestinationCIMXML     0            0      0'
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add dests, filters, subscription  --permanent/owned OK.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination pdest1 -l http://someone:50000 --permanent',  # noqa: E501
                'subscription add-filter pfilter1 -q "SELECT * from CIM_Indication" --permanent',  # noqa: E501
                'subscription add-subscription pdest1 pfilter1  --permanent',

                'subscription add-destination odest1 -l http://someone:50001 --owned',  # noqa: E501
                'subscription add-filter ofilter1 -q "SELECT * from CIM_Indication" --owned',  # noqa: E501
                'subscription add-subscription odest1 ofilter1 --owned',  # noqa: E501

                '-o simple subscription list',
                '-o simple subscription list-destinations',
                '-o simple subscription list-filters',
                '-o simple subscription list-subscriptions', ]},
     {'stdout': ['Added permanent destination: Name=pdest1',
                 'Added permanent filter: Name=pfilter1',
                 'Added permanent subscription: DestinationName=pdest1, FilterName=pfilter1',  # noqa: E501
                 'Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',  # noqa: E501
                 'Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'Added owned subscription: DestinationName=pywbemdestination:defaultpywbemcliSubMgr:odest1, FilterName=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        1            1      2',
                 'CIM_IndicationFilter              1            1      2',
                 'CIM_ListenerDestinationCIMXML     1            1      2',
                 'Indication Destinations:',
                 'permanent pdest1 pdest1  http://someone:50000  2  2  1',
                 'owned odest1  pywbemdestination:defaultpywbe  http://someone:50001 3 2  1',  # noqa: E501
                 'Indication Filters:',
                 'permanent pfilter1 pfilter1 SELECT * from   WQL root/cimv2 1',
                 'owned ofilter1  pywbemfilter:defaultpywbemcliS  SELECT * from   WQL root/cimv2 1',  # noqa: E501
                 'Indication Subscriptions:',
                 'permanent  pdest1(permanent) pfilter1(permanent)  http://someone:50000  SELECT * from CIM_Indication  WQL'],  # noqa: E501
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add destinations, filters, subscriptions  --permanent/owned mismatch fails to add subscriptions.',  # noqa: E501
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination pdest1 -l http://someone:50000 --permanent',  # noqa: E501
                'subscription add-filter pfilter1 -q "SELECT * from CIM_Indication" --permanent',  # noqa: E501
                'subscription add-subscription pdest1 pfilter1  --permanent',

                'subscription add-destination odest1 -l http://someone:50001 --owned',  # noqa: E501
                'subscription add-filter ofilter1 -q "SELECT * from CIM_Indication" --owned',  # noqa: E501
                'subscription add-subscription odest1 ofilter1  --owned',
                # The following should all fail
                'subscription add-subscription odest1 ofilter1 -permanent',  # noqa: E501
                'subscription add-subscription odest1 pfilter1 -permanent',  # noqa: E501
                'subscription add-subscription pdest1 ofilter1 -permanent',  # noqa: E501
                '-o simple subscription list']},
     {'stdout': ['Added permanent destination: Name=pdest1',
                 'Added permanent filter: Name=pfilter1',
                 'Added permanent subscription: DestinationName=pdest1, FilterName=pfilter1',  # noqa: E501
                 'Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',  # noqa: E501
                 'Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'Added owned subscription: DestinationName=pywbemdestination:defaultpywbemcliSubMgr:odest1, FilterName=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        1            1      2',
                 'CIM_IndicationFilter              1            1      2',
                 'CIM_ListenerDestinationCIMXML     1            1      2',
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add dests, filters, subscription --permanent/owned, remove-server '
     'OK.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://someone:50000 --owned',  # noqa: E501
                'subscription add-filter ofilter1 -q "SELECT * from CIM_Indication" --owned',  # noqa: E501
                'subscription add-subscription odest1 ofilter1 --owned',
                'subscription add-destination pdest2 -l http://someone:50001  --permanent',  # noqa: E501
                'subscription add-filter pfilter2 -q "SELECT * from CIM_Indication" --permanent',  # noqa: E501
                'subscription add-subscription pdest2 pfilter2 --permanent',  # noqa: E501
                '-o simple subscription list',
                '-o simple subscription list-subscriptions',
                'subscription remove-server',
                '-o simple subscription list']},
     {'stdout': ['http://FakedUrl:5988',
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        1            1      2',
                 'CIM_IndicationFilter              1            1      2',
                 'CIM_ListenerDestinationCIMXML     1            1      2',
                 # Fails test issue # 1055 The subscription should be owned
                 # 'owned  odest1(owned) ofilter1(owned) http://someone:50000  SELECT * from CIM_Indication  WQL',  # noqa: E501
                 'permanent pdest2(permanent) pfilter2(permanent) http://someone:50001  SELECT * from CIM_Indication  WQL',  # noqa: E501
                 'CIM_IndicationSubscription        0            1      1',
                 'CIM_IndicationFilter              0            1      1',
                 'CIM_ListenerDestinationCIMXML     0            1      1', ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add dest, filter, subscrip & list-* handles --permanent, remove-server OK.',  # noqa: E501
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination pdest1 -l http://blah:50000 --permanent',  # noqa: E501
                'subscription add-destination odest1 -l http://blah:50000 --owned',  # noqa: E501'
                'subscription add-filter pfilter1 -q "SELECT" --permanent',  # noqa: E501
                'subscription add-filter ofilter1 -q "SELECT" --owned',  # noqa: E501
                'subscription add-subscription pdest1 pfilter1 --permanent',
                'subscription add-subscription odest1 ofilter1 --owned',
                # Test list with --permanent option
                '-o simple subscription list',
                '-o plain subscription list-destinations --type permanent',
                '-o plain subscription list-filters --type permanent',
                '-o plain subscription list-subscriptions --type permanent',
                'subscription remove-server',
                '-o simple subscription list']},
     {'stdout': ['Added permanent destination: Name=pdest1',
                 'Added permanent filter: Name=pfilter1',
                 'Added permanent subscription: DestinationName=pdest1, FilterName=pfilter1',  # noqa: E501
                 'Added owned subscription: DestinationName=pywbemdestination:defaultpywbemcliSubMgr:odest1, FilterName=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 # Confirm one permanent instance of each created
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        1            1      2',
                 'CIM_IndicationFilter              1            1      2',
                 'CIM_ListenerDestinationCIMXML     1            1      2',
                 # Test if displays permanent objects as table
                 'permanent pfilter1 pfilter1 SELECT WQL root/cimv2  1',
                 'permanent pdest1 pdest1 http://blah:50000 2 2 1',
                 'permanent  pdest1(permanent) pfilter1(permanent) http://blah:50000 ',  # noqa: E501
                 # Confirms remove server removed owned elements only
                 'CIM_class                        owned    permanent    all',
                 '-----------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription           0            1      1',
                 'CIM_IndicationFilter                 0            1      1',
                 'CIM_ListenerDestinationCIMXML        0            1      1',
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify remove_subscription --remove-associated-instances OK,',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination pdest1 -l http://blah:50000 --permanent',  # noqa: E501
                'subscription add-filter pfilter1 -q "SELECT" --permanent',  # noqa: E501
                'subscription add-subscription pdest1 pfilter1 --permanent',
                # Add a permanent destination, filter, subscription
                'subscription add-destination odest1 -l http://blah:50000 --owned',  # noqa: E501
                'subscription add-filter ofilter1 -q "SELECT" --owned',  # noqa: E501
                'subscription add-subscription odest1 ofilter1 --owned',
                '-o simple subscription list',
                'subscription remove-subscription odest1 ofilter1 --remove-associated-instances',  # noqa: E501
                'subscription remove-subscription pdest1 pfilter1 --remove-associated-instances',  # noqa: E501
                '-o simple subscription list']},
     {'stdout': ['Added permanent destination: Name=pdest1',
                 'Added permanent filter: Name=pfilter1',
                 'Added permanent subscription: DestinationName=pdest1, FilterName=pfilter1',  # noqa: E501
                 'Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',  # noqa: E501
                 'Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'Added owned subscription: DestinationName=pywbemdestination:defaultpywbemcliSubMgr:odest1, FilterName=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        1            1      2',
                 'CIM_IndicationFilter              1            1      2',
                 'CIM_ListenerDestinationCIMXML     1            1      2',
                 'Removed 1 subscription(s) for destination-id: odest1, filter-id: ofilter1.',  # noqa: E501
                 'Removed 1 subscription(s) for destination-id: pdest1, filter-id: pfilter1.',  # noqa: E501
                 'Removed destination: interop:CIM_ListenerDestinationCIMXML.CreationClassName="CIM_ListenerDestinationCIMXML",Name="pdest1",SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest"',  # noqa: E501
                 'Removed filter: interop:CIM_IndicationFilter.CreationClassName="CIM_IndicationFilter",Name="pfilter1",SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest"',  # noqa: E501
                 'CIM_IndicationSubscription        0            0      0',
                 'CIM_IndicationFilter              0            0      0',
                 'CIM_ListenerDestinationCIMXML     0            0      0',
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-subscription, remove-subscription/verify "y" works.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_CONFIRM_Y_FILE)},
      'stdin': ['subscription add-destination odest1 -l http://blah:50000 ',
                'subscription add-filter ofilter1 --query "blah"',
                'subscription add-subscription odest1 ofilter1 --owned',
                '-o simple subscription list',
                'subscription remove-subscription odest1 ofilter1 --verify',
                '-o simple subscription list']},
     {'stdout': ['Added owned destination: ',
                 'Added owned filter:',
                 'Added owned subscription:',
                 'TOTAL INSTANCES      3            0      3',
                 'Verify subscription instance(s) to be removed:',
                 'MOCK_CLICK_CONFIRM(y):',
                 'Removed 1 subscription(s) for destination-id: odest1, filter-id: ofilter1',  # noqa: E501
                 # Should be no subscription after the remove statement
                 'CIM_IndicationSubscription  0     0  0'
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-subscription, remove-subscription/verify "n" works.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_CONFIRM_N_FILE)},
      'stdin': ['subscription add-destination odest1 -l http://blah:50000 ',
                'subscription add-filter ofilter1 --query "blah"',
                'subscription add-subscription odest1 ofilter1 --owned',
                '-o simple subscription list',
                'subscription remove-subscription odest1 ofilter1 --verify',
                '-o simple subscription list']},
     {'stdout': ['Added owned destination: ',
                 'Added owned filter:',
                 'Added owned subscription:',
                 'TOTAL INSTANCES      3            0      3',
                 'Verify subscription instance(s) to be removed:',
                 'MOCK_CLICK_CONFIRM(n):',
                 # Subscription should not be removed
                 'CIM_IndicationSubscription  1     0  1'
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-subscription with duplicate destinations no select fails,',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_PROMPT_0_FILE)},
      'stdin': ['subscription add-destination pdest1 -l http://blah:5000 --permanent',  # noqa: E501
                'subscription add-destination destdup -l http://blah:5001 --owned',  # noqa: E501
                'subscription add-destination destdup -l http://blah:5002 --permanent',  # noqa: E501

                'subscription add-filter pfilter1 -q "SELECT 3" --permanent',
                'subscription add-filter filterdup -q "SELECT 2" --owned',
                'subscription add-filter filterdup -q "SELECT 3" --permanent',
                # This command generates click exception which is hidden
                'subscription add-subscription destdup pfilter1 --permanent',
                'subscription add-subscription pdest1 filterdup --permanent',
                'subscription add-subscription destdup filterdup --permanent',
                '-o simple subscription list', ]},
     {'stdout': ['Added permanent destination: Name=pdest1',  # noqa: E501
                 'Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:destdup',  # noqa: E501
                 'Added permanent destination: Name=destdup',

                 'Added permanent filter: Name=pfilter1',
                 'Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:filterdup',  # noqa: E501
                 'Added permanent filter: Name=filterdup',
                 # No indication subscriptions created
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        0            0      0',
                 'CIM_IndicationFilter              1            2      3',
                 'CIM_ListenerDestinationCIMXML     1            2      3',
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify add-subscription permanent with owned destination/filter fails,',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_PROMPT_0_FILE)},
      'stdin': ['subscription add-destination odest1 -l http://blah:5000 --owned',  # noqa: E501
                'subscription add-destination pdest1 -l http://blah:5000 --permanent',  # noqa: E501
                'subscription add-filter ofilter1 -q "SELECT 3" --owned',
                'subscription add-filter pfilter1 -q "SELECT 3" --permanent',
                # All 3 subscriptions should fail
                'subscription add-subscription odest1 pfilter1 --permanent',
                'subscription add-subscription pdest1 ofilter1 --permanent',
                'subscription add-subscription odest1 ofilter1 --permanent',
                '-o simple subscription list', ]},
     {'stdout': ['Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',  # noqa: E501
                 'Added permanent destination: Name=pdest1',
                 'Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'Added permanent filter: Name=pfilter1',
                 # No indication subscriptions created
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        0            0      0',
                 'CIM_IndicationFilter              1            1      2',
                 'CIM_ListenerDestinationCIMXML     1            1      2',
                 ],
      'stderr': ['Permanent subscriptions cannot be created with owned filters or destinations'],  # noqa: E501
      'test': 'innows'},
     None, OK],

    ['Verify duplicate filter names, different paths on filters with --select OK.',  # noqa: E501
     # SUBSCRIPTIONTEST_MOF adds filter subclass to allow creating conflicts
     # Windows bypassed because the add-mof command not correctly created
     # in stdin
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_PROMPT_0_FILE)},
      'stdin': ['subscription add-filter duptestfilter -q "SELECT * from CIM_Indication" --permanent',  # noqa: E501
                'server add-mof ' + str(SUBSCRIPTIONTEST_MOF_FILEPATH) + ' -n interop',  # noqa: E501
                '-o simple subscription list',
                'subscription remove-filter duptestfilter --permanent --select',
                '-o simple subscription list'],
      'platform': 'win32'},  # ignore this platform
     {'stdout': ['CIM_IndicationFilter   0  2 2',
                 '0: CIM_IndicationFilter.CreationClassName="CIM_IndicationFilter",Name="duptestfilter",SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest',  # noqa: E501
                 '1: CIM_IndicationFilterSub.CreationClassName="CIM_IndicationFilterSub",Name="duptestfilter",SystemCreationClassName="CIM_ComputerSystem",SystemName="blah',  # noqa: E501
                 'Removed permanent indication filter: identity=duptestfilter, Name=duptestfilter',  # noqa: E501
                 'CIM_IndicationFilter   0  1 1'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify add-destination permanent fails if IDENTITY already exists.',
     # SUBSCRIPTIONTEST_MOF adds destination subclass to force conflicts
     # Windows bypassed because the add-mof command not correctly created
     # in stdin
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_PROMPT_0_FILE)},
      'stdin': ['server add-mof ' + str(SUBSCRIPTIONTEST_MOF_FILEPATH) + ' -n interop',  # noqa: E501
                'subscription add-destination duptestdest -l http://blah:5000 --permanent'],  # noqa: E501
      'platform': 'win32'},  # ignore this platform
     {'stderr': ['permanent destination: Name=[duptestdest] add failed. Duplicates URL of existing destination'],  # noqa: E501
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify add-filter permanent fails if IDENTITY already exists.',
     # SUBSCRIPTIONTEST_MOF adds filter subclass to allow creating conflicts
     # Windows bypassed because the add-mof command not correctly created
     # in stdin
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_PROMPT_0_FILE)},
      'stdin': ['server add-mof ' + str(SUBSCRIPTIONTEST_MOF_FILEPATH) + ' -n interop',  # noqa: E501
                'subscription add-filter duptestfilter -q "blah" --permanent'],  # noqa: E501
      'platform': 'win32'},  # ignore this platform
     {'stderr': ['permanent filter: Name=[duptestfilter] add failed. Duplicates URL of existing filter'],  # noqa: E501
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify duplicate names,different paths on filters w/o --select OK.',
     # Can only be created by adding filter subclass
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-filter duptestfilter -q "SELECT * from CIM_Indication" --permanent',  # noqa: E501
                'server add-mof ' + str(SUBSCRIPTIONTEST_MOF_FILEPATH) + ' -n interop',  # noqa: E501
                '-o simple subscription list',
                # Test that that the remove-filter without --select OK
                'subscription remove-filter duptestfilter --permanent',
                '-o simple subscription list'],
      'platform': 'win32'},  # ignore on windows
     {'stderr': ['Remove failed. Multiple filters meet criteria identity=duptestfilter, owned=permanent.',  # noqa: E501
                 '* CIM_IndicationFilter.CreationClassName="CIM_IndicationFilter",Name="duptestfilter",SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest',  # noqa: E501
                 '* CIM_IndicationFilterSub.CreationClassName="CIM_IndicationFilterSub",Name="duptestfilter",SystemCreationClassName="CIM_ComputerSystem",SystemName="blah', ],  # noqa: E501
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify dup names, different paths on destinations OK w --select.',
     # Can only be created by adding destination subclass
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_PROMPT_0_FILE)},
      'stdin': ['subscription add-destination duptestdest -l http://blah:5000 --permanent',  # noqa: E501
                'server add-mof ' + str(SUBSCRIPTIONTEST_MOF_FILEPATH) + ' -n interop',  # noqa: E501
                '-o simple subscription list',
                'subscription remove-destination duptestdest --permanent --select',  # noqa: E501
                '-o simple subscription list'],
      'platform': 'win32'},  # ignore on windows
     {'stdout': ['CIM_ListenerDestinationCIMXML   0  2 2',
                 '0: CIM_ListenerDestinationCIMXML.CreationClassName="CIM_ListenerDestinationCIMXML",Name="duptestdest",SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest',  # noqa: E501
                 '1: CIM_ListenerDestinationCIMXMLSub.CreationClassName="CIM_ListenerDestinationCIMXMLSub",Name="duptestdest",SystemCreationClassName="CIM_ComputerSystem",SystemName="blah',  # noqa: E501
                 'Removed permanent indication destination: identity=duptestdest, Name=duptestdest',  # noqa: E501
                 'CIM_ListenerDestinationCIMXML   0  1 1'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify dup names,different paths on destinations OK w/o --select.',
     # Can only be created by adding destination subclass
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination duptestdest -l http://blah:5000 --permanent',  # noqa: E501
                'server add-mof ' + str(SUBSCRIPTIONTEST_MOF_FILEPATH) + ' -n interop',  # noqa: E501
                '-o simple subscription list',
                # Test that that the remove-destination without --select OK
                'subscription remove-destination duptestdest --permanent',
                '-o simple subscription list'],
      'platform': 'win32'},  # ignore on windows
     {'stderr': ['Remove failed. Multiple destinations meet criteria identity=duptestdest, owned=permanent',  # noqa: E501
                 '* CIM_ListenerDestinationCIMXML.CreationClassName="CIM_ListenerDestinationCIMXML",Name="duptestdest",SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest',  # noqa: E501
                 '* CIM_ListenerDestinationCIMXMLSub.CreationClassName="CIM_ListenerDestinationCIMXMLSub",Name="duptestdest",SystemCreationClassName="CIM_ComputerSystem",SystemName="blah'],  # noqa: E501

      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify add-subscription with duplicate destinations with select OK,',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'env': {STARTUP_SCRIPT_ENVVAR: GET_TEST_PATH_STR(MOCK_PROMPT_0_FILE)},
      'stdin': ['subscription add-destination odest1 -l http://blah:5000 --owned',  # noqa: E501
                'subscription add-destination destdup -l http://blah:5001 --owned',  # noqa: E501
                'subscription add-destination destdup -l http://blah:5002 --permanent',  # noqa: E501

                'subscription add-filter ofilter1 -q "SELECT 1" --owned',
                'subscription add-filter filterdup -q "SELECT 2" --owned',
                'subscription add-filter filterdup -q "SELECT 3" --permanent',
                # This command generates click exception which is hidden
                'subscription add-subscription odest1 ofilter1 --owned',
                # This command triggers the prompt mock
                'subscription add-subscription destdup ofilter1 --owned --select',  # noqa: E501
                'subscription add-subscription odest1 filterdup --owned --select',  # noqa: E501
                '-o simple subscription list',
                '-o simple subscription list-subscriptions',
                # This command should list the options and generate exception
                'subscription remove-subscription destdup ofilter1 --remove-associated-instances',  # noqa: E501
                # Following commands should each remove a subscription using
                # --select and prompt mock
                'subscription remove-subscription destdup ofilter1 --remove-associated-instances --select',  # noqa: E501
                'subscription remove-subscription odest1 filterdup --remove-associated-instances --select',  # noqa: E501
                'subscription remove-subscription odest1 ofilter1 --remove-associated-instances --select',  # noqa: E501
                '-o simple subscription list-subscriptions',
                '-o simple subscription list',
                '-o simple subscription list-filters',
                '-o simple subscription list-destinations']},
     {'stdout': ['Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:odest1',  # noqa: E501
                 'Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:destdup',  # noqa: E501
                 'Added permanent destination: Name=destdup',

                 'Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:filterdup',  # noqa: E501
                 'Added permanent filter: Name=filterdup',

                 'Added owned subscription: DestinationName=pywbemdestination:defaultpywbemcliSubMgr:odest1, FilterName=pywbemfilter:defaultpywbemcliSubMgr:ofilter1',  # noqa: E501
                 'CIM_class                     owned    permanent    all',
                 '--------------------------  -------  -----------  -----',
                 'CIM_IndicationSubscription        3            0      3',
                 'CIM_IndicationFilter              2            1      3',
                 'CIM_ListenerDestinationCIMXML     2            1      3',
                 'Removed 1 subscription(s) for destination-id: odest1, filter-id: ofilter1.',  # noqa: E501
                 # TODO: Check'Removed 1 subscription(s) for destination-id: pdest1, filter-id: pfilter1.',  # noqa: E501
                 'Removed destination: interop:CIM_ListenerDestinationCIMXML.CreationClassName="CIM_ListenerDestinationCIMXML",Name="destdup",SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest"',  # noqa: E501
                 'Removed filter: interop:CIM_IndicationFilter.CreationClassName="CIM_IndicationFilter",Name="pywbemfilter:defaultpywbemcliSubMgr:ofilter1",SystemCreationClassName="CIM_ComputerSystem",SystemName="MockSystem_WBEMServerTest"',  # noqa: E501
                 'CIM_IndicationSubscription        0            0      0',
                 # 'CIM_IndicationFilter            0            0      0',
                 # 'CIM_ListenerDestinationCIMXML   0            0      0',
                 # TODO add this to test
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    ['Verify remove-filter with permanent and owned same name OK.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-filter dupfilter -q "SELECT * from CIM_Indication"',  # noqa: E501
                'subscription add-filter dupfilter -q "SELECT * from CIM_Indication" --permanent',  # noqa: E501
                'subscription remove-filter dupfilter',
                'subscription remove-filter dupfilter --permanent',
                '-o simple subscription list']},
     {'stdout': ['Removed owned indication filter: identity=dupfilter, Name=pywbemfilter:defaultpywbemcliSubMgr:dupfilter',  # noqa: E501
                 'Removed permanent indication filter: identity=dupfilter, Name=dupfilter',  # noqa: E501
                 'CIM_IndicationFilter   0  0 0'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify duplicate add-destination fails second add.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://blah:5000 --owned',  # noqa: E501
                'subscription add-destination odest1 -l http://blah:5000 --owned',  # noqa: E501
                '-o simple subscription list']},
     {'stdout': ['CIM_ListenerDestinationCIMXML   1  0 1'],
      'stderr': ["add-destination failed. Name property "
                 "'pywbemdestination:defaultpywbemcliSubMgr:odest1' "
                 "already exists"],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify add-filter duplicate identity/ownership  fails second add.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-filter ofilter1 -q "SELECT" --owned',
                'subscription add-filter ofilter1 -q "SELECT" --owned',
                '-o simple subscription list']},
     {'stdout': ['CIM_IndicationFilter   1  0 1'],
      'stderr': ["add-filter Failed. Filter name='ofilter1' already exists"],
      'rc': 0,
      'test': 'innows'},
     None, OK],


    ['Verify add dest, filter, subscription and remove --permanent OK.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://someone:50000',
                'subscription add-filter ofilter1 -q "blah"',
                'subscription add-subscription odest1 ofilter1',
                '-o simple subscription list --detail']},
     {'stdout': ['Indication Destinations: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988, type=all',  # noqa: E501
                 'Indication Filters: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988 type=all',  # noqa: E501
                 'Indication Subscriptions: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988, type=all'  # noqa: E501
                 ],
      'stderr': [],
      'test': 'innows'},
     None, OK],

    #
    #  Error tests
    #

    # NOTE: Some tests below to not require MOCK_SERVER_MODEL_FILE becasue they
    # fail in click before load of mock file.
    ['Verify any subscription command with no server specified fails.',
     ['add-filter', 'ofilter1', '-q', 'blah', '--owned'],
     {'stderr': ["No WBEM server defined."],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify add destination with invalid url (no port) fails.',
     ['add-destination', 'baddest1', '-l', 'http://blah'],
     {'stderr': ["Port component missing in URL"],
      'rc': 1,
      'test': 'innows'},
     MOCK_SERVER_MODEL_FILE, OK],

    # NOTE: regex used in following tests because python 3.4 produces
    # output for missing argument with double instead of single quote
    ['Verify add-filter no identity fails.',
     ['add-filter', '--owned'],
     {'stderr': ["Missing argument .IDENTITY."],
      'rc': 2,
      'test': 'regex'},
     None, OK],

    ['Verify remove-filter no identity fails.',
     ['remove-filter', '--owned'],
     {'stderr': ["Missing argument .IDENTITY."],
      'rc': 2,
      'test': 'regex'},
     None, OK],

    ['Verify add-destination no identity fails.',
     ['add-filter', '--owned'],
     {'stderr': ["Missing argument .IDENTITY."],
      'rc': 2,
      'test': 'regex'},
     None, OK],

    ['Verify remove-destination no identity fails.',
     ['add-filter', '--owned'],
     {'stderr': ["Missing argument .IDENTITY."],
      'rc': 2,
      'test': 'regex'},
     None, OK],

    ['Verify add-subscription no identity fails.',
     ['add-subscription', '--owned'],
     {'stderr': ["Missing argument .DESTINATION."],
      'rc': 2,
      'test': 'regex'},
     None, OK],

    ['Verify add-subscription only one identity fails.',
     ['add-subscription', 'pdest1', '--owned'],
     {'stderr': ["Missing argument .FILTER."],
      'rc': 2,
      'test': 'regex'},
     None, OK],

    ['Verify remove-subscription no identity fails.',
     ['remove-subscription'],
     {'stderr': ["Missing argument .DESTINATION."],
      'rc': 2,
      'test': 'regex'},
     None, OK],

    ['Verify remove-subscription only one identity fails.',
     ['add-subscription', 'pdest1', '--owned'],
     {'stderr': ["Missing argument .FILTER."],
      'rc': 2,
      'test': 'regex'},
     None, OK],

    ['Verify list-destinations --summary and --detail fails.',
     ['list-destinations', '--summary', '--detail'],
     {'stderr': ["Conflicting options: `summary` is mutually exclusive with "
                 "options: (--detail, --names-only)"],
      'rc': 2,
      'test': 'innows'},
     None, OK],

    ['Verify list-filters --summary and --detail fails.',
     ['list-filters', '--summary', '--detail'],
     {'stderr': ["Conflicting options: `summary` is mutually exclusive with "
                 "options: (--detail, --names-only)"],
      'rc': 2,
      'test': 'innows'},
     None, OK],

    ['Verify list-subscriptions --summary and --detail fails.',
     ['list-destinations', '--summary', '--detail'],
     {'stderr': ["Conflicting options: `summary` is mutually exclusive with "
                 "options: (--detail, --names-only)"],
      'rc': 2,
      'test': 'innows'},
     None, OK],

    ['Verify add_destination  invalid url fails.',
     ['add-destination', 'odest1', '--listener-url', 'fred://blah:50000',
      '--owned'],
     {'stderr': ["add-destination failed: Unsupported scheme 'fred' in URL "
                 "'fred://blah:50000"],
      'rc': 1,
      'test': 'innows'},
     MOCK_SERVER_MODEL_FILE, OK],

    ['Verify add_destination no port on url fails.',
     ['add-destination', 'odest1', '--listener-url', 'http://blah', '--owned'],
     {'stderr': ["add-destination failed: Port component missing in URL "
                 "'http://blah'"],
      'rc': 1,
      'test': 'innows'},
     MOCK_SERVER_MODEL_FILE, OK],

    ['Verify add permanent subscription with owned filter/dest fails.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://blah:5000',
                'subscription add-filter ofilter1 -q "SELECT * from CIM_Indication"',  # noqa: E501
                'subscription add-subscription odest1 ofilter1 --permanent',
                '-o simple subscription list']},
     {'stdout': ["CIM_IndicationSubscription           0            0      0"],
      'stderr': ["Permanent subscriptions cannot be created with owned filters "
                 "or destinations."],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify remove-filter with associations fails.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://blah:5000',
                'subscription add-filter ofilter1 -q "SELECT * from CIM_Indication"',  # noqa: E501
                'subscription add-subscription odest1 ofilter1',
                'subscription remove-filter ofilter1']},
     {'stderr': ["remove-filter failed", "(CIM_ERR_FAILED)",
                 "The indication filter is referenced by subscriptions"],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify remove-destination with associations fails.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-destination odest1 -l http://blah:5000',
                'subscription add-filter ofilter1 -q "SELECT * from CIM_Indication"',  # noqa: E501
                'subscription add-subscription odest1 ofilter1',
                'subscription remove-destination odest1']},
     {'stderr': ["remove-destination failed:", "(CIM_ERR_FAILED)",
                 "The listener destination is referenced by subscriptions"],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify add-filter with colon in name fails.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription add-filter ofilter:1 -q "blah"', ]},
     {'stderr': ["add-filter failed", "Filter ID contains ':': 'ofilter:1"],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify remove-destination unknown destination fails.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription remove-destination odest', ]},
     {'stderr': ["No owned destination found foridentity=odest", ],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify remove-filter unknown filter fails.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription remove-filter ofilter1', ]},
     {'stderr': ["No owned filter found foridentity=ofilter1", ],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify remove-subscription unknown destination/filter fails.',
     {'general': ['-m', MOCK_SERVER_MODEL_PATH],
      'stdin': ['subscription remove-subscription blah blah', ]},
     {'stderr': ["No destination found for identity: blah", ],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    # TESTS TO IMPLEMENT
    # 1. test of fail when add-subscription reverses dest and filter ids
    # 2. test of fail when remove-subscription reverses dest and filter ids
    # 5. Tests of summary and --detail beyond existing tests
    # 6. Add tests-listpermanent and all and both types of owned
    # 7. tests of output format text for those commands that implement this.
    # 8. Test fail with destination and filter if create duplicated.
    # 9. Add-subscription fail, value or type error
    # 10. dest/filter_for_type, owned (list-destinations owned)
    # 11. find_destinations_for_name( fail_if_none
    # 12. subscription_class  select_id_str( not tested, not used.
    # 13. pick_one_path_from_instances_list( subscription )

]
# pylint: enable=enable=line-too-long


class TestSubcmdClass(CLITestsBase):  # pylint: disable=too-few-public-methods
    """
    Test all of the class command variations.
    """
    command_group = 'subscription'

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition",
        TEST_CASES)
    def test_class(self, desc, inputs, exp_response, mock, condition):
        """
        Common test method for those commands and options in the
        class command that can be tested.  This includes:

          * Subcommands like help that do not require access to a server

          * Subcommands that can be tested with a single execution of a
            pywbemcli command.
        """
        # Temp bypass of windows platform because of issue with one test
        # TODO: Solve issue of concatenating model path into a string for
        # windows platform.  This causes loss of backslashes.
        # See test_generaloptions.py also
        if 'platform' in inputs:
            if sys.platform == inputs['platform']:
                return

        # Create the connection file from the 'yaml' input
        if 'yaml' in inputs:
            # pylint: disable=unspecified-encoding
            with open(TEST_SUBSCRIPTIONS_FILE_PATH, "wt") as repo_file:
                repo_file.write(inputs['yaml'])

        # All tests in for subscriptions will use the subscriptions
        # connections file.
        connections_file = TEST_SUBSCRIPTIONS_FILE_PATH
        if 'general' in inputs:
            inputs['general'].extend(['--connections-file', connections_file])
        else:
            inputs = {"args": inputs}
            inputs['general'] = ['--connections-file', connections_file]
        assert '--connections-file' in inputs['general']

        self.command_test(desc, self.command_group, inputs, exp_response,
                          mock, condition)
