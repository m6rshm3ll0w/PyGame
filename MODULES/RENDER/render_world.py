import os

from MODULES.RENDER.MAP2IMG import map_visualise
import pygame as pg
from MODULES.init import CONFIG
from PIL import Image
from MODULES.init import BLACK, RED

TILES = CONFIG['world_gen']['tile_set']["tiles"]
SIZE = CONFIG['world_gen']['tile_set']["size"]



class Floor_entity(pg.sprite.Sprite):
    def __init__(self, width, height, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pg.draw.rect(self.image, RED, (x, y, SIZE, SIZE))

        self.rect = self.image.get_rect()



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

    def draw_floor(self):
        up_right_draw_corner = center[0] - SIZE//2, center[1] - SIZE//2

        try:
            obj_ = Floor_entity(self.floor_surface.get_width(),
                                self.floor_surface.get_width(),
                                up_right_draw_corner[0],
                                up_right_draw_corner[1])
            self.FLOOR.add(obj_)
        except AttributeError:
            raise AttributeError("ээээээ я хз что это")

    def draw_wall(self):
        render_list = []

        data = self.WORLD.get_data()
        start_point = data.start_point
        center = self.floor_surface.get_width() / 2, self.floor_surface.get_height() / 2
        map = self.WORLD.get_map()

        render_list = map.copy()

        render_list = render_list[int(start_point["row"]) + self.draw_dist:][:self.draw_dist * 2 + 1]

        for n, row in enumerate(render_list):
            render_list[n] = row[int(start_point["col"]) + self.draw_dist:][:self.draw_dist * 2 + 1]




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

            tmppath = f"\\DATA\\tmp\\tiles\\init"

            if not os.path.exists(os.getcwd()+tmppath):
                os.mkdir(os.getcwd()+tmppath)

            path = f"./DATA/tmp/tiles/{tile}.png"
            nt.save(path)
            self.tiles_img[tile] = path

    def sprite_list_Floor(self):
        return self.FLOOR

    def sprite_list_Wall(self):
        return self.WALL