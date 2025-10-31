import os

import pygame
import random
import numpy as np

from moviepy import VideoFileClip
from moviepy.config import check

# constants
MUSIC_END_EVENT = pygame.USEREVENT + 1
DONE = -1

# real_questions and random questions are both arrays  that contains hashmaps with the following elements:
# image -> path to image we show that asks the question
# right -> answer representing the right side of the screen
# left -> answer representing the left side of the screen
# sound_right -> path to a wav file that we plan if the user answers with the right button
# sound_left -> path to a wav file that we plan if the user answers with the left button
# right_next -> index into the next real question to ask if they answered right
# left_next -> index into the next real question to ask if they answered left
real_questions = []
random_questions = []

# this records the answers that were given to the real questions
# the key to the array will match the key to the real_questions array and the value will be the answer they chose
answer_map = []



real_questions.append({"image": "images/pikachu.jpg", "right": "pokemon", "left": "kpop", "sound_right": "sounds/sound1.mp3", "sound_left": "sounds/sound2.mp3", "right_next": 1, "left_next": 1})
real_questions.append({"image": "images/gengar.jpg", "right": "chocolate", "left": "chewy", "sound_right": "sounds/sound3.mp3", "sound_left": "sounds/sound4.mp3", "right_next": 3, "left_next": 2})
real_questions.append({"image": "images/pikachu.jpg", "right": "fruit", "left": "sour", "sound_right": "sounds/sound5.mp3", "sound_left": "sounds/sound6.mp3", "right_next": DONE, "left_next": DONE})
real_questions.append({"image": "images/gengar.jpg", "right": "peanut", "left": "no-nuts", "sound_right": "sounds/sound7.mp3", "sound_left": "sounds/sound8.mp3", "right_next": DONE, "left_next": DONE})


def game_loop():
    # this records the answers that were given to the real questions
    # the key to the array will match the key to the real_questions array and the value will be the answer they chose
    answer_map = []
    question_index = 0

    while question_index != DONE:
        question = real_questions[question_index]
        screen.fill(BLACK)
        showImage(question["image"])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                    break;
                elif event.key == pygame.K_LEFT:
                    answer_map.append(question["left"])
                    playSound(question["sound_left"])
                    question_index = question["left_next"]
                elif event.key == pygame.K_RIGHT:
                    answer_map.append(question["right"])
                    playSound(question["sound_right"])
                    question_index = question["right_next"]

            if question_index != DONE:
                break


    print(f"Answer map: {answer_map}")
    return True


def soundEnded():
    screen.fill(BLACK)

def playSound(file_name):
    # effect = pygame.mixer.music.load(file_name)
    # pygame.mixer.music.play(0)
    pygame.mixer.Sound(file_name).play()

def showImage(file_name):
    original_image = pygame.image.load(file_name).convert()

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

screen = pygame.display.set_mode((800, 600))  # Use a standard window size of 800x600
# Create a fullscreen display
#screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Joystick Color Boxes")

# Joystick initialization
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
if not joysticks:
    print("No joystick detected!")
    # pygame.quit()
    # exit()

print(f"Detected {len(joysticks)} joystick(s).")

# --- Main loop ---
running = True
while running:
    running = game_loop()

# while running:
#     # Event handling
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_q:
#                 running = False
#         elif event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYHATMOTION:
#             playSound(event.button)
#         elif event.type == MUSIC_END_EVENT:
#             soundEnded()
#
#     # Update the display
#     pygame.display.flip()

# Quit pygame
pygame.quit()