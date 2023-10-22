import pygame
import random
import sys
import asyncio

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 1000, 800
ICEBERG_WIDTH, ICEBERG_HEIGHT = 280, 160
ICEBERG_X, ICEBERG_Y = 200, 630
ICEBERG_SPEED = 7
ICEBERG_MELT_RATE = 0.06
OBSTACLE_SPEED = 4
OBSTACLE_GAP = 200
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 100, 100  # smaller obstacles
OBSTACLE_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
ITEM_SPEED = 4
ITEM_WIDTH, ITEM_HEIGHT = 30, 30
FONT = pygame.font.Font(None, 36)
polar_bear_width, polar_bear_height = 130, 100
obstacle_spawn_chance = 0.2
POLAR_BEAR_DISPLACEMENT = 0.02

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Iceberg Runner")

# Load images and scale the background
polar_bear = pygame.image.load("polar_bear.png").convert_alpha()
iceberg_image = pygame.image.load("iceberg.png").convert_alpha()
obstacle_image = pygame.image.load("plastic.png").convert_alpha()
new_obstacle_image = pygame.image.load("new_obstacle.png").convert_alpha()  # Load the new obstacle image
powerup_indicator = pygame.image.load("powerup.png").convert_alpha()
background_image1 = pygame.image.load("bg.jpg").convert()
background_image2 = pygame.image.load("bg.jpg").convert()
background_image1 = pygame.transform.scale(background_image1, (WIDTH, HEIGHT))
background_image2 = pygame.transform.scale(background_image2, (WIDTH, HEIGHT))
polar_bear = pygame.transform.scale(polar_bear, (polar_bear_width, polar_bear_height))

# Create the iceberg and initialize variables
iceberg = pygame.Rect(ICEBERG_X, ICEBERG_Y, ICEBERG_WIDTH, ICEBERG_HEIGHT)
iceberg_health = 100
obstacles = []
items = []
score = 0
clock = pygame.time.Clock()

# Create a list of obstacle images
obstacle_images = [obstacle_image, new_obstacle_image]  # Include the new obstacle image

# Function to generate obstacles with random rotation angles
def generate_obstacle():
    x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
    y = -OBSTACLE_HEIGHT  # Use the OBSTACLE_HEIGHT variable
    rotation_angle = random.randint(-45, 45)  # Random rotation angle between -45 and 45 degrees
    selected_image = random.choice(obstacle_images)  # Randomly select an image from the list
    return pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT), rotation_angle, selected_image


# Function to display text on the screen
def draw_text(text, x, y):
    text_surface = FONT.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

# Function to display game over screen
def game_over():
    screen.fill(BLACK)
    draw_text("Game Over - the polar bear's iceberg melted too fast!", 150, 400)
    draw_text(f"Score: {score}", WIDTH // 2 - 50, HEIGHT // 2 + 20)
    pygame.display.update()

# Function to initialize the game variables
def init_game():
    global ICEBERG_WIDTH, ICEBERG_HEIGHT, ICEBERG_X, ICEBERG_Y, ICEBERG_SPEED, ICEBERG_MELT_RATE
    global OBSTACLE_SPEED, OBSTACLE_GAP, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, ITEM_SPEED, ITEM_WIDTH, ITEM_HEIGHT
    global iceberg, iceberg_health, obstacles, obstacle_rotation_angles, items, score, polar_bear_x, polar_bear_y, polar_bear_xm, polar_bear_xy
    global powerup_used, powerup_start_time, background_y, running

    ICEBERG_WIDTH, ICEBERG_HEIGHT = 280, 160
    ICEBERG_X, ICEBERG_Y = 200, 630
    ICEBERG_SPEED = 7
    ICEBERG_MELT_RATE = 0.06
    OBSTACLE_SPEED = 4
    OBSTACLE_GAP = 200
    OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 100, 100  # smaller obstacles
    ITEM_SPEED = 4
    ITEM_WIDTH, ITEM_HEIGHT = 30, 30

    iceberg = pygame.Rect(ICEBERG_X, ICEBERG_Y, ICEBERG_WIDTH, ICEBERG_HEIGHT)
    iceberg_health = 100
    obstacles = []
    obstacle_rotation_angles = random.randint(-90, 90)
    items = []
    score = 0

    # Reset the polar bear's position
    polar_bear_x = iceberg.x + (ICEBERG_WIDTH // 4)  # Adjust the position based on the new iceberg size
    polar_bear_y = iceberg.y - (ICEBERG_HEIGHT // 4)  # Adjust the position based on the new iceberg size

    powerup_used = False
    powerup_start_time = 0
    background_y = 0

init_game()
polar_bear_x = iceberg.x + 50
polar_bear_y = iceberg.y - 20
polar_bear_xm = iceberg.x + 100
polar_bear_xy = iceberg.y
powerup_used = False
powerup_start_time = 0
background_y = 0
running = True
playing = True
collide_ability = True



# Main game loop
async def main():
    global OBSTACLE_WIDTH, OBSTACLE_HEIGHT  # Include OBSTACLE_WIDTH and OBSTACLE_HEIGHT here
    global ICEBERG_WIDTH, ICEBERG_HEIGHT, ICEBERG_X, ICEBERG_Y, ICEBERG_SPEED, ICEBERG_MELT_RATE
    global OBSTACLE_SPEED, OBSTACLE_GAP, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, ITEM_SPEED, ITEM_WIDTH, ITEM_HEIGHT
    global iceberg, iceberg_health, obstacles, items, score, polar_bear_x, polar_bear_y, polar_bear_xm, polar_bear_xy
    global powerup_used, powerup_start_time, background_y, running
    global running, playing, iceberg_image, collide_ability
    global collide_ability
    collide_ability = True
    global collide_ab_check
    collide_ab_check = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if random.randint(0, 100) < obstacle_spawn_chance:
            obstacles.append(generate_obstacle())
            obstacles.append(generate_obstacle()) # add another obstacle
 
        for obstacle, rotation_angle, obstacle_image in obstacles:
            if iceberg.colliderect(obstacle) and playing and collide_ability:
                iceberg_health -= 5
            if iceberg.colliderect(obstacle) and playing:
                obstacles.remove((obstacle, rotation_angle, obstacle_image))

        OBSTACLE_WIDTH = max(OBSTACLE_WIDTH, 10)  # Ensure that OBSTACLE_WIDTH doesn't become negative
        OBSTACLE_HEIGHT = max(OBSTACLE_HEIGHT, 10)  # Ensure that OBSTACLE_HEIGHT doesn't become negative
        if collide_ability:
            iceberg_health -= ICEBERG_MELT_RATE
            ICEBERG_WIDTH -= ICEBERG_MELT_RATE
            ICEBERG_HEIGHT -= ICEBERG_MELT_RATE
            polar_bear_xm += POLAR_BEAR_DISPLACEMENT
            polar_bear_xy += POLAR_BEAR_DISPLACEMENT

        if playing:
            score += 1

        iceberg_image = pygame.transform.scale(iceberg_image, (ICEBERG_WIDTH, ICEBERG_HEIGHT))

        obstacles = [(obstacle.move(0, OBSTACLE_SPEED), rotation_angle, obstacle_image) for obstacle, rotation_angle, obstacle_image in obstacles]
        obstacles = [(obstacle, rotation_angle, obstacle_image) for obstacle, rotation_angle, obstacle_image in obstacles if obstacle.top < HEIGHT]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            iceberg.x -= ICEBERG_SPEED
            polar_bear_xm -= ICEBERG_SPEED
            rotation_angle = 15
        elif keys[pygame.K_RIGHT]:
            iceberg.x += ICEBERG_SPEED
            polar_bear_xm += ICEBERG_SPEED
            rotation_angle = -15
        elif keys[pygame.K_h] and not powerup_used:
            iceberg_health = 100
            powerup_used = True
            ICEBERG_WIDTH = 280
            ICEBERG_HEIGHT = 160
            iceberg_image = pygame.transform.scale(iceberg_image, (ICEBERG_WIDTH, ICEBERG_HEIGHT))
            powerup_start_time = pygame.time.get_ticks()
        elif keys[pygame.K_i]:
            collide_ability = False
            global immunity_powerup_used
            immunity_powerup_used = True
        else:
            rotation_angle = 0

        if collide_ability == False:
            collide_ab_check += 1

        if collide_ab_check > 400:
            collide_ability = True

        polar_bear_x = iceberg.x + 50
        polar_bear_y = iceberg.y - 20

        rotated_iceberg = pygame.transform.rotate(iceberg_image, -rotation_angle)
        rotated_rect = rotated_iceberg.get_rect(center=iceberg.center)

        rotated_polar_bear = pygame.transform.rotate(polar_bear, rotation_angle)
        rotated_polar_bear_rect = rotated_polar_bear.get_rect(center=(polar_bear_xm, polar_bear_xy))
        mirrored_polar_bear = pygame.transform.flip(rotated_polar_bear, True, False)
        mirrored_polar_bear_rect = mirrored_polar_bear.get_rect(center=(polar_bear_xm, polar_bear_xy))

        # Move the background downwards
        background_y += OBSTACLE_SPEED
        if background_y > HEIGHT:
            background_y -= HEIGHT

        # Adjust the position of the second background image
        background_rect1 = background_image1.get_rect(topleft=(0, background_y))
        background_rect2 = background_image2.get_rect(topleft=(0, background_y - HEIGHT))
        screen.blit(background_image1, background_rect1)
        screen.blit(background_image2, background_rect2)

        screen.blit(rotated_iceberg, rotated_rect)
        screen.blit(mirrored_polar_bear, (polar_bear_xm - 50, polar_bear_xy + -20))

        if collide_ability == False:
            immunity_image = pygame.image.load("immunity.png").convert_alpha()
            scaled_immunity_image = pygame.transform.scale(immunity_image, (200, 200))
            screen.blit(scaled_immunity_image, (50, 50))

        if powerup_used:
            if pygame.time.get_ticks() - powerup_start_time < 5000:
                scaled_powerup = pygame.transform.scale(powerup_indicator, (powerup_indicator.get_width() // 3, powerup_indicator.get_height() // 3))
                screen.blit(scaled_powerup, (10, 60))

        # Check if the iceberg is at the edge of the screen
        if iceberg.right <= 0:
            iceberg.right = 400
            # Handle this condition if needed
        elif iceberg.right >= WIDTH:
            iceberg.left = 100

        # Check if the polar bear is at the edge of the screen
        if polar_bear_xm <= 0:
            polar_bear_xm = iceberg.x + 100
            # Handle this condition if needed
        elif polar_bear_xm >= WIDTH - polar_bear_width:
            polar_bear_xm = iceberg.x + 100

        # Scale the obstacle images to a smaller size
        scaled_obstacle_images = [pygame.transform.scale(image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)) for image in obstacle_images]
        for obstacle, rotation_angle, obstacle_image in obstacles:
            screen.blit(pygame.transform.scale(obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)), obstacle.topleft)


        health_bar_width = int(max(0, min(200, iceberg_health * 2)))
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, health_bar_width, 20))
        draw_text(f"Score: {score}", 10, 40)

        if iceberg_health <= 0:
            game_over()
            playing = False

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
pygame.quit()
