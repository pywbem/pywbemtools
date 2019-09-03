#!/bin/bash

#
# This is a simple shell script to execute a number of pywbemcli commands
# It executed the command and tests for error on the response.  Any errors
# are set into an array and displayed when the execution is complete
# Today this executes agains the WBEMServer defined by the HOST variable

# We will replace this by a corresponding python tool to avoid issues with
# particular operating systems and shells.
#

HOST=http://localhost
ERRORS=0
FAILED_CMDS=()

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
        FAILED_CMDS+=("$CMD")
    fi
}

#
#  The following is the input arguments for a single pywbemcli command
#
cmd "class get CIM_ManagedElement"
cmd "class get CIM_ManagedElement -l"
cmd "class get CIM_ManagedElement --local-only"
cmd "class get CIM_ManagedElement --no-qualifiers"
cmd "class get CIM_ManagedElement -c"
cmd "class get CIM_ManagedElement --include-classorigin"
cmd "class get CIM_ManagedElement --include-classorigin"
cmd "class get CIM_ManagedElement --namespace root/PG_Interop"
cmd "class get CIM_ManagedElement -p InstanceID -p Caption"
cmd "class get CIM_ManagedElement -p InstanceID"
cmd "class get CIM_ManagedElement -p ''"

cmd "class enumerate"
cmd "class enumerate CIM_System"
cmd "class enumerate CIM_System -d"
cmd "class enumerate CIM_System -l"
cmd "class enumerate CIM_System -s"
cmd "class enumerate CIM_System --local-only"
cmd "class enumerate CIM_System --names-only"
cmd "class enumerate CIM_System -o"
cmd "class enumerate CIM_System -o -s"

#
cmd "class associators CIM_System"
cmd "class associators CIM_System -s"
cmd "class associators CIM_System -o"
cmd "class associators CIM_System -o -s"

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
cmd "instance get PyWBEM_Person.CreationClassName=PyWBEM_Person,name=Bob"
cmd "instance create PyWBEM_Person --property Name=Fred --property GivenName=Jones --property CreationClassName=PyWBEM_Person"
cmd "instance delete PyWBEM_Person.CreationClassName=PyWBEM_Person,Name=Fred"

cmd "instance create pywbem_alltypes --property instanceId=array1 --property scalBool=True --property arrayBool=True,False"
cmd "instance get pywbem_alltypes.InstanceId=array1"
cmd "instance get pywbem_alltypes.InstanceId=array1 -p InstanceId"
cmd "instance get pywbem_alltypes.InstanceId=array1 -p InstanceID -p scalBool"
cmd "instance get pywbem_alltypes.InstanceId=array1 -p InstanceID,scalBool"
cmd "instance delete pywbem_alltypes.InstanceId=array1"

## invoke method

## query

# Instance count function. Displays count of instances in a namespace
cmd "instance count"
cmd "instance count -s"
cmd "instance count --sort"
cmd "instance count py"

# server general commands
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
    for i in "${FAILED_CMDS[@]}"
    do
        echo "$i"
    done
    exit 1
fi
exit 0
