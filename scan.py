import asyncio
from bleak import BleakScanner, BleakClient

SCALE_NAME = "MI SCALE2"
WEIGHT_MEASUREMENT_UUID = "00002a9d-0000-1000-8000-00805f9b34fb"

async def find_scale():
    return await BleakScanner.find_device_by_name(SCALE_NAME)
            
            
def notification_handler(sender, data):
    weight = int.from_bytes(data[1:3], byteorder="little") / 200
    print(f"Weight: {weight} kg")


async def get_weight_data():
    scan_task = asyncio.create_task(find_scale())
    scale2 = await scan_task
    
    async with BleakClient(scale2.address) as client:
        print("Connected to the Xiaomi Smart Scale 2")
        
        try:
            await client.start_notify(WEIGHT_MEASUREMENT_UUID, notification_handler)
            # Keep the connection open for a while to receive data
            await asyncio.sleep(20)

            await client.stop_notify(WEIGHT_MEASUREMENT_UUID)
            print("Stopped notifications")
            
        except Exception as e:
            print(f"Failed to read weight data: {e}")
    


if __name__ == "__main__":
    asyncio.run(get_weight_data())