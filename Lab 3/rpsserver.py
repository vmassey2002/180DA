import paho.mqtt.client as mqtt
import random

class RockPaperScissorsGame:
    def __init__(self):
        self.user_choices = {'r': 'rock', 'p': 'paper', 's': 'scissors'}
        self.results = {'win': 0, 'lose': 0, 'draw': 0}

    def determine_winner(self, user_choice, user_choice2):
        if user_choice == user_choice2:
            return 'draw'
        elif (user_choice == 'r' and user_choice2 == 's') or \
             (user_choice == 'p' and user_choice2 == 'r') or \
             (user_choice == 's' and user_choice2 == 'p'):
            return 'win'
        else:
            return 'lose'

    def play_game(self, user_choice):
        user_choice2 = self.get_bot_choice()
        result = self.determine_winner(user_choice, user_choice2)

        self.results[result] += 1
        self.print_results()

        return f"You chose {self.user_choices[user_choice]}\nThe bot chose {self.user_choices[user_choice2]}\nYou {result}!\n"

    def get_bot_choice(self):
        return random.choice(list(self.user_choices.keys()))

    def print_results(self):
        print("----- Results -----")
        print(f"Wins: {self.results['win']}")
        print(f"Loses: {self.results['lose']}")
        print(f"Draws: {self.results['draw']}")
        print("-------------------")

# MQTT callbacks
# MQTT callbacks
counter = 0
user_choice = None
user_choice2 = None

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/game", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    global counter, user_choice, user_choice2

    counter = counter + 1
    if counter == 1:
        user_choice = message.payload.decode('utf-8')
    elif counter == 2:
        user_choice2 = message.payload.decode('utf-8')
        counter = 0

        # Now you have both user choices, you can call play_game
        result = game.determine_winner(user_choice, user_choice2)

        result_message = f"You chose {game.user_choices[user_choice]}\nPlayer 2 chose {game.user_choices[user_choice2]}\nResult: {result}!\n"
        print(result_message)

        client.publish("ece180d/result", result_message, qos=1)

# MQTT setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

# Game setup
game = RockPaperScissorsGame()

while True:
    pass  # Keep the script running to listen for MQTT messages
