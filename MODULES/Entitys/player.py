import pygame
import math
from MODULES.init import CONFIG

FPS = int(CONFIG["pygame"]["FPS"])


class Player:
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y
        self.speed: float = 200

        desired_width, desired_height = 30, 30

        self.original_image_scaled1 = self.make_image('player1.png', desired_width,
                                                      desired_height)

        self.original_image_scaled2 = self.make_image('player2.png', desired_width,
                                                      desired_height)

        self.original_image_scaled3 = self.make_image('player3.png', desired_width,
                                                      desired_height)

        self.images = [
            self.original_image_scaled1,
            self.original_image_scaled2,
            self.original_image_scaled1,
            self.original_image_scaled3,
            self.original_image_scaled1
        ]

        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.width = desired_width
        self.height = desired_height

        self.last_image_change = 0
        self.animation_interval = 100

    def make_image(self, filename, desired_wdth, desired_hght):
        img = pygame.image.load(f'./DATA/reses/player/{filename}')
        scalled_img = pygame.transform.scale(img, (desired_wdth, desired_hght))
        return scalled_img

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, keys, center):
        speed_per_frame = self.speed / FPS
        diagonal_speed = speed_per_frame / math.sqrt(2)

        move_up = keys[pygame.K_w]
        move_left = keys[pygame.K_a]
        move_down = keys[pygame.K_s]
        move_right = keys[pygame.K_d]

        if move_up and move_left:
            angle = 45
            self.x -= diagonal_speed
            self.y -= diagonal_speed
        elif move_up and move_right:
            angle = -45
            self.x += diagonal_speed
            self.y -= diagonal_speed
        elif move_down and move_left:
            angle = 135
            self.x -= diagonal_speed
            self.y += diagonal_speed
        elif move_down and move_right:
            angle = -135
            self.x += diagonal_speed
            self.y += diagonal_speed
        elif move_up:
            angle = 0
            self.y -= speed_per_frame
        elif move_down:
            angle = 180
            self.y += speed_per_frame
        elif move_left:
            angle = 90
            self.x -= speed_per_frame
        elif move_right:
            angle = -90
            self.x += speed_per_frame
        else:
            angle = 0

        if angle != 0:
            self.image = pygame.transform.rotate(self.images[self.current_image_index], angle)
        else:
            self.image = self.images[self.current_image_index]

        self.rect = self.image.get_rect(center=(self.x, self.y))

        if move_up or move_left or move_down or move_right:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_image_change > self.animation_interval:
                self.last_image_change = current_time
                self.current_image_index += 1
                if self.current_image_index >= len(self.images):
                    self.current_image_index = 0
        else:
            self.current_image_index = 0
            self.image = self.images[self.current_image_index]
            self.rect = self.image.get_rect(center=(self.x, self.y))

        if (self.x - center[0]) >= 64:
            self.x -= speed_per_frame - 1
        elif (center[0] - self.x) >= 64:
            self.x += speed_per_frame - 1

        if (self.y - center[1]) >= 64:
            self.y -= speed_per_frame - 1
        elif (center[1] - self.y) >= 64:
            self.y += speed_per_frame - 1

        self.rect = self.image.get_rect(center=(self.x, self.y))
