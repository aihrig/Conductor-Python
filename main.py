from machine import Pin
import network
import socket
from time import sleep
from MicroWebSrv2 import *
import conductor
from instance import config as cfg
from conductor import views

# Initialize onboard LED
led = Pin(13, Pin.OUT)
led.on()

# Connect to WiFi
print('Connecting to WiFi...')
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(cfg.network['ssid'], cfg.network['password'])
while station.isconnected() == False:
    # led.value(not led.value())
    sleep(0.5)

# led.on()
print('')
print('Successfully connected to {0}'.format(cfg.network['ssid']))
print(station.ifconfig())


def main():
    '''
    Set up single web server in a managed pool with minimal resources
    '''
    print('Welcome to the Rad FX Express!')
    
    # Start web server
    mws2 = MicroWebSrv2()
    mws2.RequestsTimeoutSec = 10
    mws2.SetEmbeddedConfig()
    mws2.StartManaged()

    try:
        while True:
            sleep(0.5)
    except KeyboardInterrupt:
        mws2.Stop()


if __name__ == '__main__':
    main()
