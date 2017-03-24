**Overview of pywbemcli help with the multiple subcommands***



pywbemcli  --help
=================

```
b'Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]...\n\n  Command line browser for WBEM Servers. This cli tool implements the\n  CIM/XML client APIs as defined in pywbem to make requests to a WBEM\n  server.\n\n  The options shown above that can also be specified on any of the\n  (sub-)commands.\n\nOptions:\n  -s, --server TEXT               Hostname or IP address with scheme of the\n                                  WBEMServer (EnvVar: PYWBEMCLI_SERVER).\n  -d, --default_namespace TEXT    Default Namespace to use in the target\n                                  WBEMServer if no namespace is defined in the\n                                  subcommand(EnvVar:\n                                  PYWBEMCLI_DEFAULT_NAMESPACE). (Default:\n                                  root/cimv2).\n  -u, --user TEXT                 User name for the WBEM Server connection.\n                                  (EnvVar: PYWBEMCLI_USER).\n  -p, --password TEXT             Password for the WBEM Server (EnvVar:\n                                  PYWBEMCLI_PASSWORD ).\n  -t, --timeout TEXT              Operation timeout for the WBEM Server.\n                                  (EnvVar: PYWBEMCLI_TIMEOUT).\n  -n, --noverify                  If set, client does not verify server\n                                  certificate.\n  -x, --certfile TEXT             Server certfile. Ignored if noverify flag\n                                  set. (EnvVar: PYWBEMCLI_CERTFILE).\n  -k, --keyfile TEXT              Client private key file. (EnvVar:\n                                  PYWBEMCLI_KEYFILE).\n  -o, --output-format [mof|xml|table|csv|text]\n                                  Output format (Default: mof). pywbemcli may\n                                  override the format choice depending on the\n                                  operation since not all formats apply to all\n                                  output data types\n  --debug                         Display transmited and received packets\n                                  TEMP.\n  -v, --verbose                   Display extra information about the\n                                  processing.\n  --version                       Show the version of this command and exit.\n  --help                          Show this message and exit.\n\nCommands:\n  class       Command Group to manage CIM Classes.\n  connection  Command group to manage WBEM connections...\n  help        Show help message for interactive mode.\n  instance    Command Group to manage CIM instances.\n  qualifier   Command Group to manage CIM...\n  repl        Enter interactive (REPL) mode (default) and...\n  server      Command Group for WBEM server operations.\n'
```

pywbemcli class --help
======================

```
b"Usage: pywbemcli class [COMMAND-OPTIONS] COMMAND [ARGS]...\n\n  Command Group to manage CIM Classes.\n\n  In addition to the command-specific options shown in this help text, the\n  general options (see 'pywbemcli --help') can also be specified before the\n  command. These are NOT retained after the command is executed.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  associators   Get the associated classes for the CLASSNAME.\n  enumerate     Enumerate classes from the WBEMServer.\n  find          Find all classes that match the CLASSNAME...\n  get           get and display a single class from the WBEM...\n  hierarchy     Display class inheritance hierarchy as a...\n  invokemethod  Invoke the class method named methodname in...\n  names         Get and display classnames from the...\n  references    Get the reference classes for the CLASSNAME.\n"
```

pywbemcli class get --help
==========================

```
b'Usage: pywbemcli class get [COMMAND-OPTIONS] CLASSNAME\n\n  get and display a single class from the WBEM Server\n\nOptions:\n  -l, --localonly                 Show only local properties of the class.\n  --includequalifiers / --no_includequalifiers\n                                  Include qualifiers in the result. Default is\n                                  to include qualifiers\n  -c, --includeclassorigin        Include classorigin in the result.\n  -p, --propertylist <property name>\n                                  Define a propertylist for the request. If\n                                  not included a Null property list is defined\n                                  and the server returns all properties. If\n                                  defined as empty string the server returns\n                                  no properties. ex: -p propertyname1 -p\n                                  propertyname2 or -p\n                                  propertyname1,propertyname2\n  -n, --namespace <name>          Namespace to use for this operation. If\n                                  defined that namespace overrides the general\n                                  options namespace\n  --help                          Show this message and exit.\n'
```

pywbemcli class invokemethod --help
===================================

```
b'Usage: pywbemcli class invokemethod [COMMAND-OPTIONS] classname name\n\n  Invoke the class method named methodname in the class classname\n\nOptions:\n  -p, --parameter parameter  Optional multiple method parameters of form\n                             name=value\n  -n, --namespace <name>     Namespace to use for this operation. If defined\n                             that namespace overrides the general options\n                             namespace\n  --help                     Show this message and exit.\n'
```

pywbemcli class names --help
============================

```
b'Usage: pywbemcli class names [COMMAND-OPTIONS] CLASSNAME\n\n  Get and display classnames from the WBEMServer.\n\n  Enumerates the classnames from the WBEMServer starting either at the top\n  of the class hierarchy or from  the position in the class hierarch defined\n  by the optional`classname` argument if provided.\n\n  The output format is normally a list of the classnames\n\n  This command corresponds to `class enumerate  -o`\n\n  The deepinheritance option defines whether the complete hiearchy is\n  retrieved or just the next level in the hiearchy.\n\nOptions:\n  -d, --deepinheritance           Return complete subclass hiearchy for this\n                                  class.\n  -d, --deepinheritance           Return complete subclass hiearchy for this\n                                  class.\n  --includequalifiers / --no_includequalifiers\n                                  Include qualifiers in the result. Default is\n                                  to include qualifiers\n  -c, --includeclassorigin        Include classorigin in the result.\n  -s, --sort                      Sort into alphabetical order by classname.\n  -n, --namespace <name>          Namespace to use for this operation. If\n                                  defined that namespace overrides the general\n                                  options namespace\n  --help                          Show this message and exit.\n'
```

pywbemcli class enumerate --help
================================

```
b'Usage: pywbemcli class enumerate [COMMAND-OPTIONS] CLASSNAME\n\n  Enumerate classes from the WBEMServer.\n\n  Enumerates the classes (or classnames) from the WBEMServer starting either\n  at the top of the class hierarchy or from  the position in the class\n  hierarch defined by `classname` argument if provided.\n\n  The output format is defined by the output_format global option.\n\n  The includeclassqualifiers, includeclassorigin options define optional\n  information to be included in the output.\n\n  The deepinheritance option defines whether the complete hiearchy is\n  retrieved or just the next level in the hiearchy.\n\nOptions:\n  -d, --deepinheritance           Return complete subclass hierarchy for this\n                                  class if set. Otherwise retrieve only the\n                                  next hierarchy level.\n  -l, --localonly                 Show only local properties of the class.\n  --includequalifiers / --no_includequalifiers\n                                  Include qualifiers in the result. Default is\n                                  to include qualifiers\n  -c, --includeclassorigin        Include classorigin in the result.\n  -o, --names_only                Show only local properties of the class.\n  -s, --sort                      Sort into alphabetical order by classname.\n  -n, --namespace <name>          Namespace to use for this operation. If\n                                  defined that namespace overrides the general\n                                  options namespace\n  --help                          Show this message and exit.\n'
```

pywbemcli class associators --help
==================================

```
b'Usage: pywbemcli class associators [COMMAND-OPTIONS] CLASSNAME\n\n  Get the associated classes for the CLASSNAME.\n\n  Get the classes(or classnames) that are associated with the CLASSNAME\n  argument filtered by the assocclass, resultclass, role and resultrole\n  arguments options.\n\n  Results are displayed as defined by the output format global option.\n\nOptions:\n  -a, --assocclass <class name>   Filter by the associated class name\n                                  provided.\n  -c, --resultclass <class name>  Filter by the result class name provided.\n  -r, --role <role name>          Filter by the role name provided.\n  -R, --resultrole <role name>    Filter by the role name provided.\n  --includequalifiers / --no_includequalifiers\n                                  Include qualifiers in the result. Default is\n                                  to include qualifiers\n  -c, --includeclassorigin        Include classorigin in the result.\n  -p, --propertylist <property name>\n                                  Define a propertylist for the request. If\n                                  not included a Null property list is defined\n                                  and the server returns all properties. If\n                                  defined as empty string the server returns\n                                  no properties. ex: -p propertyname1 -p\n                                  propertyname2 or -p\n                                  propertyname1,propertyname2\n  -o, --names_only                Show only local properties of the class.\n  -s, --sort                      Sort into alphabetical order by classname.\n  -n, --namespace <name>          Namespace to use for this operation. If\n                                  defined that namespace overrides the general\n                                  options namespace\n  --help                          Show this message and exit.\n'
```

pywbemcli class references --help
=================================

```
b'Usage: pywbemcli class references [COMMAND-OPTIONS] CLASSNAME\n\n  Get the reference classes for the CLASSNAME.\n\n  Get the reference classes (or their classnames) for the CLASSNAME argument\n  filtered by the role and result class options and modified  by the other\n  options.\n\nOptions:\n  -r, --resultclass <class name>  Filter by the classname provided.\n  -x, --role <role name>          Filter by the role name provided.\n  --includequalifiers / --no_includequalifiers\n                                  Include qualifiers in the result. Default is\n                                  to include qualifiers\n  -c, --includeclassorigin        Include classorigin in the result.\n  -p, --propertylist <property name>\n                                  Define a propertylist for the request. If\n                                  not included a Null property list is defined\n                                  and the server returns all properties. If\n                                  defined as empty string the server returns\n                                  no properties. ex: -p propertyname1 -p\n                                  propertyname2 or -p\n                                  propertyname1,propertyname2\n  -o, --names_only                Show only local properties of the class.\n  -s, --sort                      Sort into alphabetical order by classname.\n  -n, --namespace <name>          Namespace to use for this operation. If\n                                  defined that namespace overrides the general\n                                  options namespace\n  --help                          Show this message and exit.\n'
```

pywbemcli class find --help
===========================

```
b'Usage: pywbemcli class find [COMMAND-OPTIONS] CLASSNAME regex\n\n  Find all classes that match the CLASSNAME regex.\n\n  Find all of the classes in the namespace  of the defined WBEMServer that\n  match the CLASSNAME  regular expression argument in the namespaces of the\n  defined WBEMserver.\n\n  The CLASSNAME argument is required.\n\n  The CLASSNAME argument may be either a complete classname or a regular\n  expression that can be matched to one or more classnames. To limit the\n  filter to a single classname, terminate the classname with $.\n\n  The regular expression is anchored to the beginning of the classname and\n  is case insensitive. Thus pywbem_ returns all classes that begin with\n  PyWBEM_, pywbem_, etc.\n\n  The namespace option limits the search to the defined namespace\n\nOptions:\n  -s, --sort              Sort into alphabetical order by classname.\n  -n, --namespace <name>  Namespace to use for this operation. If defined that\n                          namespace overrides the general options namespace\n  --help                  Show this message and exit.\n'
```

pywbemcli class hierarchy --help
================================

```
b'Usage: pywbemcli class hierarchy [COMMAND-OPTIONS] CLASSNAME\n\n  Display class inheritance hierarchy as a tree.\n\n  The classname option, if it exists defines the topmost class of the\n  hierarchy to include in the display. This is a separate subcommand because\n  it is tied specifically to displaying in a tree format.\n\nOptions:\n  -s, --superclasses      Display the superclasses to CLASSNAME.  In this case\n                          CLASSNAME is required\n  -n, --namespace <name>  Namespace to use for this operation. If defined that\n                          namespace overrides the general options namespace\n  --help                  Show this message and exit.\n'
```

pywbemcli instance get --help
=============================

```
b'Usage: pywbemcli instance get [COMMAND-OPTIONS] INSTANCENAME\n\n  Get a single CIMInstance.\n\n  Gets the instance defined by instancename.\n\n  This may be executed interactively by providing only a classname and the\n  interactive option.\n\nOptions:\n  -l, --localonly                 Show only local properties of the returned\n                                  instance.\n  -q, --includequalifiers         Include qualifiers in the result.\n  -c, --includeclassorigin        Include Class Origin in the returned\n                                  instance.\n  -p, --propertylist <property name>\n                                  Define a propertylist for the request. If\n                                  not included a Null property list is defined\n                                  and the server returns all properties. If\n                                  defined as empty string the server returns\n                                  no properties. ex: -p propertyname1 -p\n                                  propertyname2 or -p\n                                  propertyname1,propertyname2\n  -n, --namespace <name>          Namespace to use for this operation. If\n                                  defined that namespace overrides the general\n                                  options namespace\n  -i, --interactive               If set, instancename argument must be a\n                                  class and  user is provided with a list of\n                                  instances of the  class from which the\n                                  instance to delete is selected.\n  --help                          Show this message and exit.\n'
```

pywbemcli instance delete --help
================================

```
b'Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME\n\n  Delete a single instance defined by instancename from the WBEM server.\n  This may be executed interactively by providing only a classname and the\n  interactive option.\n\nOptions:\n  -i, --interactive       If set, instancename argument must be a class and\n                          user is provided with a list of instances of the\n                          class from which the instance to delete is selected.\n  -n, --namespace <name>  Namespace to use for this operation. If defined that\n                          namespace overrides the general options namespace\n  --help                  Show this message and exit.\n'
```

pywbemcli instance create --help
================================

```
b'Usage: pywbemcli instance create [COMMAND-OPTIONS] classname\n\n  Create an instance of classname.\n\nOptions:\n  -x, --property property         Optional multiple property definitions of\n                                  form name=value\n  -p, --propertylist <property name>\n                                  Define a propertylist for the request. If\n                                  not included a Null property list is defined\n                                  and the server returns all properties. If\n                                  defined as empty string the server returns\n                                  no properties. ex: -p propertyname1 -p\n                                  propertyname2 or -p\n                                  propertyname1,propertyname2\n  -n, --namespace <name>          Namespace to use for this operation. If\n                                  defined that namespace overrides the general\n                                  options namespace\n  --help                          Show this message and exit.\n'
```

pywbemcli instance invokemethod --help
======================================

```
b'Usage: pywbemcli instance invokemethod [COMMAND-OPTIONS] name name\n\n  Invoke the method defined by instancename and methodname with parameters.\n\n  This issues an instance level invokemethod request and displays the\n  results.\n\nOptions:\n  -p, --parameter parameter  Optional multiple method parameters of form\n                             name=value\n  -n, --namespace <name>     Namespace to use for this operation. If defined\n                             that namespace overrides the general options\n                             namespace\n  --help                     Show this message and exit.\n'
```

pywbemcli instance query --help
===============================

```
b'Usage: pywbemcli instance query [COMMAND-OPTIONS] <query string>\n\n  Execute the query defined by the query argument.\n\nOptions:\n  -l, --querylanguage <query language>\n                                  Use the query language defined. (Default:\n                                  DMTF:CQL.\n  -n, --namespace <name>          Namespace to use for this operation. If\n                                  defined that namespace overrides the general\n                                  options namespace\n  -s, --sort                      Sort into alphabetical order by classname.\n  --help                          Show this message and exit.\n'
```

pywbemcli instance names --help
===============================

```
b'Usage: pywbemcli instance names [COMMAND-OPTIONS] [CLASSNAME]\n\n  Get and display a list of instance names of the classname argument.\n\n  This is equivalent to pywbemcli instance enumerate -o\n\nOptions:\n  -n, --namespace <name>  Namespace to use for this operation. If defined that\n                          namespace overrides the general options namespace\n  -s, --sort              Sort into alphabetical order by classname.\n  --help                  Show this message and exit.\n'
```

pywbemcli instance enumerate --help
===================================

```
b'Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME\n\n  Enumerate instances or instance names from the WBEMServer starting either\n  at the top  of the hiearchy (if no classname provided) or from the\n  classname argument provided.\n\n  Displays the returned instances or names\n\nOptions:\n  -l, --localonly                 Show only local properties of the class.\n  -d, --deepinheritance           Return properties in subclasses of defined\n                                  target.  If not specified only properties in\n                                  target class are returned\n  -q, --includequalifiers         Include qualifiers in the result.\n  -c, --includeclassorigin        Include ClassOrigin in the result.\n  -p, --propertylist <property name>\n                                  Define a propertylist for the request. If\n                                  not included a Null property list is defined\n                                  and the server returns all properties. If\n                                  defined as empty string the server returns\n                                  no properties. ex: -p propertyname1 -p\n                                  propertyname2 or -p\n                                  propertyname1,propertyname2\n  -n, --namespace <name>          Namespace to use for this operation. If\n                                  defined that namespace overrides the general\n                                  options namespace\n  -o, --names_only                Show only local properties of the class.\n  -s, --sort                      Sort into alphabetical order by classname.\n  --help                          Show this message and exit.\n'
```

pywbemcli instance count --help
===============================

```
b'Usage: pywbemcli instance count [COMMAND-OPTIONS] CLASSNAME regex\n\n  Get number of instances for each class in namespace.\n\n  The size of the response may be limited by CLASSNAME argument which\n  defines a classname regular expression so that only those classes are\n  counted\n\n  The CLASSNAME argument is optional.\n\n  The CLASSNAME argument may be either a complete classname or a regular\n  expression that can be matched to one or more classnames. To limit the\n  filter to a single classname, terminate the classname with $.\n\n  The regular expression is anchored to the beginning of the classname and\n  is case insensitive. Thus pywbem_ returns all classes that begin with\n  PyWBEM_, pywbem_, etc.\n\nOptions:\n  -s, --sort              Sort by instance count. Otherwise sorted by\n                          classname\n  -n, --namespace <name>  Namespace to use for this operation. If defined that\n                          namespace overrides the general options namespace\n  --help                  Show this message and exit.\n'
```

pywbemcli instance references --help
====================================

```
b'Usage: pywbemcli instance references [COMMAND-OPTIONS] INSTANCENAME\n\n  Get the reference instances or instance names.\n\n  For the INSTANCENAME argument provided return instances or instance names\n  (names-only option) filtered by the role and result class options. This\n  may be executed interactively by providing only a classname and the\n  interactive option.\n\nOptions:\n  -r, --resultclass <class name>  Filter by the result class name provided.\n  -o, --role <role name>          Filter by the role name provided.\n  -q, --includequalifiers         Include qualifiers in the result.\n  -c, --includeclassorigin        Include classorigin in the result.\n  -p, --propertylist <property name>\n                                  Define a propertylist for the request. If\n                                  not included a Null property list is defined\n                                  and the server returns all properties. If\n                                  defined as empty string the server returns\n                                  no properties. ex: -p propertyname1 -p\n                                  propertyname2 or -p\n                                  propertyname1,propertyname2\n  -o, --names_only                Show only local properties of the class.\n  -n, --namespace <name>          Namespace to use for this operation. If\n                                  defined that namespace overrides the general\n                                  options namespace\n  -s, --sort                      Sort into alphabetical order by classname.\n  -i, --interactive               If set, instancename argument must be a\n                                  class and  user is provided with a list of\n                                  instances of the  class from which the\n                                  instance to delete is selected.\n  --help                          Show this message and exit.\n'
```

pywbemcli instance associators --help
=====================================

```
b'Usage: pywbemcli instance associators [COMMAND-OPTIONS] INSTANCENAME\n\n  Get the associated instances or instance names.\n\n  Returns the associated instances or names (names-only option) for the\n  INSTANCENAME argument filtered by the assocclass, resultclass, role and\n  resultrole arguments. This may be executed interactively by providing only\n  a classname and the interactive option.\n\nOptions:\n  -a, --assocclass <class name>   Filter by the associated instancename\n                                  provided.\n  -r, --resultclass <class name>  Filter by the result class name provided.\n  -x, --role <role name>          Filter by the role name provided.\n  -o, --resultrole <class name>   Filter by the result role name provided.\n  -q, --includequalifiers         Include qualifiers in the result.\n  -c, --includeclassorigin        Include classorigin in the result.\n  -p, --propertylist <property name>\n                                  Define a propertylist for the request. If\n                                  not included a Null property list is defined\n                                  and the server returns all properties. If\n                                  defined as empty string the server returns\n                                  no properties. ex: -p propertyname1 -p\n                                  propertyname2 or -p\n                                  propertyname1,propertyname2\n  -o, --names_only                Show only local properties of the class.\n  -n, --namespace <name>          Namespace to use for this operation. If\n                                  defined that namespace overrides the general\n                                  options namespace\n  -s, --sort                      Sort into alphabetical order by classname.\n  -i, --interactive               If set, instancename argument must be a\n                                  class and  user is provided with a list of\n                                  instances of the  class from which the\n                                  instance to delete is selected.\n  --help                          Show this message and exit.\n'
```

pywbemcli qualifier --help
==========================

```
b"Usage: pywbemcli qualifier [COMMAND-OPTIONS] COMMAND [ARGS]...\n\n  Command Group to manage CIM QualifierDeclarations.\n\n  Includes the capability to get and enumerate qualifier declarations.\n\n  This does not provide the capability to create or delete CIM\n  QualifierDeclarations\n\n  In addition to the command-specific options shown in this help text, the\n  general options (see 'pywbemcli --help') can also be specified before the\n  command. These are NOT retained after the command is executed.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  enumerate  Enumerate CIMQualifierDeclaractions.\n  get        Display CIMQualifierDeclaration.\n"
```

pywbemcli qualifier enumerate --help
====================================

```
b'Usage: pywbemcli qualifier enumerate [COMMAND-OPTIONS]\n\n  Enumerate CIMQualifierDeclaractions.\n\n  Displays all of the CIMQualifierDeclaration objects in the defined\n  namespace in the current WBEM Server\n\nOptions:\n  -n, --namespace <name>  Namespace to use for this operation. If defined that\n                          namespace overrides the general options namespace\n  -s, --sort              Sort into alphabetical order by classname.\n  --help                  Show this message and exit.\n'
```

pywbemcli qualifier get --help
==============================

```
b'Usage: pywbemcli qualifier get [COMMAND-OPTIONS] NAME\n\n  Display CIMQualifierDeclaration.\n\n  Displays a single CIMQualifierDeclaration for the defined namespace in the\n  current WBEMServer\n\nOptions:\n  -n, --namespace <name>  Namespace to use for this operation. If defined that\n                          namespace overrides the general options namespace\n  --help                  Show this message and exit.\n'
```

pywbemcli server --help
=======================

```
b"Usage: pywbemcli server [COMMAND-OPTIONS] COMMAND [ARGS]...\n\n  Command Group for WBEM server operations.\n\n  In addition to the command-specific options shown in this help text, the\n  general options (see 'pywbemcli --help') can also be specified before the\n  command. These are NOT retained after the command is executed.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  brand       Display the interop namespace name in the...\n  connection  Display information on the connection used by...\n  info        Display the brand information on the current...\n  interop     Display the interop namespace name in the...\n  namespaces  Display the set of namespaces in the current...\n  profiles    Display profiles on the current WBEM Server.\n"
```

pywbemcli server brand --help
=============================

```
b'Usage: pywbemcli server brand [COMMAND-OPTIONS]\n\n  Display the interop namespace name in the WBEM Server.\n\nOptions:\n  --help  Show this message and exit.\n'
```

pywbemcli server connection --help
==================================

```
b'Usage: pywbemcli server connection [COMMAND-OPTIONS]\n\n  Display information on the connection used by this server.\n\nOptions:\n  --help  Show this message and exit.\n'
```

pywbemcli server info --help
============================

```
b'Usage: pywbemcli server info [COMMAND-OPTIONS]\n\n  Display the brand information on the current WBEM Server.\n\nOptions:\n  --help  Show this message and exit.\n'
```

pywbemcli server namespaces --help
==================================

```
b'Usage: pywbemcli server namespaces [COMMAND-OPTIONS]\n\n  Display the set of namespaces in the current WBEM server\n\nOptions:\n  -s, --sort  Sort into alphabetical order by classname.\n  --help      Show this message and exit.\n'
```

pywbemcli server interop --help
===============================

```
b'Usage: pywbemcli server interop [COMMAND-OPTIONS]\n\n  Display the interop namespace name in the WBEM Server.\n\nOptions:\n  --help  Show this message and exit.\n'
```

pywbemcli server profiles --help
================================

```
b'Usage: pywbemcli server profiles [COMMAND-OPTIONS]\n\n  Display profiles on the current WBEM Server.\n\n  This display may be filtered by the optional organization and profile name\n  options\n\nOptions:\n  -o, --organization <org name>   Filter by the defined organization. (ex. -o\n                                  DMTF\n  -n, --profilename <profile name>\n                                  Filter by the profile name. (ex. -n Array\n  --help                          Show this message and exit.\n'
```

pywbemcli connection show --help
================================

```
b'Usage: pywbemcli connection show [COMMAND-OPTIONS]\n\n  Show the current connection information, i.e. all the variables that make\n  up the current connection\n\nOptions:\n  --help  Show this message and exit.\n'
```
