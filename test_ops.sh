#!/bin/bash

HOST=http://localhost
function cmd {
    echo pywbemcli $HOST $1
    pywbemcli -s $HOST $1
    if [ $? != 0 ]; then
        echo ERROR pywbemcli $HOST $1
    fi
}


cmd "class get CIM_ManagedElement"
cmd "class enumerate"
cmd "class enumerate CIM_System"
cmd "class enumerate CIM_System -d"
cmd "class enumerate CIM_System -l"
cmd "class find CIM_System"
cmd "class find PyWBEM"

cmd "class tree CIM_System"
cmd "class tree CIM_System -s"
cmd "class tree CIM_ManagedElement -s"



cmd "instance enumerate PyWBEM_Person"
cmd "instance enumerate PyWBEM_Person -p name"
cmd "instance enumerate PyWBEM_Person -o"

cmd "instance get PyWBEM_Person -i"
cmd "instance get PyWBEM_Person.name=bob"

cmd "instance count"

cmd "server brand"
cmd "server info"
cmd "server interop"
cmd "server namespaces"
cmd "server profiles"
cmd "server profiles -o DMTF"
# -n broken
cmd "server profiles -n \"CPU Profile\""

