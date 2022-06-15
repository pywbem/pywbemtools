# (C) Copyright 2021 IBM Corp.
# (C) Copyright 2021 Inova Development Inc.
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
Click Command definition for the subscription command group which includes
commands for managing subscriptions to indications on WBEM servers including
adding, displaying, and remvoving destinations, filters, and subscriptions from
a WBEM server.

This command group is based on the  pywbem WBEMSubscriptionManager class.
"""
from __future__ import absolute_import

import re

import click

from pywbem import CIMError, Error, WBEMSubscriptionManager, \
    CIM_ERR_ALREADY_EXISTS

from pywbem._subscription_manager import SUBSCRIPTION_CLASSNAME, \
    DESTINATION_CLASSNAME, FILTER_CLASSNAME

from .pywbemcli import cli

from .._options import add_options, help_option

from ._display_cimobjects import display_cim_objects, fold_strings

from .._click_extensions import PywbemtoolsGroup, PywbemtoolsCommand, \
    CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT, MutuallyExclusiveOption

from ._common import pick_one_index_from_list, sort_cimobjects, \
    verify_operation

from .._output_formatting import validate_output_format, \
    output_format_is_table, output_format_is_cimobject, format_table

DEFAULT_QUERY_LANGUAGE = 'WQL'

DEFAULT_SUB_MGR_ID = "defaultpywbemcliSubMgr"

OWNED_STR = True
ALL_STR = 'all'

ownedadd_flag_option = [              # pylint: disable=invalid-name
    click.option("--owned/--permanent", default=True,
                 help=u"Defines whether an owned or permanent filter, "
                      u"destination, or subscription is to be added.  "
                      u"Default: owned"),
]

ownedremove_flag_option = [              # pylint: disable=invalid-name
    click.option("--owned/--permanent", default=True,
                 help=u"Defines whether an owned or permanent filter, "
                      u"destination, or subscription is to be removed.  "
                      u"Default: owned"),
]

ownedlist_choice_option = [              # pylint: disable=invalid-name
    click.option("--type", default='all',
                 type=click.Choice(['owned', 'permanent', 'all'],
                                   case_sensitive=False),
                 help=u"Defines whether the command filters owned, "
                      u" permanent, or all objects for the response.  "
                      u"Default: all"),
]

names_only_option = [              # pylint: disable=invalid-name
    click.option('--names-only', '--no', is_flag=True, required=False,
                 cls=MutuallyExclusiveOption,
                 mutually_exclusive=["summary", 'detail'],
                 show_mutually_exclusive=True,
                 help=u'Show the CIMInstanceName elements of the instances. '
                      u'This only applies when the --output-format is one '
                      u'of the CIM object options (ex. mof.')
]

detail_option = [             # pylint: disable=invalid-name
    click.option('-d', '--detail', is_flag=True, required=False,
                 cls=MutuallyExclusiveOption,
                 mutually_exclusive=["summary", 'names-only'],
                 show_mutually_exclusive=True,
                 help=u"Show more detailed information. Otherwise only "
                 u"non-null or predefined property values are displayed. It "
                 u"applies to both MOF and TABLE output formats.")
]

detail_subscription_option = [             # pylint: disable=invalid-name
    click.option('-d', '--detail', is_flag=True, required=False,
                 cls=MutuallyExclusiveOption,
                 mutually_exclusive=["summary", 'names-only'],
                 show_mutually_exclusive=True,
                 help=u"Show more detailed information including MOF of "
                 "referenced listeners and filters. Otherwise only "
                 u"non-null or predefined property values are displayed. The "
                 u"extra properties applies to both MOF and TABLE output "
                 u"formats.")
]

summary_option = [             # pylint: disable=invalid-name
    click.option('-s', '--summary', is_flag=True, required=False,
                 cls=MutuallyExclusiveOption,
                 mutually_exclusive=["detail", 'names-only'],
                 show_mutually_exclusive=True,
                 help=u'Show only summary count of instances.')
]

verify_remove_option = [       # pylint: disable=invalid-name
    click.option('-v', '--verify', is_flag=True, default=False,
                 help=u'Prompt user to verify instances to be removed before '
                      u'request is sent to WBEM server.')
]

select_option = [             # pylint: disable=invalid-name
    click.option('--select', is_flag=True, default=False,
                 help=u'Prompt user to select from multiple objects '
                      u'that match the IDENTITY. Otherwise, if the command '
                      u'finds multiple instance that match the IDENTITY, the '
                      u'operation fails.')
]

##################################################################
#
# Subcommand Click definitions
#
###################################################################


@cli.group('subscription', cls=PywbemtoolsGroup,
           options_metavar=GENERAL_OPTS_TXT, subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
def subscription_group():
    """
    Command group to manage WBEM indication subscriptions.

    This group uses the pywbem subscription manager to create, view, and remove
    CIM Indication subscriptions for a WBEM Server.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    command. These are NOT retained after the command is executed.
    """
    pass


@subscription_group.command('add-destination', cls=PywbemtoolsCommand,
                            options_metavar=CMD_OPTS_TXT)
@click.argument('identity', type=str, metavar='IDENTITY', required=True,)
@click.option('-l', '--listener-url', type=str, metavar='URL',
              help=u'Defines the URL of the target listener in the format: '
                   u'[SCHEME://]HOST:PORT. SCHEME must be "https" (default) '
                   u'or "http". HOST is a short or long hostname or literal '
                   u'IPV4/v6 address. PORT is a positive integer and is '
                   u'required')
@add_options(ownedadd_flag_option)
@add_options(help_option)
@click.pass_obj
def subscription_add_destination(context, identity, **options):
    """
    Add new listener destination.

    This command adds a listener destination to be the target of indications
    sent by a WBEM server a WBEM server, by adding an instance of the CIM class
    "CIM_ListenerDestinationCIMXML" in the Interop namespace of the WBEM
    server.

    A listener destination defines the target of a WBEM indication
    listener including URI of the listener including the listener port.

    The required IDENTITY argument along with the --owned/--permanent option
    define the ``Name`` key property of the new instance.  If the instance is to
    be owned by the current SubscriptionManager, pywbemcli creates a 'Name'
    property value with the format: "pywbemdestination:"
    <SubscriptionManagerID> ":" <IDENTITY>. If the destination instance is to
    be permanent, the value of the IDENTITY argument becomes the value of the
    'Name' property.

    Owned destinations are added or updated conditionally: If the destination
    instance to be added is already registered with this subscription manager
    and has the same property values, it is not created or modified. If an
    instance with this path and properties does not exist yet (the normal
    case), it is created on the WBEM server.

    Permanent listener destinations are created unconditionally, and it is up to
    the user to ensure that such an instance does not already exist.

    If the --verbose general option is set, the created instance is displayed.
    """
    context.execute_cmd(
        lambda: cmd_subscription_add_destination(context, identity, options))


@subscription_group.command('add-filter', cls=PywbemtoolsCommand,
                            options_metavar=CMD_OPTS_TXT)
@click.argument('identity', type=str, metavar='IDENTITY', required=True,)
@click.option('-q', '--query', type=str, metavar='FILTER',
              required=True,
              help=u'Filter query definition. This is a SELECT '
                   u'statement in the query language defined in the '
                   u'filter-query-language parameter')
@click.option('--query-language', type=str, metavar='TEXT',
              required=False,
              default=DEFAULT_QUERY_LANGUAGE,
              help=u"Filter query language for this subscription The query "
                   u"languages normally implemented are 'DMTF:CQL' and 'WQL' . "
                   u" Default: {0}".format(DEFAULT_QUERY_LANGUAGE))
@click.option('--source-namespaces', type=str, metavar='TEXT',
              required=False, default=None,
              multiple=True,
              help=u"The namespace(s) for which the query is defined. Multiple "
                   u"values may be defined with a single comma-separated "
                   u"string of namespaces or multiple options. If defined the "
                   u"namespaces will be inserted into the SourceNamespaces "
                   u"property. Otherwise the property will not be created and "
                   u"the WBEM server typically use the Interop namespace for "
                   u"the indication filter.")
@add_options(ownedadd_flag_option)
@add_options(help_option)
@click.pass_obj
def subscription_add_filter(context, identity, **options):
    """
    Add new indication filter.

    This command adds an indication filter to a WBEM server, by
    creating an indication filter instance (CIM class
    "CIM_IndicationFilter") in the Interop namespace of the server.

    A indication listener defines the query and query language to be used
    by the WBEM server to create indications for an indication subscription.

    The required IDENTITY argument of the command and the --owned/--permanent
    option defines the 'Name' key property of the the created instance.  If the
    the instance is to be owned by the current SubscriptionManager, pywbemcli
    indirectly specifies the 'Name' property value with the format:
    "pywbemfilter:" "<SubscriptionManagerID>" ":" <identity>``. If the
    destination instance is to be permanent, the value of the IDENTITY argument
    directly becomes the value of the Name property.

    Owned indication filters are added or updated conditionally: If the
    indication filter instance to be added is already registered with
    this subscription manager and has the same property values, it is not
    created or modified. If it has the same path but different property
    values, it is modified to get the desired property values. If an
    instance with this path does not exist yet (the normal case), it is
    created.

    Permanent indication filters are created unconditionally; it is
    up to the user to ensure that such an instance does not exist yet.

    If the --verbose general option is set, the created instance is displayed.
    """
    context.execute_cmd(
        lambda: cmd_subscription_add_filter(context, identity, options))


@subscription_group.command('add-subscription', cls=PywbemtoolsCommand,
                            options_metavar=CMD_OPTS_TXT)
@click.argument('destination-identity', type=str, metavar='DESTINATIONID',
                required=True,)
@click.argument('filter-identity', type=str, metavar='FILTERID', required=True,)
@add_options(ownedadd_flag_option)
@add_options(select_option)
@add_options(help_option)
@click.pass_obj
def subscription_add_subscription(context, destination_identity,
                                  filter_identity, **options):
    """
    Add new indication subscription.

    Adds an indication subscription to the current WBEM server for a particular
    DESTINATIONID and FILTERID. The command creates an instance of CIM
    association class "CIM_IndicationSubscription" in the Interop namespace of
    the server.

    The destination and filter instances to be used in the subscription is
    based on the DESTINATIONID and FILTERID arguments which define the
    the 'Handler' and 'Filter' reference properties of the subscription
    instance to be created.

    The required DESTINATIONID argument defines the existing destination
    instance that will be attached to the 'Handler' reference of the
    association class. This argument may consist of either the value of the
    'Name' property of the target destination instance or the identity of that
    instance.  The identity is the full value of the 'Name' property for
    permanent destinations and is a component of the 'Name' property for owned
    instances. If just the identity is used, this will result in multiple
    destinations being found if the same string is defined as the identity of
    an owned and permanent destination.

    The required FILTERID argument defines the existing filter instance that
    will be attached to the 'Filter' reference of the association class. This
    argument may consist of either the value of the 'Name' property of the
    target filter instance or the identity of that instance.  The identity is
    the full value of the 'Name' property for permanent filters and is a
    component of the 'Name' property for owned instances. If just the identity
    is used, this will result in multiple filters being found if the same
    string is defined as the identity of an owned and permanent filter.

    When creating permanent subscriptions, the indication filter and the
    listener destinations must not be owned. for owned subscriptions,
    indication filter and listener destination may be either owned or permanent.

    Owned subscriptions are added or updated conditionally: If the
    subscription instance to be added is already registered with
    this subscription manager and has the same path, it is not
    created.

    Permanent subscriptions are created unconditionally, and it is up to
    the user to ensure that such an instance does not already exist.

    Upon successful return of this method, the added subscription is active on
    the WBEM server, so that the specified WBEM listeners may immediately
    receive indications.

    If the --verbose general option is set, the created instance is displayed.
    """
    # pylint: disable=line-too-long
    context.execute_cmd(
        lambda: cmd_subscription_add_subscription(context, destination_identity, filter_identity, options))  # noqa: E501


@subscription_group.command('list', cls=PywbemtoolsCommand,
                            options_metavar=CMD_OPTS_TXT)
@add_options(ownedlist_choice_option)
@add_options(summary_option)
@add_options(detail_option)
@add_options(help_option)
@click.pass_obj
def subscription_list(context, **options):
    """
    Display indication subscriptions overview.

    This command provides an overview of the count of subscriptions, filters,
    and destinations retrieved from the WBEM server. The level of detail
    depends on the --summary and --detail options. '--summary' displays only
    a single count for each; --detail displays a table for the instances
    of each. The default is to display a table of the count of owned and
    permanent for each.
    """
    context.execute_cmd(lambda: cmd_subscription_list(context, options))


@subscription_group.command('list-destinations', cls=PywbemtoolsCommand,
                            options_metavar=CMD_OPTS_TXT)
@add_options(ownedlist_choice_option)
@add_options(detail_option)
@add_options(names_only_option)
@add_options(summary_option)
@add_options(help_option)
@click.pass_obj
def subscription_list_destinations(context, **options):
    """
    Display indication listeners on the WBEM server.

    Display existing CIM indication listener destinations on the current
    connection. The listener destinations to be displayed can be filtered
    by the owned choice option (owned, permanent, all).

    The data display is determined by the --detail, --names_only, and --summary
    options and can be displayed as either a table or CIM objects (ex. mof)
    format using the --output general option (ex. --output mof).
    """
    context.execute_cmd(
        lambda: cmd_subscription_list_destinations(context, options))


@subscription_group.command('list-filters', cls=PywbemtoolsCommand,
                            options_metavar=CMD_OPTS_TXT)
@add_options(ownedlist_choice_option)
@add_options(detail_option)
@add_options(names_only_option)
@add_options(summary_option)
@add_options(help_option)
@click.pass_obj
def subscription_list_filters(context, **options):
    """
    Display indication filters on the WBEM server.

    Display existing CIM indication filters (CIM_IndicationFilter class) on the
    current connection. The indication filters to be displayed can be filtered
    by the owned choice option (owned, permanent, all).

    The data display is determined by the --detail, --names-only, and --summary
    options and can be displayed as either a table or CIM objects (ex. mof)
    format using the --output general option (ex. --output mof).

    """
    context.execute_cmd(lambda: cmd_subscription_list_filters(context, options))


@subscription_group.command('list-subscriptions', cls=PywbemtoolsCommand,
                            options_metavar=CMD_OPTS_TXT)
@add_options(ownedlist_choice_option)
@add_options(detail_subscription_option)
@add_options(names_only_option)
@add_options(summary_option)
@add_options(help_option)
@click.pass_obj
def subscription_list_subscriptions(context, **options):
    """
    Display indication subscriptions on the WBEM server.

    Displays information on indication subscriptions on the WBEM server,
    filtering the subscriptions to be displayed can be filtered by the owned
    choice option (owned, permanent, all).

    The default display is a table of information from the associated
    Filter and Handler instances

    The data display is determined by the --detail, --names-only, and --summary
    options and can be displayed as either a table or CIM objects (ex. mof)
    format using the --output general option (ex. --output mof).

    """
    context.execute_cmd(
        lambda: cmd_subscription_list_subscriptions(context, options))


@subscription_group.command('remove-destination', cls=PywbemtoolsCommand,
                            options_metavar=CMD_OPTS_TXT)
@click.argument('identity', type=str, metavar='IDENTITY', required=True)
@add_options(ownedremove_flag_option)
@add_options(select_option)
@add_options(help_option)
@add_options(verify_remove_option)
@click.pass_obj
def subscription_remove_destination(context, identity, **options):
    """
    Remove a listener destination from the WBEM server.

    Removes a listener destination instance (CIM_ListenerDestinationCIMXML)
    from the WBEM server where the instance to be removed is identified by the
    IDENTITY argument and optional owned option of the command.

    The required IDENTITY argument may be the value of the IDENTITY used to
    create the destination or may be the full value of the destination 'Name'
    property. This is the value of the 'Name' property for permanent
    destinations and a component of the 'Name' property for owned destinations.

    If the instance is owned by the current pywbem SubscriptionManager,
    pywbemcli indirectly specifies the Name property value with the format:
    "pywbemdestination:" "<SubscriptionManagerID>" ":" <IDENTITY>``. If the
    destination instance is permanent, the value of the IDENTITY argument
    is the value of the Name property.

    Some listener_destination instances on a server may be static in which
    case the server should generate an exception. Pywbemcli has no way to
    identify these static destinations and they will appear as permanent
    destination instances.

    The --select option can be used if, for some reason, the IDENTITY and
    ownership returns multiple instances. This should only occur in rare cases
    where destination instances have been created by other tools. If the
    --select option is not used pywbemcli displays the paths of the instances
    and terminates the
    command.
    """
    context.execute_cmd(
        lambda: cmd_subscription_remove_destination(context, identity, options))


@subscription_group.command('remove-filter', cls=PywbemtoolsCommand,
                            options_metavar=CMD_OPTS_TXT)
@click.argument('identity', type=str, metavar='IDENTITY', required=True)
@add_options(ownedremove_flag_option)
@add_options(select_option)
@add_options(verify_remove_option)
@add_options(help_option)
@click.pass_obj
def subscription_remove_filter(context, identity, **options):
    """
    Remove an indication filter from the WBEM server.

    Removes a single indication filter instance (CIM_IndicationFilter class)
    from the WBEM server where the instance to be removed is identified by the
    IDENTITY argument and optional --owned option of the command.

    The required IDENTITY argument may be the value of the IDENTITY
    used to create the filter or may be the full value of the filter Name
    property. For permanent filters the value of the Name property is required;
    for owned destinations the IDENTITY component of the Name property is
    sufficient.

    If the instance is owned by the current pywbem SubscriptionManager,
    pywbemcli indirectly specifies the Name property value with the format:
    "pywbemfilter:" "<SubscriptionManagerID>" ":" <IDENTITY>``. If the
    destination instance is permanent, the value of the IDENTITY argument
    is the value of the Name property.

    The --select option can be used if, the IDENTITY and ownership returns
    multiple instances. This should only occur in rare cases where filter
    instances have been created by other tools. If the --select option is not
    used pywbemcli displays the paths of the instances and terminates the
    command.
    """
    context.execute_cmd(
        lambda: cmd_subscription_remove_filter(context, identity, options))


@subscription_group.command('remove-subscription', cls=PywbemtoolsCommand,
                            options_metavar=CMD_OPTS_TXT)
@click.argument('destination-identity', type=str, metavar='DESTINATIONID',
                required=True,)
@click.argument('filter-identity', type=str, metavar='FILTERID', required=True,)
@add_options(verify_remove_option)
@click.option('--remove-associated-instances', is_flag=True,
              default=False,
              help=u'Attempt to remove the instances associated with this '
                   u'subscription. They will only be removed if they do not '
                   u'participate in any other associations.')
@add_options(select_option)
@add_options(help_option)
@click.pass_obj
def subscription_remove_subscription(context, destination_identity,
                                     filter_identity, **options):
    """
    Remove indication subscription from the WBEM server.

    This command removes an indication subscription instance from the
    WBEM server.

    The selection of subscription to be removed is defined by the
    DESTINATIONID and FILTERID arguments which define the Name property of the
    destination and filter associations of the subscription to be
    removed.

    The required DESTINATIONID argument defines the existing destination
    instance that will be attached to the Filter reference of the association
    class. This argument may consist of either the value of the Name property
    of the target destination instance or the identity of that instance.  The
    identity is the full value of the Name property for permanent destinations
    and is a component of the Name property for owned instances. If just the
    identity is used, this will result in multiple destinations being found if
    the same string is defined as the identity of an owned and permanent
    destination.

    The required FILTERID argument defines the existing filter instance that
    will be attached to the 'Filter' reference of the association class. This
    argument may consist of either the value of the 'Name' property of the
    target filter instance or the identity of that instance.  The identity is
    the full value of the 'Name' property for permanent filters and is a
    component of the 'Name' property for owned instances. If just the identity
    is used, this may result in multiple filters being found if the same string
    is defined as the identity of an owned and permanent filter.

    This operation does not remove associated filter or destination instances
    unless the option --remove-associated-instances is included in the command
    and the associated instances are not used in any other association.
    """
    context.execute_cmd(
        # pylint: disable=line-too-long
        lambda: cmd_subscription_remove_subscription(context, destination_identity, filter_identity, options))  # noqa: E501


@subscription_group.command('remove-server', cls=PywbemtoolsCommand,
                            options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def subscription_remove_server(context, **options):
    """
    Remove current WBEM server from the SubscriptionManager.

    This command unregisters owned listeners from the WBEM server and removes
    all owned indication subscriptions, owned indication filters, and owned
    listener destinations for this server-id from the WBEM server.
    """
    context.execute_cmd(
        lambda: cmd_subscription_remove_server(context, options))


#####################################################################
#
# Class to communicate with WBEMSubscriptionManager
#
#####################################################################

def owned_flag_str(owned_flag):
    """Return string owned or all based on boolean owned_flag"""
    return "owned" if owned_flag else "permanent"


class CmdSubscriptionManager(object):
    """
    Encapsulate the initial parsing and common variables of subscriptions in
    a single class and provide a set of methods that mirror the
    SubscriptionManager class but for the defined subscription manager id and
    server id.

    All communication with the WBEMSubscriptionManager pass through this class
    and exceptions from WBEMSubscriptionManager are captured in these
    methods to simplify the command action functions.

    Some of the WBEMSubscriptionManager methods have been compressed from
    multiple (owned/all) methods into a single method with an owned parameter.
    """
    def __init__(self, context, options):
        """
        Initialize the CmdSubscriptionManager instance and the
        WBEMSubscriptionManager instance with the subscriptionmananager_id
        defined.  This retrieves any owned objects from the WBEMServer defined
        by the server_id.
        Parameters:

          context(:class:`'~pywbemtools._context_obj.ContextObj`):
            The pywbemcli context object for the current command passed to
            the action function.

          options :class:`py:dict`:
            The options variable passes to the current command action function.
        """
        if not context.pywbem_server_exists():
            raise click.ClickException("No WBEM server defined.")
        self._context = context
        if 'submgr_id' in options:
            self._submgr_id = options['submgr_id']
        else:
            self._submgr_id = DEFAULT_SUB_MGR_ID

        # ValueError and TypeError fall through. They are real programming
        # errors in this code.
        self._submgr = WBEMSubscriptionManager(
            subscription_manager_id=self._submgr_id)

        # Register the server in the subscription manager and get
        # owned subscriptions, filter, and destinations from server
        # Do not catch Value and Key exceptions. They fall through
        self._server_id = self._submgr.add_server(
            context.pywbem_server.wbem_server)

        # Define the Name property prefix and search pattern for owned filters,
        # etc. This is determined by a constant and the submgr_id string.
        self.owned_destination_prefix = \
            "pywbemdestination:{0}".format(self.submgr_id)
        self.owned_filter_prefix = "pywbemfilter:{0}".format(self.submgr_id)

        self.filter_name_pattern = re.compile(
            r'^pywbemfilter:{0}:([^:]*)$'.format(self.submgr_id))
        self.destination_name_pattern = re.compile(
            r'^pywbemdestination:{0}:([^:]*)$'.format(self.submgr_id))

    @property
    def server_id(self):
        """
        Return the server_id init variable
        """
        return self._server_id

    @property
    def submgr(self):
        """
        Return the submger object instance
        """
        return self._submgr

    @property
    def submgr_id(self):
        """
        Return the subscription manager id string
        """
        return self._submgr_id

    @property
    def context(self):
        """
        return the Click context object supplied to command action function
        """
        return self._context

    # The following methods interface to the pywbem SubscriptionManager.
    # They all catch pywbem Error and some catch other exceptions.

    def get_destinations(self, owned_flag):
        """
        Get the owned indication destinations or all indication
        destinations from WBEMSubscriptionManager. This method uses
        pywbem.SubscriptionManager APIs to return either owned or all
        destination instances based on the owned parameter.

        Parameters:

          owned (:class:`py:bool`):
            If True,return only owned destination instances. Otherwise return
            all destination instances the match to the filter_id or name.

        Returns:
            List of CIM_ListenerDestinationCIMXML objects

        Raises:
            click.ClickException if the request encounters an error.
        """
        try:
            if owned_flag:
                return self.submgr.get_owned_destinations(self.server_id)

            return self.submgr.get_all_destinations(self.server_id)

        except Error as er:
            raise click.ClickException(
                self.err_msg("Get {0} destinations failed".
                             format(owned_flag_str(owned_flag)), er))

    def get_filters(self, owned_flag):
        """
        Get either the owned indication filters or all indication filters from
        WBEMSubscriptionManager. This method uses pywbem.SubscriptionManager
        APIs to return either owned filters or all filters based on the owned
        parameter.

        Parameters:

          owned (:class:`py:bool`):
            If True,return only owned filters. Otherwise return all filters
            the match to the filter_id or name

        Returns:
            List of CIM_IndicationFilter objects

        Raises:
            click.ClickException if the request encounters an error.
        """
        try:
            if owned_flag:
                return self.submgr.get_owned_filters(self.server_id)

            return self.submgr.get_all_filters(self.server_id)

        except Error as er:
            raise click.ClickException(
                self.err_msg("Get {0} filters failed".
                             format(owned_flag_str(owned_flag)), er))

    def get_subscriptions(self, owned_flag):
        """
        Get  subscriptions from the server.  This method uses
        pywbem.SubscriptionManager APIs to return either owned subscriptions
        or all subscriptions based on the owned parameter.

        Parameters:

            owned_flag (:class:`py:bool`):
                True is owned, False is all subscriptions

        Returns:
            list of subscriptions either owned or all subscriptions

        """
        try:
            if owned_flag:
                return self.submgr.get_owned_subscriptions(self.server_id)

            return self.submgr.get_all_subscriptions(self.server_id)

        except Error as er:
            raise click.ClickException(
                self.err_msg("Get {0} subscriptions failed".
                             format(owned_flag_str(owned_flag)), er))

    def add_destination(self, listener_url, owned_flag, destination_id,
                        destination_name, persistence_type=None):
        """
        Add listener destination URLs. Adds one listener destination to
        the current WBEM server target using the Subscription Manager APIs.

        Returns exception if destination already exists.

        See pywbem.WBEMSubscriptionManager.add_destination for parameter
        details.

        Returns:
          Instance created by pywbem SubscriptionManager.

        Raises:
            click.ClickException for all errors
        """
        try:
            dest = self.submgr.add_destination(
                self.server_id, listener_url, owned_flag,
                destination_id, destination_name,
                persistence_type=persistence_type)
            return dest

        # Invalid input parameters exception
        except ValueError as ve:
            raise click.ClickException(
                "add-destination failed: {0}".format(ve))
        except Error as er:
            raise click.ClickException(
                self.err_msg("add-destination {0} failed".
                             format(owned_flag_str(owned_flag)), er))

    def add_filter(self, source_namespaces, query,
                   query_language=DEFAULT_QUERY_LANGUAGE, owned_flag=True,
                   filter_id=None, name=None, source_namespace=None):
        """
        Add an indication filter calls WBEMSubscriptionManager.add_filter and
        captures exceptions.  See WBEMSubscriptionManager for details of
        parameters.

        See pywbem.SubscriptionManager.add_filter for information on
            parameters.

        Returns:
            The created indication filter instance created by
            pywbwm SubscriptionManager.

        Raises:
            click.ClickException for all exceptions received from pywbem
        """
        try:
            return self.submgr.add_filter(
                self.server_id, source_namespaces, query,
                query_language=query_language, owned=owned_flag,
                filter_id=filter_id, name=name,
                source_namespace=source_namespace)

        except (TypeError, ValueError) as exc:
            raise click.ClickException(
                self.err_msg("add-filter failed. Pywbem parameter error", exc))
        except CIMError as ce:
            if ce.status_code == CIM_ERR_ALREADY_EXISTS:
                name_value = filter_id or name
                raise click.ClickException(
                    "add-filter Failed. Filter name='{0}' already exists".
                    format(name_value))

            raise click.ClickException(
                self.err_msg("add-filter failed with server exception", ce))
        except Error as er:
            raise click.ClickException(
                self.err_msg("add-filter failed with server exception", er))

    def add_subscriptions(self, filter_path, destination_paths=None,
                          owned_flag=True):
        """
        Add the subscription defined by filter_path and dest_path. Note that
        if the path of the subscription already exists it is not added.
        The ownership is defined by the ownership of the filter and
        destination and they must match
        """
        try:
            return self.submgr.add_subscriptions(
                self.server_id, filter_path,
                destination_paths=destination_paths,
                owned=owned_flag)

        except ValueError as ex:
            raise click.ClickException(
                "add-subscription failed. pybwem SubscriptionManager "
                "exception: {0}.".format(ex))
        except Error as er:
            raise click.ClickException(
                self.err_msg("add-subscription failed", er))

    def remove_destinations(self, destination_paths):
        """
        Remove the destination instances defined by the destination paths
        parameter.

        Parameters:
            See pywbem.SubscriptionManager.remove_destinations
        Raises:

            Exceptions raised by :class:`~pywbem.WBEMConnection`.
            CIMError: CIM_ERR_FAILED, if there are referencing subscriptions.

        """  # noqa: E501
        try:
            return self.submgr.remove_destinations(self.server_id,
                                                   destination_paths)
        except Error as er:
            raise click.ClickException(
                self.err_msg("remove-destination failed", er))

    def remove_filter(self, filter_path):
        """
        Remove the filter defined by filter_path from the WBEM Server.
        """
        try:
            return self.submgr.remove_filter(self.server_id, filter_path)
        except Error as er:
            raise click.ClickException(
                self.err_msg("remove-filter failed: {0} path: {1} failed".
                             format(er, filter_path), er))

    def remove_subscriptions(self, subscription_paths):
        """
        Remove subscriptions calls the SubscriptionManager remove_subscriptions

        Raises:
            click.ClickException if SubscriptionManager returns exception
        """
        try:
            return self.submgr.remove_subscriptions(self.server_id,
                                                    subscription_paths)
        except Error as er:
            raise click.ClickException(
                self.err_msg("remove-subscriptions failed", er))

    def remove_server(self):
        """
        Remove the WBEM server defined by the server_id from the subscription
        manager and also unregister destinations and remove owned
        destinations, filters, and subscriptions from the server.

        Raises:
            click.ClickException if SubscriptionManager returns exception
        """
        try:
            self.submgr.remove_server(self.server_id)
        except Error as er:
            raise click.ClickException(self.err_msg("remove-Server failed", er))

    # The following are local methods and only call pywbem
    # SubscriptionManager through one of the above methods

    def is_owned_destination(self, instance):
        """
        Test Destination instance/path Name property/key and return True
        if it has correct prefix for owned, type-choice is owned, all, or
        permanent.
        """
        return instance['Name'].startswith(self.owned_destination_prefix)

    def is_owned_filter(self, instance):
        """
        Test Filter instance Name property or instance_path Name key and return
        True if it has correct prefix for owned
        """
        return instance['Name'].startswith(self.owned_filter_prefix)

    def is_owned_subscription(self, instance):
        """
        Test if subscription instance and instance path are owned instances.
        """
        hdlr = self.is_owned_destination(instance.path['Handler'])
        fltr = self.is_owned_filter(instance.path['Filter'])
        return fltr or hdlr

    def _get_permanent_destinations(self):
        """
        Get just the permanent destinations
        """
        all_dests = self.get_destinations(False)
        return [d for d in all_dests if not
                d['Name'].startswith(self.owned_destination_prefix)]

    def _get_permanent_filters(self):
        """
        Get just the permanent filters
        """
        all_filters = self.get_filters(False)
        return [d for d in all_filters if not
                d['Name'].startswith(self.owned_filter_prefix)]

    def _get_permanent_subscriptions(self):
        """
        Get just the permanent subscriptions (all - owned)
        """
        all_subscriptions = self.get_subscriptions(False)
        owned_subscriptions = self.get_subscriptions(True)

        # Future: The test here is excessive. Should test only paths
        return [s for s in all_subscriptions if s not in owned_subscriptions]

    def get_destinations_for_owned_choice(self, choice):
        """
        Get list of destinations based on choice where choice is all, permanent,
        or owned. type-choice is owned, all, or permanent.
        """
        assert choice in ('owned', 'all', 'permanent')
        if choice == 'owned':
            return self.get_destinations(True)
        if choice == 'all':
            return self.get_destinations(False)

        return self._get_permanent_destinations()

    def get_filters_for_owned_choice(self, choice):
        """
        Get list of destinations based on choice where choice is all, permanent,
        or owned.
        """
        assert choice in ('owned', 'all', 'permanent')
        if choice == 'owned':
            return self.get_filters(True)
        if choice == 'all':
            return self.get_filters(False)

        return self._get_permanent_filters()

    def get_subscriptions_for_owned_choice(self, choice):
        """
        Get list of subscriptions based on choice where choice is all,
        permanent, or owned
        """
        assert choice in ('owned', 'all', 'permanent')
        if choice == 'owned':
            return self.get_subscriptions(True)
        if choice == 'all':
            return self.get_subscriptions(False)

        return self._get_permanent_subscriptions()

    def find_destinations_for_name(self, destination_name):
        """
        Find destination instances that match the identity provided
        where the identity is the value of the Name property.
        The identity prefix determines whether the owned or
        all destination list is processed.

          Parameters:
            destination_name (:term:`string`):

          Returns:
            destination instances found that match destination_name or None
            if no destinations with the destination_name parameter exist
        """
        owned_destination_flag = destination_name.startswith(
            self.owned_destination_prefix)

        destinations = self.get_destinations(owned_destination_flag)

        return [f for f in destinations if f['Name'] == destination_name]

    def find_filters_for_name(self, filter_name):
        """
        Find filter instances that match the identity provided
        where the identity is the value of the Name property.
        The name prefix determines whether the owned or
        all filters lists are searched.

          Parameters:
            filter_name (:term:`string`):

          Returns:
            filter instances found that match destination_name or None
            if no destinations with the filter_name parameter exist
        """
        owned_filter_flag = filter_name.startswith(self.owned_filter_prefix)
        filters = self.get_filters(owned_filter_flag)

        return [f for f in filters if f['Name'] == filter_name]

    def err_msg(self, text, er):
        """
        Create a text message from the inputs and return it to the caller.
        """
        return "{0}; {1}: Exception :{2}. Subscription mgr id: '{3}', " \
               "server id: '{4}', " .format(er, text, er.__class__.__name__,
                                            self.submgr, self.server_id)

##########################################################################
#
#   Common functions/classes for this command group
#
##########################################################################


class BaseIndicationObjectInstance(object):
    """
    Base class for the Indication Instances. Common attributes and methods.
    These classes encapsulate the processing for a single indication
    destination, filter, or subscription instance including parsing
    Name property, getting property values, and building the select_id used
    when instances are to be selected from the console.
    """
    def __init__(self, csm, instance):
        """ Initialize common attributes """
        self.csm = csm
        self.instance = instance
        self._owned_flag = None

    @property
    def owned_flag_str(self):
        """
        Returns boolean True if this instance is owned. Otherwise returns False
        """
        return owned_flag_str(self._owned_flag)

    def instance_property(self, property_name):
        """
        Return the value of the property_name in the filter or an empty
        string
        """
        return self.instance.get(property_name, "")


class IndicationDestination(BaseIndicationObjectInstance):
    """
    Process an IndicationDestination instance to create values for owned,
    other identity characteristics.
    """
    def __init__(self, csm, destination_instance):
        """
        Initialize the object and parse the identity for components
        """
        super(IndicationDestination, self).__init__(csm, destination_instance)

        m = re.match(csm.destination_name_pattern,
                     self.instance.path.keybindings['Name'])

        self._owned_flag = bool(m)

        self.destination_id = m.group(1) if m else ""
        self.destination_name = "" if m else \
            self.instance.path.keybindings['Name']

        self.identity = self.destination_id if self._owned_flag \
            else self.destination_name

    def select_id_str(self):
        """
        Build an identification string for use in picking destinations.
        Consists of ownership, url, destination property and name
        Returns path without namespace as string to use in select.
        """
        path = self.instance.path.copy()
        path.namespace = None
        return str(path)


class IndicationFilter(BaseIndicationObjectInstance):
    """
    Class that contains name property parsing and other common methods for
    procesing indication filter instances
    """
    def __init__(self, csm, filter_instance):
        super(IndicationFilter, self).__init__(csm, filter_instance)

        path_ = filter_instance.path
        m = re.match(csm.filter_name_pattern, path_.keybindings['Name'])
        self._owned_flag = bool(m)

        self.filter_id = m.group(1) if m else ""
        self.filter_name = "" if m else path_.keybindings['Name']

        self.identity = self.filter_id if self._owned_flag else self.filter_name

    def select_id_str(self):
        """
        Build an identification string for use in picking filters. This includes
        properties from the instance that help to determine its uniqueness.
        The Name property cannot always be this because the owned name is too
        long so only the filter_id is used in this case and is not the
        only item that can distinguish filters.
        """
        path = self.instance.path.copy()
        path.namespace = None
        return str(path)


class IndicationSubscription(BaseIndicationObjectInstance):
    """
    Process an IndicationSubscription instance to create values for owned,
    other identity characteristics.
    """
    def __init__(self, csm, subscription_instance):
        super(IndicationSubscription, self).__init__(csm, subscription_instance)
        self._owned_flag = csm.is_owned_subscription(subscription_instance)

    def select_id_str(self):
        """
        Build an identification string for use in picking subscriptions.  This
        short string contains information from the associated filter
        and destination instances.
        """
        conn = self.csm.context.pywbem_server.conn
        filter_inst = conn.GetInstance(self.instance.path['Filter'])
        dest_inst = conn.GetInstance(self.instance.path['Handler'])

        # Get filter and destination select_id_str strings
        filterinst = IndicationFilter(self.csm, filter_inst)
        filter_str = filterinst.select_id_str()

        destinst = IndicationDestination(self.csm, dest_inst)
        dest_str = destinst.select_id_str()

        return '{0} {1} {2}'.format(self._owned_flag, dest_str, filter_str)


def display_inst_nonnull_props(context, options, instances, output_format):
    """
    Display the instances defined in instances after removing any properties
    that are Null for all instances.
    """
    pl = None
    # Create a dictionary of all properties that have non-null values
    pldict = {}
    for inst in instances:
        for name, prop in inst.properties.items():
            if prop.value:
                pldict[name] = True
    pl = list(pldict.keys())

    display_cim_objects(context, instances, output_format,
                        summary=options['summary'], property_list=pl)


def pick_one_inst_from_instances_list(csm, instances, pick_msg):
    """
    Pick one instance from list using pywbemcli pick method.
    Presents list of paths to user and returns with picked instance
    """
    path = pick_one_path_from_instances_list(csm, instances, pick_msg)
    rtn_inst = [i for i in instances if i.path == path]
    assert len(rtn_inst) == 1
    return rtn_inst[0]


def pick_one_path_from_instances_list(csm, instances, pick_msg):
    """
    Pick one instance from list using the pywbemcli pick method.
    This presents list of instance information to user and returns with picked
    object path.

    Returns:
        Instance path of instance selected.

    Raises:
        click.ClickException for any error.
    """
    assert instances is not None
    instances = sort_cimobjects(instances)
    paths = [inst.path for inst in instances]

    # Get the short info() string for the class defined for this instance
    if paths[0].classname == FILTER_CLASSNAME:
        display_list = \
            [IndicationFilter(csm, i).select_id_str() for i in instances]
    elif paths[0].classname == DESTINATION_CLASSNAME:
        display_list = \
            [IndicationDestination(csm, i).select_id_str() for i in instances]
    elif paths[0].classname == SUBSCRIPTION_CLASSNAME:
        display_list = \
            [IndicationSubscription(csm, i).select_id_str() for i in instances]
    else:
        click.echo("Class {0} is not one of pywbem subscription mgr classes".
                   format(paths[0].classname))
        display_list = paths
    try:
        index = pick_one_index_from_list(csm.context, display_list, pick_msg)
        return paths[index]
    except ValueError as exc:
        raise click.ClickException(str(exc))


def resolve_instances(csm, instances, identity, obj_type_name,
                      select_opt, cmd_str):
    """
    Resolve list of instances to a single instance or exception.
    If select_opt, ask user to select.  Otherwise, generate
    exception with info for each object to help user pick.

      Parameters:
        csm (csm object):

        instances (list)
            List of instances that are canidates to be used where only
            one is allowed.

        identity (:term:`string`):
            String defining the identity that selected the instances.
            Used in the select statement as part of the prompt.

        object_type_name (:term: String):
            either 'destination' or 'filter'. Used in exception messages.

        select_opt (:class:`py:bool`):
            The value of the select option.  If True, the the prompt for
            the user to select one of the list of instances will be
            presented.  If False, the command will be terminated with

        cmd_str (:term:`string`)
            The name of the command ('add' or 'remove') to be used in
            the displays

    Returns:
        One of the instances in instances if it matches the identity
        string

    Raises:
        click.ClickException:  This terminates the current command

    """
    # Exception, at least one instance must exist.
    if not instances:
        raise click.ClickException("No {0} found for identity: {1}".
                                   format(obj_type_name, identity))
    # Return the single item
    if len(instances) == 1:
        return instances[0]

    # Ask user to pick one from list with prompt
    if select_opt:
        # FUTURE: Need better than path for prompt info.
        inst = pick_one_inst_from_instances_list(
            csm, instances, "Pick one {0} to use for {1}:".
            format(obj_type_name, cmd_str))
        return inst

    # Generate an exception with summary info on the instances
    paths_str = "\n  *".join([str(i.path) for i in instances])
    raise click.ClickException(
        "The identity: '{0}' returned multiple {1} instances. "
        "Use --select option to pick one instance from:\n  * {2}".
        format(identity, obj_type_name, paths_str))


def get_insts_for_subscription_identities(csm, destination_identity,
                                          filter_identity, cmd_str,
                                          select_opt):
    """
    Identity resolution for add and remove subscriptions where two identities
    are provided as arguments for the command. Returns the instances
    found or an exception if no instances for the destination and filter found.
    The identity can be either the full name as target or only the
    id suffix of an owned element.

    Returns: Two instances, instance of destination and instance of
        filter if the identties match.
    """
    # Initial and only search if destination includes owned prefix
    destination_id_owned = destination_identity.startswith(
        csm.owned_filter_prefix)

    # Searches for match to the identity value provided
    # FUTURE: may have issue here in that we have identity without ownership
    destination_instances = csm.find_destinations_for_name(destination_identity)

    # If the Identity  does not include owned prefix, search also for
    # the full owned name
    if not destination_id_owned:
        d2 = csm.find_destinations_for_name(
            "{0}:{1}".format(csm.owned_destination_prefix,
                             destination_identity))
        if d2:
            destination_instances.extend(d2)

    # Resolve to a single instance or use select if set or fail if resolve
    # returns multiple instances.
    sub_destination_inst = resolve_instances(
        csm, destination_instances, destination_identity,
        'destination', select_opt, cmd_str)

    filter_id_owned = filter_identity.startswith(csm.owned_filter_prefix)
    filter_instances = csm.find_filters_for_name(filter_identity)

    # If Identity not specifically owned, look also in owned with the owned
    # prefix. This may result  in multiples that must be resolved
    if not filter_id_owned:
        f2 = csm.find_filters_for_name("{0}:{1}".format(
            csm.owned_filter_prefix, filter_identity))
        if f2:
            filter_instances.extend(f2)

    sub_filter_inst = resolve_instances(csm, filter_instances, filter_identity,
                                        'filter', select_opt, cmd_str)

    return sub_destination_inst, sub_filter_inst


#####################################################################
#
#  Command action functions for each subcommands in the subscription group
#
#####################################################################

def get_CmdSubscriptionManager(context, options):
    """
    Get the instance of CmdSubscriptionManager from the context or
    instantiate a new instance.  All subscription action functions should
    call this method to set up the instance of subscription manager and
    cache that instance in the context PywbemServer.
    """
    if not context.pywbem_server_exists():
        raise click.ClickException("No WBEM server defined.")

    if context.pywbem_server.subscription_manager:
        return context.pywbem_server.subscription_manager
    csm = CmdSubscriptionManager(context, options)
    context.pywbem_server.subscription_manager = csm
    return context.pywbem_server.subscription_manager


def cmd_subscription_add_destination(context, identity, options):
    """
    Add indication destination CIM instance to wbem server.
    """
    csm = get_CmdSubscriptionManager(context, options)

    owned_flag_opt = options['owned']
    destination_id = identity if owned_flag_opt else None
    destination_name = None if owned_flag_opt else identity

    # FUTURE: Should we make this an input parameter under some circumstances.
    # ex. if name, we could set transient or permanent. Always transient
    # if filter_id has value.
    persistence_type = "transient" if destination_id else "permanent"

    # For permanent destinations. test if  destination already exists before
    # making request.
    # We do not allow permanent destinations with same name property
    # independent of complete path being equal to keep Name properties unique
    if not owned_flag_opt:
        dests = csm.find_destinations_for_name(destination_name)
        if dests:
            dests_str = ", ".join([str(d.path) for d in dests])
            raise click.ClickException(
                "{0} destination: Name=[{1}] add failed. Duplicates URL of "
                "existing destination(s): [{2}. Pywbemcli does not allow "
                "permanent destinations with same Name property to keep Name "
                "properties unique.".
                format(owned_flag_str(owned_flag_opt), destination_name,
                       dests_str))

    destination_result = csm.add_destination(
        options['listener_url'], owned_flag_opt, destination_id,
        destination_name, persistence_type=persistence_type)

    # Success: Show resulting name and conditionally, details
    context.spinner_stop()

    # If the URL, etc. of this owned add matches an existing owned destination
    # pywbem returns the existing destination which has different name.
    if owned_flag_opt and not destination_result['Name'].endswith(
            ":{}".format(destination_id)):
        rslt_info = IndicationDestination(csm, destination_result)
        raise click.ClickException(
            "{0} destination: Name={1} Not added. Duplicates URL of "
            "existing {2} destination: {3} URL: {4} PersistenceType: {5}.".
            format(owned_flag_str(owned_flag_opt),
                   destination_id,
                   rslt_info.owned_flag_str,
                   destination_result['Name'],
                   destination_result['Destination'],
                   destination_result['PersistenceType']))
    click.echo(
        "Added {0} destination: Name={1}".
        format(owned_flag_str(owned_flag_opt), destination_result['Name']))

    if context.verbose:
        click.echo("\npath={0}\n\n{1}".
                   format(str(destination_result.path),
                          destination_result.tomof()))


def cmd_subscription_add_filter(context, identity, options):
    """
    Add a filter defined by the input argument to the target server.
    """
    csm = get_CmdSubscriptionManager(context, options)
    owned_flag_opt = options['owned']
    filter_id = identity if owned_flag_opt else None
    filter_name = None if owned_flag_opt else identity

    # Get source namespaces, multiple strings in tuple and/or
    # multiple namespace names comma-separated in any string in tuple.
    # NOTE: SubscriptionManager requires list as input, not tuple
    source_ns_opt = options['source_namespaces'] or \
        [context.pywbem_server.conn.default_namespace]
    source_namespaces = []
    for ns in source_ns_opt:
        if ',' in ns:
            source_namespaces.extend(ns.split(','))
        else:
            source_namespaces.append(ns)

    if not owned_flag_opt:
        filters = csm.find_filters_for_name(filter_name)
        if filters:
            filters_str = ", ".join([str(f.path) for f in filters])
            raise click.ClickException(
                "{0} filter: Name=[{1}] add failed. Duplicates URL of "
                "existing filters(s): [{2}. Pywbemcli does not allow "
                "permanent filters with same Name property to keep Name "
                "properties unique.".
                format(owned_flag_str(owned_flag_opt), filter_name,
                       filters_str))

    result_inst = csm.add_filter(source_namespaces, options['query'],
                                 options['query_language'],
                                 owned_flag_opt, filter_id,
                                 filter_name)

    # Success: Show resulting name and conditionally, details
    context.spinner_stop()
    click.echo("Added {0} filter: Name={1}".
               format(owned_flag_str(owned_flag_opt), result_inst['Name']))

    if context.verbose:
        click.echo("\npath={0}\n\n{1}".
                   format(str(result_inst.path), result_inst.tomof()))


def cmd_subscription_add_subscription(context, destination_identity,
                                      filter_identity, options):
    """
    Add a subscription based on selected a filter and destination.

    The owned option defines the ownership of the resulting indication
    subscription.

    If the owned option is True, either owned or permanent filters and
    listeners may be attached.

    If the owned option is False (--permanent) only permanent filters and
    listeners may be attached
    """
    csm = get_CmdSubscriptionManager(context, options)

    owned_flag_opt = options['owned']
    select_opt = options['select']

    # Search the existing filters and destinations to find instances
    # that match the destination_identity and filter_identity
    sub_dest_inst, sub_filter_inst = get_insts_for_subscription_identities(
        csm, destination_identity, filter_identity, 'add-subscription',
        select_opt)

    # Duplicates test in SubscriptionManager but with message for parameters of
    # the command rather than the pywbem API.
    if (csm.is_owned_filter(sub_filter_inst) or
            csm.is_owned_destination(sub_dest_inst)) and not owned_flag_opt:
        raise click.ClickException(
            "Permanent subscriptions cannot be created with owned filters "
            "or destinations. Create an owned subscription or use a "
            "permanent filter and destination. Destination Name={0}, "
            "Filter Name={1}".format(sub_dest_inst['Name'],
                                     sub_filter_inst['Name']))

    rslt = csm.add_subscriptions(sub_filter_inst.path,
                                 sub_dest_inst.path, owned_flag_opt)

    context.spinner_stop()
    click.echo("Added {0} subscription: DestinationName={1}, FilterName={2}".
               format(owned_flag_str(owned_flag_opt),
                      sub_dest_inst.path['Name'],
                      sub_filter_inst.path["Name"]))
    if context.verbose:
        click.echo("\n\n{0}".format(rslt[0].tomof()))


def cmd_subscription_list(context, options):
    """
    Display overview information on the subscriptions, filters and indications
    """

    # If --detail set, execute call to list all of the tables but
    # with some options set to False
    if options['detail']:
        options['names_only'] = False
        options['detail'] = False
        cmd_subscription_list_destinations(context, options)
        click.echo("\n")
        cmd_subscription_list_filters(context, options)
        click.echo("\n")
        cmd_subscription_list_subscriptions(context, options)
        return

    output_format = validate_output_format(context.output_format,
                                           ['TEXT', 'TABLE'],
                                           default_format="table")
    csm = get_CmdSubscriptionManager(context, options)

    summary_opt = options['summary']

    all_subscriptions = csm.get_subscriptions_for_owned_choice(ALL_STR)
    all_destinations = csm.get_destinations_for_owned_choice(ALL_STR)
    all_filters = csm.get_filters_for_owned_choice(ALL_STR)

    owned_subscriptions = csm.get_subscriptions(OWNED_STR)
    owned_destinations = csm.get_destinations(OWNED_STR)
    owned_filters = csm.get_filters(OWNED_STR)

    if summary_opt:
        headers = ['subscriptions', 'filters', 'destinations']
        rows = [[len(all_subscriptions), len(all_filters),
                 len(all_destinations)]]

    else:
        headers = ['CIM_class', 'owned', 'permanent', 'all']

        rows = []
        rows.append([SUBSCRIPTION_CLASSNAME,
                     len(owned_subscriptions),
                     len(all_subscriptions) - len(owned_subscriptions),
                     len(all_subscriptions)])
        rows.append([FILTER_CLASSNAME,
                     len(owned_filters),
                     len(all_filters) - len(owned_filters),
                     len(all_filters)])
        rows.append([DESTINATION_CLASSNAME,
                     len(owned_destinations),
                     len(all_destinations) - len(owned_destinations),
                     len(all_destinations)])
        # pylint: disable=consider-using-generator
        rows.append(["TOTAL INSTANCES",
                     sum([r[1] for r in rows]),
                     sum([r[2] for r in rows]),
                     sum([r[3] for r in rows])])

    summary_str = "summary" if summary_opt else ""
    title = "Subscription instance {0} counts: submgr-id={1}, svr-id={2}". \
            format(summary_str, csm.submgr_id, csm.server_id)

    context.spinner_stop()
    if output_format_is_table(output_format):
        click.echo(format_table(rows, headers, title=title,
                                table_format=output_format))

    else:  # output in TEXT format
        if summary_opt:
            click.echo("{0} subscriptions, {1} filters, {2} destinations".
                       format(len(all_subscriptions), len(all_filters),
                              len(all_destinations)))
        else:
            for row in rows:
                click.echo("{0}: {1}, {2}, {3}".format(row[0], row[1], row[2],
                                                       row[3]))


def get_reference_count(subscription_paths, inst_name, role):
    """
    Get count of references to object_name for role in
    CIM_IndicationSubscription instances.  This implements

    The alternate path covers cases where references returns an error

    Returns: int
      Count of instance that match the reference definition

    Raises:
       ClickException if Error exception occurs
    """
    cnt = sum(path[role] == inst_name for path in subscription_paths)

    return cnt


def cmd_subscription_list_destinations(context, options):
    """
    List the subscription destinations objects found on the current connection.

    Since these are complex objects there are a variety of display options
    including table, CIM objects, etc.
    """
    output_format = validate_output_format(context.output_format,
                                           ['CIM', 'TABLE'],
                                           default_format="table")
    csm = get_CmdSubscriptionManager(context, options)

    ownedchoice_opt = (options['type']).lower()

    destinations = csm.get_destinations_for_owned_choice(ownedchoice_opt)

    if output_format_is_cimobject(output_format):
        if options['names_only']:
            paths = [inst.path for inst in destinations]
            display_cim_objects(context, paths, output_format)
        elif options['detail']:
            display_inst_nonnull_props(context, options, destinations,
                                       output_format)
        else:
            display_cim_objects(context, destinations, output_format,
                                summary=options['summary'])

    elif output_format_is_table(output_format):
        if options['names_only']:
            paths = [inst.path for inst in destinations]
            display_cim_objects(context, paths, output_format)
            return

        headers = ['Ownership', 'Identity', 'Name\nProperty', 'Destination',
                   'Persistence\nType', 'Protocol', 'Subscription\nCount']
        if options['detail']:
            headers.extend([
                'CreationclassName', 'SystemCreationClassName', 'SystemName'])
        rows = []

        # FUTURE: summary with table not covered.

        # subscription_paths = [s.path for s in csm.get_subscriptions(False)]
        subscription_paths = [s.path for s in
                              csm.get_subscriptions_for_owned_choice("all")]
        for dest in destinations:
            ref_cnt = get_reference_count(subscription_paths,
                                          dest.path, 'Handler')

            d = IndicationDestination(csm, dest)
            row = [d.owned_flag_str,
                   d.identity,
                   fold_strings(d.instance_property('Name'), 30,
                                break_long_words=True),
                   d.instance_property('Destination'),
                   d.instance_property('PersistenceType'),
                   d.instance_property('Protocol'),
                   ref_cnt]
            if options['detail']:
                row.extend([d.instance_property('CreationClassName'),
                            d.instance_property('SystemCreationClassName'),
                            d.instance_property('SystemName')])

            rows.append(row)

        title = "Indication Destinations: submgr-id={0}, svr-id={1}, " \
            "type={2}". \
            format(csm.submgr_id, csm.server_id, ownedchoice_opt)

        context.spinner_stop()
        click.echo(format_table(rows, headers, title=title,
                                table_format=output_format))

    else:
        assert False, "{0} Invalid output format for this command". \
            format(output_format)


def cmd_subscription_list_filters(context, options):
    """
    List the indication filters found in the current SubscriptionManager
    object
    """
    output_format = validate_output_format(context.output_format,
                                           ['CIM', 'TABLE'],
                                           default_format="table")
    csm = get_CmdSubscriptionManager(context, options)

    filterchoice_opt = options['type']
    details_opt = options['detail']

    filters = csm.get_filters_for_owned_choice(filterchoice_opt)

    if output_format_is_cimobject(output_format):
        if options['names_only']:
            paths = [inst.path for inst in filters]
            display_cim_objects(context, paths, output_format,
                                options['summary'])
        elif options['detail']:
            display_inst_nonnull_props(context, options, filters,
                                       output_format)
        else:
            display_cim_objects(context, filters, output_format,
                                summary=options['summary'])

    elif output_format_is_table(output_format):
        if options['names_only']:
            paths = [inst.path for inst in filters]
            display_cim_objects(context, paths, output_format)
            return
        headers = ['Ownership', 'Identity', 'Name\nProperty', 'Query',
                   'Query\nLanguage', 'Source\nNamespaces',
                   'Subscription\nCount']
        if options['detail']:
            headers.extend(
                ['CreationclassName', 'SystemCreationClassName',
                 'SystemName'])

        rows = []
        subscription_paths = [s.path for s in
                              csm.get_subscriptions_for_owned_choice("all")]
        for filter_ in filters:
            ref_cnt = get_reference_count(subscription_paths,
                                          filter_.path, 'Filter')

            f = IndicationFilter(csm, filter_)
            row = [f.owned_flag_str,
                   f.identity,
                   fold_strings(f.instance_property('Name'), 30,
                                break_long_words=True),
                   fold_strings(f.instance_property('Query'), 25),
                   f.instance_property('QueryLanguage'),
                   "\n".join(f.instance_property('SourceNamespaces')),
                   ref_cnt]
            if details_opt:
                row.extend([
                    f.instance_property('CreationClassName'),
                    f.instance_property('SystemCreationClassName'),
                    f.instance_property('SystemName')])
            rows.append(row)
        title = "Indication Filters: submgr-id={0}, svr-id={1} type={2}". \
            format(csm.submgr_id, csm.server_id, filterchoice_opt)

        context.spinner_stop()
        click.echo(format_table(rows, headers, title=title,
                                table_format=output_format))

    else:
        assert False, "{0} Invalid output format for this command". \
            format(output_format)


def cmd_subscription_list_subscriptions(context, options):
    """
    Display the list of indication subscriptions on the defined server.
    """
    output_format = validate_output_format(context.output_format,
                                           ['CIM', 'TABLE'],
                                           default_format="table")
    csm = get_CmdSubscriptionManager(context, options)

    svr_subscriptions = csm.get_subscriptions_for_owned_choice(options['type'])
    # Get all destinations and filters
    svr_destinations = csm.get_destinations(False)
    svr_filters = csm.get_filters(False)
    details_opt = options['detail']

    # Otherwise display subscriptions, indications, filters.
    # For each subscription, display the subscription, filter,
    # and destination
    inst_list = []
    if output_format_is_cimobject(output_format):
        for subscription in svr_subscriptions:
            inst_list.append(subscription)
            # Only show handler and filter instances if detail option
            if details_opt:
                for filter_ in svr_filters:
                    if subscription.path['Filter'] == filter_.path:
                        inst_list.append(filter_)
                for dest in svr_destinations:
                    if subscription.path['Handler'] == dest.path:
                        inst_list.append(dest)
        if options['names_only']:
            paths = [inst.path for inst in svr_subscriptions]
            display_cim_objects(context, paths, output_format,
                                options['summary'])
        elif options['summary'] or not details_opt:
            display_cim_objects(context, inst_list,
                                output_format='mof', summary=options['summary'])
        elif details_opt:
            display_inst_nonnull_props(context, options, inst_list,
                                       output_format)
        else:
            display_cim_objects(context, inst_list, output_format,
                                summary=options['summary'])

    elif output_format_is_table(output_format):
        if options['names_only']:
            paths = [inst.path for inst in svr_subscriptions]
            display_cim_objects(context, paths, output_format)
            return
        headers = ['Ownership', 'Handler\nIdentity', 'Filter\nIdentity',
                   'Handler\nDestination', 'Filter\nQuery',
                   'Filter Query\nlanguage', 'Subscription\nStartTime']
        if details_opt:
            headers.extend(
                ['TimeOfLast\nStateChange', 'Subscription\nState'])

        rows = []
        conn = context.pywbem_server.conn
        for subscription in svr_subscriptions:
            is_ = IndicationSubscription(csm, subscription)

            try:
                filter_inst = conn.GetInstance(subscription.path['Filter'])
                dest_inst = conn.GetInstance(subscription.path['Handler'])
            except Error as er:
                raise click.ClickException("GetInstance Failed {0}".format(er))

            id_ = IndicationDestination(csm, dest_inst)
            if_ = IndicationFilter(csm, filter_inst)

            start_time = is_.instance_property('SubscriptionStartTime')
            start_time = start_time.datetime.strftime("%x %X") if start_time \
                else ""

            row = [is_.owned_flag_str,
                   "{0}({1})".format(id_.identity, id_.owned_flag_str),
                   "{0}({1})".format(if_.identity, if_.owned_flag_str),
                   dest_inst['Destination'],
                   fold_strings(if_.instance_property('query'), 30),
                   filter_inst['QueryLanguage'],
                   start_time]
            if details_opt:
                row.extend([
                    is_.instance_property('CreationClassName'),
                    is_.instance_property('SystemCreationClassName')])
            rows.append(row)

        title = "Indication Subscriptions: submgr-id={0}, svr-id={1}, " \
            "type={2}".format(csm.submgr_id, csm.server_id, options['type'])

        context.spinner_stop()
        click.echo(format_table(rows, headers, title=title,
                                table_format=output_format))

    else:
        assert False, "{0} Invalid output format for this command". \
            format(output_format)


def verify_instances_removal(instance_names, instance_type):
    """Request that user verify instances to be removed."""

    if isinstance(instance_names, list):
        verify_paths = "\n".join([str(p) for p in instance_names])
    else:
        verify_paths = instance_names

    verify_msg = "Verify {0} instance(s) to be removed:\n {1}". \
        format(instance_type, verify_paths)

    if not verify_operation(verify_msg):
        raise click.ClickException("Instances not removed.")


def cmd_subscription_remove_destination(context, identity, options):
    """
    Remove multiple destination objects from the WBEM Server.
    """
    csm = get_CmdSubscriptionManager(context, options)
    owned_flag_opt = options['owned']

    if owned_flag_opt and not identity.startswith(csm.owned_destination_prefix):
        target_name = "{0}:{1}".format(csm.owned_destination_prefix, identity)
    else:
        target_name = identity

    dest_insts = csm.get_destinations(owned_flag_opt)
    matching_destinations = [d for d in dest_insts if d['Name'] == target_name]

    if not matching_destinations:
        raise click.ClickException(
            "No {0} destination found for identity={1}, Name-property={2}".
            format(owned_flag_str(owned_flag_opt), identity, target_name))

    if len(matching_destinations) == 1:
        destination_path = matching_destinations[0].path

    else:  # Multiple instances returned
        context.spinner_stop()
        click.echo('{0} "{1}" multiple matching destinations'.
                   format(owned_flag_str(owned_flag_opt), identity))

        if options['select']:
            destination_path = pick_one_path_from_instances_list(
                csm, matching_destinations,
                "Pick indication destination to remove")
        else:
            inst_display = [IndicationDestination(csm, d).select_id_str() for
                            d in matching_destinations]
            raise click.ClickException(
                "Remove failed. Multiple destinations meet criteria "
                "identity={0}, owned={1}. Use --select option to pick one "
                "destination:\n  * {2}".
                format(identity, owned_flag_str(owned_flag_opt),
                       "\n  * ".join(inst_display)))

    if options['verify']:
        verify_instances_removal(destination_path, 'destination')

    name_property = destination_path['Name']
    csm.remove_destinations(destination_path)

    context.spinner_stop()
    click.echo("Removed {0} indication destination: identity={1}, Name={2}.".
               format(owned_flag_str(owned_flag_opt), identity, name_property))
    if context.verbose:
        click.echo("indication destination path: {0}.".format(destination_path))

    return


def cmd_subscription_remove_filter(context, identity, options):
    """
    Remove a single indication filter found by the get_all_filters
    method.
    """
    csm = get_CmdSubscriptionManager(context, options)

    owned_flag_opt = options['owned']

    # Determine if name should include owned identity components.
    # Search depends on correct definition of owned option.
    if owned_flag_opt and not identity.startswith(csm.owned_filter_prefix):
        target_name = "{0}:{1}".format(csm.owned_filter_prefix, identity)
    else:
        target_name = identity

    filter_insts = csm.get_filters(owned_flag_opt)
    matching_filters = [f for f in filter_insts if f['Name'] == target_name]

    if not matching_filters:
        raise click.ClickException(
            "No {0} filter found for identity={1}, Name-property={2}, ".
            format(owned_flag_str(owned_flag_opt), identity, target_name))
    # Multiples can only occur if outside client has added filters that match
    # name but not other components of path. Owned flag on cmd eliminates
    # multiples if permanent and owned ids are the same.
    if len(matching_filters) > 1:
        context.spinner_stop()
        click.echo('{0} "{1}" multiple matching filters.'.
                   format(owned_flag_str(owned_flag_opt), identity))

        if options['select']:
            filter_path = pick_one_path_from_instances_list(
                csm, matching_filters, "Pick indication filter to remove")
        else:
            inst_disp = [IndicationFilter(csm, f).select_id_str()
                         for f in matching_filters]
            raise click.ClickException(
                "Remove failed. Multiple filters meet criteria identity={0}, "
                "owned={1}. Use --select option to pick one filter:\n  * {2}".
                format(identity, owned_flag_str(owned_flag_opt),
                       "\n  * ".join(inst_disp)))

    else:  # one filter returned
        filter_path = matching_filters[0].path

    if options['verify']:
        verify_instances_removal(filter_path, 'filter')

    name_property = filter_path['Name']
    csm.remove_filter(filter_path)

    context.spinner_stop()
    click.echo("Removed {0} indication filter: identity={1}, Name={2}.".
               format(owned_flag_str(owned_flag_opt), identity, name_property))
    if context.verbose:
        click.echo("Indication filter path: {0}.".format(filter_path))

    return


def cmd_subscription_remove_subscription(context, destination_identity,
                                         filter_identity, options):
    """
    Remove an indication subscription from the WBEM server. Removal is based
    on the same parameter set as create, a destination and filter because
    there is no identifying name on subscriptions.
    """
    csm = get_CmdSubscriptionManager(context, options)

    # find instances for the associations using the input identity parameters
    dest_inst, filter_inst = get_insts_for_subscription_identities(
        csm, destination_identity, filter_identity, 'remove-subscription',
        options['select'])

    # FUTURE: account for multiples subscription cases.
    # FUTURE: account for owned/not-owned from the dest and filters when that
    # works.

    subscriptions = csm.get_subscriptions(False)

    # Find the subscription defined by destination_identity and filter_identity
    remove_list = []

    for subscription in subscriptions:
        if subscription.path['Filter'] == filter_inst.path and \
                subscription.path['Handler'] == dest_inst.path:
            remove_list.append(subscription)

    if not remove_list:
        raise click.ClickException(
            "Arguments destination_id={0} and filter_id={1} did not locate "
            "any subscriptions to remove."
            .format(destination_identity, filter_identity))

    if remove_list:
        remove_paths = [i.path for i in remove_list]

        if options['verify']:
            verify_instances_removal(remove_paths, 'subscription')

        # Get the list of destination paths to possibly remove these
        # associations.
        destination_paths = [i.path['Handler'] for i in remove_list]
        filter_paths = [i.path['Filter'] for i in remove_list]

        csm.remove_subscriptions(remove_paths)

        context.spinner_stop()
        click.echo("Removed {0} subscription(s) for destination-id: {1}, "
                   "filter-id: {2}.".
                   format(len(remove_paths), destination_identity,
                          filter_identity))

        if context.verbose:
            subscription_paths_str = '\n'.join([str(x) for x in remove_paths])
            click.echo("Removed subscription(s) paths: {0}".
                       format(subscription_paths_str))

        # If option set, remove filter and destination if not used in other
        # associations:
        # FUTURE: should we only remove owned instances???
        if options['remove_associated_instances']:
            conn = context.pywbem_server.conn
            for dest_path in destination_paths:
                dest_refs = conn.ReferenceNames(
                    dest_path, ResultClass=SUBSCRIPTION_CLASSNAME,
                    Role='Handler')
                if not dest_refs:
                    csm.remove_destinations(dest_path)
                    click.echo("Removed destination: {0}".
                               format(dest_path))
            for filter_path in filter_paths:
                filter_refs = conn.ReferenceNames(
                    filter_path, ResultClass=SUBSCRIPTION_CLASSNAME,
                    Role='Filter')
                if not filter_refs:
                    csm.remove_filter(filter_path)
                    click.echo("Removed filter: {0}".format(filter_path))


def cmd_subscription_remove_server(context, options):
    """
    Remove the current server_id which also un-registers listener destinations
    and removes all owned destinations, filters, and subscriptions.
    """
    csm = get_CmdSubscriptionManager(context, options)

    filters = csm.get_filters(True)
    dests = csm.get_destinations(True)
    subscripts = csm.get_subscriptions(True)

    context.spinner_stop()
    click.echo("Removing owned destinations, filters, and subscriptions "
               "for server-id {0}. Remove counts: destinations={1}, "
               "filters={2}, subscriptions={3}".
               format(csm.server_id, len(dests), len(filters), len(subscripts)))

    csm.remove_server()
    context.pywbem_server.subscription_manager = None
