from machine import Pin, I2C, reset, RTC, unique_id, Timer
import time
import ntptime

from mqtt_handler import MQTTHandler
from watchdog import TimerWatchdog
from devices import Device
from relay import Relay

devicelist = { b'\xd5\x9f\xa1\x00' : b'zistvorne',   # Shelly1
               b'\xfd\x76\xf8\x00' : b'schlazilicht',   # ESP01-relay
           }  
 
####
# Main
####

mydevice = Device(devicelist)

wdt = TimerWatchdog(interval = 180)
wdt.feed()

# time to connect WLAN, since marginal reception
time.sleep(5)

sc = MQTTHandler(b'pentling/' + mydevice.name, '192.168.0.13')

if mydevice.name == b'zistvorne':
    relay = Relay(4)
    sc.register_action('pump_enable', relay.set_state)
    sc.register_publisher('pump', relay.get_state)

elif mydevice.name == b'schlazilicht':
    relay = Relay(0)
    sc.register_action('relay_set', relay.set_state)
    sc.register_publisher('relay', relay.get_state)

else:
    while True:
        print('unknown device - Press CTLR-C to stop')
        time.sleep(10)

def mainloop():
    count = 1
    errcount = 0

    while True:
        print("count: {0}".format(count))

        if sc.isconnected():
            print("MQTT is connected")
            for i in range(40):
                sc.mqtt.check_msg()
                time.sleep(0.5)
            
            sc.publish_all()

        else:
            print("MQTT not connected - try to reconnect")
            sc.connect()
            errcount += 1
            continue

        time.sleep(1)

        # Too many errors, e.g. could not connect to MQTT
        if errcount > 20:
            reset()
    
        wdt.feed()

        count += 1

mainloop()
