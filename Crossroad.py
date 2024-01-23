import pygame
from pygame import mixer
from sys import exit
import os
import random

pygame.init()

# GAME SETTINGS

width, height = 864, 768
screen = pygame.display.set_mode((864, 768))
background = pygame.image.load(os.path.join("images", "Background.png"))
game_clock = pygame.time.Clock()
pygame.display.set_caption("Frogger")


# FROG

frog_images = [
    pygame.image.load(os.path.join("images", "frog_up.png")),
    pygame.image.load(os.path.join("images", "frog_down.png")),
    pygame.image.load(os.path.join("images", "frog_left.png")),
    pygame.image.load(os.path.join("images", "frog_right.png")),
]

frog_velocity = 48

# SOUNDS
hit_sound = mixer.Sound(os.path.join("audio", "hit.mp3"))
jump_sound = mixer.Sound(os.path.join("audio", "jump.mp3"))
win_sound = mixer.Sound(os.path.join("audio", "win.mp3"))
jump_sound.set_volume(0.5)
hit_sound.set_volume(1.3)


# SPAWNER

spawn_timer = pygame.time.get_ticks()
spawn_interval = 2000

# CARS

car_velocity = 4
car_right_y = [96, 192, 384, 480, 576]
car_left_y = [144, 240, 432, 528, 624]

cars_right = []
cars_left = []

# SCORE
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# LIFES
life_value = 3


def show_life(x, y):
    life = font.render("Lives: " + str(life_value), True, (255, 255, 255))
    screen.blit(life, (x, y))


def win(frog):
    global score_value
    if frog.y <= 48:
        frog.x, frog.y = 384, 718
        score_value += 50
        win_sound.play()


def lose(life_value):
    if life_value < 0:
        pygame.quit()
        exit()


def draw_window(frog, index, cars_right, cars_left):
    screen.blit(background, (0, 0))

    screen.blit(frog_images[index], (frog.x, frog.y))

    for car in cars_right:
        screen.blit(car["image"], (car["rect"].x, car["rect"].y))

    for car in cars_left:
        screen.blit(car["image"], (car["rect"].x, car["rect"].y))

    show_score(20, 20)
    show_life(700, 20)

    pygame.display.update()


def spawn_car(direction):
    if direction == "right":
        return {
            "rect": pygame.Rect(0, random.choice(car_right_y), 96, 48),
            "image": pygame.image.load(os.path.join("images", "car_right.png")),
        }
    elif direction == "left":
        return {
            "rect": pygame.Rect(width, random.choice(car_left_y), 96, 48),
            "image": pygame.image.load(os.path.join("images", "car_left.png")),
        }


def check_collision(frog, cars_right, cars_left):
    global life_value
    frog_rect = pygame.Rect(frog.x, frog.y, 48, 48)
    for car in cars_right + cars_left:
        if frog_rect.colliderect(car["rect"]):
            frog.x, frog.y = 384, 718
            life_value -= 1
            hit_sound.play()

# Do skonczenia
def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((255, 255, 255), (0, 0))


def main():
    global score_value
    global spawn_timer
    frog = pygame.Rect(384, 718, 48, 48)

    key_released = False

    frog_rotation = 0

    while True:
        game_clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                key_released = True

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_UP] and key_released and frog.y >= 0:
            frog.y -= frog_velocity
            frog_rotation = 0
            key_released = False
            score_value += 10
            jump_sound.play()

        if (
            keys_pressed[pygame.K_DOWN]
            and key_released
            and frog.y + frog_velocity <= 720
        ):
            frog.y += frog_velocity
            frog_rotation = 1
            key_released = False
            jump_sound.play()

        if keys_pressed[pygame.K_LEFT] and key_released and frog.x - frog_velocity >= 0:
            frog.x -= frog_velocity
            frog_rotation = 2
            key_released = False
            jump_sound.play()

        if (
            keys_pressed[pygame.K_RIGHT]
            and key_released
            and frog.x + frog_velocity <= 816
        ):
            frog.x += frog_velocity
            frog_rotation = 3
            key_released = False
            jump_sound.play()

        current_time = pygame.time.get_ticks()
        if current_time - spawn_timer > spawn_interval:
            cars_right.append(spawn_car("right"))
            cars_left.append(spawn_car("left"))
            spawn_timer = current_time

        for car in cars_right:
            car["rect"].x += car_velocity
            if car["rect"].x > width:
                cars_right.remove(car)

        for car in cars_left:
            car["rect"].x -= car_velocity
            if car["rect"].x < -96:
                cars_left.remove(car)

        check_collision(frog, cars_right, cars_left)

        lose(life_value)

        win(frog)

        draw_window(frog, frog_rotation, cars_right, cars_left)


if __name__ == "__main__":
    main()
