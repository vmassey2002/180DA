import random

class RockPaperScissorsGame:
    def __init__(self):
        self.user_choices = {'r': 'rock', 'p': 'paper', 's': 'scissors'}
        self.results = {'win': 0, 'lose': 0, 'draw': 0}

    def get_user_choice(self):
        while True:
            user_input = input("Enter 'r' for rock, 'p' for paper, or 's' for scissors: ").lower()
            if user_input in self.user_choices:
                return user_input
            else:
                print("Invalid input. Please enter 'r', 'p', or 's'.")

    def get_bot_choice(self):
        return random.choice(list(self.user_choices.keys()))

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
        while True:
            user_choice = self.get_user_choice()
            bot_choice = self.get_bot_choice()

            print(f"You chose {self.user_choices[user_choice]}")
            print(f"The bot chose {self.user_choices[bot_choice]}")

            result = self.determine_winner(user_choice, bot_choice)
            print(f"You {result}!\n")

            self.results[result] += 1
            self.print_results()

            play_again = input("Do you want to play again? (y/n): ").lower()
            if play_again != 'y':
                print("Thanks for playing!")
                break

    def print_results(self):
        print("----- Results -----")
        print(f"Wins: {self.results['win']}")
        print(f"Loses: {self.results['lose']}")
        print(f"Draws: {self.results['draw']}")
        print("-------------------")


if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.play_game()
