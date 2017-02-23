#!/bin/bash

HOST=http://localhost
ERRORS=0

# Single input argument, the input arguments for the command
function cmd {
    echo '==========================================================='
    CMD="pywbemcli -s $HOST $1"
    echo pywbemcli Command: $CMD
    echo ===== Command Result
    $CMD
    if [ $? != 0 ]; then
        echo ERROR: $CMD
        ((ERRORS+=1))
    fi
}

#
#  The following is the input arguments for a single pywbemcli command
#
cmd "class get CIM_ManagedElement"
cmd "class get CIM_ManagedElement -l"
cmd "class get CIM_ManagedElement --localonly"
cmd "class get CIM_ManagedElement --no_includequalifiers"
cmd "class get CIM_ManagedElement -c"
cmd "class get CIM_ManagedElement --includeclassorigin"
cmd "class get CIM_ManagedElement --includeclassorigin"
cmd "class get CIM_ManagedElement --namespace root/PG_Interop"
cmd "class get CIM_ManagedElement -p InstanceID -p Caption"
cmd "class get CIM_ManagedElement -p InstanceID"
cmd "class get CIM_ManagedElement -p \"\""

cmd "class enumerate"
cmd "class enumerate CIM_System"
cmd "class enumerate CIM_System -d"
cmd "class enumerate CIM_System -l"
cmd "class enumerate CIM_System -s"
cmd "class enumerate CIM_System --localonly"
cmd "class enumerate CIM_System --names_only"
cmd "class enumerate CIM_System -o"
cmd "class enumerate CIM_System -o -s"

#
cmd "class assocators CIM_System"
cmd "class assocators CIM_System s" 
cmd "class assocators CIM_System -o"
cmd "class assocators CIM_System -o -s"

cmd "class references CIM_System -o"
cmd "class references CIM_System -o -s"
cmd "class references CIM_System"
cmd "class references CIM_System -s"

cmd "class find CIM_System"
cmd "class find PyWBEM"

# NOTE -s means something different here
cmd "class hierarchy CIM_System"
cmd "class hierarchy CIM_System -s"
cmd "class hierarchy CIM_ManagedElement -s"
cmd "class hierarchy CIM_ManagedElement --superclasses"
cmd "class hierarchy CIM_System --superclasses --namespace root/PG_Interop"
cmd "class hierarchy CIM_System --namespace root/PG_Interop"

# invoke method on a class

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

