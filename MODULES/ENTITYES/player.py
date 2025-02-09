import os
from PIL import Image
import pygame as pg
from pygame.key import ScancodeWrapper
from MODULES.RENDER.render_world import Tile_entity
from MODULES.init import CONFIG

FPS = int(CONFIG["pygame"]["FPS"])
SIZE = CONFIG['world_gen']['tile_set']["size"]


class Player(pg.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        pg.sprite.Sprite.__init__(self)

        self.x, self.y = x-SIZE/2, y-SIZE/2

        self.speed: float = CONFIG["player"]["speed"]

        self.move_keys_main = (pg.K_w, pg.K_a, pg.K_s, pg.K_d)
        self.move_keys = {pg.K_w: "up", 
                          pg.K_a: "left",
                          pg.K_s: "down", 
                          pg.K_d: "right"}
        self.move_names = {"up": pg.K_w, 
                           "left": pg.K_a,
                           "down": pg.K_s, 
                           "right": pg.K_d}

        self.last_direction_key: str = 'up'
        self.current_direction_key: str = 'up'
        self.current_direction: str = 'up'
        self.current_image_index: int = 1
        self.animation_sprites = CONFIG["player"]["animation_sprites"]
        self.animation_interval = 1
        self.sprite_list = CONFIG["player"]["sprite_list"]["paths"]

        self.data_list = self.setup_image_lists()

        self.width = self.desired_width = CONFIG["player"]["width"]
        self.height = self.desired_height = CONFIG["player"]["height"]

        self.last_image_change = pg.time.get_ticks()

        self.frame_load()

        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

    def crop_sprite_list(self, path: str, spritelist: str) -> dict[int, str]:
        print(f"Loading {spritelist} sprite list {path}")
        image = Image.open(path)
        imgs: dict[int, str] = {}

        sprite_number = 0
        size = CONFIG["player"]["sprite_list"]["size"]
        for row in range(1, CONFIG["player"]["sprite_list"]["rows"]+1):
            for col in range(1, CONFIG["player"]["sprite_list"]["cols"]+1):
                top_y, top_x = row, col
                top_x, top_y = (top_x - 1) * size, (top_y - 1) * size
                down_x, down_y = top_x + size, top_y + size
                nt = image.crop((top_x, top_y, down_x, down_y))

                path_to_player_pictures = "\\DATA\\tmp\\player\\"

                if not os.path.exists(os.getcwd() + path_to_player_pictures):
                    os.mkdir(os.getcwd() + path_to_player_pictures)

                path = f"./DATA/tmp/player/{spritelist}_{sprite_number}.png"
                nt.save(path)

                imgs[sprite_number] = path
                sprite_number += 1

        return imgs

    def setup_image_lists(self) -> dict[str,dict[int, str]]:
        data_list: dict[str,dict[int, str]] = {}
        for spritelist, path in self.sprite_list.items():
            images = self.crop_sprite_list(path, spritelist)
            data_list[spritelist] = images
        print("DONE")

        return data_list

    def frame_load(self) -> None:
        image_path = self.data_list[self.current_direction][self.current_image_index]
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(
            self.image, (self.desired_width, self.desired_height))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

    def handle_keydown(self, key: int) -> None:
        if key in self.move_keys_main:
            self.current_direction_key = self.move_keys[key]

    def move(self, keys: ScancodeWrapper, center: tuple[int, int]) -> None:
        speed_per_frame = self.speed / FPS
        current_key = None

        if self.move_names[self.last_direction_key] and keys[self.move_names[self.last_direction_key]]:
            current_key = self.last_direction_key
        else:
            for key in self.move_keys_main:
                if keys[key]:
                    current_key = self.move_keys[key]
                    self.last_direction_key = self.move_keys[key]
                    break

        prev_direction = self.current_direction

        if current_key == "up":
            self.y -= speed_per_frame
            self.current_direction = 'down'
        elif current_key == "down":
            self.y += speed_per_frame
            self.current_direction = 'up'
        elif current_key == "left":
            self.x -= speed_per_frame
            self.current_direction = 'left'
        elif current_key == "right":
            self.x += speed_per_frame
            self.current_direction = 'right'
        else:
            self.current_direction = 'down'

        if prev_direction != self.current_direction:
            self.current_image_index = 0

        if current_key is not None:
            current_time = pg.time.get_ticks()
            if current_time - self.last_image_change >= self.animation_interval:
                self.last_image_change = current_time
                self.current_image_index = (self.current_image_index + 1) % self.animation_sprites
                self.frame_load()

        else:
            self.current_direction = 'up'
            self.current_image_index = 0
            self.frame_load()

        if (self.x - center[0]) >= 64:
            self.x -= speed_per_frame - 1
        elif (center[0] - self.x) >= 64:
            self.x += speed_per_frame - 1

        if (self.y - center[1]) >= 64:
            self.y -= speed_per_frame - 1
        elif (center[1] - self.y) >= 64:
            self.y += speed_per_frame - 1

    def update(self, keys: ScancodeWrapper, center: tuple[int, int], wall) -> None:
        # self.mask = pg.mask.from_surface(self.image)

        # if self.mask.overlap(wall.mask, (10, 10)):
        #     # print(f"COLLISION {round(int(time.time()), 2)}")
        #     pass

        self.move(keys, center)
        self.frame_load()

    def exit_now(self, exit) -> str:
        if exit:
            print(abs(exit.rect.x - self.x), abs(exit.rect.y - self.y))
            if abs(exit.rect.x - self.x) <= 32 and abs(exit.rect.y - self.y) <= 32:
                return "win"
        return "nos"

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.image, (self.x, self.y))
