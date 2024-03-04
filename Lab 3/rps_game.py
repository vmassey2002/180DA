import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Choices
ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissors")
clock = pygame.time.Clock()

# Game loop
def game():
    player_choice = None
    computer_choice = random.choice([ROCK, PAPER, SCISSORS])

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player_choice = ROCK
                elif event.key == pygame.K_p:
                    player_choice = PAPER
                elif event.key == pygame.K_s:
                    player_choice = SCISSORS

        # Display player choice
        font = pygame.font.Font(None, 36)
        text = font.render(f"Player: {player_choice}", True, BLACK)
        screen.blit(text, (100, 300))

        # Display computer choice
        text = font.render(f"Computer: {computer_choice}", True, BLACK)
        screen.blit(text, (500, 300))

        # Determine winner
        winner = None
        if player_choice and computer_choice:
            if player_choice == computer_choice:
                winner = "It's a tie!"
            elif (
                (player_choice == ROCK and computer_choice == SCISSORS)
                or (player_choice == PAPER and computer_choice == ROCK)
                or (player_choice == SCISSORS and computer_choice == PAPER)
            ):
                winner = "You win!"
            else:
                winner = "Computer wins!"

        # Display winner
        text = font.render(winner, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 500))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    game()
