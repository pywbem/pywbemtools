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
from a list of CIM classes.  This code implements the ability to add the
information on the Association, Indication, Abstract, and Version qualifiers to
each classname (see show_detail parameter).
"""

from __future__ import absolute_import, print_function

import six
from asciitree import LeftAligned
import click

# Use an ordered Nocase dictionary for the tree. Ordered dictionary creates
# tree output that has the same order in multiple versions of python.
from pywbem._nocasedict import NocaseDict


def display_class_tree(classes, top_classname=None, show_detail=None):
    """
    Build and display in ASCII output a tree of classes. If show_detail
    is set, add class qualifier to each classname as part of
    the display

    Parameters:
        classes (list of :class:`~pywbem.CIMClass`)

        top_classname (:term: `string`)
            The top level class to display or None if the display is
            from root of the class hierarchy

        show_detal (:class": `boolean)
            Flag to indicate that more detail about each class be displayed

    """
    def build_details(klass):
        """
        Build a string of any of the qualifiers defined below.

        Returns:
          string defining the qualifiers defined.
        """
        def append_if(append_values):
            """Append the values if the append_values string exists """
            if append_values:
                rtn_values.append(append_values)

        def bool_qualifier_is(qname, qvalue):
            """
            If boolean qualifier qname exists and value matches qvalue
            return the name of the qualifier if the qualifier exists and
            matches qvalue or None if it does not exist or the value does
            not match qvalue
            """
            if qname in klass.qualifiers and \
                    klass.qualifiers[qname].value == qvalue:
                return qname

            return None

        def string_qualifier_value(qname):
            """
            Get the Version qualifier if it exists and return the value.
            If there is no Version qualifier return "".
            Returns the value or None.
            """
            q = klass.qualifiers.get(qname, None)
            if q is None:
                return None
            v = q.value
            return "{}={}".format(qname, v) if v else None

        # Build the rtn_values string from the following qualifiers and their
        # values
        rtn_values = []
        append_if(bool_qualifier_is('Association', True))
        append_if(bool_qualifier_is('Abstract', True))
        append_if(bool_qualifier_is('Indication', True))
        append_if(string_qualifier_value('Version'))
        return ', '.join(rtn_values)

    def extend_name(cln, classes_dict):
        """
        Fix the classname defined by cln by suffixing with the extended
        components for display of type and version.
        """
        if cln in classes_dict and show_detail:
            klass = classes_dict[cln]
            details = build_details(klass)
            new_cln = "{0} ({1})".format(cln, details)
            return new_cln

        return cln

    def fix_names(classname, classes_dict, flat_cln_subclns):
        """
        Modify the names in the key and list of values to the classname
        entity  that will be presented

        Parameters:

          classname (:term:`string`): Name of class to be processed

          classes_dict (dict): CIMClass objects by class name
        """
        new_key = extend_name(classname, classes_dict)
        new_values = []
        for cln in flat_cln_subclns[classname]:
            new_values.append(extend_name(cln, classes_dict))
        return new_key, new_values

    # Start of display_class_tree method

    cln_to_supercln = build_cln_to_supercln_dict(classes)

    # If top_class is none, create artifical root as superclassname from
    # entries with value None.
    top_classname_default = 'root'
    if top_classname is None:
        for cln in cln_to_supercln:
            if not cln_to_supercln[cln]:
                cln_to_supercln[cln] = top_classname_default

    flat_cln_subclns = build_subcln_in_cln(cln_to_supercln)

    # If the names are to be expanded with additional information, rebuild
    # flat_cln_subclns_dict and change all the names.

    fixed_dict = NocaseDict()
    if show_detail:
        classes_dict = {cls.classname: cls for cls in classes}
        for cln in flat_cln_subclns:
            new_name, new_values = fix_names(cln, classes_dict,
                                             flat_cln_subclns)
            fixed_dict[new_name] = new_values
        flat_cln_subclns = fixed_dict

    tcv = top_classname if top_classname else top_classname_default
    # build nested tree from the flat list of subclasses_lists in classes
    nested_class_tree = build_nested_tree(flat_cln_subclns, tcv)

    tr = LeftAligned()
    click.echo(tr(nested_class_tree))


def build_cln_to_supercln_dict(classes):
    """
    Build a dictionary of classname: superclassname and sort it by
    to order the keys from a list of CIM classes.

      Parameters:

        classes (list of :class:`~pywbem.CIMClass`)
            List of classes to be included in the tree including at least
            the classname and superclass name.  All other parameters are
            ignored

      Returns:
        NocaseDict of classes where the keys are all the classes and
        the values are either the superclass name for the class or None if
        there is no superclass
    """

    # Build dictionary of classname : superclassname from list of CIM classes
    cln_to_supercln = {cln.classname: cln.superclass for cln in classes}

    # Sort so there is a fixed order to the resulting tree and create a dict
    # classname : superclassname
    cln_supercln_sorted = NocaseDict()
    for key in sorted(cln_to_supercln.keys()):
        cln_supercln_sorted[key] = cln_to_supercln[key]

    return cln_supercln_sorted


def build_subcln_in_cln(cln_to_supercln):
    """
    Build a dictionary of the direct subclasses for each subclass in
    the cln_to_supercln dictionary
    """

    # Build the class to subclass dictionary from the
    # superclass to class dictionary by reversing the dictionary.
    # Built within a comprehension but comprehension not assigned.
    subcln_in_cln = NocaseDict()
    # pylint: disable=bad-continuation, expression-not-assigned
    [subcln_in_cln.setdefault(v, []).append(k) for (k, v) in
        six.iteritems(cln_to_supercln)]  # noqa: F841

    return subcln_in_cln


def build_nested_tree(class_subclass_dict, top_class_name):
    """
    Build a dictionary structure based on the class/subclass relationships
    in the classname to subclassname tree dictionary provided.

    Returns the dictionary structure in a form suitable for ascii tree
    display

    Parameters:
      class_subclass_dict ():
    """
    def _tree_node(cln_to_subcln_dict, cln):
        """
        Build dictionary of the class/subclass relationships for class cln
        in dictionary of class_subclass names. This maps the input dictionary,
        a flat class_name: [subclass_name] dictionary, to a tree
        of dictionaries of the class names for the hierarchy of classes.

        Returns dictionary of dictionaries in form suitable for asciitree

        Parameters:
          cln_to_subcln_dict:
            Dictionary with all class names as keys and the
            corresponding subclass names for each class name as a list of
            class names

          cln (:term:`string`):
            Class for which a tree node will be generated.  An empty node
            is generated if class not in class_to_subclass_dict.

        Returns:
          Structure of nested dictionaries defining the class/subclass structure
        """
        node_dict = NocaseDict()
        # If there is no subclass, the class will not exist in this dictionary
        if cln in cln_to_subcln_dict:
            cln_list = cln_to_subcln_dict[cln]
            # This should not be necessary if end nodes are not in the dict.
            if cln_list:
                for key in cln_list:
                    node_dict[key] = _tree_node(cln_to_subcln_dict, key)
        return node_dict

    nested_tree_dict = NocaseDict()
    # _tree_node generates dictionary node for elements in class-subclass
    # dictionary and returns complete node structure. This is recursive,
    # with _tree_node recursively calling until there are no subclasses.
    nested_tree_dict[top_class_name] = _tree_node(class_subclass_dict,
                                                  top_class_name)
    return nested_tree_dict
