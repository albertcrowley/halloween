import os
from datetime import datetime

import pygame
import random
import numpy as np

from moviepy import VideoFileClip
from moviepy.config import check

# constants
MUSIC_END_EVENT = pygame.USEREVENT + 1
DONE = -1
ANSWER_FILE = "answers.txt"
LOG_FILE = "log.txt"
QUESTION_DELAY = 500
END_DELAY = 1000
SCREEN_SIZE = (1920, 1080)

global is_fullscreen


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



real_questions.append({"image": "images/pokemon-kpop.png", "left": "pokemon", "right": "kpop",  "sound_right": "sounds/sound1.mp3", "sound_left": "sounds/sound2.mp3", "right_next": 1, "left_next": 1, "end_image_left": "images/pokemon-end.png", "end_image_right": "images/kpop-end.png"})
real_questions.append({"image": "images/chocolate-chewy.png", "left": "chocolate", "right": "chewy", "sound_right": "sounds/sound3.mp3", "sound_left": "sounds/sound4.mp3", "left_next": 3, "right_next": 2})
real_questions.append({"image": "images/fruit-sour.png", "left": "fruit", "right": "sour", "sound_right": "sounds/sound5.mp3", "sound_left": "sounds/sound6.mp3", "right_next": DONE, "left_next": DONE})
real_questions.append({"image": "images/nuts.png", "left": "peanut", "right": "no-nuts", "sound_right": "sounds/sound7.mp3", "sound_left": "sounds/sound8.mp3", "right_next": DONE, "left_next": DONE})

random_questions.append({"image": "images/random1.png", "right": "rand-right", "left": "rand-left", "sound_right": "sounds/sound1.mp3", "sound_left": "sounds/sound2.mp3", "right_next": 1, "left_next": 1})
random_questions.append({"image": "images/random2.png", "right": "rand-right", "left": "rand-left", "sound_right": "sounds/sound1.mp3", "sound_left": "sounds/sound2.mp3", "right_next": 1, "left_next": 1})
random_questions.append({"image": "images/random3.png", "right": "rand-right", "left": "rand-left", "sound_right": "sounds/sound1.mp3", "sound_left": "sounds/sound2.mp3", "right_next": 1, "left_next": 1})
random_questions.append({"image": "images/random4.png", "right": "rand-right", "left": "rand-left", "sound_right": "sounds/sound1.mp3", "sound_left": "sounds/sound2.mp3", "right_next": 1, "left_next": 1})
random_questions.append({"image": "images/random5.png", "right": "rand-right", "left": "rand-left", "sound_right": "sounds/sound1.mp3", "sound_left": "sounds/sound2.mp3", "right_next": 1, "left_next": 1})

def game_loop():
    global screen
    global real_questions
    global random_questions
    global used_random_questions
    global is_fullscreen
    used_random_questions = []  # Reset the list of used random questions
    # this records the answers that were given to the real questions
    # the key to the array will match the key to the real_questions array and the value will be the answer they chose
    answer_map = []
    question_index = 0
    end_image = None

    ask_random()

    while question_index != DONE:
        question = real_questions[question_index]
        screen.fill(BLACK)
        showImage(question["image"])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                    break;
                elif event.key == pygame.K_f:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        # Store current window size before going fullscreen
                        windowed_size = screen.get_size()
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        # Return to windowed mode with previous size
                        screen = pygame.display.set_mode(windowed_size, pygame.RESIZABLE)
                    # Redraw the current image at the new size
                    showImage(question["image"])
                elif event.key == pygame.K_LEFT:
                    answer_map.append(question["left"])
                    playSound(question["sound_left"])
                    question_index = question["left_next"]
                    if "end_image_left" in question:
                        end_image = question["end_image_left"]
                    ask_random()
                elif event.key == pygame.K_RIGHT:
                    answer_map.append(question["right"])
                    playSound(question["sound_right"])
                    question_index = question["right_next"]
                    if "end_image_right" in question:
                        end_image = question["end_image_right"]
                    ask_random()
                update_answers(answer_map)
            elif event.type == pygame.VIDEORESIZE:
                # Update the screen size when window is resized
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # Redraw the current image at the new size
                showImage(question["image"])


            if question_index != DONE:
                break

            pygame.time.wait(QUESTION_DELAY)



    print(f"Answer map: {answer_map}")
    log_entry(f"Answer map: {answer_map}")
    show_end_image(end_image)
    return True

def ask_random():
    global real_questions
    global random_questions
    global question_index
    global used_random_questions  # Add this at the start of each game loop

    # If we've used all random questions, reset the used questions list
    if len(used_random_questions) >= len(random_questions):
        used_random_questions.clear()

    # Get available indices that haven't been used yet
    available_indices = [i for i in range(len(random_questions)) if i not in used_random_questions]

    # Select a random index from the available ones
    question_index = random.choice(available_indices)
    used_random_questions.append(question_index)  # Mark this index as used

    question = random_questions[question_index]

    print (f"{available_indices} and this time chose {question_index}")

    screen.fill(BLACK)
    showImage(question["image"])
    pygame.display.flip()
    i = 0
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_q:
                    done = True
                    break
    pygame.time.wait(QUESTION_DELAY)

def log_entry(message):
    """
    Appends a timestamped log entry to the log file.
    Args:
        message: The message to be logged
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"

    try:
        with open(LOG_FILE, 'a') as f:
            f.write(log_message)
    except IOError as e:
        print(f"Error writing to log file: {e}")


def show_end_image(end_image):
    screen.fill(BLACK)
    if end_image:
        showImage(end_image)
    else:
        screen.fill(BLACK)
    pygame.display.flip()
    pygame.time.wait(END_DELAY)

def update_answers(answer_map):
    with open(ANSWER_FILE, 'w') as f:
        for answer in answer_map:
            f.write(answer + "\n")

def soundEnded():
    screen.fill(BLACK)

def playSound(file_name):
    # effect = pygame.mixer.music.load(file_name)
    # pygame.mixer.music.play(0)
    pygame.mixer.Sound(file_name).play()


def showImage(file_name):
    """
    Loads, scales, and blits an image to the screen.
    Includes error handling for missing or corrupted files.
    """
    global screen
    try:
        # Attempt to load the image. This is where the crash usually happens.
        original_image = pygame.image.load(file_name).convert()

        # 1. Scale the image to the exact screen size
        scaled_image = pygame.transform.scale(original_image, screen.get_size())

        # 2. Blit the scaled image
        screen.blit(scaled_image, (0, 0))
        pygame.display.flip()

    except pygame.error as e:
        print(f"ERROR: Failed to load asset '{file_name}'. Skipping image update.")
        screen.fill(BLACK)
        return  #

# def showImage(file_name):
#     original_image = pygame.image.load(file_name).convert()
#
#     # 1. Scale the image to the exact screen size
#     scaled_image = pygame.transform.scale(original_image, screen.get_size())
#
#     # 2. Blit the scaled image
#     screen.blit(scaled_image, (0, 0))
#     pygame.display.flip()


# Initialize pygame
pygame.init()



# Screen dimensions
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Colors
BLACK = (0, 0, 0)

screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)  # Use a standard window size of 800x600
# Create a fullscreen display
#screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Happy Halloween")
is_fullscreen = False

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