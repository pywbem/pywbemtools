"""
    Define the classes and instances to mock a WEMServer as the basis for
    other test mocks

    This was modified from an equivalent test tool in pywbem
"""

from __future__ import print_function, absolute_import

import os

from pywbem import ValueMapping, CIMInstance, CIMInstanceName, Error, \
    CIM_ERR_ALREADY_EXISTS
from pywbem_mock import FakedWBEMConnection

# from .dmtf_mof_schema_def import DMTF_TEST_SCHEMA_VER

DMTF_TEST_SCHEMA_VER = (2, 49, 0)

# test that GLOBALS exist. They should be provided by pywbemcli
assert "CONN" in globals()
assert 'SERVER' in globals()
assert 'VERBOSE'in globals()


# Location of DMTF schema directory used by all tests.
# This directory is permanent and should not be removed.
TESTSUITE_SCHEMA_DIR = os.path.join('tests', 'schema')

# The following dictionary represents the data required to build a
# set of classes and instances for a mock WbemServer. This dictionary defines
# the following elements of a wbem server:
#
#  dmtf_schema: The DMTF schema version (ex (2, 49, 0) of the schema that
#  will be installed and the directory into which it will be installed
#
#  system_name: The name of the system (used by the CIM_ObjectManager)
#
#  object_manager: A dictionary that defines variable element for the
#  CIM_ObjectManager class.
#
#  interop_namespace: The interop namespace. Note that that if the interop
#  namespace is defined in the WbemServerMock init method that overrides any
#  value in this dictionary
#
#  other_namespaces: Any other namespaces that the users wants to be defined
#  in the mock repository
#
#  registered_profiles: The Organization, profile name, profile version for any
#  registered profiles
#
#  referenced_profiles: Definition of CIM_ReferencedProfile associations
#  between CIM_RegisteredProfiles. This is used to test get_central_instances
#
#
DEFAULT_WBEM_SERVER_MOCK_DICT = {
    'dmtf_schema': {'version': DMTF_TEST_SCHEMA_VER,
                    'dir': TESTSUITE_SCHEMA_DIR},
    'pg_schema': {
        'dir': os.path.join(TESTSUITE_SCHEMA_DIR, 'OpenPegasus'),
        'files': ['PG_Namespace.mof']},

    'class_names': ['CIM_Namespace',
                    'CIM_ObjectManager',
                    'CIM_RegisteredProfile',
                    'CIM_ElementConformsToProfile',
                    'CIM_ReferencedProfile',
                    'CIM_ComputerSystem'],
    'class-mof': ["class MCK_StorageComputerSystem : CIM_ComputerSystem{};", ],
    'system_name': 'Mock_WBEMServerTest',
    'object_manager': {'Name': 'FakeObjectManager',
                       'ElementName': 'Pegasus',
                       'Description': 'Pegasus CIM Server Version 2.15.0'
                                      ' Released', },
    'interop_namspace': 'interop',
    'other_namespaces': [],
    'registered_profiles': [('DMTF', 'Indications', '1.1.0'),
                            ('DMTF', 'Profile Registration', '1.0.0'),
                            ('SNIA', 'Server', '1.2.0'),
                            ('SNIA', 'Server', '1.1.0'),
                            ('SNIA', 'SMI-S', '1.2.0'),
                            ('SNIA', 'Array', '1.4.0'),
                            ('SNIA', 'Software', '1.4.0'),
                            ('DMTF', 'Component', '1.4.0'), ],

    'referenced_profiles': [
        (('SNIA', 'Server', '1.2.0'), ('DMTF', 'Indications', '1.1.0')),
        (('SNIA', 'Server', '1.2.0'), ('SNIA', 'Array', '1.4.0')),
        (('SNIA', 'Array', '1.4.0'), ('DMTF', 'Component', '1.4.0')),
        (('SNIA', 'Array', '1.4.0'), ('SNIA', 'Software', '1.4.0')),

    ],
    # define profile relation to central class instance
    # First element is a profile, second is name and keybindings of a
    # CIMInstanceName
    'element_conforms_to_profile': [
        (('SNIA', 'Server', '1.2.0'),
         ("MCK_StorageComputerSystem", {'Name': "10.1.2.3",
                                        'CreationClassName':
                                            "MCK_StorageComputerSystem"})), ],
    # List of CIMInstances. Each entry is a CIM instance with classname,
    # and properties. All properties required to build the path must be
    # defined. No other properties are required for this test.
    # TODO: We may expand this for more scoping tests.
    'central-instances': [
        CIMInstance(
            'MCK_StorageComputerSystem',
            properties={
                'Name': "10.1.2.3",
                'CreationClassName': "MCK_StorageComputerSystem",
                'NameFormat': "IP"}),
    ],
    'scoping-instances': []
}


class WbemServerMock(object):
    # pylint: disable=useless-object-inheritance, too-many-instance-attributes
    """
    Class that mocks the classes and methods used by the pywbem
    WBEMServer class so that the WBEMServer class will produce valid data
    for the server CIM_ObjectManager, CIM_Namespace, CIM_RegisteredProfile
    instances.

    This can be used to test the WbemServer class but is also required for
    other tests such as the Subscription manager since that class is based
    on getting data from the WbemServer class (ex. namespace)

    It allows building a the instance data for a particular server either
    from user defined input or from standard data predefined for pywbem
    tests
    """

    def __init__(self, interop_ns=None, server_mock_data=None, verbose=None):
        """
        Build the class repository for with the classes defined for
        the WBEMSERVER.  This is built either from a dictionary of data
        that represents the mock wbem server with the elements defined in
        DEFAULT_WBEM_SERVER_MOCK_DICT or if server_mock_data is None from
        the DEFAULT_WBEM_SERVER_MOCK_DICT dictionary.
        """
        self.verbose = verbose
        if server_mock_data is None:
            self.server_mock_data = DEFAULT_WBEM_SERVER_MOCK_DICT
        else:
            self.server_mock_data = server_mock_data

        self.system_name = self.server_mock_data['system_name']
        self.object_manager_name = \
            self.server_mock_data['object_manager']['Name']

        # override dictionary interop namespace with init parameter
        if interop_ns:
            self.interop_ns = interop_ns
        else:
            self.interop_ns = self.server_mock_data['interop_ns']

        self.dmtf_schema_ver = self.server_mock_data['dmtf_schema']['version']
        self.schema_dir = self.server_mock_data['dmtf_schema']['dir']
        self.pg_schema_dir = self.server_mock_data['pg_schema']['dir']
        self.pg_schema_files = self.server_mock_data['pg_schema']['files']
        self.registered_profiles = self.server_mock_data['registered_profiles']
        # Retrieved from globals setup by pywbemcli for
        #  WBEMConnection object
        #  WBEMServer object
        global CONN  # pylint: disable=global-variable-not-assigned
        self.conn = CONN  # pylint: disable=undefined-variable
        global SERVER  # pylint: disable=global-variable-not-assigned
        self.wbem_server = SERVER  # pylint: disable=undefined-variable

        self.build_mock()

    def __str__(self):
        ret_str = 'object_manager_name=%r, interop_ns=%r, system_name=%r, ' \
            'dmtf_schema_ver=%r, schema_dir=%r, wbem_server=%s' % \
            (self.object_manager_name, self.interop_ns, self.system_name,
             self.dmtf_schema_ver, self.schema_dir,
             getattr(self, 'wbem_server', None))
        return ret_str

    def __repr__(self):
        """
        Return a representation of the class object
        with all attributes, that is suitable for debugging.
        """
        ret_str = 'WBEMServerMock(object_manager_name=%r, interop_ns=%r, ' \
            'system_name=%r, dmtf_schema_ver=%r, schema_dir=%r, ' \
            'pg_schema_dir=%r, pg_schema_files=%s, wbem_server=%r, ' \
            'registered_profiles=%r)' % \
            (self.object_manager_name, self.interop_ns, self.system_name,
             self.dmtf_schema_ver, self.schema_dir, self.pg_schema_dir,
             self.pg_schema_files,
             getattr(self, 'wbem_server', None), self.registered_profiles)
        return ret_str

    def build_classes(self, namespace):
        """
        Build the schema qualifier declarations, and the class objects in the
        repository from a DMTF schema.
        This requires only that the leaf objects be defined in a mof
        include file since the compiler finds the files for qualifiers
        and dependent classes.

        Returns:
            Instance of FakedWBEMConnection object.
        """
        # pylint: disable=protected-access

        FakedWBEMConnection._reset_logging_config()

        # Note: During tests, not needed.  When you run direct from
        # pywbemcli it fails
        try:
            self.conn.add_namespace(namespace)
        except Error as er:
            if er.status_code != CIM_ERR_ALREADY_EXISTS:
                raise

        self.conn.compile_dmtf_schema(
            self.dmtf_schema_ver, self.schema_dir,
            class_names=self.server_mock_data['class_names'],
            namespace=namespace,
            verbose=self.verbose)

        for filename in self.pg_schema_files:
            filepath = os.path.join(self.pg_schema_dir, filename)
            self.conn.compile_mof_file(filepath, namespace=namespace,
                                       search_paths=[self.pg_schema_dir],
                                       verbose=self.verbose)

        # compile the mof defined in the 'class-mof definitions
        for mof in self.server_mock_data['class-mof']:
            self.conn.compile_mof_string(mof, namespace=namespace,
                                         verbose=self.verbose)

    def inst_from_classname(self, class_name, namespace=None,
                            property_list=None,
                            property_values=None,
                            include_missing_properties=True,
                            include_path=True):
        # pylint: disable=too-many-arguments
        """
        Build instance from classname using class_name property to get class
        from a repository.
        """
        cls = self.conn.GetClass(class_name,
                                 namespace=namespace,
                                 LocalOnly=False,
                                 IncludeQualifiers=True,
                                 include_class_origin=True,
                                 property_list=property_list)

        return CIMInstance.from_class(
            cls, namespace=namespace,
            property_values=property_values,
            include_missing_properties=include_missing_properties,
            include_path=include_path)

    def build_obj_mgr_inst(self, system_name, object_manager_name,
                           object_manager_element_name,
                           object_manager_description):
        """
        Build a CIMObjectManager instance for the mock wbem server using
        fixed data defined in this method and data from the init parameter
        mock data. Build into interop namespace always
        """
        omdict = {"SystemCreationClassName": "CIM_ComputerSystem",
                  "CreationClassName": "CIM_ObjectManager",
                  "SystemName": system_name,
                  "Name": object_manager_name,
                  "ElementName": object_manager_element_name,
                  "Description": object_manager_description}

        ominst = self.inst_from_classname("CIM_ObjectManager",
                                          namespace=self.interop_ns,
                                          property_values=omdict,
                                          include_missing_properties=False,
                                          include_path=True)

        self.conn.add_cimobjects(ominst, namespace=self.interop_ns)

        rtn_ominsts = self.conn.EnumerateInstances("CIM_ObjectManager",
                                                   namespace=self.interop_ns)
        assert len(rtn_ominsts) == 1, \
            "Expected 1 ObjetManager instance, got %r" % rtn_ominsts

        return ominst

    def build_cimnamespace_insts(self, namespaces=None):
        """
        Build instances of CIM_Namespace defined by namespaces list parameter.
        These instances are built into the interop namespace. They allow the
        standard WBEM tools for getting and creating namespaces to work.
        """
        for namespace in namespaces:
            nsdict = {"SystemName": self.system_name,
                      "ObjectManagerName": self.object_manager_name,
                      'Name': namespace,
                      'CreationClassName': 'PG_Namespace',
                      'ObjectManagerCreationClassName': 'CIM_ObjectManager',
                      'SystemCreationClassName': 'CIM_ComputerSystem'}

            nsinst = self.inst_from_classname("PG_Namespace",
                                              namespace=self.interop_ns,
                                              property_values=nsdict,
                                              include_missing_properties=False,
                                              include_path=True)
            self.conn.add_cimobjects(nsinst, namespace=self.interop_ns)

        rtn_namespaces = self.conn.EnumerateInstances("CIM_Namespace",
                                                      namespace=self.interop_ns)
        assert len(rtn_namespaces) == len(namespaces), \
            "Expected namespaces: %r, got %s" % (namespaces, rtn_namespaces)

    def build_reg_profile_insts(self, profiles):
        """
        Build and install in repository the registered profiles defined by
        the profiles parameter. A dictionary of tuples where each tuple
        contains RegisteredOrganization, RegisteredName, RegisteredVersion

        Parameters:
          conn:
          profiles (dict of lists where each list contains org, name, version
             for a profiles)
        """
        # Map ValueMap to Value
        org_vm = ValueMapping.for_property(self.conn, self.interop_ns,
                                           'CIM_RegisteredProfile',
                                           'RegisteredOrganization')

        # This is a workaround hack to get ValueMap from Value
        org_vm_dict = {}   # reverse mapping dictionary (valueMap from Value)
        for value in range(0, 22):
            org_vm_dict[org_vm.tovalues(value)] = value

        for profile in profiles:
            instance_id = '%s+%s+%s' % (profile[0], profile[1], profile[2])
            reg_prof_dict = {'RegisteredOrganization': org_vm_dict[profile[0]],
                             'RegisteredName': profile[1],
                             'RegisteredVersion': profile[2],
                             'InstanceID': instance_id}
            rpinst = self.inst_from_classname("CIM_RegisteredProfile",
                                              namespace=self.interop_ns,
                                              property_values=reg_prof_dict,
                                              include_missing_properties=False,
                                              include_path=True)

            self.conn.add_cimobjects(rpinst, namespace=self.interop_ns)

        rtn_rpinsts = self.conn.EnumerateInstances("CIM_RegisteredProfile",
                                                   namespace=self.interop_ns)
        assert rtn_rpinsts, \
            "Expected 1 or more RegisteredProfile instances, got none"

    def build_elementconformstoprofile_inst(self, profile_path, element_path):
        """
        Build an instance of CIM_ElementConformsToProfile and insert into
        repository
        """
        class_name = 'CIM_ElementConformsToProfile'
        element_conforms_dict = {'ConformantStandard': profile_path,
                                 'ManagedElement': element_path}

        inst = self.inst_from_classname(class_name,
                                        namespace=self.interop_ns,
                                        property_values=element_conforms_dict,
                                        include_missing_properties=False,
                                        include_path=True)

        self.conn.add_cimobjects(inst, namespace=self.interop_ns)

        assert self.conn.EnumerateInstances(class_name,
                                            namespace=self.interop_ns)
        assert self.conn.GetInstance(inst.path)

    def build_referenced_profile_insts(self, referenced_profiles):
        """
        Build and install in repository the referemced profile instances
        defined by the referemces parameter. A dictionary of tuples where each
        tuple contains Antecedent and Dependent reference in terms of the
        profile name as a tuple (org, name, version).

        Parameters:
          profiles (dict of tuples where each tuple defines the antecedent
          and dependent)
        """
        class_name = 'CIM_ReferencedProfile'
        for profile_name in referenced_profiles:
            antecedent = profile_name[0]
            dependent = profile_name[1]
            antecedent_inst = self.wbem_server.get_selected_profiles(
                registered_org=antecedent[0],
                registered_name=antecedent[1],
                registered_version=antecedent[2])
            dependent_inst = self.wbem_server.get_selected_profiles(
                registered_org=dependent[0],
                registered_name=dependent[1],
                registered_version=dependent[2])

            assert len(antecedent_inst) == 1, \
                "Antecedent: {0}".format(antecedent)
            assert len(dependent_inst) == 1, \
                "Dependent: {0}".format(dependent)

            ref_profile_dict = {'Antecedent': antecedent_inst[0].path,
                                'Dependent': dependent_inst[0].path}

            inst = self.inst_from_classname(class_name,
                                            namespace=self.interop_ns,
                                            property_values=ref_profile_dict,
                                            include_missing_properties=False,
                                            include_path=True)

            self.conn.add_cimobjects(inst, namespace=self.interop_ns)

            assert self.conn.EnumerateInstances(class_name,
                                                namespace=self.interop_ns)
            assert self.conn.GetInstance(inst.path)

    def build_central_instances(self, central_instances):
        """
        Build the central_instances from the definitions provided in the list
        central_instance where each definition is a python CIMInstance object
        and add them to the repository. This method adds the path to each
        """
        for inst in central_instances:
            cls = self.conn.GetClass(inst.classname, namespace=self.interop_ns,
                                     LocalOnly=False, IncludeQualifiers=True,
                                     IncludeClassOrigin=True)
            inst.path = CIMInstanceName.from_instance(
                cls, inst, namespace=self.interop_ns, strict=True)

            self.conn.add_cimobjects(inst, namespace=self.interop_ns)

    def build_mock(self):
        """
            Builds the classes and instances for a mock WBEMServer from data
            in the init parameter. This calls the builder for:
              the object manager
              the namespaces
              the profiles
        """

        self.build_classes(self.interop_ns)

        if self.verbose:
            print("Built classes")
            self.conn.display_repository()

        # NOTE: The wbemserver is not complete until the instances for at
        # least object manager and namespaces have been inserted. Any attempt
        # to display the instance object before that will fail because the
        # enumerate namespaces will be inconsistent

        # Build CIM_ObjectManager instance into the interop namespace since
        # this is required to build namespace instances
        om_inst = self.build_obj_mgr_inst(
            self.system_name,
            self.object_manager_name,
            self.server_mock_data['object_manager']['ElementName'],
            self.server_mock_data['object_manager']['Description'])

        if self.verbose:
            print("Built object manager object")
            self.conn.display_repository()

        # build CIM_Namespace instances based on the init parameters
        namespaces = [self.interop_ns]
        if self.server_mock_data['other_namespaces']:
            namespaces.extend(self.server_mock_data['other_namespaces'])
        self.build_cimnamespace_insts(namespaces)

        if self.verbose:
            print("Built namespace instances")
            self.conn.display_repository()

        self.build_reg_profile_insts(self.registered_profiles)

        self.build_referenced_profile_insts(
            self.server_mock_data['referenced_profiles'])

        if self.verbose:
            print("Built profile instances")
            self.conn.display_repository()

        self.build_central_instances(self.server_mock_data['central-instances'])

        # Get element conforms for SNIA server to object manager
        # TODO this should be driven by the input dictionary
        prof_inst = self.wbem_server.get_selected_profiles(
            registered_org='SNIA',
            registered_name='Server',
            registered_version='1.1.0')
        # TODO this is simplistic form and only builds one instance of
        # conforms to.  Should expand but need better way to define instance
        # at other end.

        self.build_elementconformstoprofile_inst(prof_inst[0].path,
                                                 om_inst.path)

        # build element_conforms_to_profile insts from dictionary
        for item in self.server_mock_data['element_conforms_to_profile']:
            profile_name = item[0]
            # TODO we are fixing the host name here.  should get from conn
            central_inst_path = CIMInstanceName(
                item[1][0],
                keybindings=item[1][1],
                host='FakedUrl',
                namespace=self.wbem_server.interop_ns)
            prof_insts = self.wbem_server.get_selected_profiles(
                registered_org=profile_name[0],
                registered_name=profile_name[1],
                registered_version=profile_name[2])
            assert len(prof_insts) == 1

            self.build_elementconformstoprofile_inst(prof_insts[0].path,
                                                     central_inst_path)

        if self.verbose:
            print("Built central instances and element_conforms_to_Profile")
            self.conn.display_repository()


# Execute the WBEM Server configuration build
global VERBOSE  # pylint: disable=global-variable-not-assigned

MOCK_WBEMSERVER = WbemServerMock(interop_ns="interop",
                                 verbose=False)  # noqa: F821
# server = MOCK_WBEMSERVER.wbem_server
