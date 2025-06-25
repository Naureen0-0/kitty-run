import pygame
import sys
import subprocess


pygame.init()
pygame.mixer.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  

# Set up screen
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Page")

# Set up fonts
font = pygame.font.Font('freesansbold.ttf', 50) 
button_font = pygame.font.Font('freesansbold.ttf', 20)  

# Button class to handle button creation and drawing
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, surface, hover=False):
        # Draw the button rectangle (change color if hovered)
        button_color = WHITE if hover else BLUE
        pygame.draw.rect(surface, button_color, self.rect, border_radius = 20)

        # Add a glow if hovered
        if hover:
            pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=20) 

        # Draw the button text in the center
        text_surface = button_font.render(self.text, True, BLACK)
        surface.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2, 
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def click(self):
        if self.action:
            self.action()

# Functions for button actions
def start_game():
    print("Starting Kitty-Run game...")
    subprocess.Popen(['python', 'test.py'])
    pygame.quit()
    sys.exit()

def quit_game():
    print("Exiting game...") 
    pygame.quit()
    sys.exit()

def toggle_music():
    global is_music_muted
    if is_music_muted:
        pygame.mixer.music.set_volume(1.0)  # Unmute music
        is_music_muted = False
    else:
        pygame.mixer.music.set_volume(0.0)  # Mute music
        is_music_muted = True

button_width = 300
button_height = 80
# Center the buttons
start_button = Button("Start Game", (WIDTH - button_width) // 2, 200, button_width, button_height, start_game)
quit_button = Button("Quit", (WIDTH - button_width) // 2, 320, button_width, button_height, quit_game)

buttons = [start_button, quit_button]

# Load the mute and unmute icons
mute_icon = pygame.image.load('assets/menu/mute.png')  # Path to mute icon
unmute_icon = pygame.image.load('assets/menu/ummute.png')  # Path to unmute icon

# Resize icons (optional, adjust size as needed)
mute_icon = pygame.transform.scale(mute_icon, (1000, 1000))
unmute_icon = pygame.transform.scale(unmute_icon, (1000, 1000))

# Mute button (just the icon)
mute_button_rect = pygame.Rect((WIDTH - 50) // 2, 20, 50, 50)  # Positioned at the top center

# Global variable to track music mute status
is_music_muted = False

# Play background music
pygame.mixer.music.load("assets\menu\The Game Show Theme Music.mp3")  # Replace with your music file path
pygame.mixer.music.play(-1, 0.0)  # Play music indefinitely (-1 for loop), 0.0 for start at the beginning


# Load the images for the moving characters (now only 3 images)
image_paths = [
    "assets/menu/4.png",  
    "assets/menu/2.png",  
    "assets/menu/3.png",   
    "assets/menu/5.png",
    "assets/menu/1.png",
]

images = [pygame.image.load(path) for path in image_paths]
images = [pygame.transform.scale(image, (60, 60)) for image in images] 


def create_dots():
    dot_radius = 5
    dot_spacing = 20
    dots = []
    for i in range(0, WIDTH, dot_spacing):
        dots.append(pygame.Rect(i - dot_radius, HEIGHT - 50 - dot_radius, 2 * dot_radius, 2 * dot_radius))
    return dots


def check_collision(image_rect, dots, image_index, initial_dots, black_dots):
    if image_index == 1: 
        for dot in dots[:]:
            if image_rect.colliderect(dot):  # If image intersects with a dot
                if dot not in black_dots:
                    black_dots.append(dot)  # Add to the list of black dots
    elif image_index == 0:  # Image 1 (index 0)
        # Re-add dots back from initial_dots if not already black
        for dot in initial_dots:
            if dot not in dots and dot not in black_dots:
                dots.append(dot)  # Re-add the dot to the list (dot reappears)

        # Turn black dots back to white when Image 1 collides
        for dot in black_dots[:]:
            if image_rect.colliderect(dot):  # If Image 1 collides with black dot
                black_dots.remove(dot)  # Remove from black dots list

# Main menu 
def main_menu():
    image_count = len(images) 

    x_positions = [0] * image_count  
    speed = 0.07
    start_time = pygame.time.get_ticks()  

    spacing = 100 

    initial_dots = create_dots()
    dots = initial_dots[:]  
    black_dots = []  

    while True:
        screen.fill(BLACK)

        # Draw title
        title_text = font.render("Kitty-Run", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Draw remaining dots (dots that are not black)
        for dot in dots:
            if dot not in black_dots: 
                pygame.draw.circle(screen, WHITE, dot.center, dot.width // 2)

        # Draw black dots (dots that are turned black after Image 2 collision)
        for dot in black_dots:
            pygame.draw.circle(screen, BLACK, dot.center, dot.width // 2)

        # Draw buttons with hover effect
        for button in buttons:
            # Check if the mouse is over the button
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = button.is_hovered(mouse_pos)
            button.draw(screen, hover=is_hovered)

        # Calculate how much time has passed (in seconds)
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000.0  # Time in seconds

        # Update the positions of the images based on time
        for i in range(image_count):
            if i == 1:  
                gap_between_2_and_3 = 370
                x_positions[i] = (elapsed_time * speed * WIDTH + gap_between_2_and_3) % WIDTH 
            elif i == 2:  
                gap_between_3_and_4 = 60 
                x_positions[i] = (elapsed_time * speed * WIDTH + gap_between_3_and_4) % WIDTH  

            elif i == 3:
                gap_between_4_and_5 = -60
                x_positions[i] = (elapsed_time * speed * WIDTH + gap_between_4_and_5) % WIDTH 
            
            elif i == 4:
                gap_between_5_and_1 = -110
                x_positions[i] = (elapsed_time * speed * WIDTH + gap_between_5_and_1) % WIDTH 

            else:
                x_positions[i] = (elapsed_time * speed * WIDTH) % WIDTH  

        image_rects = [pygame.Rect(x, HEIGHT - 80, images[0].get_width(), images[0].get_height()) for x in x_positions]
        

        # Check if any image overlaps with the dots
        for i, rect in enumerate(image_rects):
            check_collision(rect, dots, i, initial_dots, black_dots)

        # Draw the images 
        for i, x in enumerate(x_positions):
            screen.blit(images[i], (x, HEIGHT - 80))  # Position each image over the dots

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse click
                    for button in buttons:
                        if button.is_hovered(mouse_pos):
                            button.click()

        # Update the display
        pygame.display.update()



# Run the menu
main_menu()
