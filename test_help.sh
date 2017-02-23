#!/bin/bash
#
#  This script exercises the pywbemcli help functions.
#  It should have an entry for each subcommand to work completely
#  It does not validate the options or text, just that the commands do
#  not fail
#
HOST=http://localhost
ERRORS=0
function cmd {
    echo ==========================================================
    CMD="pywbemcli -s $HOST $1 --help"
    echo  pywbemcli command:  $CMD
    echo ===== Cmd help output 
    $CMD
    if [ $? != 0 ]; then
        echo ERROR: $CMD
        ((ERRORS=ERRORS+1))
    fi
}

#
# Each of the following is a subcmd sequence.  Since there is no
# concept of listing all help in click today we use this to get each command
#
cmd ""
cmd "class"
cmd "class get"
cmd "class invokemethod"
cmd "class names"
cmd "class enumerate"
cmd "class associators"
cmd "class references"
cmd "class find"
cmd "class hierarchy"

cmd "instance get"
cmd "instance delete"
cmd "instance create"
cmd "instance invokemethod"
cmd "instance query"
cmd "instance names"
cmd "instance enumerate"
cmd "instance count"
cmd "instance references"
cmd "instance associators"

cmd "qualifier"
cmd "qualifier enumerate"
cmd "qualifier get"

cmd "server"
cmd "server brand"
cmd "server connection"
cmd "server info"
cmd "server namespaces"
cmd "server interop"
cmd "server profiles"

if (( $ERRORS != 0 )); then
    echo ERROR: $ERRORS Cmds failed
    exit 1
fi
exit 0

