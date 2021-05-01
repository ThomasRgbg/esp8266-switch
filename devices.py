
from machine import unique_id



class Device:
    def __init__(self, devicelist):
        self.myid = unique_id()
        self.name = devicelist[self.myid]
        

