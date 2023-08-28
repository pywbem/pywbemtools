#!/bin/bash
#
#  Example of invokemethod to request that an OpenPegasus server send
#  a number of indications defined by a parameter in the invoke method
#
#  This test is unique to OpenPegasus and also only useful if an OpenPegasus
#  test class in installed.
#
#    Sends an invokemethod request to the WBEM server requesting that the server
#    send test indications to an indication listener.
#
#    This only works when an indication subscription has already be defined
#    in the WBEM server specifically for these indications.  See
#    pegaus_indications_example.sh for the subscription creation and
#    removal code.
#    Two input parameters are allowed:
#    1. URL of OpenPegasus wbem server
#    2. Number of indications to send
#

echo "pegasus_send_indications.sh"

# Default option variable values. Set these to other values to change tests
# Server url. Default is typical open pegasus container url

URL=http://localhost:15988
# Number of indications to send
INDICATION_SEND_COUNT=1
# Set verbose flag for pywbemcli cmd execution
VERBOSE=False
# enable pywbemcli log output
LOG=True

# change input variables to define the options for each
VERBOSE=$([ -z "${VERBOSE}" ] && echo "" || echo "--verbose")
LOG=$([ -z "${LOG}" ] && echo "" || echo "--log all")

SERVER_GENERAL_OPTIONS="-s ${URL} ${VERBOSE} ${LOG} ${KEY_FILE} ${CERT_FILE}"
#
#  Send InvokeMethod request for indications. This is an OpenPegasus specific
#  namespace, class and method
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

