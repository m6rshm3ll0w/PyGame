import os
from PIL import Image
import pygame as pg
import time
from pygame.key import ScancodeWrapper
from MODULES.RENDER.render_world import WorldClass
from MODULES.init import CONFIG, logger

FPS = int(CONFIG["pygame"]["FPS"])
SIZE = CONFIG['world_gen']['tile_set']["size"]


class Player(pg.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        pg.sprite.Sprite.__init__(self)

        self.x, self.y = x-SIZE/2+1, y-SIZE/2+1

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
        self.animation_fps = 1/CONFIG["player"]["animation_fps"]
        self.sprite_list = CONFIG["player"]["sprite_list"]["paths"]

        self.data_list = self.setup_image_lists()

        self.width = self.desired_width = CONFIG["player"]["width"]
        self.height = self.desired_height = CONFIG["player"]["height"]

        self.last_image_change = time.time()

        self.frame_load()

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y) 

        self.load_mask()

        self.last_key = "up"

    def crop_sprite_list(self, path: str, spritelist: str) -> dict[int, str]:
        logger.info(f"Loading {spritelist} sprite list {path}")

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
        logger.info("setup image lists - DONE")

        return data_list

    def frame_load(self) -> None:
        image_path = self.data_list[self.current_direction][self.current_image_index]
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(
            self.image, (self.desired_width, self.desired_height))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y) 

    def load_mask(self):
        mask_path =CONFIG["player"]["mask"]
        mask_img = pg.image.load(mask_path).convert_alpha()
        mask_img = pg.transform.scale(
            mask_img, (self.desired_width, self.desired_height))
        self.mask = pg.mask.from_surface(mask_img)

        logger.info("player mask loaded")

    def handle_keydown(self, key: int) -> None:
        if key in self.move_keys_main:
            self.current_direction_key = self.move_keys[key]

    def get_collision(self, world):
        now_collisions = pg.sprite.spritecollide(self, world.wall, False, pg.sprite.collide_mask)

        for wall in now_collisions:
            # Вычисляем пересечение двух rect (self и wall)
            overlap_x = min(self.rect.right, wall.rect.right) - max(self.rect.left, wall.rect.left)
            overlap_y = min(self.rect.bottom, wall.rect.bottom) - max(self.rect.top, wall.rect.top)

            # Определяем наименьшее перекрытие, чтобы сдвигать по наименее глубокой оси
            if overlap_x < overlap_y:
                # Выталкивание по оси X
                if self.rect.centerx > wall.rect.centerx:
                    self.x += 2
                else:
                    self.x -= 2
            elif overlap_y < overlap_x:
                # Выталкивание по оси Y
                if self.rect.centery > wall.rect.centery:
                    self.y += 2
                else:
                    self.y -= 2
            else:
                # Иначе
                if self.rect.centery > wall.rect.centery:
                    self.y -= 2
                else:
                    self.rect.y += 2

    def move(self, keys: ScancodeWrapper, center: tuple[int, int], world) -> None:
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
            current_direction = 'down'
        elif current_key == "down":
            self.y += speed_per_frame
            current_direction = 'up'
        elif current_key == "left":
            self.x -= speed_per_frame
            current_direction = 'left'
        elif current_key == "right":
            self.x += speed_per_frame
            current_direction = 'right'
        else:
            current_direction = 'up'


        self.current_direction = current_direction


        allise = world.anti_allise(get=True)
        error = (self.x + SIZE/2 - center[0], self.y  + SIZE/2 - center[1])
        
        if error[0] > 12 and "x+" not in allise:
            self.x -= speed_per_frame - 0.7
        elif error[0] < -12 and "x-" not in allise:
            self.x += speed_per_frame - 0.7

        if error[1] > 12 and "y+" not in allise:
            self.y -= speed_per_frame - 0.7
        elif error[1] < -12 and "y-" not in allise:
            self.y += speed_per_frame - 0.7


        if current_key is not None:
            current_time = time.time()
            if current_time - self.last_image_change >= self.animation_fps:
                self.last_image_change = time.time()
                self.current_image_index = (self.current_image_index + 1) % self.animation_sprites
                self.frame_load()
        else:
            self.current_image_index = 0

        if prev_direction != self.current_direction:
            self.current_image_index = 0

        self.get_collision(world)

        self.frame_load()


    def update(self, keys: ScancodeWrapper, center: tuple[int, int], world:WorldClass) -> None:
        self.move(keys, center, world)
        self.frame_load()

    def exit_now(self, exit) -> str:
        if exit:
            offset = (exit.rect.x - self.rect.x, exit.rect.y - self.rect.y)
            if self.mask.overlap(exit.mask, offset=offset):
                return "win"
        return "no"

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))
