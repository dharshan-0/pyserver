# pyserver
A simple http server form scratch using tcp sockets

## Note
This project is tested with linux but not on windows so Iam not sure it will work on windows or not.

## Installation

- Make sure you installed python in your machine.

- Clone this repo:

```bash
git clone https://github.com/dharshan-0/pyserver.git
```

- Just run it.

```bash
python server.py
```

- Note: For configuration run `python serve.py -h`

```bash
usage: server.py [-h] [-p PORT] [-addr ADDRESS] [-d DIR] [-v] [-f FILE]

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port to listen on, default is 9000
  -addr ADDRESS, --address ADDRESS
                        Address to listen on, default is localhost
  -d DIR, --dir DIR     Working directory to serve from, default is current directory
  -v, --verbose         Verbose mode
  -f FILE, --file FILE  File to serve, default is index.html
```