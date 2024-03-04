import paho.mqtt.client as mqtt
import random
end_condition = False
class RockPaperScissorsGame:
    def __init__(self):
        self.user_choices = {'r': 'rock', 'p': 'paper', 's': 'scissors'}
        self.results = {'win': 0, 'lose': 0, 'draw': 0}
        self.player_moves = {'player1': None, 'player2': None}
        self.game_state = 'waiting'
        self.game_end = False
    def determine_winner(self, user_choice, bot_choice):
        if user_choice == bot_choice:
            return 'draw'
        elif (user_choice == 'r' and bot_choice == 's') or \
             (user_choice == 'p' and bot_choice == 'r') or \
             (user_choice == 's' and bot_choice == 'p'):
            return 'win'
        else:
            return 'lose'

    def play_game(self):
        if self.game_state == 'completed':
            return  # Ignore if the game is already completed

        if self.player_moves['player1'] is not None and self.player_moves['player2'] is not None:
            result = self.determine_winner(self.player_moves['player1'], self.player_moves['player2'])
            self.results[result] += 1
            self.print_results()

            # Notify both players of the result
            client.publish("rps/player1/result", result, qos=1)
            client.publish("rps/player2/result", result, qos=1)

            # Reset moves and set the state to 'waiting'
            self.player_moves = {'player1': None, 'player2': None}
            self.game_state = 'waiting'

    def print_results(self):
        print("----- Results -----")
        print(f"Player1 Wins: {self.results['win']}")
        print(f"Player2 Wins: {self.results['lose']}")
        print(f"Draws: {self.results['draw']}")
        print("-------------------")

game = RockPaperScissorsGame()

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("rps/player1", qos=1)
    client.subscribe("rps/player2", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    player_choice = str(message.payload, 'utf-8')
    print(f"Received move '{player_choice}' from {message.topic}")
    if (player_choice == "q"): 
        global end_condition 
        end_condition= True
        print (str(message.topic)[4:] ,"ended the game")

    if message.topic == "rps/player1":
        game.player_moves['player1'] = player_choice
    elif message.topic == "rps/player2":
        game.player_moves['player2'] = player_choice
        
    game.play_game()

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

while (not end_condition):
    
    pass  # Continue running the loop to listen for messages

