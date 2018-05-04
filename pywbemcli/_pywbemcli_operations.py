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
from __future__ import absolute_import
import os

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from pywbem import WBEMConnection
import pywbem_mock

from .config import DEFAULT_MAXPULLCNT

#  __all__ = ['PYWBEMCLIConnection', 'PYWBEMCLIFakedConnection']


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

        result = [path for path in self.IterEnumerateInstancePaths(
            ClassName,
            namespace=namespace,
            FilterQueryLanguage=FilterQueryLanguage,
            FilterQuery=FilterQuery,
            OperationTimeout=OperationTimeout,
            ContinueOnError=ContinueOnError,
            MaxObjectCount=MaxObjectCount)]
        return result

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

        result = [inst for inst in self.IterEnumerateInstances(
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
            MaxObjectCount=MaxObjectCount)]
        return result

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

        result = [path for path in self.IterReferenceInstancePaths(
            InstanceName,
            ResultClass=ResultClass,
            Role=Role,
            FilterQueryLanguage=FilterQueryLanguage,
            FilterQuery=FilterQuery,
            OperationTimeout=OperationTimeout,
            ContinueOnError=ContinueOnError,
            MaxObjectCount=MaxObjectCount)]
        return result

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

        result = [inst for inst in self.IterReferenceInstances(
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
            MaxObjectCount=MaxObjectCount)]
        return result

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

        result = [path for path in self.IterAssociatorInstancePaths(
            InstanceName,
            AssocClass=AssocClass,
            ResultClass=ResultClass,
            Role=Role,
            ResultRole=ResultRole,
            FilterQueryLanguage=FilterQueryLanguage,
            FilterQuery=FilterQuery,
            OperationTimeout=OperationTimeout,
            ContinueOnError=ContinueOnError,
            MaxObjectCount=MaxObjectCount)]
        return result

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

        result = [inst for inst in self.IterAssociatorInstances(
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
            MaxObjectCount=MaxObjectCount)]
        return result

    def PyWbemcliQueryInstances(self, FilterQueryLanguage, FilterQuery,
                                namespace=None, ReturnQueryResultClass=None,
                                OperationTimeout=None, ContinueOnError=None,
                                MaxObjectCount=DEFAULT_MAXPULLCNT,
                                **extra):
        # pylint: disable=invalid-name
        """
        Execute IterQueryInstances and retrieve the instances. Returns
        the instances that result from iterating the IterQueryInstances.

        Uses the same parameters as the IterQueryInstances method.

        All exceptions from the underlying method are passed through this
        method.
        """

        result = [inst for inst in self.IterQueryInstances(
            FilterQueryLanguage,
            FilterQuery,
            namespace=namespace,
            ReturnQueryResultClass=ReturnQueryResultClass,
            OperationTimeout=OperationTimeout,
            ContinueOnError=ContinueOnError,
            MaxObjectCount=MaxObjectCount)]
        return result


class BuildRepositoryMixin(object):  # pylint: disable=too-few-public-methods
    """
    Builds the mock repository from the pywbemcli url input.

    The input url defines:

    An action as the netloc(the text  between :// and the next //) which could
    be:

    1. A file reference if netloc == 'file'

    2. A callback to a method if netloc == 'callback' and the callback is in
       the same process.

    TODO expand this if necessary

    If the netloc == 'file'" the path component of the url is interpreted as
    a path name where:

    1. If it has the extension .mof is compiled into the repository using the
       :meth:`~pywbem_mock.FakedWBEMConnection.compile_mof_file` method.

    2. if it has the extension .py. NOTE: There are two possibilities with this
       type, a) execute it b) limit the .py extension to just objects that
       will be compiled using the
       :meth:`~pywbem_mock.FakedWBEMConnection.add_cimobjects`

    Known issues with what we have:

    1. The direct execution of a method a security hole.

    2. In order to compile dmtf schema and also add objects or other files
       at least two files are needed. Today we are providing for only one
       file
    """
    def build_repository(self, conn, fake_url, verbose):
        """
        Build the repository from the input url.
        """
        # assume path is a directory and file name

        url_components = urlparse(fake_url)

        if url_components.netloc == 'file':
            file_path = url_components.path
            ext = os.path.splitext(file_path)[1]
            if not os.path.exists(file_path):
                raise ValueError('File name %s does not exit' % file_path)
            if ext == '.mof':
                conn.compile_mof_file(file_path)
            elif ext == '.py':
                with open(file_path) as myfile:
                    objs = myfile.readlines()
                conn.add_cimobjects(objs)
            else:
                ValueError('Invalid extension %s on file %s' % (ext, file_path))
        elif url_components.netloc == 'callback':
            methodname = url_components.path
            # TODO do we do anything with result or expect any result back
            # from the method?
            result = bound_method(self, methodname)
        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = repr(traceback.format_exception(exc_type, exc_value,
                                                 exc_traceback))

        else:
            raise ValueError('Fake URL netloc must be "file" or "callback". '
                             ' "%s" found' %
                             url_components.netloc)

        if verbose:
            self.display_repository()


class PYWBEMCLIConnection(WBEMConnection, PYWBEMCLIConnectionMixin):
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
