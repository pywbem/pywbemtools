#!/bin/bash

HOST=http://localhost
ERRORS=0

# Single input argument, the input arguments for the command
function cmd {
    echo '==========================================================='
    CMD="pywbemcli -s $HOST $1"
    echo $CMD
    $CMD
    if [ $? != 0 ]; then
        echo ERROR: $CMD
        ((ERRORS+=1))
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

# invoke method

cmd "instance enumerate PyWBEM_Person"
cmd "instance enumerate PyWBEM_Person -p name"
cmd "instance enumerate PyWBEM_Person -o"

# TODO find way to do interactive in batch
# cmd "instance get PyWBEM_Person -i"
cmd "instance get PyWBEM_Person.name=bob"

cmd "instance create  -x Name=Fred -x GivenName=Jones -x CreationClassName=PyWBEM_Person PyWBEM_Person"
cmd "instance delete PyWBEM_Person.name=Fred"

## invoke method

## query

cmd "instance count"

cmd "server brand"
cmd "server info"
cmd "server interop"
cmd "server namespaces"
cmd "server profiles"
cmd "server profiles -o DMTF"
# -n broken
cmd "server profiles -n CPU"

if (( $ERRORS != 0 )); then
    echo ERROR: $ERRORS cmds failed
    exit 1
fi
exit 0

