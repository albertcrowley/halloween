import os

import pygame
import random
import numpy as np

from moviepy import VideoFileClip
from moviepy.config import check

video_map = {}
video_map[1] = os.path.join("videos", "pikachu.mp4");

def playVideo(button):

    check()

    video_path = video_map[button]
    print(f"Playing video: {video_path}")
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return

    clip = VideoFileClip(video_path)
    clip.preview()

    while clip.is_playing:
        print ("ticking")
        pygame.time.Clock().tick(60)



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
            playVideo(1)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
