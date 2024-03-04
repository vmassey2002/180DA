import tkinter as tk

class RPSGUI:
    def __init__(self, player_name, mqtt_client, mqtt_topic):
        self.player_name = player_name
        self.mqtt_client = mqtt_client
        self.mqtt_topic = mqtt_topic
        self.result_received = False  # Flag to indicate when the result is received

        self.root = tk.Tk()
        self.root.title(f"Rock Paper Scissors - {player_name}")

        self.heading_label = tk.Label(self.root, text=f"Player {player_name[-1]}'s GUI")
        self.heading_label.pack()

        self.label = tk.Label(self.root, text="Enter your move (r for rock, p for paper, s for scissors):")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.button = tk.Button(self.root, text="Submit Move", command=self.submit_move)
        self.button.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.subscribe(self.mqtt_topic + "/result", qos=1)

    def submit_move(self):
        move = self.entry.get()
        if move.lower() == "q":
            self.root.destroy()  # Close the GUI if 'q' is entered
        else:
            self.result_label.config(text=f"Move '{move}' sent to referee.")
            self.mqtt_client.publish(self.mqtt_topic, move, qos=1)

    def on_message(self, client, userdata, message):
        result = str(message.payload, 'utf-8')
        if result == 'win':
            self.result_label.config(text=f"Player 1 Wins!")
        elif result == 'lose':
            self.result_label.config(text=f"Player 2 Wins!")
        elif result == 'draw':
            self.result_label.config(text="It's a draw!")
        self.result_received = True  # Set the flag to indicate that the result is received

    def start(self):
        self.root.mainloop()