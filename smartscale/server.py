#!/usr/bin/python3

import dbus
import json
import threading
from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor
from dbcontroller import dbcontroller


GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"

#Dummy data
height = 170  # cm
dob = "15/08/1995"
gender = "male"
activity_factor = 1.55  

json_data = {
    "id": 2,
    "weight": 64
}

calculate_task = threading.Thread(target=dbcontroller.process_data, args=(json_data['id'], json_data['weight']))
calculate_task.start()
calculate_task.join()

body_metrics = {
  "weight": 64.1,
  "bmi": 23.1,
  "bmr": 1578,
  "tdee": 2304.55,
  "lbm": 50.72,
  "fat_percentage": 18.3,
  "water_percentage": 47.2,
  "bone_mass": 7.8,
  "muscle_mass": 46.15,
  "protein_percentage": 21.5,
  "visceral_fat": 8.21,
  "ideal_weight": 70.4
}


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
        json_data = json.loads(string_data)
        print(f"received: {string_data}")
        
        calculate_task = threading.Thread(target=dbcontroller.process_data, args=(json_data['id'], json_data['weight']))
        calculate_task.start()
            
    def ReadValue(self, options):
        value = []
        json_string = json.dumps(dbcontroller.get_body_metrics())
        
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
