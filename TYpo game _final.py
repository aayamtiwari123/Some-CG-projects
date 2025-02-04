import pygame
import nltk
from nltk.corpus import words
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Typo Game')

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

nltk.download('words')

# Load word list
word_list = words.words()

# Font setup
font = pygame.font.SysFont("Arial", 32)

# Game variables
random_word = random.choice(word_list)
x = random.randint(50, WIDTH - 150)
y = 0

score = 0
input_text = ""
fall_speed = 1  # Initial fall speed
frame_rate = 30  # Initial FPS
game_over = False  # Track game state
paused = False  # Pause state
level = None  # None until player selects a level

def draw_level_selection():
    """Displays level selection screen."""
    screen.fill(WHITE)
    title_text = font.render("Select Level:", True, BLACK)
    easy_text = font.render("Press 1 for EASY", True, GREEN)
    hard_text = font.render("Press 2 for HARD", True, RED)
    
    screen.blit(title_text, (WIDTH // 2 - 80, HEIGHT // 3))
    screen.blit(easy_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(hard_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
    
    pygame.display.flip()

def fall_word():
    """Moves the falling word down."""
    global y, game_over
    screen.fill(WHITE)

    if not game_over and not paused:
        y += fall_speed  # Move word down
        text = font.render(random_word, True, BLUE)
        screen.blit(text, (x, y))

        # If word reaches bottom, end game
        if y > HEIGHT - 50:
            game_over = True

def display_input():
    """Displays the user input on screen."""
    input_surface = font.render(f"Input: {input_text}", True, BLACK)
    screen.blit(input_surface, (10, HEIGHT - 40))

def display_game_over():
    """Displays the game over screen."""
    game_over_text = font.render(f"Game Over! Score: {score}", True, RED)
    restart_text = font.render("Press R to Restart", True, BLACK)
    
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 40))

def display_pause():
    """Displays the pause screen."""
    pause_text = font.render("Game Paused. Press ESC to Resume", True, BLACK)
    screen.blit(pause_text, (WIDTH // 2 - 150, HEIGHT // 2))

def check_input():
    """Checks if the input matches the falling word."""
    global input_text, random_word, x, y, score, fall_speed, frame_rate
    if input_text.lower() == random_word.lower():
        score += 1  # Increase score by 1
        y = 0
        random_word = random.choice(word_list)
        x = random.randint(50, WIDTH - 150)
        input_text = ""  # Reset input

        # Increase difficulty based on level
        if level == "easy":
            frame_rate = min(300, frame_rate + 5)  # Easy mode: +5 FPS
        elif level == "hard":
            frame_rate = min(300, frame_rate + 10)  # Hard mode: +10 FPS

# Game loop
running = True
clock = pygame.time.Clock()

# Level selection
while level is None:
    draw_level_selection()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            level = "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                level = "easy"
            elif event.key == pygame.K_2:
                level = "hard"

# Main game loop
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not paused:
                check_input()
            elif event.key == pygame.K_BACKSPACE and not paused:
                input_text = input_text[:-1]
            elif event.key == pygame.K_ESCAPE:  # Toggle pause with ESC
                paused = not paused
            elif not paused:
                input_text += event.unicode

        # Restart game if game over
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            # Reset game variables
            game_over = False
            score = 0
            fall_speed = 1
            frame_rate = 30
            y = 0
            random_word = random.choice(word_list)
            x = random.randint(50, WIDTH - 150)
            input_text = ""

    if paused:
        display_pause()
    elif not game_over:
        fall_word()
        display_input()

        # Display score
        score_surface = font.render(f"Score: {score}", True, GREEN)
        screen.blit(score_surface, (WIDTH - 150, 10))
    else:
        display_game_over()

    pygame.display.flip()
    clock.tick(frame_rate)  # Dynamic FPS
