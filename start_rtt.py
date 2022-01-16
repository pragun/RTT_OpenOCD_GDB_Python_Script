import gdb


def locate_rtt_address():
    print("Locating _acDownBuffer...\n")
    a = str(gdb.parse_and_eval('_SEGGER_RTT').address)
    addr = a.split(' ')[0]
    print("Address at: ",addr,"\n")
    return addr

def rp2040_setup_rtt(rtt_address, core=0):
    if core not in [0,1]:
        print("Expected core 0 or 1 for RP2040\n")
    else:
        cmd = 'monitor rp2040.core%d rtt setup %s 16 "SEGGER RTT"'%(core,rtt_address,)
        print(cmd)
        gdb.execute(cmd)

def rp2040_start_rtt(core=0):
    if core not in [0,1]:
        print("Expected core 0 or 1 for RP2040\n")
    else:
        gdb.execute('monitor rp2040.core%d rtt start'%(core,))

def rp2040_start_rtt_telnet(port=4445,channel=0):
    gdb.execute('monitor rtt server start %d %d'%(port,channel))


