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
DEBOUNCE_TIME = 1500
FADE_TIME = 500
END_DELAY = 5000
SCREEN_SIZE = (1920, 1080)

# Input constants
LEFT = "LEFT"
RIGHT = "RIGHT"
QUIT = "QUIT"
PROCEED = "PROCEED"

global is_fullscreen
global windowed_size
global last_input_time
global last_image_displayed
windowed_size = SCREEN_SIZE  # Initialize windowed size
is_fullscreen = False
last_input_time = 0
last_image_displayed = None


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



real_questions.append({"image": "images/a-pokepop.jpg", "left": "pokemon", "right": "kpop",  "sound_right": "sounds/sound1.mp3", "sound_left": "sounds/sound2.mp3", "right_next": 1, "left_next": 1, "end_image_left": "images/pokemon-end.png", "end_image_right": "images/kpop-end.png"})
real_questions.append({"image": "images/a-chewycrunchy.jpg", "left": "chocolate", "right": "chewy", "sound_right": "sounds/sound3.mp3", "sound_left": "sounds/sound4.mp3", "left_next": 3, "right_next": 2})
real_questions.append({"image": "images/a-soursweet.jpg", "left": "sour", "right": "sweet", "sound_right": "sounds/sound5.mp3", "sound_left": "sounds/sound6.mp3", "right_next": DONE, "left_next": DONE})
real_questions.append({"image": "images/a-peanut.jpg", "left": "peanut", "right": "no-nuts", "sound_right": "sounds/sound7.mp3", "sound_left": "sounds/sound8.mp3", "right_next": DONE, "left_next": DONE})

random_questions.append({"image": "images/Slide4.JPG"})
random_questions.append({"image": "images/Slide5.JPG"})
random_questions.append({"image": "images/Slide6.JPG"})
random_questions.append({"image": "images/Slide7.JPG"})
random_questions.append({"image": "images/Slide8.JPG"})
random_questions.append({"image": "images/Slide9.JPG"})
random_questions.append({"image": "images/Slide10.JPG"})
random_questions.append({"image": "images/Slide11.JPG"})
random_questions.append({"image": "images/Slide12.JPG"})
random_questions.append({"image": "images/Slide13.JPG"})
random_questions.append({"image": "images/Slide14.JPG"})
random_questions.append({"image": "images/Slide15.JPG"})
random_questions.append({"image": "images/Slide16.JPG"})

button_sound_bank = []
button_sound_bank.append("sounds/level-up.mp3")
button_sound_bank.append("sounds/soda_pop.mp3")
button_sound_bank.append("sounds/mmm.mp3")
button_sound_bank.append("sounds/nintendo-game-boy-startup.mp3")
button_sound_bank.append("sounds/mario-galaxy.mp3")
button_sound_bank.append("sounds/arceus.mp3")

def wait_for_input(current_image_path, sound_path):
    """
    Waits for user input (LEFT, RIGHT, f, q) with debouncing across screens.
    Handles fullscreen toggling and quitting.
    Returns LEFT, RIGHT, or QUIT.
    Implements debouncing with DEBOUNCE_TIME milliseconds that persists across screens.
    Supports both keyboard and joystick input.
    """
    global screen, is_fullscreen, windowed_size, last_input_time

    while True:
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return QUIT
                elif event.key == pygame.K_f:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        windowed_size = screen.get_size()
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode(windowed_size, pygame.RESIZABLE)
                    showImage(current_image_path)
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    # Check if enough time has passed since last input
                    if current_time - last_input_time >= DEBOUNCE_TIME:
                        print(f"cur {current_time} and last {last_input_time} and diff {current_time - last_input_time}")
                        last_input_time = current_time
                        if sound_path:
                            playSound(sound_path)
                        return LEFT if event.key == pygame.K_LEFT else RIGHT
            elif event.type == pygame.JOYBUTTONDOWN:
                # Check if enough time has passed since last input
                if current_time - last_input_time >= DEBOUNCE_TIME:
                    print(f"cur {current_time} and last {last_input_time} and diff {current_time - last_input_time}")
                    last_input_time = current_time
                    if event.button == 0:  # Button 1 (index 0)
                        if sound_path:
                            playSound(sound_path)
                        return LEFT
                    elif event.button == 1:  # Button 2 (index 1)
                        if sound_path:
                            playSound(sound_path)
                        return RIGHT
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                showImage(current_image_path)

def wait_for_any_key(current_image_path):
    """
    Waits for LEFT, RIGHT, or q.
    Used for screens that just need a key to proceed.
    Handles fullscreen and quitting.
    Returns PROCEED or QUIT.
    """
    global screen, is_fullscreen, windowed_size
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return QUIT
                elif event.key == pygame.K_f:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        windowed_size = screen.get_size()
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode(windowed_size, pygame.RESIZABLE)
                    showImage(current_image_path)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    return PROCEED
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                showImage(current_image_path)


def game_loop():
    global screen
    global real_questions
    global random_questions
    global used_random_questions
    global is_fullscreen
    global answer_map  # Ensure answer_map is global
    used_random_questions = []  # Reset the list of used random questions
    answer_map = []  # Reset answers
    question_index = 0
    end_image = None

    if attract_screen() == QUIT:
        return False

    if instruction_screen() == QUIT:
        return False

    if ask_random() == QUIT:
        return False

    while question_index != DONE:
        question = real_questions[question_index]
        screen.fill(BLACK)
        showImage(question["image"])

        action = wait_for_input(question["image"], button_sound_bank)

        if action == QUIT:
            return False
        elif action == LEFT:
            answer_map.append(question["left"])
            question_index = question["left_next"]
            if "end_image_left" in question:
                end_image = question["end_image_left"]
            update_answers(answer_map)
            if question_index != DONE:
                if ask_random() == QUIT:
                    return False
        elif action == RIGHT:
            answer_map.append(question["right"])
            question_index = question["right_next"]
            if "end_image_right" in question:
                end_image = question["end_image_right"]
            update_answers(answer_map)
            if question_index != DONE:
                if ask_random() == QUIT:
                    return False

        # Original delay was here, but it's now handled by the blocking input
        # and the delay inside ask_random()
        # pygame.time.wait(QUESTION_DELAY)

    print(f"Answer map: {answer_map}")
    log_entry(f"Answer map: {answer_map}")
    show_end_image(end_image)
    return True

def attract_screen():
    screen.fill(BLACK)
    showImage("images/attract.png")
    pygame.display.flip()

    action = wait_for_input("images/attract.png", button_sound_bank)
    if action == QUIT:
        return QUIT
    return PROCEED

def instruction_screen():
    screen.fill(BLACK)
    showImage("images/instructions.png")
    pygame.display.flip()

    action = wait_for_input("images/instructions.png", button_sound_bank)
    if action == QUIT:
        return QUIT
    return PROCEED



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

    screen.fill(BLACK)
    showImage(question["image"])
    pygame.display.flip()

    action = wait_for_input(question["image"], button_sound_bank)
    if action == QUIT:
        return QUIT

    return PROCEED


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
        playSound("sounds/item-received.mp3")
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
    try:
        # If file_name is a list/array, randomly select one file
        if isinstance(file_name, (list, tuple)):
            if not file_name:  # Check if array is empty
                return
            selected_file = random.choice(file_name)
        else:
            selected_file = file_name

        pygame.mixer.Sound(selected_file).play()
    except pygame.error as e:
        print(f"ERROR: Failed to play sound '{selected_file}'. Skipping.")
        log_entry(f"ERROR: Failed to play sound '{selected_file}': {e}")

def showImage(file_name, fade_in=True, new_image = True):
    """
    Loads, scales, and blits an image to the screen while maintaining aspect ratio,
    with fade out/in effects.
    """
    global screen
    global last_image_displayed

    if not file_name:
        return

    # we were called to change the image, so first fade out the old one
    if new_image:
        showImage(last_image_displayed, fade_in=False, new_image=False)


    last_image_displayed = file_name
    try:
        # Load and scale the new image
        original_image = pygame.image.load(file_name).convert()
        image_width, image_height = original_image.get_size()
        screen_width, screen_height = screen.get_size()

        # Calculate the scaling ratio while maintaining aspect ratio
        width_ratio = screen_width / image_width
        height_ratio = screen_height / image_height
        scale_ratio = min(width_ratio, height_ratio)

        # Calculate new dimensions
        new_width = int(image_width * scale_ratio)
        new_height = int(image_height * scale_ratio)

        # Scale the image
        scaled_image = pygame.transform.scale(original_image, (new_width, new_height))

        # Calculate position to center the image
        x_pos = (screen_width - new_width) // 2
        y_pos = (screen_height - new_height) // 2


        # Create a surface for the new image with alpha
        new_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        new_surface.fill(BLACK)
        new_surface.blit(scaled_image, (x_pos, y_pos))

        # Fade in
        alphas = range(0, 256, 5) if fade_in else range(256,0,-5)
        for alpha in alphas:  # Gradually change alpha
            screen.fill(BLACK)
            new_surface.set_alpha(alpha)
            screen.blit(new_surface, (0, 0))
            draw_arrows()
            pygame.display.flip()
            pygame.time.delay(FADE_TIME // 51)  # Distribute fade time evenly

        # Final display at full alpha
        screen.fill(BLACK)
        if fade_in:
            screen.blit(scaled_image, (x_pos, y_pos))
            draw_arrows()
            pygame.display.flip()

    except pygame.error as e:
        print(f"ERROR: Failed to load asset '{file_name}'. Skipping image update.")
        log_entry(f"ERROR: Failed to load asset '{file_name}': {e}")
        screen.fill(BLACK)
        pygame.display.flip()
        return

def draw_arrows():
    # Get the current screen dimensions
    screen_width, screen_height = screen.get_size()

    # Arrow properties
    arrow_color = (255, 165, 0)  # Orange in RGB
    arrow_width = 40  # Thickness of arrow lines
    arrow_length = 100  # Length of the main arrow body
    head_size = 50  # Size of arrow head

    # Vertical position (middle of screen)
    y_pos = screen_height // 2

    # Left arrow
    # Main body
    pygame.draw.line(screen, arrow_color,
                     (100 + arrow_length, y_pos),
                     (100, y_pos),
                     arrow_width)
    # Arrow head
    x_basis = 100 - arrow_length // 2
    pygame.draw.polygon(screen, arrow_color, [
        (x_basis, y_pos),
        (x_basis + head_size, y_pos - head_size),
        (x_basis + head_size, y_pos + head_size)
    ])

    # Right arrow
    # Main body
    pygame.draw.line(screen, arrow_color,
                     (screen_width - 100 - arrow_length, y_pos),
                     (screen_width - 100, y_pos),
                     arrow_width)
    # Arrow head
    x_basis = screen_width - 100 + arrow_length // 2
    pygame.draw.polygon(screen, arrow_color, [
        (x_basis, y_pos),
        (x_basis - head_size, y_pos - head_size),
        (x_basis - head_size, y_pos + head_size)
    ])

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize mixer for sounds

# Screen dimensions
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Colors
BLACK = (0, 0, 0)

screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Happy Halloween")

# Joystick initialization
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
if not joysticks:
    print("No joystick detected!")
else:
    print(f"Detected {len(joysticks)} joystick(s).")
    # Note: Joystick input is not handled in the new input functions.
    # The original active code didn't handle it either.

# --- Main loop ---
running = True
while running:
    running = game_loop()

# Quit pygame
pygame.quit()
