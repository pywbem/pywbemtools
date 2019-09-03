Design Document for a PyWBEM Command Line Browser
=================================================


Status: In Process
Date: 9 Feb. 2017

Update: 11 Feb 2017

Update: 20 Feb 2017 - Add more subcommands and define characteristics of
        create instances and invoke method.

Update: 27 Feb 2017 - Clarify further the taxonomy and try to reduce the
        number of different subcommands (i.e. list vs enumerate)

Goals
-----
* Provide the capability to inspect and manage WBEM Servers and in particular
  WBEM Servers compatible with the DMTF and SNIA specifications from a command
  line interface.
* Use the pywbem API and classes as the basis for interfacing with WBEM
  servers
* This is primarily a user tool and not an internal test tool so it needs
  to protect the user and provide as much convience as possible for the user.
* Usable effectively by both occasional and power users:

  * Interactive mode - Use a REPL so that within pywbemcli the user can
    execute multiple commands without exiting the pywbemcli shell. Thus, the
    user can make a connection and then explore that connection with multiple
    commands.
  * Script mode (complete command entered from command line)
* Capable of executing all WBEM CIM-XML operations (with specific exceptions)
* Include commands for other operations that will be a real advantage to
  developers, users, etc.
* Integrated help to minize requirement for external documentation.
* Python based and pure python implementation so that it can be used almost
  any python environment.
* Expandable. Users should be able to add functionality with plugins


To make this really usable for testers, developers, etc. we need to
provide a rich set of display/analysis tools within the tool.  Just
having an implementation of the 20 some cim/xml operations is NOT sufficient.
We want the user to be able to see:

* Structure information on the WBEM server environment; how components relate
  to one another.  This means showing a visutal reprentation of the
  hierarchy of multiple items like classes and associations
* Size information on the environment (how many instances, classes, etc.)
* Time sequences of changing things within the environment
* etc.

Licensing
---------

Since the goal is to have the code in a separate repository, we propose to use
a more liberal license.  Either MIT or the Apache license is logical.  Since
the Apache v2 license has one additional feature above MIT (patent right to use)
that seems like a logical solution.

Conclusion: Use Apache 2 license. However, lets do license/ copyright statements
once and ref in files instead of keeping whole license statement in each file.


Code Location/repository
------------------------

We propose that the code be in a separate git repository in the pywbem project
for a number of reasons including:

* It uses a number of additional packages that are not used elsewhere in the
  pywbem client package and this imposes an extra set of constraints on uses
  of just the infrastructure.
* It is not certain that the cli can meet the same python versoning constraints
  as the client infrastructure code because of the extra packages used some of
  which are not today compatible with python 2.6.

It would have its own release cycle, etc.  However since pywbem and pywbemcli
are closely developed we should seriously consider integrating them into a
single documentation set.

The only negatives to this approach are:

* We now have two repositories to maintain with two issue lists, etc.
* It will be more difficult to consider using pywbemcli as a testtool for
  pywbem itself, in part because they are on different development and release
  cycles.


Command Taxonomy
----------------

Overall we propose that this be written in the manner of a command <subcommand>
environment where there is a single cli and multiple subcommands.

Wheras most wbem clis are written to parallel the client api taxonomy
(separate subcommands to match the individual methods of the client api)
we propose that the taxonomy of this cli be organized around the following
levels:

* first subcommand - noun representing the entity type against which the
  command is to be executed (class, instance, qualifierdecl, server,
  subscription manager, log, connection, etc.)
* the second level subcommand be an action on that entity, for example, get,
  delete, create, enumarate, etc.
* The options for each subcommand represent:

  * All of the options available for the corresponding client api (i.e.
    localonly, includeclassorigin, includequalifiers, propertylist, etc.)
  * Include only the maxObjectCount as an option to represent the existence
    of pull operations
  * ability to select namespace be included in all commands except those that
    do not need a namespace or use all namespaces.

The following is the current overall taxonomy of subcommands and their major
options.  The commands and subcommands are shown in **bold**:

**pywbemwcli**

* **class**

  * **get** <classname> --namespace <getclass options> (corresponds to getclass)
  * **invokemethod** <classname> <methodname > [--parameter <name>=<value>]* --namespace
  * **query** <query> --query-language <name> -- namespace
  * **enumerate**  (corresponds to enumerateclasses) <classname> --namespace --names-only &lt;enumerateclass options>
  * **references**  <sourceclass> --namespace --names-only &lt;references options>(corresponds to class references)
  * **associators** <sourceclass> --namespace --names-only &lt;associator options>(corresponds to class associators)
  * **method** <classname> <methodname> [<param_name=value>]*
  * **find** Find a class across namespaces (regex names allowed)
  * **hierarchy** Show a tree of the class hiearchy

* **instance**

  * **get** <inst_name>  --namespace <get inst options> (corresponds to GetInstance)
  * **delete** <instname> | <classname>   (use classname for interactive select mode)
  * **create**  <classname> --property <name>=<value>
  * **invokemethod** &lt:cinstancename> &lt:methodname > [--parameter <name>=<value>]* --namespace
  * **enumerate** <instname> --namespace --names-only <enumerate inst options> (corresponds to EnumerateInstances)
  * **references** <instname> --namespace --names-only <references options>(corresponds to inst references)
  * **associators** <instname> --namespace --names-only <associator options>(corresponds to inst associators)
  * **invokemethod** <instname> <methodname> [<param_name=value>]*
* **qualifier**             # operations on the QualifierDecl type

  * **get** <qualifier_name>  --namespace <get qualifier options> (corresponds to GetQualifier)
  * **enumerate**   --namespace <enumerate qualifier options> (corresponds to EnumerateQualifiers)

* **server**                # operations on the pywbem Server Class

  * **namespaces**          # return list of all namespaces
  * **interop**             # return interop namespace
  * **branding**            #Present overall name/brand info
  * **profiles**            #List with options for filtering
  *  <possible other server objects, etc. adapters>

* **profiles**            # Further operations on the pywbem server class

  * **enumerate**         # Enumerae profiles
  * TODO can we show profile relationships (reference profiles)?

* **subscriptions**       # Operations on the PywbemSubscriptionManager Class

  * **enumerate** --filters --subs --dest
  * **create** <filter|destination|subscription>
  * **delete** <filter|destination|subscription>
  * TODO: Should there be capability for listener in some modes???

* **connection**          # changes to the WBEMConnection Class

  * **show**              # detailed info on current connection
  * **save**              # save the detailed information on the connection as exports
  * **setdefaultnamespace**
  * **THE FOLLOWING ARE FUTURE to allow multiple connections to be saved**
  * list                  # list connections saved in persistent storage
  * select                # select connection from persistent and make current
  * create                # create new connection and save
  * delete                # delete a connection
  * NOTE: Probably needs new general options (ex. --severname, --configfile)

* **job FUTURE**                # Operations on a future Jobs Class *FUTURE*

  *  list
  *  TBD

* **profile FUTURE**             # Lots unknown here. This is where we can expand into profiles

  * **profilename**
    * **info**
    * **classes**
    * **attached_instances**

Special Operations
------------------
While most of the operations are fairly straight forward, requiring possibly
an argument (which generally defines the object to be visualized) and some
options (where generally the options represent filtering or display
characteristcs of the objects), at least the create_instance and invoke_method
operations have more extensive input requirements.  These operations require
building one or more objects to be passed to the server.

The create_instance requires building an instance of a class with possible
properties and the invoke_method requires building parameters which consist
of CIMData types.

Create_Instance cmd line input requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This command requires:
#. an argument defining the CIMClass for which the instance is to be created.

#. Multiple inputs arguments representing the values of the properties to be
   included in the request.  For each property the input parameters must be
   capable of representing:

   #. The property name
   #. The property value type
   #. The scalar value if it is a scalar property. This might be any of the
      CIM Types
   #. The Array value for array properties. This might be an array of any of
      the CIMTypes.
   #. Whether the property is array type
   #. The size of the array (optional)
   #. The value for an embedded instance property.

Since all we have available is:

1. Command line arguments
2. The existence of the class defining the properties

We want to make this simple enough that a command line user can enter
property information without excessive formatting wo we prpose the following
limitations:

1. Pywbemcli will make use of both the CIM class for the property from the server
   and the input arguments. Specifically:

   1. The CIM class will be used to get the property type and whether it
      is an array.
   2. This information can be used to validate the input arguments
   3. The array_size attribute of properties will be ignored.  It is not really
       use in any case.

Each property will be represented by an options (ex. -p) which will define
the name and value of the property as a single string of the form

    <name>'='<value>

Thus, for example:

* ``Id=3``
* ``fred=thisStringValue``
* ``fred="this String Value``

Representing the CIM Data types

Representing arrays

Arrays will be represented either as a single name value pair with the
values separated by commas or as repeated arguments with the same name
component.

Thus an array property could be represented as:

* ``-p pname=1,2,3,55,88,11``
* ``-p pname=Fred,John,Louie``
* ``-p pname="Fred and John","Jim and Ron"``

or

* ``-p pname=1 -p pname=2``

In the second case, pywbemcli will assemble the multiple parameters into
a single array parameter.

NOTE: We are NOT distinguishing array properties specifically in any way in
this structure so that  ``pname=1`` could be either an array or non-array
parameter.  The information from the class is required to separate the
array property from scalars.

This means that that there is a limitation in that we are trying to create
correct properties and not provide for the user to create properties that
are specifically incorrect on invalid.  Therefore the pybwbemcli property
parser will tell the user immediatly if the property is a valid scalar or
array value.

ALTERNATIVES TO CONSIDER:

1. Different option name for array and scalar properties.

Embedded Instance Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**TODO**




General Options
---------------

The general options/arguments will include;
* arguments to define the connection to a wbem server (uri, defaultnamespace,
credentials, security, etc.)

* arguments that customize the general operation
  * output_format
  * verbosity of output
  * etc

This can parallel the existing parameter set in wbemcli.

ISSUES: This is a lot of overhead for each command.  There are two logical
solutions:

1. Click includes the capability to use environment variables as alternate
   to cmd line input for options.  We must take advantage of that capability.

2. It is probably seriously time to begin to use a config file for at least
   some characteristics so that the user can set defaults, specific options,
   etc.  This will require some thought since the use of config files has
   many variations.  See the connection group of the above taxonomy. That
   would seem to solve the problem

Output Formats
^^^^^^^^^^^^^^
The following output formats should be supported:

  * mof - Mof display of cim objects and lists of cim objects
  * xml - cim/xml output for cim objects and lists of cim objects
  * table - For at least properties of instances
  * json - output for cim objects and lists of cim objects. Uses cim rest fmt
  * csv - Similar to table output except creates output that could be loaded
    into a spreadsheet.
  * NOTE that there may be more outputs. (ex. html)


Required Packages
-----------------

We are going to base this on the python click package and other contributions
to click so at least click and possibly several of the click contributions will
be required.

User Defined Extensions
-----------------------
Reserve for future.  Lets not put this in V1

Testing
-------
Required for V1

We need several types of testing:
1. Testing of functions
2. Testing of the help functionality
3. Testing against known server similar to pywbem.
4. Testing against some sort of mock environment.  However, the mocking in
pywbem is strictly for testing against single operations against predefined
responses at the xml, request level. We need something where we can set up
a fake server environment and perform actions/get responses from a predefined
set of classes/instances/qualifiers.   This is sort of a mini-server.

Lets consider that in a separate design document.

Proposal
--------

single tool with git-like subcommand structure::

    pywbemcli [generat-option]* command usb-command [specific-option]*

Examples::

    pywbemcli -s http://localhost -o mof class get CIM_ManagedElement
    # Returns the mof for CIM_ManagedElement

    pywbem -s http://localhost instance get CIM_Blah -i
    # Does get instances of CIM_Blah and offers user selection for operation

    pywbem -s http://localhost class find TST_
    # finds all classes in environment that begin with TST_ and returns list
    # of class and namespace

The overall directory structure is probably:

**root**

   * **pywbemcli** - Add files that define the click infrastructure
   * **pywbemclient** - interface with the pywbem apis.
   * **tests**
   * **doc**

QUESTION: Should we break up the code into a package that implements the
commands and subcommands and a separate one that implements the action functions
as shown above. At this point we have grouped each subcommand group into a
single file (i.e. _cmd_class.py, _cmd_instance.py where the action function
for that subcommand is part of the same file.)

TODO Items
----------

Timing of execution
^^^^^^^^^^^^^^^^^^^
Timing of cmd execution. Should we have an option to time the execution of
commands

Command Chaining
^^^^^^^^^^^^^^^^
Is there a way to achieve command chaining.

TODO Need real example first.

Command Aliases
^^^^^^^^^^^^^^^
There are at least two possibilities for aliases:

  * subcommand alias (en substitutes for enumerate)
  * general text aliasing where a combination of text elements could be
    aliased (as git does). Thus, the text 'class get' could be aliased to
    getclass or gc.

I believe that the current `alias` contrib handles the first but not the second
form of aliasing.

Manual level documentation
--------------------------
 TODO
