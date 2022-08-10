from network import Sigfox
import socket
from machine import ADC
from dht import DHT
from machine import Pin
import time
from struct import pack


sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)


s.setblocking(True)


adc = ADC()
th = DHT(Pin('P10', mode=Pin.OPEN_DRAIN), 0)

time.sleep(2)

earth = adc.channel(pin='P13', attn=ADC.ATTN_11DB)

while True:
    earth()
    atm = th.read()
    payload = pack('>hbb', int(earth.value()), int(atm.temperature), int(atm.humidity))
    s.send(payload)
    print('Data sent:')
    print(payload)

    time.sleep(600)
