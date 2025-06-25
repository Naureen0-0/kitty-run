import pygame
import math

pygame.init()

# Set screen size to 700x750
WIDTH = 700
HEIGHT = 750
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)

player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f"assets/player_images/{i}.png"), (45, 45)))

# Set the grid size and spacing
GRID_WIDTH = WIDTH // 30  # Width of each grid cell
GRID_HEIGHT = (HEIGHT - 50) // 32  # Height of each grid cell (accounting for margin at bottom)

# Set the starting position of the player at the center of the grid, but move it further down
start_x = 15  # Starting column (near the center)
start_y = 18  # Starting row (moved down further)

# Calculate the player's pixel position based on grid position
player_x = start_x * GRID_WIDTH + (GRID_WIDTH // 2) - 22  # Centered in the grid cell
player_y = start_y * GRID_HEIGHT + (GRID_HEIGHT // 2) - 22  # Centered in the grid cell

direction = 0  # Default direction (0 = right)
counter = 0
flicker = False
player_speed = 2
score = 0

# Example of a simple grid level (walls are represented by 1)
# You can adjust or replace this with your actual level design
level = [[1 if (i == 0 or i == 31 or j == 0 or j == 29) else 0 for j in range(30)] for i in range(32)]  # A grid with walls

def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, HEIGHT - 30))  # Adjusted to fit the new screen height

def draw_board():
    # Render the grid and walls
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                # Draw walls as blue squares
                pygame.draw.rect(screen, 'blue', (j * GRID_WIDTH, i * GRID_HEIGHT, GRID_WIDTH, GRID_HEIGHT))
            elif level[i][j] == 0:
                # Draw empty spaces as black
                pygame.draw.rect(screen, 'black', (j * GRID_WIDTH, i * GRID_HEIGHT, GRID_WIDTH, GRID_HEIGHT))

def draw_players():
    global counter
    # Player images (rotate depending on direction)
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def move_player():
    global player_x, player_y
    if direction == 0:  # Move right
        player_x += player_speed
    elif direction == 1:  # Move left
        player_x -= player_speed
    elif direction == 2:  # Move up
        player_y -= player_speed
    elif direction == 3:  # Move down
        player_y += player_speed

run = True
while run:
    timer.tick(fps)

    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    screen.fill('black')  # Fill the screen with black before drawing everything else
    draw_board()  # Draw the board/grid
    draw_players()  # Draw the player
    draw_misc()  # Draw the score

    move_player()  # Move the player based on input

    # Handle player input for direction changes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 0  # Move right
            if event.key == pygame.K_LEFT:
                direction = 1  # Move left
            if event.key == pygame.K_UP:
                direction = 2  # Move up
           
