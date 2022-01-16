#!/bin/env python

from telnetlib import Telnet
import time
import re

address = b'0x20002154'
core_id = 0
core_txt = b'rp2040.core'
core = b'%b%d'%(core_txt,core_id)
id = b"SEGGER RTT"
setup_cmd = b'%b rtt setup %s 16 "%b"\n'%(core,address,id)
core_start_cmd = b'%b rtt start\n'%(core,)
core_stop_cmd = b'%b rtt stop\n'%(core,)

port = 4445
channel = 0

server_stop_cmd = b'rtt server stop %d\n'%(port,)
server_start_cmd = b'rtt server start %d %d\n'%(port,channel)

with Telnet('localhost', 4444) as tn:
    tn.read_until(b"Open On-Chip Debugger")
    print("Connected.\n")
    #tn.write(setup_cmd)
    #response = tn.expect([re.compile(b">")])
    #print(response)
    time.sleep(0.1)

    while(True):
        print("Trying to start RTT...\n")
        tn.write(core_start_cmd)
        (idx,match,data) = tn.expect([re.compile(b"^(.*?)No control block found",flags=re.DOTALL),re.compile(b"^(.*?)Control block found at(.*?)$",flags=re.DOTALL)],timeout=1.0)
        print(idx,match,data)
        if idx == 1:
            break

        print("Stopping RTT. \n")
        tn.write(core_stop_cmd)
        tn.read_until(b">")
        time.sleep(1)

    print("Control block found.\n")
    tn.write(server_stop_cmd)
    tn.read_until(b">")

    tn.write(server_start_cmd)
    (idx,match,data) = tn.expect([re.compile(b"^(.*?)Listening on port ([0-9]+?) for rtt connections",flags=re.DOTALL)],timeout=1.0)
    print(idx,match,data)

    if idx == 0:
        print("RTT Server started successfully on port:%d\n"%(port,))

    tn.close()

exit()
