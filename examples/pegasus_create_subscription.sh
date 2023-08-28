#!/bin/bash
#
# Example of creating indicationsubscription for pegasus test indications.
# This script only creates the subscription objects defined specifically to
# define a subscription for the OpenPegasus test send_indications provider
# and assumes that they do not exist when the script is called.

# create_subscription server-general-options dest_id filter_id listener_url query source-namespace
LISTENER_PORT=5000
WBEM_SERVER_URL=http://localhost:15988
PORT=5000
# Subsription Destination address
# If using OpenPegasus in a container, the real IP address
# of the host system must be used as the destination in the subscription.
# If running with WBEM server and listener in same system, "localhost" may
# be used host name in listener url
HOST_REAL_IP_ADDRESS=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127' | grep -v '172')
echo "Subscription Destination IP: ${HOST_REAL_IP_ADDRESS}"
LISTENER_DEST_URL="http://${HOST_REAL_IP_ADDRESS}:${LISTENER_PORT}"

DESTID=odest1
FILTERID=ofilter1
VERBOSE=
LOG=
QUERY="SELECT * from Test_IndicationProviderClass"
SOURCE_NAMESPACES=test/TestProvider

VERBOSEOPT=$([ -z "${VERBOSE}" ] && echo "" || echo "--verbose")
LOGOPT=$([ -z "${LOG}" ] && echo "" || echo "--log all")

LISTENER_NAME="lis-example"
INDICATION_RCV_FILE="ExampleIndRcvd.txt"
# Listener bind address. May be either a public host name/IP address,
# a wildcard IP address or no value. Default with no value signals
# pywbemlistener to use the wildcard address.
BINDADDR=

rm --force ${INDICATION_RCV_FILE}

SERVER_GENERAL_OPTIONS="-s ${WBEM_SERVER_URL} ${LOGAPT} ${VERBOSEOPT}"

if [ ! -z ${VERBOSE} ]; then
    echo pywbemcli ${SERVER_GENERAL_OPTIONS}  subscription add-filter \
    ${FILTERID}  \
    --query "${QUERY}" \
    --source-namespaces ${SOURCE_NAMESPACES}
fi

pywbemcli ${SERVER_GENERAL_OPTIONS} subscription add-filter \
    ${FILTERID} \
    --query "${QUERY}" \
    --source-namespaces ${SOURCE_NAMESPACES}
(($? != 0)) && { echo "pywbemcli subscription add-filter exit $?"; exit 1; }

pywbemcli ${SERVER_GENERAL_OPTIONS} \
    subscription add-destination ${DESTID} \
    --listener-url ${LISTENER_DEST_URL}
(($? != 0)) && { echo "pywbemcli subscription add-destination exit $?"; exit 1; }

if [ ! -z ${VERBOSE} ]; then
    pywbemcli ${SERVER_GENERAL_OPTIONS} --output-format=plain\
        subscription list-destinations
    (($? != 0)) && { echo "pywbemcli subscription list-destinations exit $?"; exit 1; }
fi

pywbemcli ${SERVER_GENERAL_OPTIONS} \
    subscription add-subscription \
    ${DESTID} \
    ${FILTERID}
(($? != 0)) && { echo "pywbemcli subscription add-subcription exit $?"; exit 1; }

if [ ! -z ${VERBOSE} ]; then
    pywbemcli ${SERVER_GENERAL_OPTIONS} \
        subscription list-subscription \
        ${DESTID} \
        ${FILTERID}
    (($? != 0)) && { echo "pywbemcli subscription list-subscription exit $?"; exit 1; }
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


