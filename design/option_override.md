These tables describe the desired behavior for different override situations (meant to be a proposal), and lists the required changes to the existing implementation (incomplete).

Next steps:
* Agree on desired behavior
* Determine changes to existing implementation

**Options with connection context:**

Kinds of overrides:
* "conn -> opt" - If the --name option is specified on a command, what should happen when the option in question is specified on the same command. This applies to both command line commands and interactive session commands.
* "cmd -> int" - If there is a connection inherited from the command line to an interactive session, what should happen when the option in question is specified on an interactive command in that session. This applies regardless of how the connection at the command line level was crafted.

The 'desired' columns describe the desired behavior:
* 'update PS' means to update the currently used PywbemServer object from the option.
* 'reset+update PS' means to reset the currently used PywbemServer object to default values and then to update it from the option. This is processed as the first option.
* 'replace PS' means to update the currently used PywbemServer object from the new connection, replacing all connection attributes.

The 'changes' columns describe the necessary changes to the existing implementation, in order to have the desired behavior.

| type | general option name | desired conn -> opt | desired cmd -> int | changes conn -> opt | changes cmd -> int |
|:---- |:------------------- |:------------------- |:------------------ |:------------------- |:------------------ |
| both | name                | N/A                 | replace PS         |                     |                    |
| mock | mock-server         | reject              | reset+update PS    |                     |                    |
| real | server              | reject              | reset+update PS    |                     |                    |
| real | default-namespace   | update PS           | update PS          |                     |                    |
| real | user                | update PS           | update PS          |                     |                    |
| real | password            | update PS           | update PS          |                     |                    |
| real | verify              | update PS           | update PS          |                     |                    |
| real | certfile            | update PS           | update PS          |                     |                    |
| real | keyfile             | update PS           | update PS          |                     |                    |
| real | ca-certs            | update PS           | update PS          |                     |                    |
| both | timeout             | update PS           | update PS          |                     |                    |
| both | use-pull            | update PS           | update PS          |                     |                    |
| both | pull-max-cnt        | update PS           | update PS          | add to PS           |                    |

**Options with cmd context:**

The 'desired' column describes the desired behavior:
* 'inherit+update' means to inherit the command line value of the option into the interactive session, and then to override it from the option on the interactive command, if specified.

The 'changes' column describes the necessary changes to the existing implementation, in order to have the desired behavior.

| type | general option name | desired            | changes            |
|:---- |:------------------- |:------------------ |:------------------ |
| both | verbose             | inherit+update     |                    |
| both | timestats           | inherit+update     |                    |
| both | format              | inherit+update     |                    |
| both | log                 | inherit+update     |                    |
| both | pdb                 | inherit+update     |                    |

**Other changes:**

* Reject type-specific connection options when the connection is not of that type
