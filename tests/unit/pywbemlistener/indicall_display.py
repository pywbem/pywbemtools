"""
Indication callback function for testing pywbemlistener.
"""


def display(indication, host):
    """
    Indication callback function that displays the indication on stdout.

    Parameters:

      indication (:class:`~pywbem.CIMInstance`):
        Representation of the CIM indication that has been received.
        Its `path` attribute is `None`.

      host (:term:`string`):
        Host name or IP address of WBEM server sending the indication.
    """
    props = ['{}={!r}'.format(pn, p.value)
             for pn, p in indication.properties.items()]
    print("{}:{}:{}".format(host, indication.classname, ','.join(props)))
