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
everywhere a WBEMConnection possible pull operation is called.

It also adds a method to FakeWBEMConnection to build the repository.
"""

from __future__ import absolute_import, print_function

import os
import sys
import traceback
import click
import packaging.version
import pywbem
import pywbem_mock

from .config import DEFAULT_MAXPULLCNT

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


class BuildRepositoryMixin(object):
    # pylint: disable=too-few-public-methods
    """
    Builds the mock repository from the definitions in self._mock_server.

    Each item in the iterable in self._mock_server must be a file path
    identifying a file to be used to prepare for the mock test.

    Each file path may be:

      a python file if the suffix is 'mof'. A mof file is compiled into the
      repository with the method

    Returns a variety of errors for file not found, MOF syntax errors, and
    python syntax errors.
    """

    @staticmethod
    def build_repository(conn, server, file_path_list, verbose):
        """
        Build the repository from the file_path list
        """
        for file_path in file_path_list:
            if not os.path.exists(file_path):
                raise IOError('No such file: {}'.format(file_path))

            ext = os.path.splitext(file_path)[1]
            if ext == '.mof':
                try:
                    # Displays any MOFParseError already
                    conn.compile_mof_file(file_path)
                except pywbem.Error as er:
                    # Abort the entire pywbemcli command because the
                    # MOF compilation might have caused inconsistencies in the
                    # mock repository.

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
                    click.echo(msg, err=True)
                    raise click.Abort()
            else:
                assert ext == '.py'  # already checked
                with open(file_path) as fp:
                    # May raise IOError
                    file_source = fp.read()
                    # the exec includes CONN and VERBOSE
                    globalparams = {'CONN': conn,
                                    'SERVER': server,
                                    'VERBOSE': verbose}
                    try:
                        # Using compile+exec instead of just exec allows
                        # specifying the file name, causing it to appear in
                        # any tracebacks.
                        file_code = compile(file_source, file_path, 'exec')
                        # pylint: disable=exec-used
                        exec(file_code, globalparams, None)
                    except Exception:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        tb = traceback.format_exception(exc_type, exc_value,
                                                        exc_traceback)
                        # Abort the entire pywbemcli command because the
                        # script might have caused inconsistencies in the
                        # Python namespace and in the mock repository.
                        click.echo(
                            "Mock Python script '{}' failed:\n{}".
                            format(file_path, "\n".join(tb)),
                            err=True)
                        raise click.Abort()


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


class PYWBEMCLIFakedConnection(pywbem_mock.FakedWBEMConnection,
                               PYWBEMCLIConnectionMixin,
                               BuildRepositoryMixin):
    """
    PyWBEMCLIFakedConnection subclass adds the methods added by
    PYWBEMCLIConnectionMixin
    """
    def __init__(self, *args, **kwargs):
        """
        ctor passes all input parameters to superclass
        """
        super(PYWBEMCLIFakedConnection, self).__init__(*args, **kwargs)
