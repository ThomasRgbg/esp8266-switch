from machine import Pin, I2C, reset, RTC, unique_id
import time
import ntptime

from mqtt_handler import MQTTHandler



class Relais:
    def __init__(self):
        self.pin=Pin(4,Pin.OUT)
        self.pin.value(0)

    def on(self):
        print("Set GPIO on")
        self.pin.value(1)

    def off(self):
        print("Set GPIO off")
        self.pin.value(0)

    @property
    def state(self):
        return self.pin.value()

    @state.setter
    def state(self, value):
        print("Setting Relais to {0}".format(value))
        if int(value) == 1:
            self.on()
        else:
            self.off()

    def set_state(self, value):
        self.state = int(value)

####
# Main
####

# time to connect WLAN, since marginal reception
time.sleep(5)

relais = Relais()

sc = MQTTHandler(b'pentling/zistvorne', '192.168.0.13')
sc.register_action('pump_enable', relais.set_state)

def mainloop():
    count = 1
    errcount = 0

    while True:

        if sc.isconnected():
            print("send to MQTT server")
            for i in range(25):
                sc.mqtt.check_msg()
                time.sleep(1)
            sc.publish_generic('pump', relais.state)
        else:
            print("MQTT not connected - try to reconnect")
            sc.connect()
            errcount += 1
            continue

        time.sleep(5)

        # Too many errors, e.g. could not connect to MQTT
        if errcount > 20:
            reset()

        count += 1

mainloop()
