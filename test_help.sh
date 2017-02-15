#!/bin/bash

pywbemcli --help
pywbemcli class --help
pywbemcli class get --help
pywbemcli class names  --help
pywbemcli class enumerate --help
pywbemcli class associators --help
pywbemcli class references --help
pywbemcli class find --help

pywbemcli instance associators --help
pywbemcli instance delete --help
pywbemcli instance enumerate --help
pywbemcli instance get --help
pywbemcli instance names --help
pywbemcli instance number --help
pywbemcli instance references --help

pywbemcli qualifier --help
pywbemcli qualifier enumerate --help
pywbemcli qualifier get --help
pywbemcli server --help
pywbemcli server brand --help
pywbemcli server connection --help
pywbemcli server info --help
pywbemcli server namespaces --help
pywbemcli server interop --help
pywbemcli server profiles --help

pywbemcli -s http://localhost class get CIM_ManagedElement
pywbmecli -s http://localhost class class enumerate
pywbmecli -s http://localhost class class enumerate CIM_ManagedElement
pywbmecli -s http://localhost class class enumerate CIM_ManagedElement -d
pywbmecli -s http://localhost class class enumerate CIM_ManagedElement -l
pywbemcli -s http://localhost class find CIM_ManagedElement
pywbemcli -s http://localhost class find PyWBEM

pywbemcli -s http://localhost instance enumerate PyWBEM_Person
pywbemcli -s http://localhost instance enumerate PyWBEM_Person -p name
pywbemcli -s http://localhost instance enumerate PyWBEM_Person -o

pywbemcli -s http://localhost instance get PyWBEM_Person -i
pywbemcli -s http://localhost instance get PyWBEM_Person.name=bob

pywbemcli -s http://localhost instance count

pywbemcli -s http://localhost server brand
pywbemcli -s http://localhost server info
pywbemcli -s http://localhost server interop
pywbemcli -s http://localhost server namespaces
pywbemcli -s http://localhost server profiles
pywbemcli -s http://localhost server profiles -o DMTF
# -n broken
pywbemcli -s http://localhost server profiles -n "CPU Profile"

