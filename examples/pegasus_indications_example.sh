#!/bin/bash
#
#  Example of creating subscription for pegasus test indications requesting
#  and receiving indications, and then removing the subscriptions from the
#  command line with pywbemcli and pywbemlistener

# The following are the parameters used in this script to create subscriptions,
# create a listener, and request indications from the OpenPegasus server.

# Default listener port
LISTENER_PORT=5000
# WBEM Server URL.  The default is an OpenPegasus container.
# If using  a local OpenPegasus WBEM server, localhost may be used as the
# address.
# In some cases localhost can still be used in the server URL with an
# OpenPegasus container. An OpenPegasus container is available from Docker
# with the name kschopmeyer/openpegasus-server:0.1.3 (or later version)
WBEM_SERVER_URL=http://localhost:15988

# Number of indications server should send
INDICATION_SEND_COUNT=1

# Subsription Destination address
# If usingOpenPegasus in a container, the real IP address
# of the host system must be used as the destination in the subscription.
# If running with WBEM server and listener in same system, "localhost" may
# be used host name in listener url
HOST_REAL_IP_ADDRESS=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127' | grep -v '172')
echo "Subscription Destination IP: ${HOST_REAL_IP_ADDRESS}"
LISTENER_DEST_URL="http://${HOST_REAL_IP_ADDRESS}:${LISTENER_PORT}"

# Listener bind address. May be either a public host name/IP address,
# a wildcard IP address or no value. Default with no value signals
# pywbemlistener to use the wildcard address.
BINDADDR=
# Change to set value to display verbose info on execution
VERBOSE=
#VERBOSE=1
# set to some value if log output
LOG=
#log=1

# Set General Option name and value for the following:
VERBOSE=$([ -z "${VERBOSE}" ] && echo "" || echo "--verbose")
LOGGV=$([ -z "${LOG}" ] && echo "" || echo "--log all")
SERVER_GENERAL_OPTIONS="-s ${WBEM_SERVER_URL} ${VERBOSE} ${LOGGV}"

if [ ! -z ${VERBOSE} ]; then
    echo WBEM Server General Options : ${SERVER_GENERAL_OPTIONS}
fi

LISTENER_NAME="lis-example"
INDICATION_RCV_FILE="ExampleIndRcvd.txt"

rm --force ${INDICATION_RCV_FILE}

# Confirm server exists
pywbemcli ${SERVER_GENERAL_OPTIONS} connection test
(($? != 0)) && { echo "pywbemcli connection test exit $?"; exit 1; }

#
#  Create the Destination, Filter, and Indication Subscription
#
QUERY="SELECT * from Test_IndicationProviderClass"

if [ ! -z ${VERBOSE}]; then
    echo Add destination ID=DEST1 listener-url=${LISTENER_DEST_URL}
fi
pywbemcli ${SERVER_GENERAL_OPTIONS} \
    subscription add-destination DEST1 \
    --listener-url ${LISTENER_DEST_URL}
(($? != 0)) && { echo "pywbemcli subscription add-filter exit $?"; exit 1; }

if [ ! -z ${VERBOSE}]; then
    echo Addfilter ID=FILTER1 QUERY=${QUERY}
fi
pywbemcli ${SERVER_GENERAL_OPTIONS} \
    subscription add-filter \
    FILTER1 \
    --query "SELECT * from Test_IndicationProviderClass" \
    --source-namespaces test/TestProvider \
    --owned
(($? != 0)) && { echo "pywbemcli subscription add-filter exit $?"; exit 1; }

if [ ! -z ${VERBOSE}]; then
    echo Add subscription Dest ID=DEST1 filter ID=FILTER1 QUERY=${QUERY}
fi

if [ ! -z ${VERBOSE}]; then
    pywbemcli ${SERVER_GENERAL_OPTIONS} --output-format=mof \
        subscription list-destinations

    pywbemcli ${SERVER_GENERAL_OPTIONS} --output-format=mof \
        subscription list-filters
fi

pywbemcli ${SERVER_GENERAL_OPTIONS} \
    subscription add-subscription \
    DEST1 \
    FILTER1
(($? != 0)) && { echo "pywbemcli subscription add-subcription exit $?"; exit 1; }

if [ ! -z ${VERBOSE}]; then
    pywbemcli ${SERVER_GENERAL_OPTIONS} subscription list
fi

if [ ! -z ${VERBOSE} ]; then
    echo "pywbemlistener start ${LISTENER_NAME} \
       --port ${LISTENER_PORT} --bind-addr ${BINDADDR} --scheme http \
       --indi-file ${INDICATION_RCV_FILE}"
fi

if [ ! -z ${BINDADDR} ];then
    BINDADDR_OPTION="--bind-addr ${BINDADDR}"
else
    BINDADDR_OPTION=
fi

pywbemlistener start ${LISTENER_NAME} \
    --port ${LISTENER_PORT} \
    ${BINDADDR_OPTION} \
    --scheme http \
    --indi-file ${INDICATION_RCV_FILE}
(($? != 0)) && { echo "pywbemlistener start exited $?"; exit 1; }

#  Send InvokeMethod request for indications. This is an OpenPegasus specific
#  namespace, class and method
if [ ! -z ${VERBOSE} ]; then
    echo "Send request for test indication count = ${INDICATION_SEND_COUNT}"
fi

echo "Send request for test indication count = ${INDICATION_SEND_COUNT}"
echo "SERVER_GENERAL_OPTIONS= ${SERVER_GENERAL_OPTIONS}"
pywbemcli ${SERVER_GENERAL_OPTIONS} class invokemethod \
    Test_IndicationProviderClass \
    SendTestIndicationsCount \
    --namespace test/TestProvider \
    -p indicationSendCount=${INDICATION_SEND_COUNT}
(($? != 0)) && { echo "pywbemcli InvokeMethod Request for indications exited $?"; exit 1; }

echo "InvokeMethod sent OK"

# Wait for expected indications count.
TIME_TO_SLEEP=$((2 + (${INDICATION_SEND_COUNT} / 100) ))

if [ ! -z ${VERBOSE} ]; then
    echo "Wait ${TIME_TO_SLEEP} sec. for indications to be received"
fi

echo wait $TIME_TO_SLEEP sec. for indications to arrive
sleep $TIME_TO_SLEEP

COUNT=0
if [ -f  "${INDICATION_RCV_FILE}" ]; then
    COUNT=$(wc -l < $INDICATION_RCV_FILE)
fi

if [[ ${COUNT} == ${INDICATION_SEND_COUNT} ]]; then
    RESULT="SUCCESS"
else
    RESULT="FAILED"
fi
echo "${RESULT}; ${INDICATION_SEND_COUNT} indications expected, ${COUNT} received"

# Close the listener and remove the subscription.
if [ ! -z ${VERBOSE} ]; then
    echo "Remove the subscription and stop the listener ${LISTENER_NAME}"
fi

pywbemlistener stop ${LISTENER_NAME}
(($? != 0)) && { echo "pywbemlistener stop Request exited $?"; exit 1; }

if [ ! -z ${VERBOSE} ]; then
    pywbemlistener list
fi

# Remove the subscription server object with optio to removes all owned
# subscriptions
pywbemcli ${SERVER_GENERAL_OPTIONS} \
    subscription remove-subscription \
     DEST1 FILTER1 \
    --remove-associated-instances
if [ ! -z ${VERBOSE} ]; then
    pywbemcli ${SERVER_GENERAL_OPTIONS} subscription list --summary
fi

rm --force ${INDICATION_RCV_FILE}
