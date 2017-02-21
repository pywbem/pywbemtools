Design Document for a PyWBEM Command Line Browser
=================================================


Status: In Process
Date: 9 Feb. 2017
Update: 11 Feb 2017
Update: 20 Feb 2017 - Add more subcommands and define characteristics of
        create instances and invoke method.

Goals
-----

* Python Based
* Expandable. Users should be able to add functionality with plugins
* Usable effectively by both occasional and power users
  * Interactive mode
  * Script mode (complete command entered from command line)
* Capable of executing all WBEM CIM/XML operations (with specific exceptions)
* Include commands for other operations that will be a real advantage to
  developers, users, etc.
* Good integrated help to minize requirement for external documentation
* This is primarily a user tool and not an internal test tool so it needs
  to protect the user and provide as much convience as possible for the user.

Also, to make this really usable for testers, developers, etc. we need to
provide a rich set of display/analysis tools within the structure.  Just
having an implementation of the 20 some cim/xml operations is NOT sufficient.
We want the user to be able to see:

* Structure information on the environment. How components relate to one another
* Size information on the environment (how many instances, classes, etc.)
* 

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
* The options for each subcommand represent
  * All of the options available for the corresponding client api (i.e.
    localonly, includeclassorigin, includequalifiers, propertylist, etc.)
  * Include only the maxObjectCount as an option to represent the existence
    of pull operations
  * ability to select namespace be included in all commands except those that
    do not need a namespace or use all namespaces.

The following is the current overall taxonomy of subcommands and their major
options.

**pywbemwcli**

* **class**
  * **get** &lt;classname> --namespace &lt;getclass options> (corresponds to getclass)
  * **invokemethod** &lt:classname> &lt:methodname > [--parameter <name>=<value>]* --namespace
  * **query** &lt:query> --querylanguage <name> -- namespace
  * **enumerate**  (corresponds to enumerateclasses) &lt;classname> --namespace --names-only &lt;enumerateclass options>  
  * **references**  &lt;sourceclass> --namespace --names_only &lt;references options>(corresponds to class references)  
  * **associators** &lt;sourceclass> --namespace --names_only &lt;associator options>(corresponds to class associators)  
  * **method** &lt;classname> &lt;methodname> [&lt;param_name=value>]*  
  * **find** Find a class across namespaces (regex names allowed)
  * **tree** Show a tree of the class hiearchy
  
* **instance**
  * **get** &lt;inst_name>  --namespace &lt;get inst options> (corresponds to GetInstance)
  * **delete** &lt;instname> | &lt;classname>   (use classname for interactive select mode)
  * **create**  &lt;classname> --property <name>=<value>
  * **invokemethod** &lt:cinstancename> &lt:methodname > [--parameter <name>=<value>]* --namespace
  * **enumerate** &lt;instname>-- namespace --names-only &lt;enumerate inst options> (corresponds to EnumerateInstances)
  * **references** &lt;instname>--namespace --names_only &lt;references options>(corresponds to inst references)
  * **associators** &lt;instname> --namespace --names_only &lt;associator options>(corresponds to inst associators)
  * **invokemethod** &lt;instname> &lt;methodname> [&lt;param_name=value>]*
* **qualifier**             # operations on the QualifierDecl type
  * **get** &lt;qualifier_name>  --namespace &lt;get qualifier options> (corresponds to GetQualifier)
  * **enumerate**   --namespace &lt;enumerate qualifier options> (corresponds to EnumerateQualifiers)
* **server**                # operations on the pywbem Server Class       
  * **namespaces**          # return list of all namespaces
  * **interop**             # return interop namespace
  * **branding**            #Present overall name/brand info
  * **profiles**            #List with options for filtering
  *  &lt;possible other server objects, etc. adapters> 
* **subscriptions**       # Operations on the PywbemSubscriptionManager Class
  * **list** --filters --subs --dest
  * **create** &lt;filter|destination|subscription>
  * **delete** &lt;filter|destination|subscription>
  * TODO: Should there be capability for listener in some modes???  
  * **profiles**            # Further operations on the pywbem server class
    * **list**
    * ???
* **connection**          # changes to the WBEMConnection Class
  * **info**              # detailed info on current connection
  * **setdefaultnamespace**
  * list                  # list connections saved in persistent storage
  * select                # select connection from persistent and make current
  * create                # create new connection and save
  * delete                # delete a connection
  * NOTE: Needs new general options (ex. --severname, --configfile)
* **job**                # Operations on a future Jobs Class *FUTURE* 
  *  list
  *  TBD   
* **profile**             # Lots unknown here. This is where we can expand into profiles
  * **profilename**
    * **info**
    * **classes**
    * **attached_instances**

Specialized Options
-------------------
There are a few specialized arguments/options, specifically to implement
those operations that create things (instance create, invokemethod parameters).
These differ from most of the options/arguments in that:

* They must be complete enough to define properties with values and
parameters with values
* The values that are to be implemented include
   * all of the CIM Types
   * Both scalars and Arrays
   * Reference property values
   * embedded objects

In cimcli we implemented this with extra parameters on the command line of
the form <name>=<value>

where value could be:
    * scalar (integer, float, string, boolean, etc.)
    * Arrays where arrays could be made up of repetititions of a scalar or
      comma separated values with brackets to indicate that it was an array
      ex.
         propertyx=[123.345]
         propertyx=123 propertyx=345

    * embedded objects - TODO


General Options
---------------

The general options/arguments will include;
* arguments to define the connection to a wbem server (uri, defaultnamespace,
credentials, security, output format, verbosity, etc.)

This can parallel the existing parameter set in wbemcli.

ISSUES: This is a lot of overhead for each command.  There are two logical
solutions:

1. Click includes the capability to use environment variables as alternate
   to cmd line input for options.  We should take advantage of that

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

single tool with git-like subcommand structure:

    pywbemcli [generat-option]* command usb-command [specific-option]*

Examples:

    pywbemcli http://localhost -o mof class get CIM_ManagedElement
    # Returns the mof for CIM_ManagedElement

    pywbem http://localhost instance get CIM_Blah -i
    # Does get instances of CIM_Blah and offers user selection for operation

    pywbem http://localhost class fine TST_
    # finds all classes in environment that begins with TST_ and returns list
    # of class and namespace

The overall directory structure is probably:

**root**

   * **pywbemcli** - Add files that define the click infrastructure
   * **pywbemclient** - interface with the pywbem apis.
   * **tests**
   * **doc**

QUESTION: Should we break up the code into a package that implements the
commands and subcommands and a separate one that implements the action functions
as shown above. Question: Advantages/disadvantages

## TODO Items

### Timing
Timing of cmd execution. Should we have an option to time the execution of
commands

### Command Chaining
Is there a way to achieve command chaining.

TODO Need real example first.

### Aliases
There are at least two possibilities for aliases:

  * subcommand alias (en substitutes for enumerate)
  * general text aliasing where a combination of text elements could be
    aliased (as git does). Thus, the text 'class get' could be aliased to
    getclass or gc.
    
I believe that the current `alias` contrib handles the first but not the second
form of aliasing.

### Manual level documentation
 TODO 

