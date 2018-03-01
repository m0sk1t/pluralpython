## Installation and running

Run

    ./install.sh

to install dependencies, then run

    ./run_server.sh

to start a web-server.

## CLI usage

To setup CLI connection you must change settings in `[server]` section of `settings.ini` file, otherwise settings in `[default]` section would be used.

To reset whole tree run:

    python3 cli/cli.py reset

To delete branch with <boss_id> and all its children run:

    python3 cli/cli.py drop <boss_id>

To add a new record run:

    python3 cli/cli.py add "B1,E1,E2,E3" ["B2,E34,E55,E1" ...]

It takes one or more strings of the following shape: "B1,E1,E2,E3,..." where B1 is boss and E1,... are employees, all just simple strings.

## Web

For viewing chart, open link below in your browser

    http://127.0.0.1:5000/
