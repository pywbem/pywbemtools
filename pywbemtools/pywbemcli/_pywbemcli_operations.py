# (C) Copyright 2017 IBM Corp.
# (C) Copyright 2017 Inova Development Inc.
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
Mixin class that adds methods to WBEMConnection and FakeWBEMConnection for
pywbemcli usage

This contains only methods that use the iter<...> operations  but also execute
the complete iterations so that we can use these as common operations for
pywbemcli instead of having to execute an algorithm of pull vs non-pull
everywhere xa WBEMConnection possible pull operation is called.

It also adds a method to FakeWBEMConnection to build the repository.
"""

from __future__ import absolute_import, print_function

import os
import io
import errno
import glob
import hashlib
import pickle
import click
import packaging.version
import pywbem
import pywbem_mock

from .config import DEFAULT_MAXPULLCNT
from ._utils import ensure_bytes, ensure_unicode, DEFAULT_CONNECTIONS_FILE
from . import mockscripts

PYWBEM_VERSION = packaging.version.parse(pywbem.__version__)


#  __all__ = ['PYWBEMCLIConnection', 'PYWBEMCLIFakedConnection']


# pylint: disable=useless-object-inheritance
class PYWBEMCLIConnectionMixin(object):
    """
    Mixin class to extend WBEMConnection with a set of methods that use the
    iter<...> methods as the basis for getting Instances, etc. but add the
    generator processing to retrieve the instances.  These can be used within
    pywbemcli to allow one method call to ack as either a pull or traditional
    operation pushing the differences into this mixin.

    These methods do not resolve the core issues between the traditional and
    pull operations such as the fact that only the pull operations pass
    the FilterQuery parameter.

    They are a pywbemcli convience to simplify the individual action processing
    methods to a single call.
    """
    def PyWbemcliEnumerateInstancePaths(self, ClassName, namespace=None,
                                        FilterQueryLanguage=None,
                                        FilterQuery=None,
                                        OperationTimeout=None,
                                        ContinueOnError=None,
                                        MaxObjectCount=DEFAULT_MAXPULLCNT,
                                        **extra):
        # pylint: disable=unused-argument
        # pylint: disable=invalid-name
        """
        Execute IterEnumerateInstancePaths and retrieve the instances. Returns
        the returned instances.

        Uses the same parameters as the IterEnumerateInstancePaths method.

        All exceptions from the underlying command are passed through this
        method.
        """

        result = self.IterEnumerateInstancePaths(
            ClassName,
            namespace=namespace,
            FilterQueryLanguage=FilterQueryLanguage,
            FilterQuery=FilterQuery,
            OperationTimeout=OperationTimeout,
            ContinueOnError=ContinueOnError,
            MaxObjectCount=MaxObjectCount)
        return list(result)

    def PyWbemcliEnumerateInstances(self, ClassName, namespace=None,
                                    LocalOnly=None,
                                    DeepInheritance=None,
                                    IncludeQualifiers=None,
                                    IncludeClassOrigin=None, PropertyList=None,
                                    FilterQueryLanguage=None, FilterQuery=None,
                                    OperationTimeout=None, ContinueOnError=None,
                                    MaxObjectCount=DEFAULT_MAXPULLCNT,
                                    **extra):
        # pylint: disable=unused-argument
        # pylint: disable=invalid-name
        """
        Execute IterEnumerateInstances and retrieve the instances. Returns
        the returned instances.

        Uses the same parameters as the IterEnumerateInstances method.

        All exceptions from the underlying method are passed through this
        method.
        """

        result = self.IterEnumerateInstances(
            ClassName,
            namespace=namespace,
            LocalOnly=LocalOnly,
            DeepInheritance=DeepInheritance,
            IncludeQualifiers=IncludeQualifiers,
            IncludeClassOrigin=IncludeClassOrigin,
            PropertyList=PropertyList,
            FilterQueryLanguage=FilterQueryLanguage,
            FilterQuery=FilterQuery,
            OperationTimeout=OperationTimeout,
            ContinueOnError=ContinueOnError,
            MaxObjectCount=MaxObjectCount)
        return list(result)

    def PyWbemcliReferenceInstancePaths(self, InstanceName, ResultClass=None,
                                        Role=None,
                                        FilterQueryLanguage=None,
                                        FilterQuery=None,
                                        OperationTimeout=None,
                                        ContinueOnError=None,
                                        MaxObjectCount=DEFAULT_MAXPULLCNT,
                                        **extra):
        # pylint: disable=unused-argument
        # pylint: disable=invalid-name
        """
        Execute IterReferemceInstancePaths and retrieve the instances. Returns
        the paths that result from iterating the IterReferenceInstancePaths.

        Uses the same parameters as the IterReferemceInstancePaths method.

        All exceptions from the underlying method are passed through this
        method.
        """

        result = self.IterReferenceInstancePaths(
            InstanceName,
            ResultClass=ResultClass,
            Role=Role,
            FilterQueryLanguage=FilterQueryLanguage,
            FilterQuery=FilterQuery,
            OperationTimeout=OperationTimeout,
            ContinueOnError=ContinueOnError,
            MaxObjectCount=MaxObjectCount)
        return list(result)

    def PyWbemcliReferenceInstances(self, InstanceName, ResultClass=None,
                                    Role=None, IncludeQualifiers=None,
                                    IncludeClassOrigin=None, PropertyList=None,
                                    FilterQueryLanguage=None, FilterQuery=None,
                                    OperationTimeout=None, ContinueOnError=None,
                                    MaxObjectCount=DEFAULT_MAXPULLCNT,
                                    **extra):
        # pylint: disable=unused-argument
        # pylint: disable=invalid-name
        """
        Execute IterReferencesInstances and retrieve the instances. Returns
        the returned instances.

        Uses the same parameters as the IterReferencesInstances method.

        All exceptions from the underlying method are passed through this
        method.
        """

        result = self.IterReferenceInstances(
            InstanceName,
            ResultClass=ResultClass,
            Role=Role,
            IncludeQualifiers=IncludeQualifiers,
            IncludeClassOrigin=IncludeClassOrigin,
            PropertyList=PropertyList,
            FilterQueryLanguage=FilterQueryLanguage,
            FilterQuery=FilterQuery,
            OperationTimeout=OperationTimeout,
            ContinueOnError=ContinueOnError,
            MaxObjectCount=MaxObjectCount)
        return list(result)

    def PyWbemcliAssociatorInstancePaths(self, InstanceName, AssocClass=None,
                                         ResultClass=None,
                                         Role=None, ResultRole=None,
                                         FilterQueryLanguage=None,
                                         FilterQuery=None,
                                         OperationTimeout=None,
                                         ContinueOnError=None,
                                         MaxObjectCount=DEFAULT_MAXPULLCNT,
                                         **extra):
        # pylint: disable=unused-argument
        # pylint: disable=invalid-name
        """
        Execute IterAssociatorInstancePaths and retrieve the paths. Returns
        the paths that result from iterating the IterAssociatorInstancePaths.

        Uses the same parameters as the IterAssociatorInstancePaths method.

        All exceptions from the underlying method are passed through this
        method.
        """

        result = self.IterAssociatorInstancePaths(
            InstanceName,
            AssocClass=AssocClass,
            ResultClass=ResultClass,
            Role=Role,
            ResultRole=ResultRole,
            FilterQueryLanguage=FilterQueryLanguage,
            FilterQuery=FilterQuery,
            OperationTimeout=OperationTimeout,
            ContinueOnError=ContinueOnError,
            MaxObjectCount=MaxObjectCount)
        return list(result)

    def PyWbemcliAssociatorInstances(self, InstanceName, AssocClass=None,
                                     ResultClass=None,
                                     Role=None, ResultRole=None,
                                     IncludeQualifiers=None,
                                     IncludeClassOrigin=None, PropertyList=None,
                                     FilterQueryLanguage=None, FilterQuery=None,
                                     OperationTimeout=None,
                                     ContinueOnError=None,
                                     MaxObjectCount=DEFAULT_MAXPULLCNT,
                                     **extra):
        # pylint: disable=unused-argument
        # pylint: disable=invalid-name
        """
        Execute IterAssociatorInstances and retrieve the instances. Returns
        the instances that result from iterating the IterAssociatorInstances.

        Uses the same parameters as the IterAssociatorInstances method.

        All exceptions from the underlying method are passed through this
        method.
        """

        result = self.IterAssociatorInstances(
            InstanceName,
            AssocClass=AssocClass,
            ResultClass=ResultClass,
            Role=Role,
            ResultRole=ResultRole,
            IncludeQualifiers=IncludeQualifiers,
            IncludeClassOrigin=IncludeClassOrigin,
            PropertyList=PropertyList,
            FilterQueryLanguage=FilterQueryLanguage,
            FilterQuery=FilterQuery,
            OperationTimeout=OperationTimeout,
            ContinueOnError=ContinueOnError,
            MaxObjectCount=MaxObjectCount)
        return list(result)

    def PyWbemcliQueryInstances(self, FilterQueryLanguage, FilterQuery,
                                namespace=None, ReturnQueryResultClass=None,
                                OperationTimeout=None, ContinueOnError=None,
                                MaxObjectCount=DEFAULT_MAXPULLCNT,
                                **extra):
        # pylint: disable=unused-argument
        # pylint: disable=invalid-name
        """
        Execute IterQueryInstances and retrieve the instances. Returns
        the instances that result from iterating the IterQueryInstances.

        Uses the same parameters as the IterQueryInstances method.

        All exceptions from the underlying method are passed through this
        method.
        """

        result = self.IterQueryInstances(
            FilterQueryLanguage,
            FilterQuery,
            namespace=namespace,
            ReturnQueryResultClass=ReturnQueryResultClass,
            OperationTimeout=OperationTimeout,
            ContinueOnError=ContinueOnError,
            MaxObjectCount=MaxObjectCount)
        return list(result)


class BuildMockenvMixin(object):
    # pylint: disable=too-few-public-methods
    """
    Mixin class for pywbem_mock.FakedWBEMConnection that adds the ability to
    build the mock environment of a connection from a connection definition in
    a connections file.
    """

    def build_mockenv(self, server, file_path_list, connections_file,
                      connection_name, verbose):
        """
        Builds the mock environment of the 'self' connection from the input
        files, or from the mock cache of the connection if it is up to date.
        If the mock environment was built from the input files, the mock
        environment of the connection is dumped to its cache.

        The input files for building the mock environment are:

        * MOF files with a suffix of '.mof'.

          These files are compiled into the default namespace of the connection.

        * Python files with a suffix of '.py'.

          These files are mock scripts that are imported and thereby executed.
          The mock scripts can be used for any kind of setup of the mock
          environment, for example for creating namespaces, for defining
          provider classes and registering providers, or for adding CIM objects
          either directly through add_cimobjects() or by compiling MOF files.

          Mock scripts support two approaches for passing the connection and
          server objects they should operate on:

          * via a setup() function defined in the mock script. This is the
            recommended approach, and it supports caching. The setup()
            function has the following parameters:

              conn (pywbem_mock.FakedWBEMConnection): The mock connection.

              server (pywbem.WBEMServer): The server object for the mock
                connection.

              verbose (bool): Verbose flag from the command line.

          * via global variables made available to the mock script. This
            approach prevents caching. The following global variables are
            made available:

              CONN (pywbem_mock.FakedWBEMConnection): The mock connection.

              SERVER (pywbem.WBEMServer): The server object for the mock
                connection.

              VERBOSE (bool): Verbose flag from the command line.

        Parameters:

          self (pywbem_mock.FakedWBEMConnection): The mock connection.

          server (pywbem.WBEMServer): The server object for the mock connection.

          file_path_list (list of string): The path names of the input files
            for building the mock environment, from the connection definition.

          connections_file (string): Path name of the connections file.

          connection_name (string): The name of the connection definition in
            the connections file.

          verbose (bool): Verbose flag from the command line.

        Raises:
          MockFileError: Mock file does not exist.
          MockMOFCompileError: Mock MOF file fails to compile.
          MockScriptError: Mock script fails to execute.
          SetupNotSupportedError (py<3.5): New-style setup in mock script not
            supported.
        """

        # Check that the input files exist. Since we loop through them multiple
        # times, we check that once.
        for file_path in file_path_list:
            if not os.path.exists(file_path):
                raise mockscripts.MockFileError(
                    "Mock file does not exist: {}".format(file_path))

        # The connections file is set if a named connection is used, i.e.
        # when specifying the -n general option. It is not set when the -s or -m
        # general options were specified. When no connections file is set, no
        # caching happens because there is no connection definition context
        # which is required for caching.
        if connections_file == DEFAULT_CONNECTIONS_FILE:

            cache_rootdir = mockcache_rootdir()
            if not os.path.isdir(cache_rootdir):
                os.mkdir(cache_rootdir)

            cache_dir = mockcache_cachedir(
                cache_rootdir, connections_file, connection_name)
            if not os.path.isdir(cache_dir):
                os.mkdir(cache_dir)

            # The mockenv pickle file contains the pickled state of the mock
            # environment.
            mockenv_pickle_file = os.path.join(cache_dir, 'mockenv.pkl')

            # The depreg pickle file contains the provider dependents
            # registry of the connection. It is used to look up the dependent
            # files of a mock script. The content of these dependent files is
            # also taken into account when determining whether the cache is up
            # to date. This needs to go into a separate pickle file because
            # it needs to be loaded and examined before the mckenv pickle
            # file is loaded.
            depreg_pickle_file = os.path.join(cache_dir, 'depreg.pkl')

            # The md5 file contains the MD5 hash value of the content of the
            # input files for the mock environment, and also taken into account
            # when determining whether the cache is up to date.
            md5_file = os.path.join(cache_dir, 'mockfiles.md5')

            # Flag indicating that the mock environment needs to be built
            # (or re-built). If False, the mock environment cache can be used.
            need_rebuild = False

            # Determine whether the mock environment needs to be rebuilt based
            # on the (non-)existence of the cache files.
            if not os.path.isfile(mockenv_pickle_file) \
                    or not os.path.isfile(depreg_pickle_file) \
                    or not os.path.isfile(md5_file):
                if verbose:
                    click.echo("Mock environment for connection definition "
                               "'{}' will be built because it was not cached.".
                               format(connection_name))
                need_rebuild = True

            try:
                depreg = self._load_depreg(depreg_pickle_file)
            except (IOError, OSError) as exc:
                if exc.errno == errno.ENOENT:
                    depreg = pywbem_mock.ProviderDependentRegistry()
                else:
                    raise

            # Calculate the MD5 hash value of the content of the input files
            md5 = hashlib.md5()
            for file_path in file_path_list:
                with io.open(file_path, 'rb') as fp:
                    file_source = fp.read()
                    md5.update(file_source)

                # For mock scripts, take their dependent files into account
                if file_path.endswith('.py'):
                    dep_files = depreg.iter_dependents(file_path)
                    for dep_file in dep_files:
                        with io.open(dep_file, 'rb') as fp:
                            file_source = fp.read()
                            md5.update(file_source)

            # Add the cache dir, so that manual tweaks on the cache files
            # invalidates the cache.
            md5.update(ensure_bytes(cache_dir))

            new_md5_value = ensure_unicode(md5.hexdigest())

            # Determine whether the mock environment needs to be rebuilt based
            # on the MD5 hash value of the input file content.
            if not need_rebuild:
                with io.open(md5_file, 'r', encoding='utf-8') as fp:
                    cached_md5_value = fp.read()
                if new_md5_value != cached_md5_value:
                    if verbose:
                        click.echo("Mock environment for connection "
                                   "definition '{}' is cached but will be "
                                   "rebuilt because the mock files have "
                                   "changed.".format(connection_name))
                    need_rebuild = True

            cache_it = True

        elif connections_file:
            # User-specified connections file used.

            if verbose:
                click.echo("Mock environment for connection definition '{}' "
                           "will be built because user-specified connections "
                           "files are not cached.".format(connection_name))
            need_rebuild = True
            cache_it = False

        else:
            # No connections file context.

            if verbose:
                click.echo("Mock environment for connection definition '{}' "
                           "will be built because no connections file is "
                           "known.".format(connection_name))
            need_rebuild = True
            cache_it = False

        if need_rebuild:
            try:
                self._build_mockenv(server, file_path_list, verbose)
            except mockscripts.NotCacheable as exc:
                if verbose:
                    click.echo("Mock environment for connection definition "
                               "'{}' will be built because it is not "
                               "cacheable: {}.".format(connection_name, exc))
            else:
                if connections_file and cache_it:
                    self._dump_mockenv(mockenv_pickle_file)
                    self._dump_depreg(
                        self.provider_dependent_registry, depreg_pickle_file)
                    with io.open(md5_file, 'w', encoding='utf-8') as fp:
                        fp.write(new_md5_value)
                    if verbose:
                        click.echo("Mock environment for connection "
                                   "definition '{}' has been written to "
                                   "cache.".format(connection_name))
        else:
            # When no rebuild is needed, there must have been a connections
            # file set.
            assert connections_file
            try:
                self._load_mockenv(mockenv_pickle_file, file_path_list)
                if verbose:
                    click.echo("Mock environment for connection definition "
                               "'{}' has been loaded from cache.".
                               format(connection_name))
            except mockscripts.NotCacheable as exc:
                if verbose:
                    click.echo("Mock environment for connection definition "
                               "'{}' will be rebuilt because it is not "
                               "cacheable: {}.".format(connection_name, exc))
                self._build_mockenv(server, file_path_list, verbose)

    def _build_mockenv(self, server, file_path_list, verbose):
        """
        Build the mock environment from the input files.

        Parameters:

          self (pywbem_mock.FakedWBEMConnection): The mock connection.

          server (pywbem.WBEMServer): The server object for the mock connection.

          file_path_list (list of string): The path names of the input files
            for building the mock environment, from the connection definition.

          verbose (bool): Verbose flag from the command line.

        Raises:
          NotCacheable (py<3.5): Mock environment is not cacheable.
          MockMOFCompileError: Mock MOF file fails to compile.
          MockScriptError: Mock script fails to execute.
          SetupNotSupportedError (py<3.5): New-style setup in mock script not
            supported.
        """
        for file_path in file_path_list:
            ext = os.path.splitext(file_path)[1]
            if ext == '.mof':
                try:
                    # Displays any MOFParseError already
                    self.compile_mof_file(file_path, verbose=verbose)
                except pywbem.Error as er:
                    # Abort the entire pywbemcli command because the
                    # MOF compilation might have caused inconsistencies in
                    # the mock repository.

                    if PYWBEM_VERSION.release >= (1, 0, 0):
                        # display just the exception.
                        msg = "MOF compile failed:\n{0}".format(er)
                    else:
                        # display file name.  Error text displayed already.
                        if isinstance(er, pywbem.MOFParseError):
                            msg = "MOF compile failed: File: '{0}'" \
                                "(see above)".format(file_path)
                        else:  # not parse error, display exception
                            msg = "MOF compile failed: File: {0} " \
                                "Error: {1}".format(file_path, er)
                    new_exc = mockscripts.MockMOFCompileError(msg)
                    new_exc.__cause__ = None
                    raise new_exc
            else:
                assert ext == '.py'  # already checked

                # May raise various mockscripts.MockError exceptions.
                # NotCacheable will be handled by the caller by building the
                # mock env.
                mockscripts.setup_script(file_path, self, server, verbose)

    def _dump_mockenv(self, mockenv_pickle_file):
        """
        Dump the mock environment of the connection to the mockenv pickle file.

        Parameters:

          self (pywbem_mock.FakedWBEMConnection): The mock connection.

          mockenv_pickle_file (pywbem.WBEMServer): Path name of the mockenv
            pickle file.
        """

        # Save the provider registry and the CIM repository

        # We construct a single object, because the CIM repository is
        # referenced from each provider, and pickle properly handles
        # multiple references to the same object.
        mockenv = dict(
            cimrepository=self.cimrepository,
            # pylint: disable=protected-access
            provider_registry=self._provider_registry,
        )
        with io.open(mockenv_pickle_file, 'wb') as fp:
            pickle.dump(mockenv, fp)

    def _load_mockenv(self, mockenv_pickle_file, file_path_list):
        """
        Load the mock environment from the mockenv pickle file.

        This method also imports the Python scripts from the input files in
        order to re-establish any class definitions that may be needed, for
        example provider classes.

        Parameters:

          self (pywbem_mock.FakedWBEMConnection): The mock connection.

          mockenv_pickle_file (pywbem.WBEMServer): Path name of the mockenv
            pickle file.

          file_path_list (list of string): The path names of the input files
            for building the mock environment, from the connection definition.

        Raises:
          NotCacheable (py<3.5): Mock environment is not cacheable.
        """

        # Restore the provider classes
        for file_path in file_path_list:
            ext = os.path.splitext(file_path)[1]
            if ext == '.py':
                # May raise mockscripts.NotCacheable which will be handled by
                # the caller by building the mock env.
                mockscripts.import_script(file_path)

        # Restore the provider registry and the CIM repository
        with io.open(mockenv_pickle_file, 'rb') as fp:
            mockenv = pickle.load(fp)

        # Others have references to the self._cimrepository object, so we are
        # not replacing that object, but are rather replacing the state of
        # that object.
        cimrepository = mockenv['cimrepository']
        assert isinstance(cimrepository, pywbem_mock.InMemoryRepository)
        # pylint: disable=protected-access
        self._cimrepository.load(cimrepository)

        provider_registry = mockenv['provider_registry']
        assert isinstance(provider_registry, pywbem_mock.ProviderRegistry)
        # pylint: disable=protected-access
        self._provider_registry.load(provider_registry)

    @staticmethod
    def _dump_depreg(depreg, depreg_pickle_file):
        """
        Dump a provider dependent registry to a pickle file.

        Parameters:

          depreg (pywbem_mock.ProviderDependentRegistry): Provider dependent
            registry to be dumped.

          depreg_pickle_file (string): Path name of the pickle file.
        """
        with io.open(depreg_pickle_file, 'wb') as fp:
            pickle.dump(depreg, fp)

    @staticmethod
    def _load_depreg(depreg_pickle_file):
        """
        Load a provider dependent registry from a pickle file and return it.

        Parameters:

          depreg_pickle_file (string): Path name of the pickle file to be
            loaded.

        Returns:
          pywbem_mock.ProviderDependentRegistry: Provider dependent registry.
        """
        with io.open(depreg_pickle_file, 'rb') as fp:
            depreg = pickle.load(fp)
        return depreg


class PYWBEMCLIConnection(pywbem.WBEMConnection, PYWBEMCLIConnectionMixin):
    """
    PyWBEMCLIConnection subclass adds the methods added by
    PYWBEMCLIConnectionMixin
    """

    def __init__(self, *args, **kwargs):
        """
        ctor passes all input parameters to superclass
        """
        super(PYWBEMCLIConnection, self).__init__(*args, **kwargs)


class PYWBEMCLIFakedConnection(BuildMockenvMixin,
                               PYWBEMCLIConnectionMixin,
                               pywbem_mock.FakedWBEMConnection):
    """
    PyWBEMCLIFakedConnection subclass adds the methods added by
    PYWBEMCLIConnectionMixin
    """
    def __init__(self, *args, **kwargs):
        """
        ctor passes all input parameters to superclass
        """
        super(PYWBEMCLIFakedConnection, self).__init__(*args, **kwargs)


def mockcache_rootdir():
    """
    Return the directory path of the mock cache root directory.
    """
    dir_path = os.path.join(os.path.expanduser('~'), '.pywbemcli_mockcache')
    return dir_path


def mockcache_cachedir(rootdir, connections_file, connection_name):
    """
    Return the directory path of the mock cache directory for a connection.
    """
    # Construct a (reproducible) cache ID from connections file path and
    # connection definition name.
    # Example: 6048a3da1a34a3ec605825a1493c7bb5.simple
    try:
        connections_file = os.path.relpath(
            connections_file, os.path.expanduser('~'))
    except ValueError:
        # On Windows, os.path.relpath() raises ValueError when the paths
        # are on different drives
        pass
    md5 = hashlib.md5()
    md5.update(connections_file.encode("utf-8"))
    cache_id = "{}.{}".format(md5.hexdigest(), connection_name)
    dir_path = os.path.join(rootdir, cache_id)
    return dir_path


def delete_mock_cache(connections_file, connection_name):
    """
    Delete the mock cache of the connection, if it exists.

    Parameters:

      self (pywbem_mock.FakedWBEMConnection): The mock connection.

      connections_file (string): Path name of the connections file.

      connection_name (string): The name of the connection definition in
        the connections file.

    Raises:
      OSError: Mock cache cannot be deleted.
    """
    cache_dir = mockcache_cachedir(
        mockcache_rootdir(), connections_file, connection_name)
    if os.path.isdir(cache_dir):
        file_list = glob.glob(os.path.join(cache_dir, '*'))
        for _file in file_list:
            os.remove(_file)
        os.rmdir(cache_dir)
