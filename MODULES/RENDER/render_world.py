import os

import pygame.image

from MODULES.RENDER.MAP2IMG import map_visualise
import pygame as pg
from MODULES.init import CONFIG
from PIL import Image
from MODULES.init import BLACK

TILES = CONFIG['world_gen']['tile_set']["tiles"]
SIZE = CONFIG['world_gen']['tile_set']["size"]


class Tile_entity(pg.sprite.Sprite):
    def __init__(self, x, y, path):
        pg.sprite.Sprite.__init__(self)

        img = pygame.image.load(path)

        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = x
        self.rect.y = y



class WorldClass:
    def __init__(self, WORLD, floor_surface, wall_surface):
        self.FLOOR = pg.sprite.Group()
        self.WALL = pg.sprite.Group()
        self.WORLD = WORLD
        self.floor_surface = floor_surface
        self.wall_surface = wall_surface
        self.tiles_img = None

        self.draw_dist = CONFIG["pygame"]["distance"]

        self.crop_tiles()

    def generate_worldmap(self, vis=False):
        self.WORLD.generate_world()
        if vis:
            MAP = self.WORLD.get_map()
            map_visualise(MAP)

    def get_center_tile_corner(self):
        center = self.floor_surface.get_rect().center
        up_left_draw_corner = center[0] - SIZE // 2, center[1] - SIZE // 2

        return (up_left_draw_corner[0] - (SIZE * self.draw_dist + 1),
                up_left_draw_corner[1] - (SIZE * self.draw_dist + 1))

    def draw_floor(self):
        center = self.get_center_tile_corner()

        for x_c in range(center[0], center[0] + (SIZE*self.draw_dist*2)+1, SIZE):
            for y_c in range(center[1], center[1] + (SIZE*self.draw_dist*2)+1, SIZE):
                self.draw_tile(up_left_draw_corner=(x_c, y_c), tile_type=self.tiles_img["floor"])


    def draw_tile(self, up_left_draw_corner, tile_type, wall=False):
        if not wall:
            try:
                obj_ = Tile_entity(up_left_draw_corner[0],
                                   up_left_draw_corner[1], tile_type)
                self.FLOOR.add(obj_)
            except AttributeError:
                raise AttributeError("ээээээ я хз что это")

        if wall:
            try:
                obj_ = Tile_entity(up_left_draw_corner[0],
                                   up_left_draw_corner[1], tile_type)
                self.WALL.add(obj_)
            except AttributeError:
                raise AttributeError("ээээээ я хз что это")

    def draw_wall(self):
        render_list = []

        data = self.WORLD.get_data()
        start_point = data.start_point
        center = self.get_center_tile_corner()
        map = self.WORLD.get_map()

        render_list = map.copy()

        # render_list = render_list[int(start_point["row"]) + self.draw_dist:][:self.draw_dist * 2 + 1]
        #
        # for n, row in enumerate(render_list):
        #     render_list[n] = row[int(start_point["col"]) + self.draw_dist:][:self.draw_dist * 2 + 1]

    def search(self, row, col):
        TILEMAP = self.WORLD.get_map()
        for tile, data in TILES.items():
            if data["ej"] == TILEMAP[row][col]:
                return tile

    def get_world(self):
        return self.WORLD

    def crop_tiles(self):
        image = Image.open("./DATA/reses/tileset/tileset.png")
        self.tiles_img = {}

        for tile, data in TILES.items():
            top_y, top_x = data['coord']
            top_x, top_y = (top_x - 1) * SIZE, (top_y - 1) * SIZE
            down_x, down_y = top_x + SIZE, top_y + SIZE

            nt = image.crop((top_x, top_y, down_x + 1, down_y + 1))

            tmppath = f"\\DATA\\tmp\\tiles\\"

            if not os.path.exists(os.getcwd()+tmppath):
                os.mkdir(os.getcwd()+tmppath)

            path = f"./DATA/tmp/tiles/{tile}.png"
            nt.save(path)
            self.tiles_img[tile] = path

    def sprite_list_Floor(self):
        return self.FLOOR

    def sprite_list_Wall(self):
        return self.WALL