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
Subclass of pywbem cim_operations.py to capture the specialized functions
for pywbemcli.

This contains only those classes that use the inter functions and actually
do the complete operation to emulate the original enumerate operations
"""
from __future__ import absolute_import

from pywbem import WBEMConnection, DEFAULT_NAMESPACE

from .config import DEFAULT_MAXPULLCNT

__all__ = ['PYWBEMCLIConnection']


class PYWBEMCLIConnection(WBEMConnection):
    """
    Subclass WBEM_Connection to build the specialized operations needed
    by pywbemcli,

    """

    def __init__(self, url, creds=None, default_namespace=DEFAULT_NAMESPACE,
                 x509=None, verify_callback=None, ca_certs=None,
                 no_verification=False, timeout=None, use_pull_operations=None,
                 stats_enabled=False):

        super(PYWBEMCLIConnection, self).__init__(
            url, creds=creds,
            default_namespace=default_namespace,
            x509=x509,
            verify_callback=verify_callback,
            ca_certs=ca_certs,
            no_verification=no_verification,
            timeout=timeout,
            use_pull_operations=use_pull_operations,
            stats_enabled=stats_enabled)

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

    def IterQueryInstances(self, FilterQueryLanguage, FilterQuery,
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
