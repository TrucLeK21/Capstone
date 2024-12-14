#!/usr/bin/python3

from datetime import datetime
import dbus
import json
import threading
from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor
from dbcontroller import dbcontroller
from facial_recognition import run_face_recognition
import base64


GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
lock_to_append = threading.Lock()
image_chunks = []



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


class FaceRecognitionService(Service):
    FACE_RECOGNITION_SVC_UUID = "00000001-6acc-4ba4-b29c-475d7b407faf"

    def __init__(self, index):

        Service.__init__(self, index, self.FACE_RECOGNITION_SVC_UUID, True)
        self.add_characteristic(FaceRecognitionCharacteristic(self))
        
class FaceRecognitionCharacteristic(Characteristic):
    FACE_RECOGNITION_CHARACTERISTIC_UUID = "00000002-6acc-4ba4-b29c-475d7b407faf"
    receiving_image = False
    
    def __init__(self, service):
            self.notifying = False
            Characteristic.__init__(
                    self, self.FACE_RECOGNITION_CHARACTERISTIC_UUID,
                    ["read", "write"], service)
            self.add_descriptor(FaceRecognitionDescriptor(self))
            


    def WriteValue(self, value, options):
        # Decode the chunk value (Base64 and JSON format)
        byte_data = bytes(value)
        string_data = byte_data.decode('utf-8')

        if not self.receiving_image:
            print("Receiving image...")
            self.receiving_image = True

        try:
            convert_task = threading.Thread(target=self.process_chunk, args=(string_data, ))
            convert_task.start()
        except Exception as e:
            # Handle any other unexpected exceptions
            print("An unexpected error occurred:", e)
        # print(chunk)

        # # Append chunk data to the list
        # image_chunks.append(chunk)



    def process_chunk(self, value):
        try:
            # Attempt to parse the JSON string
            chunk = json.loads(value)
            lock = threading.Lock()
            # Synchronize access to the shared list
            with lock:
                image_chunks.append(chunk)
            
            # If 'EOF' is received, process the complete data
            if chunk['data'] == 'EOF':
                self.receiving_image = False
                self.reconstruct_image()
                    
        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            print("Failed to decode JSON:", e)
        except Exception as e:
            # Handle any other unexpected exceptions
            print("An unexpected error occurred:", e)

    def reconstruct_image(self):
        """
        Sort and combine the chunks to reconstruct the image.
        """
        id = 1
        # Sort the chunks by the sequence number
        sorted_chunks = sorted(image_chunks, key=lambda x: x['seq'])
        
        # Combine the data (Base64 decoding each chunk)
        combined_data = b"".join(base64.b64decode(chunk['data']) for chunk in sorted_chunks if chunk['data'] != 'EOF')

        # Save or process the image data (e.g., save to a file)
        self.save_image(id, combined_data)

    def save_image(self, id, data):
        """
        Save the image data to a file.
        """
        current_date = datetime.now().strftime("%Y-%m-%d")
        imageName = f"{id}_{current_date}.jpg"
        imagePath = f"face_rec_source/image_to_test/{imageName}"
        
        with open(imagePath, "wb") as f:
            f.write(data)
        
        # Clear the list for next use
        image_chunks.clear()    
        print(f"Image saved under the name {imageName}")
        run_face_recognition("test-face", imagePath)
            
    def ReadValue(self, options):
        value = []
        json_string = json.dumps(dbcontroller.get_body_metrics())
        
        for c in json_string:                                                                                 
            value.append(dbus.Byte(c.encode())) 
            
        return value
    
class FaceRecognitionDescriptor(Descriptor):
    FACE_RECOGNITION_DESCRIPTOR_UUID = "2901"
    FACE_RECOGNITION_DESCRIPTOR_VALUE = "Fake data"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.FACE_RECOGNITION_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.FACE_RECOGNITION_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value


app = Application()

app.add_service(WeightService(0))
app.add_service(FaceRecognitionService(1))
app.register()

adv = WeightScaleAdvertisement(0)
adv.register()


try:
    app.run()
    
except KeyboardInterrupt:
    app.quit()
