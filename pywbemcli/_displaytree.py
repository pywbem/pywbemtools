# Copyright TODO
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
Click Command definition for the qualifer command group which includes
cmds for get and enumerate for CIM qualifier types.
"""

from __future__ import absolute_import

from asciitree import LeftAligned
from collections import OrderedDict as OD


def display_class_tree(classes):
    """ Display the list of classes as a left justified tree"""

    # Create list of top level classes

    top_classes = [cl.classname for cl in classes if cl.superclass is None]

    cl_tree = {cl.classname: cl.superclassname for cl in classes}
    print(top_classes)
    print(cl_tree)
    # TODO finish this. The following is example of dictionary we must build

    tree = {
        'root': OD([
            ('sometimes',
                {'you': {}}),
            ('just',
                {'want': OD([
                    ('to', {}),
                    ('draw', {}),
                ])}),
            ('trees', {}),
            ('in', {
                'your': {
                    'terminal': {}
                }
            })
        ])
    }

    tr = LeftAligned
    print(tr(tree))
