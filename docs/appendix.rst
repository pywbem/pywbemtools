
.. _`Appendix`:

Appendix
========

This section contains information that is referenced from other sections,
and that does not really need to be read in sequence.


.. _'Special terms`:

Special terms
-------------

This documentation uses a few special terms to refer to Python types:

.. glossary::

   CIM-XML
      The name of the protocol used in the DMTF specification :term:`DSP0200`
      that pywbem/pywbemcli use to communicate with WBEM servers.

   CIM model output formats
      Several of the output formats defined and available in the
      ``-o\--output-format`` general option are specific for the presentation
      of CIM objects(CIMClass, CIMInstance, CIMParameter, CIMMethod,
      CIMClassName and CIMInstanceName) This includes the format choices
      ``mof`` , ``xml`` , ``repr`` , and ``txt`` .

   INSTANCENAME
      an argument of several of the command-group ``instance`` subcommands that
      allows two possible inputs based on another subcommand option( ``--interactive`` ).

      When the ``interactive`` option is not set, the INSTANCENAME is a string
      representation of a CIMInstanceName must be formatted as defined by
      :term:`WBEM-URI`

      Otherwise the INSTANCENAME should be a classname in which case pywbemcli
      will get the instance names from the WBEM server and present a
      selection list for the user to select an instance
      name :ref:`Displaying CIM instances or CIM instance names`

   connection id
      a string that uniquely identifies each :class:`pywbem.WBEMConnection`
      object created. The connection id is immutable and is accessible from
      :attr:`pywbem.WBEMConnection.conn_id`. It is included in of each log
      record created for pywbem log output and may be used to correlate pywbem
      log records for a single connection.

   DeprecationWarning
      a standard Python warning that indicates a deprecated functionality.
      See section :ref:`Deprecation and compatibility policy` and the standard
      Python module :mod:`py:warnings` for details.

   CIM namespace
      A CIM namespace (defined in :term:`DSP0004`) provides a scope of
      uniqueness  for cim objects; specifically, the names of class objects and
      of qualifier type objects shall be unique in a namespace. The compound
      key of non- embedded instance objects shall also be unique across all
      non-embedded instances of the class (not including subclasses) within the
      namespace.

   connections file
      A file maintained by pywbemcli and managed by the pywbemcli
      ``connections`` command group.  The file name is ``pywbemcli_connections.json``
      and the file must be in the directory in which pywbemcli is executed.
      Multiple connection files may exist in different directories.
      The connection file contains a JSON definition of the parameters for
      each connection with a name for the connection so that connections may
      be predefined and pywbemcli commands executed against them using only
      the connection name.

   MOF
      MOF(Managed Object Format) is the language used by the DMTF to
      describe in textual form CIM objects including CIM classes,
      CIM Instance, etc.  It is one of the output formats provided for
      the display of CIM objects in pywbemcli. See DMTF term:`DSP0004` for more
      information on the MOF format.

   WBEM management profile
      The DMTF and SNIA define specific profiles of manageability that are
      published as specifications in the DMTF and within the SMI-S specification
      in SNIA. A management profile defines the manageability characteristics
      of a specic set of services in terms of the CIM model and WBEM operations.
      These profiles are documented by name and version and are incorporated into
      compliant WBEM servers so that they can be discovered by WBEM clients to
      determine the management capabilities of the WBEM server.
      See :ref:`Profile advertisement methodologies`

   WBEM-URI
      The wbem-uri is a standardized text form for CIM instance names. It is
      documented in DMTF :term:`DSP0207`. Pywbemcli uses the untyped WBEM URI
      as the format for instance names in CLI input parameters
      (i.e. :term:`INSTANCENAME`)::

            WBEM-URI = WBEM-URI-UntypedNamespacePath /
                       WBEM-URI-UntypedClassPath /
                       WBEM-URI-UntypedInstancePath

            WBEM-URI-UntypedNamespacePath = namespacePath
            WBEM-URI-UntypedClassPath     = namespacePath ":" className
            WBEM-URI-UntypedInstancePath  = WBEM-URI-UntypedInstancePath
                                            className "." key_value_pairs

            namespacePath = [namespaceType ":"] namespaceHandle
            namespaceType = ("http" ["s"]) / ("cimxml.wbem" ["s"])
            namespaceHandle = ["//" authority] "/" [namespaceName]
            namespaName     = IDENTIFIER *("/"IDENTIFIER))

            // Untyped key value pairs
            key_value_pairs  = key_value_pair *("," key_value_pair)
            key_value_pair   = key_name "=" key_value
            key_value        = stringValue / charValue / booleanValue /
                               integerValue / realValue /
                               "\"" datetimeValue "\"" /
                               "\"" referenceValue "\""

      In pywbemcli the WBEM-URI is used as the format for instance names on
      commands such as ``instance get <instance-name>``

      In these cases, the normal use is to specify only the classname and
      keybindings so that examples of valid WBEM-URIs would be::

        CIM_RegisteredProfile.InstanceID="acme:1"
        CIM_RegisteredProfile.InstanceID=100

   REPL
      Stands for "Read-Execute-Print-Loop" which is a term that denotes the
      pywbemcli shell interactive mode where multiple command-groups and
      subcommands may be executed within the context of a connection defined
      by a set of general options.

   GLOB
      A pathname pattern pattern expansion used in Unix environments. It is
      used by pywbemcli to expand classnames in the ``class find`` subcommand.
      No tilde expansion is done, but ``*``, ``?``, and character ranges
      expressed with ``[]`` will be correctly matched.


.. _`Profile advertisement methodologies`:

Profile advertisement methodologies
-----------------------------------

This section briefly explains the profile advertisement methodologies defined
by DMTF. A full description can be found in :term:`DSP1033`.

These methodologies describe how a client can discover the central instances
of a management profile. Discovering the central instances through a management
profile is the recommended approach for clients, over simply enumerating a CIM
class of choice. The reason is that this approach enables clients to work
seamlessly with different server implementations, even when they have
implemented a different set of management profiles.

The DMTF defines three profile advertisement methodologies in :term:`DSP1033`:

* GetCentralInstances methodology (new in :term:`DSP1033` 1.1)
* Central class methodology
* Scoping class methodology

At this point, the GetCentralInstances methodology has not widely been
implemented, but pywbem supports it nevertheless.

All three profile advertisement methodologies start from the
`CIM_RegisteredProfile` instance that identifies the management profile, by
means of registered organization, registered name, and registered version.

It is important to understand that the `CIM_RegisteredProfile` instance not
only identifies the management profile, but represents a particular use of the
management profile within its scoping profiles. For an autonomous profile,
there are no scoping profiles, so in that case, there is only one use of the
autonomous profile in a server. However, component profiles do have scoping
profiles, and it is well possible that a component profile is used multiple
times in a server, in different scoping contexts. If that is the case, and if
discovery of central instances using any of the profile advertisement
methodologies is supposed to work, then each such use of the profile needs to
have its own separate `CIM_RegisteredProfile` instance, because each such
use of the profile will also have its own separate set of central instances.

Unfortunately, neither the DMTF standards nor the SMI-S standards are clear
about that requirement, and so there are plenty of implementations that
share a single `CIM_RegisteredProfile` instance identifying a particular
component profile, for multiple distinct uses of the profile by its scoping
profiles. In such a case, the profile advertisement methodologies will
not be able to distinguish the distinct sets of central instances alone,
and other means need to be used to distinguish them.

It is also important to understand that the choice which profile advertisement
methodology to implement, is done by the WBEM server side. Therefore, a WBEM
client such as pywbem needs to support all methodologies and needs to try them
one by one until one succeeds. Pywbem tries the three methodologies in the
order listed above.

In the *GetCentralInstances methodology*, the `CIM_RegisteredProfile` instance
has a CIM method named `GetCentralInstances` that returns the instance paths
of the central instances of the use of the profile.

In the *central class methodology*, the `CIM_RegisteredProfile` instance
is associated directly with the set of central instances of the use of the
profile, via a `CIM_ElementConformsToProfile` association.

In the *scoping class methodology*, the `CIM_RegisteredProfile` instance
is not associated directly with the set of central instances of the use of the
profile, but delegates that to its scoping profile.
The client navigates up to the `CIM_RegisteredProfile` instance representing
the (use of the) scoping profile, looks up its central instances, and
from each of those, navigates down along the reversed scoping path to the
central instances of the profile in question. The scoping path of a component
profile describes the traversal across associations and ordinary classes from
the central class to the scoping class of the profile. This profile
advertisement methodology is obviously the most complex one of the three.

Pywbem encapsulates the complexity and choice of these methodologies into
a single invocation of an easy-to use method
:meth:`pywbem.WBEMServer.get_central_instances`.

Profile implementations in a WBEM server are not entirely free when making a
choice of which methodology to implement:

* Autonomous profiles in a WBEM server must implement the central-class
  methodology, and may in addition implement the GetCentralInstances
  methodology.

  Note that the scoping class methodology falls together with the
  central class methodology for autonomous profiles, because their scoping
  class is also their central class.

* Component profiles in a WBEM server may implement the central class
  methodology and the GetCentralInstances methodology, and must support the
  scoping class methodology.

  Note that implementing the scoping class methodology in a WBEM server
  requires implementing the classes and associations of the scoping path,
  which are usually mandatory anyway. So while the scoping class methodology
  is more complex to use for clients than the central class methodology, it is
  easier to implement for servers.

Use of the scoping class methodology by a client requires knowing the central
class, scoping class and scoping path defined by the component profile.

:term:`DSP1001` requires that conformant autonomous profiles specify a central
class, and that conformant component profiles specify a central class, scoping
class and a scoping path.

Older DMTF component profiles and older SNIA subprofiles do not always specify
scoping class and scoping path. In such cases, the scoping class and scoping
path can often be determined from the class diagram in the specification for
the profile.
Many times, ``CIM_System`` or ``CIM_ComputerSystem`` is the scoping class.
.. _'Glossary`:

Glossary
--------

.. glossary::


.. _`References`:

References
----------

.. glossary::

   DSP0004
      `DMTF DSP0004, CIM Infrastructure, Version 2.8 <https://www.dmtf.org/standards/published_documents/DSP0004_2.8.pdf>`_

   DSP0200
      `DMTF DSP0200, CIM Operations over HTTP, Version 1.4 <https://www.dmtf.org/standards/published_documents/DSP0200_1.4.pdf>`_

   DSP0201
      `DMTF DSP0201, Representation of CIM in XML, Version 2.4 <https://www.dmtf.org/standards/published_documents/DSP0201_2.4.pdf>`_

   DSP0207
      `DMTF DSP0207, WBEM URI Mapping, Version 1.0 <https://www.dmtf.org/standards/published_documents/DSP0207_1.0.pdf>`_

   DSP0212
      `DMTF DSP0212, Filter Query Language, Version 1.0.1 <https://www.dmtf.org/standards/published_documents/DSP0212_1.0.1.pdf>`_

   DSP1001
      `DMTF DSP1001, Management Profile Specification Usage Guide, Version 1.1 <https://www.dmtf.org/standards/published_documents/DSP1001_1.1.pdf>`_

   DSP1033
      `DMTF DSP1033, Profile Registration Profile, Version 1.1 <https://www.dmtf.org/standards/published_documents/DSP1033_1.1.pdf>`_

   RFC3986
      `IETF RFC3986, Uniform Resource Identifier (URI): Generic Syntax, January 2005 <https://tools.ietf.org/html/rfc3986>`_

   RFC6874
      `IETF RFC6874, Representing IPv6 Zone Identifiers in Address Literals and Uniform Resource Identifiers, February 2013 <https://tools.ietf.org/html/rfc6874>`_

   WBEM Standards
      `DMTF WBEM Standards <https://www.dmtf.org/standards/wbem>`_

   SMI-S
      `SNIA Storage Management Initiative Specification <https://www.snia.org/forums/smi/tech_programs/smis_home>`_

   Python Glossary
      * `Python 2.7 Glossary <https://docs.python.org/2.7/glossary.html>`_
      * `Python 3.4 Glossary <https://docs.python.org/3.4/glossary.html>`_

   pywbem
      pywbem is both a `github repository <http://pywbem.github.io/pywbemtools/index.html>`_ and the Python package pywbem, a WBEM client and  WBEM listener within this repository.
