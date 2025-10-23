import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Colors
BLACK = (0, 0, 0)

# Create a fullscreen display
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Joystick Color Boxes")

# Joystick initialization
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
if not joysticks:
    print("No joystick detected!")
    pygame.quit()
    exit()

print(f"Detected {len(joysticks)} joystick(s).")

# --- Main loop ---
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
        elif event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYHATMOTION:
            # Draw a random color box at a random location
            box_width = random.randint(50, 150)
            box_height = random.randint(50, 150)
            box_x = random.randint(0, screen_width - box_width)
            box_y = random.randint(0, screen_height - box_height)
            random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pygame.draw.rect(screen, random_color, (box_x, box_y, box_width, box_height))

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
