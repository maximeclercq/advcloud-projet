# -------------------------------------------------------------------------
# Author : Thibault GARROT
# 
# --------------------------------------------------------------------------
import os
import asyncio
import random
import logging
import json

import socket
import os.path

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device import Message, MethodResponse
from datetime import timedelta, datetime

logging.basicConfig(level=logging.ERROR)

# The device "Thermostat" that is getting implemented using the above interfaces.
# This id can change according to the company the user is from
# and the name user wants to call this Plug and Play device

model_id = "ImageDetector" #TODO : Replace it by a name device parameter

#####################################################
# TELEMETRY TASKS


async def send_telemetry_from_device(device_client, telemetry_msg):
    msg = Message(json.dumps(telemetry_msg))
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    print("Sent message")
    await device_client.send_message(msg)


# END TELEMETRY TASKS
#####################################################

#####################################################
# An # END KEYBOARD INPUT LISTENER to quit application


def stdin_listener():
    """
    Listener for quitting the sample
    """
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break


# END KEYBOARD INPUT LISTENER
#####################################################


#####################################################
# PROVISION DEVICE
async def provision_device(provisioning_host, id_scope, registration_id, symmetric_key, model_id):
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=registration_id,
        id_scope=id_scope,
        symmetric_key=symmetric_key,
    )
    provisioning_device_client.provisioning_payload = {"modelId": model_id}
    return await provisioning_device_client.register()


#####################################################
# MAIN STARTS
async def main():
    switch = os.getenv("IOTHUB_DEVICE_SECURITY_TYPE")
    # Not useful now
    if switch == "DPS":
        provisioning_host = (
            os.getenv("IOTHUB_DEVICE_DPS_ENDPOINT")
            if os.getenv("IOTHUB_DEVICE_DPS_ENDPOINT")
            else "global.azure-devices-provisioning.net"
        )
        id_scope = os.getenv("IOTHUB_DEVICE_DPS_ID_SCOPE")
        registration_id = os.getenv("IOTHUB_DEVICE_DPS_DEVICE_ID")
        symmetric_key = os.getenv("IOTHUB_DEVICE_DPS_DEVICE_KEY")

        registration_result = await provision_device(
            provisioning_host, id_scope, registration_id, symmetric_key, model_id
        )

        if registration_result.status == "assigned":
            print("Device was assigned")
            print(registration_result.registration_state.assigned_hub)
            print(registration_result.registration_state.device_id)

            device_client = IoTHubDeviceClient.create_from_symmetric_key(
                symmetric_key=symmetric_key,
                hostname=registration_result.registration_state.assigned_hub,
                device_id=registration_result.registration_state.device_id,
                product_info=model_id,
            )
        else:
            raise RuntimeError(
                "Could not provision device. Aborting Plug and Play device connection."
            )

    elif switch == "connectionString":
        conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING") #TODO for nuvla intregation: Replace it by nuvla env variable
        print("Connecting using Connection String " + conn_str)
        device_client = IoTHubDeviceClient.create_from_connection_string(
            conn_str, product_info=model_id
        )
    else:
        raise RuntimeError(
            "At least one choice needs to be made for complete functioning of this sample."
        )

    # Connect the client.
    await device_client.connect()

    ################################################
    # Send telemetry (current data)

    # TODO : Replace this function by a listener function which retrieve and send data from the IoT device

    async def send_telemetry(): 
        print("Waiting to send data to the hub")

        if os.path.exists("/tmp/docker_socket.s"):
            os.remove("/tmp/docker_socket.s")

        print("Opening socket...")
        server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        server.bind("/tmp/docker_socket.s")

        print("Listening...")
        while True:
            data = server.recv(1024)
            # data  = struct.unpack("s", data)
            data = data.decode('utf-8')
            if not data:
                break
            else:
                print("-" * 20)
                print(data)
                await send_telemetry_from_device(device_client, data)
        print("-" * 20)
        print("Shutting down...")
        server.close()
        os.remove("/tmp/docker_socket.s")
        print("Done")

    send_telemetry_task = asyncio.create_task(send_telemetry())

    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)
    # # Wait for user to indicate they are done listening for method calls
    await user_finished

    send_telemetry_task.cancel()

    # Finally, shut down the client
    await device_client.shutdown()


#####################################################
# EXECUTE MAIN

if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
