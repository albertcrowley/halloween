import os

import pygame
import random
import numpy as np

from moviepy import VideoFileClip
from moviepy.config import check

sound_map = {}
sound_map[0] = os.path.join("sounds", "pikachu.wav");
sound_map[1] = os.path.join("sounds", "gengar.wav");

image_map = {}
image_map[0] = os.path.join("images", "pikachu.jpg");
image_map[1] = os.path.join("images", "gengar.jpg");

MUSIC_END_EVENT = pygame.USEREVENT + 1

def soundEnded():
    screen.fill(BLACK)

def playSound(button):
    if button not in sound_map:
        print (f"button {button} not found")
    else:
        print (f"pressed {button}")
        effect = pygame.mixer.music.load(sound_map[button])
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

    if button in image_map:
        original_image = pygame.image.load(image_map[button]).convert()

        # 1. Scale the image to the exact screen size
        scaled_image = pygame.transform.scale(original_image, screen.get_size())

        # 2. Blit the scaled image
        screen.blit(scaled_image, (0, 0))
        pygame.display.flip()


# Initialize pygame
pygame.init()



# Screen dimensions
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Colors
BLACK = (0, 0, 0)

#screen = pygame.display.set_mode((800, 600))  # Use a standard window size of 800x600
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
            playSound(event.button)
        elif event.type == MUSIC_END_EVENT:
            soundEnded()

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()