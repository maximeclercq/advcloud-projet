# -*- coding: utf-8 -*-
import socket
import struct
import os, os.path

print("Connecting...")
if os.path.exists("/tmp/python_unix_sockets_example"):
    client = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
    client.connect("/tmp/python_unix_sockets_example")
    print("Ready.")
    print("Ctrl-C to quit.")
    print("Sending 'DONE' shuts down the server and quits.")
    while True:
        x = input( "> " )
        if "" != x:
            print("SEND:", x)
            # x = struct.pack("s", x)
            x = x.encode("utf-8")
            client.send(x)
        if "DONE" == x:
            print("Shutting down.")
            break
    client.close()
else:
    print("Couldn't Connect!")
    print("Done")