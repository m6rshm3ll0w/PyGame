import pygame
from MODULES.init import CONFIG

FPS = int(CONFIG["pygame"]["FPS"])


class Player:
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y
        self.speed: float = 200
        self.last_direction_key = None

        desired_width, desired_height = 60, 60
        self.setup_image_lists(desired_width, desired_height)

        self.current_image_index = 0
        self.current_direction = 'w'
        self.image = self.top_images[self.current_image_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.width = desired_width
        self.height = desired_height

        self.last_image_change = 0
        self.animation_interval = 50

    def setup_image_lists(self, width, height):
        directions = {
            'top': 8,
            'back': 8,
            'left': 8,
            'right': 8
        }

        for direction, count in directions.items():
            images = []
            for i in range(1, count + 1):
                image = self.create_scaled_image(f'{direction}{i}.png', width, height)
                images.append(image)
                setattr(self, f'{direction}_image_{i}', image)
            setattr(self, f'{direction}_images', images)

    def create_scaled_image(self, filename, desired_wdth, desired_hght):
        img = pygame.image.load(f'{CONFIG['dirs']['player_pictures']}{filename}')
        return pygame.transform.scale(img, (desired_wdth, desired_hght))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_keydown(self, key):
        if key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
            self.last_direction_key = key

    def move(self, keys, center):
        speed_per_frame = self.speed / FPS
        current_key = None

        if self.last_direction_key and keys[self.last_direction_key]:
            current_key = self.last_direction_key
        else:
            for key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                if keys[key]:
                    current_key = key
                    self.last_direction_key = key
                    break

        prev_direction = self.current_direction

        if current_key == pygame.K_w:
            self.y -= speed_per_frame
            self.current_direction = 'w'
        elif current_key == pygame.K_s:
            self.y += speed_per_frame
            self.current_direction = 's'
        elif current_key == pygame.K_a:
            self.x -= speed_per_frame
            self.current_direction = 'a'
        elif current_key == pygame.K_d:
            self.x += speed_per_frame
            self.current_direction = 'd'
        else:
            self.current_direction = 'w'

        if prev_direction != self.current_direction:
            self.current_image_index = 0

        image_lists = {
            'w': self.back_images,
            's': self.top_images,
            'a': self.left_images,
            'd': self.right_images
        }
        current_images = image_lists.get(self.current_direction, self.top_images)

        if current_key is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_image_change > self.animation_interval:
                self.last_image_change = current_time
                self.current_image_index = (self.current_image_index + 1) % len(current_images)
            self.image = current_images[self.current_image_index]
        else:
            self.current_image_index = 0
            self.image = self.top_images[self.current_image_index]

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
