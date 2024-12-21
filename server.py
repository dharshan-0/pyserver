import argparse, os, mimetypes
from socket import *

PORT = 9000
HOST = "localhost"
W_DIR = os.getcwd()
FILE = "index.html"

"""
example response:
['GET / HTTP/1.1', 'Host: localhost:9000', 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language: en-US,en;q=0.5', 'Accept-Encoding: gzip, deflate, br, zstd', 'Connection: keep-alive', 'Upgrade-Insecure-Requests: 1', 'Sec-Fetch-Dest: document', 'Sec-Fetch-Mode: navigate', 'Sec-Fetch-Site: none', 'Sec-Fetch-User: ?1', 'Priority: u=0, i', '', '']
['GET /img HTTP/1.1', 'Host: localhost:9000', 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language: en-US,en;q=0.5', 'Accept-Encoding: gzip, deflate, br, zstd', 'Connection: keep-alive', 'Upgrade-Insecure-Requests: 1', 'Sec-Fetch-Dest: document', 'Sec-Fetch-Mode: navigate', 'Sec-Fetch-Site: none', 'Sec-Fetch-User: ?1', 'Priority: u=0, i', '', '']
"""


def parseResponse(response: list[str]):
    header = response[0].split(" ")
    path = header[1]
    method = header[0]
    return (method, path)


def validateArgs(args):
    if not os.path.isdir(args.dir):
        raise Exception("Invalid directory")

    if not os.path.isfile(os.path.join(args.dir, args.file)):
        raise Exception("Invalid file")


def getCommandLineArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=PORT,
        help=f"Port to listen on, default is {PORT}",
    )
    parser.add_argument(
        "-addr",
        "--address",
        type=str,
        default=HOST,
        help=f"Address to listen on, default is {HOST}",
    )
    parser.add_argument(
        "-d",
        "--dir",
        type=str,
        default=W_DIR,
        help=f"Working directory to serve from, default is current directory",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=f"{FILE}",
        help=f"File to serve, default is index.html",
    )
    return parser.parse_args()


def router(url_path, working_dir, file):
    url_path = url_path[1:]

    if not os.path.exists(os.path.join(working_dir, url_path)):
        raise Exception("File not found")

    if url_path == "":
        return os.path.join(working_dir, file)
    else:
        return os.path.join(working_dir, url_path)


def getHeaders(file_path, verbose):
    mime = mimetypes.guess_type(file_path)[0]
    if verbose:
        print("mime -> ", mime)
    return [
        b"HTTP/1.1 200 OK\r\n",
        b"Content-Type: " + mime.encode() + b"\r\n",
        b"\r\n",
    ]


def createServer(args):
    server_socket = socket(AF_INET, SOCK_STREAM)
    try:
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind((args.address, args.port))
        server_socket.listen(5)
        while 1:
            (client_socket, _) = server_socket.accept()

            res = client_socket.recv(5000).decode()
            res_arr = res.split("\r\n")
            method, path = parseResponse(res_arr)

            try:
                if method == "GET":
                    file_path = router(path, args.dir, args.file)
                    if args.verbose:
                        print("path -> ", file_path)
                    header = getHeaders(file_path, args.verbose)
                    if args.verbose:
                        print("header -> ", header)
                    with open(file_path, "rb") as ff:
                        l = os.path.getsize(file_path)
                        data = b"".join(header)
                        data += ff.read(l)
                        client_socket.sendall(data)
                        client_socket.shutdown(SHUT_WR)

                else:
                    response = b"".join(
                        [
                            b"HTTP/1.1 404 OK\r\n",
                            b"Content-Type: text/plain\r\n",
                            b"\r\n",
                            b"method not supported",
                        ]
                    )
                    client_socket.sendall(response)
                    client_socket.shutdown(SHUT_WR)

            except Exception as exc:
                print("Error 1 -> ", exc)
                response = b"".join(
                    [
                        b"HTTP/1.1 404 OK\r\n",
                        b"Content-Type: text/plain\r\n",
                        b"\r\n",
                        b"File not found",
                    ]
                )
                client_socket.sendall(response)
                client_socket.shutdown(SHUT_WR)

    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as exc:
        print("Error 2 -> ", exc)

    server_socket.close()


args = getCommandLineArguments()
try:
    validateArgs(args)
except Exception as exc:
    print("Error 3 -> ", exc)
    exit(1)

print(f"Listening on http://{args.address}:{args.port}")
createServer(args)
