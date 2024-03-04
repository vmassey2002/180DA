import paho.mqtt.client as mqtt
from rps_gui import RPSGUI

result_received = False  # Flag to indicate when the result is received

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("rps/player1/result", qos=1)
    # Additional subscription for the other player's move
    client.subscribe("rps/player2/result", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    global result_received
    result = str(message.payload, 'utf-8')
    if result == 'win':
        gui.result_label.config(text="You won!")
    elif result == 'lose':
        gui.result_label.config(text="You lose!")
    elif result == 'draw':
        gui.result_label.config(text="It's a draw!")
    result_received = True  # Set the flag to indicate that the result is received

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

player_name = "player1"
topic = f"rps/{player_name}"

gui = RPSGUI(player_name, client, topic)
while True:
    gui.start()
    # Wait for the other player to make a move
    result_received = False  # Reset the flag
    while not result_received:
        client.loop()  # Process incoming messages



        