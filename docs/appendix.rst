
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
      The name of the protocol that pywbemcli uses to communicate with WBEM
      servers. CIM-XML is defined in :term:`DSP0200`.

   CIM object output formats
      Pywbemcli output formats (specified with the
      :ref:`--output-format general option`) that format the resulting CIM
      objects or CIM object paths as MOF, CIM-XML, or using the pywbem repr or
      str formatting.
      See :ref:`CIM object formats` for details.

   Table output formats
      Pywbemcli output formats (specified with the
      :ref:`--output-format general option`) that format the result as a table.
      See :ref:`Table formats` for details.

   Tree output format
      A pywbemcli output format (specified with the
      :ref:`--output-format general option`) that formats the result as a tree
      using ASCII characters.
      See :ref:`ASCII tree format` for details.

   INSTANCENAME
      A CIM instance path in a format that is suitable as a command line
      argument or option value of pywbemcli. Several commands of the instance
      command group use INSTANCENAME as a command line argument.

      The supported formats for INSTANCENAME are an untyped :term:`WBEM URI`
      and the use of wildcard keys i.e. ``CLASSNAME.?``, as detailed in
      :ref:`Specifying the INSTANCENAME command argument`.

      Examples::

        CIM_RegisteredProfile.InstanceID="acme:1"
        CIM_System.CreationClassName="ACME_System",Name="MySystem"
        CIM_System.?

   connection id
      A string that uniquely identifies each :class:`pywbem.WBEMConnection`
      object created. The connection id is immutable and is accessible as
      :attr:`pywbem.WBEMConnection.conn_id`. It is included in each log
      record and may be used to relate pywbem log records to connections.

   DeprecationWarning
      A standard Python warning that indicates a deprecated functionality.
      See section :ref:`Deprecation and compatibility policy` and the standard
      Python module :mod:`py:warnings` for details.

   CIM namespace
      A CIM namespace (defined in :term:`DSP0004`) provides a scope of
      uniqueness for CIM objects; specifically, the names of class objects and
      of qualifier type objects shall be unique in a namespace. The compound
      key of non-embedded instance objects shall also be unique across all
      non-embedded instances of the class (not including subclasses) within the
      namespace.

   connections file
      A file maintained by pywbemcli and managed by the
      :ref:`Connection command group`.
      The connections file defines a list of named WBEM connection definitions,
      each of which is either the set of parameters for connecting to a real
      WBEM server, or the set of files for creating a mock WBEM server.
      This allows connection definitions to be persisted and referenced by name
      in pywbemcli commands, via the :ref:`--name general option`.

      By default, the connections file is ``.pywbemcli_connections.yaml``
      in the user's home directory. The user's home directory depends on the
      operating system used. It is determined with ``os.path.expanduser("~")``,
      which works on all operating systems including Windows.
      See :func:`~py3:os.path.expanduser` for details.
      The default connections file can be changed using the
      ``PYWBEMCLI_CONNECTIONS_FILE`` environment variable, or with the
      :ref:`--connections-file general option`.

   MOF
      MOF (Managed Object Format) is the language used by the DMTF to
      describe in textual form CIM objects including CIM classes,
      CIM instances, etc.  It is one of the output formats provided for
      the display of CIM objects in pywbemcli. See DMTF :term:`DSP0004` for more
      information on the MOF format.

   WBEM management profile
   management profile
      WBEM management profiles define specific management functionality
      in terms of the CIM model and WBEM operations. The DMTF publishes
      management profiles in several areas and the SNIA within the SMI-S
      specification.

      Management profiles are identified by organization, name and version.
      WBEM servers advertise the management profiles that are implemented by
      the server so that they can be discovered by WBEM clients to determine
      the management capabilities of the WBEM server. This includes providing
      the clients a programmatic access to the :term:`central instances` of the
      management profile.
      For details, see :ref:`Profile advertisement methodologies`.

   central instances
      The CIM instances that act as an algorithmic focal point for accessing
      the management functionality provided by the implementation of a
      :term:`management profile` on a WBEM server.
      The central instances typically represent the central managed resource
      in the management domain that is addressed by the management profile.

   WBEM URI
      WBEM URI is a standardized text form for CIM object paths and is
      defined in :term:`DSP0207`. Pywbemcli uses the untyped WBEM URI format
      for instance names in the command line (i.e. :term:`INSTANCENAME`).

   REPL
      Stands for "Read-Execute-Print-Loop" which is a term that denotes the
      pywbemcli shell interactive mode where multiple command groups and
      commands may be executed within the context of a connection defined
      by a set of general options.

   Unix-style path name pattern
      A pattern used in Unix environments for path names (file names and
      directory names). It is used by pywbemcli for example to expand class
      names in the ``class find`` command.
      No tilde expansion is done, but ``*``, ``?``, and character ranges
      expressed with ``[]`` are supported.
      Example: ``CIM_*Device*``.

   source end role
      The reference in an association class that is on the source side when
      performing an association traversal. The source side is where the
      traversal begins.

   far end role
      The reference in an association class that is on the far side when
      performing an association traversal. The far side is where the traversal
      ends.

   traditional operations
      The CIM-XML operations originally defined by the DMTF in
      (:term:`DSP0200`) for requesting multiple instances from a WBEM server
      are ``EnumerateInstances``, ``EnumerateInstanceNames``, ``Referencess``,
      ``ReferenceNames``, ``Associators``, ``AssociatorNames``, and
      ``ExecQuery``. These are monolithic operations and expect the WBEM server
      to prepare complete responses before returning any results. Because the
      response must be either contain all of the requested instances or
      an error response they causes issues with very large reponses. In later
      versions of (:term:`DSP0200`), an alternative  to the above operations
      named pull operations were added to improve memory and response
      efficiency.

   backslash-escaped
      The UNIX-like shells interpret single and double quotes in a certain way
      and remove them before passing the arguments on to the program invoked.
      Because the single and double quotes in INSTANCENAME need to be passed on
      to pywbemcli, they need to be protected from removal by the shell. This
      can be achieved by putting INSTANCENAME into single quotes if it only
      includes double quotes, or into double quotes if it only includes single
      quotes. If there is a mix of single and double quotes in INSTANCENAME, or
      if shell variables need to be expanded, this can be achieved by
      backslash-escaping any double quotes in INSTANCENAME, and putting it into
      double quotes.

   default connection
      A connection definition in the :term:`connections file` that is used
      by pywbemcli as the :term:`current connection` if pywbemcli is started without
      any connection definition (no :ref:`--server general option`,
      :ref:`--mock-server general option`, or :ref:`--name general option`) and
      the default connection is defined.
      A connection definition in the :term:`connections file` becomes the
      default connection on pywbemcli startup if it is specified using the
      :ref:`connection select command` and the
      ``--default``/``-d`` command option is used.

   current connection
      The connection definition in pywbemcli that is currently active; it is the
      target connection for pywbemcli commands.  The current
      connection is created on pywbemcli startup with the following options
      :ref:`--server general option`,
      :ref:`--mock-server general option`, or :ref:`--name general option` or
      if a :term:`default connection`) has been defined. The current connection can be
      changed in the interactive mode with the :ref:`connection select command`.

   CQL
      CQL (CIM Query Language) is a query language defined by DMTF for use
      by query operations against WBEM servers. In operation parameters that
      define the use of a query language, it is specified with the string
      ``DMTF:QCL``. CQL is described in DMTF standard :term:`DSP0202`.

.. _`Profile advertisement methodologies`:

Profile advertisement methodologies
-----------------------------------

This section briefly explains the profile advertisement methodologies defined
by DMTF. A full description can be found in :term:`DSP1033`.

These methodologies describe how a client can discover the central instances
of a management profile. Discovering the :term:`central instances` through a
:term:`management profile` is the recommended approach for clients, over simply enumerating a CIM
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

   DSP0202
      `DMTF DSP0202, CIM Query Language Specification, Version 1.0 <https://www.dmtf.org/standards/published_documents/DSP0202_1.0.0.pdf>`_

   DSP0207
      `DMTF DSP0207, WBEM URI Mapping, Version 1.0 <https://www.dmtf.org/standards/published_documents/DSP0207_1.0.pdf>`_

   DSP0212
      `DMTF DSP0212, Filter Query Language, Version 1.0 <https://www.dmtf.org/standards/published_documents/DSP0212_1.0.pdf>`_

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
      A WBEM client and WBEM listener written in Python. See `pywbem GitHub repository <http://pywbem.github.io/pywbemtools/index.html>`_ and the
      `pywbem package on Pypi <https://pypi.org/project/pywbem/>`_.
