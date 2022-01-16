#!/bin/env fish

while ./autostart_rtt.py; telnet localhost 4445; sleep 1; end




