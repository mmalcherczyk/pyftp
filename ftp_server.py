#!/usr/bin/env python3

import logging

import argparse
import socket
from pathlib import Path

from pyftpdlib import FTPHandler

logging.basicConfig(level=logging.INFO)


def local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        return s.getsockname()[0]

def hostname():
    return socket.gethostname()


def main():
    help_text = "help:\n" \
                "   {0} -u user -p password\n" \
                "   {0} -u user -p password --readonly\n" \
                "   {0} -u user -p password --dir /tmp\n".format(__file__)

    p = argparse.ArgumentParser(prog="FTP_SERVER",
                                description="FTP Server",
                                epilog=help_text,
                                formatter_class=argparse.RawDescriptionHelpFormatter)

    # ARGUMENTS 
    p.add_argument("--tls", action="store_true")
    p.add_argument("-u", "--user", type=str, default="user")
    p.add_argument("-p", "--password", type=str, default="passw0rd")
    p.add_argument("-d", "--dir", type=Path, default=Path().cwd())
    p.add_argument("--port", type=int, default=60000)


    args = p.parse_args()


    auth = DummyAuthorizer()
    auth.add_user(args.user, args.password, str(args.dir))


    if args.tls:
        handler = FTPHandler
    else:
        handler = FTPHandler

    handler.authorizer = auth 

    server = FTPServer((local_ip(), args.port), handler)

    
    server.serve_forever()

if __name__ == "__main__":
    main()







