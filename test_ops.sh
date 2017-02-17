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

