from machine import Pin, I2C, reset, RTC, unique_id
import time
import ntptime

from mqtt_handler import MQTTHandler
from devices import Device
from relay import Relay

devicelist = { b'\xd5\x9f\xa1\x00' : b'zistvorne',   # Shelly1
               b'\xfd\x76\xf8\x00' : b'schlazilicht',   # ESP01-relay
           }  
 
####
# Main
####

mydevice = Device(devicelist)

# time to connect WLAN, since marginal reception
time.sleep(5)

sc = MQTTHandler(b'pentling/' + mydevice.name, '192.168.0.13')

if mydevice.name == b'zistvorne':
    relay = Relay(4)
    sc.register_action('pump_enable', relay.set_state)

elif mydevice.name == b'schlazilicht':
    relay = Relay(0)
    sc.register_action('relay_set', relay.set_state)

else:
    print('unknown device')

def mainloop():
    count = 1
    errcount = 0

    while True:

        if sc.isconnected():
            print("send to MQTT server")
            for i in range(5):
                sc.mqtt.check_msg()
                time.sleep(0.25)
            if mydevice.name == b'zistvorne':
                sc.publish_generic('pump', relay.state)
            elif mydevice.name == b'schlazilicht':
                sc.publish_generic('relay', relay.state)

        else:
            print("MQTT not connected - try to reconnect")
            sc.connect()
            errcount += 1
            continue

        time.sleep(3)

        # Too many errors, e.g. could not connect to MQTT
        if errcount > 20:
            reset()

        count += 1

mainloop()
