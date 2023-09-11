import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 2
ENEMY_FREQ = 0.02
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Shooter")

# Load images
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")

# Load background image
background_img = pygame.image.load("background.jpg")

# Set up initial player position
player_x = WIDTH // 2
player_y = HEIGHT - 100

# Lists to hold bullets and enemies
bullets = []
enemies = []

# Lists to hold bullets and enemies to remove
bullets_to_remove = []
enemies_to_remove = []

# Set up the clock
clock = pygame.time.Clock()


# Function to draw the player
def draw_player(x, y):
    screen.blit(player_img, (x, y))


# Function to draw an enemy
def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))


# Function to draw a bullet
def draw_bullet(x, y):
    screen.blit(bullet_img, (x, y))


# Function to calculate distance between two points
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# Main game loop
running = True
game_over = False  # Initialize game over flag

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle game over state
    if not game_over:
        # Move the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player_x += PLAYER_SPEED

        # Shoot bullets
        if keys[pygame.K_SPACE]:
            bullet_x = player_x + player_img.get_width() // 2 - bullet_img.get_width() // 2
            bullet_y = player_y
            bullets.append([bullet_x, bullet_y])

        # Spawn enemies
        if random.random() < ENEMY_FREQ:
            enemy_x = random.randint(0, WIDTH - enemy_img.get_width())
            enemy_y = 0
            enemies.append([enemy_x, enemy_y])

        # Move bullets
        bullets = [[x, y - BULLET_SPEED] for x, y in bullets]

        # Move enemies
        enemies = [[x, y + ENEMY_SPEED] for x, y in enemies]

        # Check for collisions and mark bullets and enemies for removal
        bullets_to_remove = []
        enemies_to_remove = []
        for bullet in bullets:
            for enemy in enemies:
                if pygame.Rect(enemy[0], enemy[1], enemy_img.get_width(), enemy_img.get_height()).colliderect(
                        pygame.Rect(bullet[0], bullet[1], bullet_img.get_width(), bullet_img.get_height())):
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)

        # Check for collisions between player and enemies with distance condition
        for enemy in enemies:
            if distance(player_x, player_y, enemy[0], enemy[1]) < 30:  # Adjust the distance threshold as needed
                # Handle player-enemy collision by setting game_over to True
                game_over = True

        # Remove collided bullets and enemies
        for bullet in bullets_to_remove:
            if bullet in bullets:
                bullets.remove(bullet)
        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)

        # Clear the lists of bullets and enemies to remove
        bullets_to_remove.clear()
        enemies_to_remove.clear()

        # Remove off-screen bullets and enemies
        bullets = [bullet for bullet in bullets if bullet[1] > 0]
        enemies = [enemy for enemy in enemies if enemy[1] < HEIGHT]

    # Draw the background image
    screen.blit(background_img, (0, 0))

    # Draw everything
    draw_player(player_x, player_y)
    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1])
    for enemy in enemies:
        draw_enemy(enemy[0], enemy[1])

    # Display "Game Over" if in game over state
    if game_over:
        game_over_font = pygame.font.Font(None, 36)
        game_over_text = game_over_font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame (optional)
pygame.quit()
