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
Functions to build a tree dictionary and also a displayable tree in ascii
from a list of CIM classes.
"""

from __future__ import absolute_import, print_function

import six
from asciitree import LeftAligned
import click

# Use an ordered Nocase dictionary for the tree. Ordered dictionary creates
# tree output that has the same order in multiple versions of python.
from pydicti import odicti


def build_tree(class_subclass_dict, top_class):
    """
    Build a dictionary structure based on the class/subclass relationships
    in the class_subclass tree dictionary provided.

    Returns the dictionary structure in a form suitable for ascii tree
    display
    """
    def _tree_node(class_to_subclass_dict, cln):
        """
        Build dictionary of the class/subclass relationships for class cn
        in dictionary of class_subclass names. This maps the input dictionary
        that is a flat class_name: [subclass_name] dictionary to a tree
        of dictionaries for the hiearchy of classes.

        Returns dictionary of dictionaries in form suitable for asciitree

        Parameters:
          class_to_subclass_dict:
            Dictionary with all classes to be in as keys and the corresponding
            subclasses for each class as a list of classnames

          cln (:term:`string`):
            Class for which a tree node will be generated.  An empty node
            is generated if class not in class_to_subclass_dict.

        Returns:
          Structure of nested dictionaries defining the class/subclass structure
        """
        node_dict = odicti()
        # If there is no subclass, the class will not exist in this dictionary
        if cln in class_to_subclass_dict:
            cln_list = class_to_subclass_dict[cln]
            # This should not be necessary if end nodes are not in the dict.
            if cln_list:
                for key in cln_list:
                    node_dict[key] = _tree_node(class_to_subclass_dict, key)
        return node_dict

    rtn_dict = odicti()
    # _tree_node generates dictionary node for elements in class-subclass
    # dictionary and returns complete node structure. This is recursive,
    # with _tree_node recursively calling until there are no subclasses.
    rtn_dict[top_class] = _tree_node(class_subclass_dict, top_class)
    return rtn_dict


def build_class_tree_dict(classes, top_class=None):
    """
    Build a hierarchical dictionary of classes (each dictionary entry
    defines  a single classname: list of subclasses
    Parameters:

        classes (list of :class:`~pywbem.CIMClass`)
            List of classes to be included in the tree including at least
            the classname and superclass name.  All other parameters are
            ignored

        top_class (:term: `string`)
            The top level class to display or None if the display is
            from root. In that case, the tree builder attaches a top node
            named "root"
    """

    # Build dictionary of classname : superclassname from list of CIM classes
    cln_to_supercln = {cln.classname: cln.superclass for cln in classes}

    # Sort so there is a fixed order to the resulting tree.
    cln_supercln_sorted = odicti()
    for key in sorted(cln_to_supercln.keys()):
        cln_supercln_sorted[key] = cln_to_supercln[key]
    cln_to_supercln = cln_supercln_sorted

    # If top_class is none, create artifical root
    if top_class is None:
        for cln in cln_to_supercln:
            if not cln_to_supercln[cln]:
                cln_to_supercln[cln] = 'root'
        top_class = 'root'

    # Build the class to subclass dictionary from the
    # superclass to class dictionary by reversing the dictionary.
    # Built within a comprehension but comprehension not assigned.
    subcln_in_cln = odicti()
    # pylint: disable=bad-continuation, expression-not-assigned
    [subcln_in_cln.setdefault(v, []).append(k) for (k, v) in
        six.iteritems(cln_to_supercln)]  # noqa: F841

    return build_tree(subcln_in_cln, top_class)


def display_class_tree(classes, top_class=None):
    """
    Build and display in ASCII output a tree of classes.

    Parameters:
        classes (list of :class:`~pywbem.CIMClass`)

        top_class (:term: `string`)
            The top level class to display or None if the display is
            from root.

    """
    tree = build_class_tree_dict(classes, top_class=top_class)
    tr = LeftAligned()
    click.echo(tr(tree))
