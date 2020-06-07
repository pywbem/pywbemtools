#!/usr/bin/env python
"""
This is a simple tool to execute pywbemcli and capture the results

"""
from __future__ import absolute_import, print_function
import shlex
import os
from subprocess import Popen, PIPE


ERRORS = 0
USE_MD = False


def execute_cmd(cmd_str, shell=False):
    """
    Execute the command in cmd_str and get its exitcode, stdout and stderr.

    This function calls subprocess Popen to be able to execute the
    command and  get stdout, stderr, and the exitcode.

    Parameters:
      cmd_str (:term: `string)
        Command to be executed

      shell (boolean)
        Defines whether shell is to be used to execute the command.  Normally
        the shell should not be required.

    Return:
        Tuple of exitcode, out, err where out and err are strings representing
        the stderr and stdout data
    """
    args = shlex.split(cmd_str)

    proc = Popen(args, stdout=PIPE, stderr=PIPE, shell=shell)
    std_out_str, std_err_str = proc.communicate()
    exitcode = proc.returncode

    # return tuple of exitcode, stdout, stderr
    return exitcode, std_out_str, std_err_str


def md_headline(title, level):
    """
    Format a markdown header line based on the level argument
    """
    level_char_list = ['=', '-']
    try:
        level_char = level_char_list[level]
    except IndexError:
        level_char = '='

    return '\n{0}\n{1}\n'.format(title, (level_char * len(title)))


def headline(title, level):
    """Output a headline that separates output groups.
    """
    if USE_MD:
        md_headline(title, level)
    else:
        print('{0}\n**{1}**\n'.format(title, ('-' * len(title))))


def print_md_verbatum_text(text_str):
    """
    Print the text on input surrounded by the back quotes defining
    veratum text
    """
    print('```')
    print(text_str)
    print('```')


def execute_pywbemcli_cmd(cmd_str, general_options=''):
    """Output a command created from the input and test result.
    """
    global ERRORS  # pylint: disable=global-statement

    if isinstance(cmd_str, list):
        for cmd in cmd_str:
            execute_pywbemcli_cmd(cmd)
    else:
        command = 'pywbemcli {0} {1}'.format(general_options, cmd_str)
        if USE_MD:
            print(md_headline(command, 1))
        else:
            print('{0}\nPYWBEMCLI COMMAND: {1}'.format(('=' * 50), command))

        exitcode, out, err = execute_cmd(command)

        if USE_MD:
            print_md_verbatum_text(out)
        else:
            print(out)
        if err:
            print('**STDER:** {0}'.format(err))

        if exitcode != 0:
            ERRORS += 1
            print('**ERROR:** cmd `{0}`'.format(command))


#
#  The following is the input arguments for a single pywbemcli command
#

if not os.environ.get('PYWBEMCLI_SERVER'):
    print('PYWBEMCLI_SERVER env variable not found')
    quit
execute_pywbemcli_cmd("class get CIM_ManagedElement")

quit

execute_pywbemcli_cmd("class get CIM_ManagedElement -l")
execute_pywbemcli_cmd("class get CIM_ManagedElement --local-only")
execute_pywbemcli_cmd("class get CIM_ManagedElement --no-qualifiers")
execute_pywbemcli_cmd("class get CIM_ManagedElement -c")
execute_pywbemcli_cmd("class get CIM_ManagedElement --include-classorigin")
execute_pywbemcli_cmd("class get CIM_ManagedElement --include-classorigin")
execute_pywbemcli_cmd(
    "class get CIM_ManagedElement --namespace root/PG_Interop")
execute_pywbemcli_cmd("class get CIM_ManagedElement -p InstanceID -p Caption")
execute_pywbemcli_cmd("class get CIM_ManagedElement -p InstanceID")
execute_pywbemcli_cmd("class get CIM_ManagedElement -p \"\"")

execute_pywbemcli_cmd("class enumerate")
execute_pywbemcli_cmd("class enumerate CIM_System")
execute_pywbemcli_cmd("class enumerate CIM_System -d")
execute_pywbemcli_cmd("class enumerate CIM_System -l")
execute_pywbemcli_cmd("class enumerate CIM_System -s")
execute_pywbemcli_cmd("class enumerate CIM_System --local-only")
execute_pywbemcli_cmd("class enumerate CIM_System --names-only")
execute_pywbemcli_cmd("class enumerate CIM_System -o")
execute_pywbemcli_cmd("class enumerate CIM_System -o -s")

#
execute_pywbemcli_cmd("class associators CIM_System")
execute_pywbemcli_cmd("class associators CIM_System s")
execute_pywbemcli_cmd("class associators CIM_System -o")
execute_pywbemcli_cmd("class associators CIM_System -o -s")

execute_pywbemcli_cmd("class references CIM_System -o")
execute_pywbemcli_cmd("class references CIM_System -o -s")
execute_pywbemcli_cmd("class references CIM_System")
execute_pywbemcli_cmd("class references CIM_System -s")

execute_pywbemcli_cmd("class find CIM_System")
execute_pywbemcli_cmd("class find PyWBEM")

# NOTE -s means something different here
execute_pywbemcli_cmd("class hierarchy CIM_System")
execute_pywbemcli_cmd("class hierarchy CIM_System -s")
execute_pywbemcli_cmd("class hierarchy CIM_ManagedElement -s")
execute_pywbemcli_cmd("class hierarchy CIM_ManagedElement --superclasses")
execute_pywbemcli_cmd(
    "class hierarchy CIM_System --superclasses --namespace root/PG_Interop")
execute_pywbemcli_cmd("class hierarchy CIM_System --namespace root/PG_Interop")

# invoke method on a class

execute_pywbemcli_cmd("instance enumerate PyWBEM_Person")
execute_pywbemcli_cmd("instance enumerate PyWBEM_Person -p name")
execute_pywbemcli_cmd("instance enumerate PyWBEM_Person -o")

execute_pywbemcli_cmd("instance enumerate PyWBEM_Person -p name -p ",
                      "CreationClassName",
                      general_options='--output-format table')

# TODO: Find way to do interactive in batch. This disabled for now
# execute_pywbemcli_cmd("instance get PyWBEM_Person.?")

execute_pywbemcli_cmd(
    "instance get PyWBEM_Person.CreationClassName=PyWBEM_Person,name=Bob")

execute_pywbemcli_cmd("instance create  PyWBEM_Person -x Name=Fred -x "
                      "GivenName=Jones -x CreationClassName=PyWBEM_Person")

execute_pywbemcli_cmd("instance delete PyWBEM_Person."
                      "CreationClassName=PyWBEM_Person,Name=Fred")
# # invoke method

# # query

execute_pywbemcli_cmd("instance count")

execute_pywbemcli_cmd("server brand")
execute_pywbemcli_cmd("server info")
execute_pywbemcli_cmd("server interop")
execute_pywbemcli_cmd("server namespaces")
execute_pywbemcli_cmd("server profiles")
execute_pywbemcli_cmd("server profiles -o DMTF")
# -n broken
execute_pywbemcli_cmd("server profiles -n CPU")
