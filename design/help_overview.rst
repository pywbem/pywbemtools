
########################################################
Overview of pywbemcli help with the multiple subcommands
########################################################

This is a display of the output of the pywbemcli commands define in this file. Each help output is presented as a section title with the command as sent to pywbemcli followed by the ouput returned by pywbemcli.

*********************
pywbemcli repl --help
*********************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli repl --help`

*****************
pywbemcli  --help
*****************

::

    Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]...
    
      Command line browser for WBEM Servers. This cli tool implements the
      CIM/XML client APIs as defined in pywbem to make requests to a WBEM
      server. This browser uses subcommands to      * Explore the
      characteristics of WBEM Servers based on using the       pywbem client
      APIs.  It can manage/inspect CIM_Classes and       CIM_instanceson the
      server.
    
          * In addition it can inspect namespaces and other server information
            and inspect and manage WBEM indication subscriptions.
    
      The options shown above that can also be specified on any of the
      (sub-)commands as well as the command line.
    
    Options:
      -s, --server TEXT               Hostname or IP address with scheme of the
                                      WBEMServer in  format
                                      [{scheme}://]{host}[:{port}]. Scheme must be
                                      "https" or "http" (Default: "https"). Host
                                      defines a  short or fully qualified DNS
                                      hostname, a literal  IPV4 address (dotted)
                                      or a literal IPV6 address Port (optional)
                                      defines a  WBEM server protocol to be used
                                      (Defaults 5988(HTTP) and  5989 (HTTPS).
                                      (EnvVar: PYWBEMCLI_SERVER).
      -N, --name TEXT                 Optional name for the connection.  If the
                                      name option is not set, the name "default"
                                      is used. If the name option exists and the
                                      server option does not exist pywbemcli
                                      attempts to retrieve the connection
                                      information from persistent storage. If the
                                      server option exists that is used as the
                                      connection
      -d, --default_namespace TEXT    Default Namespace to use in the target
                                      WBEMServer if no namespace is defined in the
                                      subcommand(EnvVar:
                                      PYWBEMCLI_DEFAULT_NAMESPACE). (Default:
                                      root/cimv2).
      -u, --user TEXT                 User name for the WBEM Server connection.
                                      (EnvVar: PYWBEMCLI_USER).
      -p, --password TEXT             Password for the WBEM Server. Will be
                                      requested as part  of initialization if user
                                      name exists and it is not  provided by this
                                      option.(EnvVar: PYWBEMCLI_PASSWORD ).
      -t, --timeout TEXT              Operation timeout for the WBEM Server in
                                      seconds. (EnvVar: PYWBEMCLI_TIMEOUT).
                                      Default: 30
      -n, --noverify                  If set, client does not verify server
                                      certificate.
      -c, --certfile TEXT             Server certfile. Ignored if noverify flag
                                      set. (EnvVar: PYWBEMCLI_CERTFILE).
      -k, --keyfile TEXT              Client private key file. (EnvVar:
                                      PYWBEMCLI_KEYFILE).
      --ca_certs TEXT                 File or directory containing certificates
                                      that will be matched against a certificate
                                      received from the WBEM server. Set the --no-
                                      verify-cert option to bypass client
                                      verification of the WBEM server certificate.
                                      (EnvVar: PYWBEMCLI_CA_CERTS).Default:
                                      Searches for matching certificates in the
                                      following system directories: /etc/pki/ca-
                                      trust/extracted/openssl/ca-bundle.trust.crt
                                      /etc/ssl/certs
                                      /etc/ssl/certificates
      -o, --output-format [mof|xml|table|csv|text]
                                      Output format (Default: mof). pywbemcli may
                                      override the format choice depending on the
                                      operation since not all formats apply to all
                                      output data types
      -v, --verbose                   Display extra information about the
                                      processing.
      --version                       Show the version of this command and exit.
      --help                          Show this message and exit.
    
    Commands:
      class       Command Group to manage CIM Classes.
      connection  Command group to manage WBEM connections.
      help        Show help message for interactive mode.
      instance    Command Group to manage CIM instances.
      qualifier   Command Group to manage CIM...
      repl        Enter interactive (REPL) mode (default) and...
      server      Command Group for WBEM server operations.



**********************
pywbemcli class --help
**********************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli class --help`

**************************
pywbemcli class get --help
**************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli class get --help`

***********************************
pywbemcli class invokemethod --help
***********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli class invokemethod --help`

********************************
pywbemcli class enumerate --help
********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli class enumerate --help`

**********************************
pywbemcli class associators --help
**********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli class associators --help`

*********************************
pywbemcli class references --help
*********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli class references --help`

***************************
pywbemcli class find --help
***************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli class find --help`

********************************
pywbemcli class hierarchy --help
********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli class hierarchy --help`

*****************************
pywbemcli instance get --help
*****************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli instance get --help`

********************************
pywbemcli instance delete --help
********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli instance delete --help`

********************************
pywbemcli instance create --help
********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli instance create --help`

**************************************
pywbemcli instance invokemethod --help
**************************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli instance invokemethod --help`

*******************************
pywbemcli instance query --help
*******************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli instance query --help`

***********************************
pywbemcli instance enumerate --help
***********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli instance enumerate --help`

*******************************
pywbemcli instance count --help
*******************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli instance count --help`

************************************
pywbemcli instance references --help
************************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli instance references --help`

*************************************
pywbemcli instance associators --help
*************************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli instance associators --help`

**************************
pywbemcli qualifier --help
**************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli qualifier --help`

************************************
pywbemcli qualifier enumerate --help
************************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli qualifier enumerate --help`

******************************
pywbemcli qualifier get --help
******************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli qualifier get --help`

***********************
pywbemcli server --help
***********************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli server --help`

*****************************
pywbemcli server brand --help
*****************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli server brand --help`

**********************************
pywbemcli server connection --help
**********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli server connection --help`

****************************
pywbemcli server info --help
****************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli server info --help`

**********************************
pywbemcli server namespaces --help
**********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli server namespaces --help`

*******************************
pywbemcli server interop --help
*******************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli server interop --help`

********************************
pywbemcli server profiles --help
********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli server profiles --help`

***************************
pywbemcli connection --help
***************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli connection --help`

********************************
pywbemcli connection show --help
********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli connection show --help`

**********************************
pywbemcli connection export --help
**********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli connection export --help`

********************************
pywbemcli connection show --help
********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli connection show --help`

*******************************
pywbemcli connection set --help
*******************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli connection set --help`

********************************
pywbemcli connection test --help
********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli connection test --help`

**********************************
pywbemcli connection select --help
**********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli connection select --help`

**********************************
pywbemcli connection create --help
**********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli connection create --help`

**********************************
pywbemcli connection delete --help
**********************************

::



**STDER:** Error: No defined connection. Use -s option to define a connection

**ERROR:** cmd `pywbemcli connection delete --help`
37 ERRORS encountered in output
