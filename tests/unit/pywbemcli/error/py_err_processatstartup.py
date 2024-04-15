# !PROCESS!AT!STARTUP!
"""
This is an error test of the code that processes a script at startup. This
python code specifically includes a syntax error to be caught by pywbemcli.
Note that this file is marked to process at startup which is really a private
extension for the test environment.
"""


# Note: pylint issue "syntax-error" cannot be suppressed.
# Note: ruff issue E999 (Syntax Error) cannot be suppressed.
def mock?prompt(msg):  # noqa: E999
    """Mock function to replace pywbemcli_prompt and return a value"""
    # pylint: disable=undefined-variable
    print(msg)
    return "HaHa"
