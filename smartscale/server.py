#!/usr/bin/python3

import dbus
import json
import asyncio
from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor
import calc_metrics as calc
# from scan import my_scanner


GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"

#Dummy data
height = 170  # cm
dob = "15/08/1995"
gender = "male"
activity_factor = 1.55  


def calculate_bmi (weight):
    height = 1.7
    BMI = round(weight/(height**2), 2)
    return BMI

class WeightScaleAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("Weight Scale")
        self.include_tx_power = True
        self.receivedWeight = False;
        
class WeightService(Service):
    WEIGHT_SVC_UUID = "00000001-cbd6-4d25-8851-18cb67b7c2d9"

    def __init__(self, index):

        Service.__init__(self, index, self.WEIGHT_SVC_UUID, True)
        self.add_characteristic(WeightCharacteristic(self))
        
class WeightCharacteristic(Characteristic):
    body_metrics = []
    WEIGHT_CHARACTERISTIC_UUID = "00000002-cbd6-4d25-8851-18cb67b7c2d9"
    
    def __init__(self, service):
            self.notifying = False
            Characteristic.__init__(
                    self, self.WEIGHT_CHARACTERISTIC_UUID,
                    ["read", 'write'], service)
            self.add_descriptor(WeightDescriptor(self))

    def WriteValue(self, value, options):
        byte_data = bytes(value)
        string_data = byte_data.decode('utf-8')
        # weight = float(string_data)
        print(f"received: {string_data}")
        # self.body_metrics = calc.get_body_metrics(height, weight, dob, gender, activity_factor)
        # print(self.body_metrics)
            
    def ReadValue(self, options):
        value = []
        json_string = json.dumps(self.body_metrics)
        
        for c in json_string:                                                                                 
            value.append(dbus.Byte(c.encode())) 
            
        return value
    
    
class WeightDescriptor(Descriptor):
    WEIGHT_DESCRIPTOR_UUID = "2901"
    WEIGHT_DESCRIPTOR_VALUE = "Fake data"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.WEIGHT_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.WEIGHT_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value

app = Application()

app.add_service(WeightService(0))
app.register()

adv = WeightScaleAdvertisement(0)
adv.register()


try:
    app.run()
    
except KeyboardInterrupt:
    app.quit()
