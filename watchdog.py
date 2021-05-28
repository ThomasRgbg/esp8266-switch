from machine import Timer, reset 
import time

class TimerWatchdog:
    def __init__(self, interval):
        self.timer = Timer(0)
        self.timer.init(period=(interval*1000), mode=Timer.PERIODIC, callback=self.wdtcheck)
        self.feeded = True

    def wdtcheck(self, timer):
        if self.feeded:
            print("Watchdog feeded, all fine")
            self.feeded = False
        else:
            print("Watchdog hungry, lets do a reset in 5 sec")
            time.sleep(5)
            reset()

    def feed(self):
        self.feeded = True

