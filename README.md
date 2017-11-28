# AWX job tailer

Small python script to follow the stdout from a AWX job. The current state of the web applications output is not that good so i felt this was necessary.

Install the requirements before use.

The script will read your login from `~/.tower_cli.cfg` if available, if not, the login information can be entered as follows:

```
usage: tail.py [-h] [-a ADDRESS] [-u USERNAME] [-p PASSWORD] [-i] job

positional arguments:
  job                   The job id to follow

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        AWX/Tower address
  -u USERNAME, --username USERNAME
                        AWX/Tower username
  -p PASSWORD, --password PASSWORD
                        AWX/Tower password
  -i, --insecure        Use HTTP instead of HTTPS

```

The application will _not_ terminate by itself so when a job ends, the way out is `CTRL + C`.



