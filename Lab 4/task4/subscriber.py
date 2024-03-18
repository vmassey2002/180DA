import paho.mqtt.client as mqtt
import json
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180da-warmup/venicia/lab4/imu", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, msg):
    #load json file into dictionary
    try:
        imu_data = json.loads(msg.payload.decode())

        data = {
            'ACC_X': imu_data['ACC_X'],
            'ACC_Y': imu_data['ACC_Y'],
            'ACC_Z': imu_data['ACC_Z'],
            'GYR_X': imu_data['GYR_X'],
            'GYR_Y': imu_data['GYR_Y'],
            'GYR_Z': imu_data['GYR_Z']
        }
        formatted_data = {key: round(value, 3) for key, value in data.items()}
        print('IMU DATA', formatted_data)
    except Exception as e:
        print('error parsing mqtt values:', e)

def process_message():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect_async('mqtt.eclipseprojects.io')

    client.loop_start()
    try:
        while True:
            pass  # Perform other non-blocked tasks here
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    process_message()