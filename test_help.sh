#!/bin/bash

HOST=http://localhost
function cmd {
    echo pywbemcli $HOST $1
    pywbemcli -s $HOST $1 --help
    if [ $? != 0 ]; then
        echo ERROR pywbemcli $HOST $1
    fi
}

cmd ""
cmd "class"
cmd "class get"
cmd "class invokemethod"
cmd "class names"
cmd "class enumerate"
cmd "class associators"
cmd "class references"
cmd "class find"
cmd "class tree"

cmd "instance get"
cmd "instance delete"
cmd "instance create"
cmd "instance invokemethod"
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

