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
Click Command definition for the qualifer command group  which includes
cmds for get and enumerate for CIM qualifier types.
"""

from __future__ import absolute_import

import six

from asciitree import LeftAligned
import click
from pywbem.cim_obj import NocaseDict


def build_tree(class_subclass_dict, top_class):
    """
    Build a dictionary structure based on the class/subclass relationships
    in the class_subclass tree dictionary provided.

    Returns the dictionary structure in a form suitable for ascii tree
    display
    """
    def _tree_node(class_subclass_dict, cn):
        """
        Build dictionary of the class/subclass relationships for class cn
        in dictionary of class_subclass names.

        Returns dictionary of dictionaries in form suitable for asciitree
        """
        node_dict = NocaseDict()
        # If there is no subclass, the class will not exist in this dictionary
        if cn in class_subclass_dict:
            cn_list = class_subclass_dict[cn]
            # This should not be necessary if end nodes are not in the dict.
            if cn_list:
                for key in cn_list:
                    node_dict[key] = _tree_node(class_subclass_dict, key)
            else:
                node_dict = NocaseDict()
        else:
            return {}

        return node_dict

    rtn_dict = {}
    # _tree_node generates dictionary node for elements in class-subclass
    # dictionary and returns complete node structure
    rtn_dict[top_class] = _tree_node(class_subclass_dict, top_class)
    return rtn_dict


def display_class_tree(classes, top_class=None):
    """
    Display the list of classes as a left justified tree  in ascii to the
    click.echo output

    Parameters:
        classes (list of :class:`~pywbem.CIMClass`)

        top_class (:term: `string`)
            The top level class to display or None if the display is
            from root.
    """

    # build dictionary of classname : superclassname
    cn_supercn = {cl.classname: cl.superclass for cl in classes}

    # if top_class is none, create artifical root
    if top_class is None:
        for cn in cn_supercn:
            if not cn_supercn[cn]:
                cn_supercn[cn] = 'root'
        top_class = 'root'

    # Hack to build the class to subclass dictionary from the
    # superclass to class dictionary
    cn_subcn = NocaseDict()
    # pylint: disable=bad-continuation, expression-not-assigned
    [cn_subcn.setdefault(v, []).append(k) for (k, v) in
            six.iteritems(cn_supercn)]  # noqa: F841
    tree = build_tree(cn_subcn, top_class)

    tr = LeftAligned()
    click.echo(tr(tree))
