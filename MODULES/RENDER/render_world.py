import os

from MODULES.MAP.generate import MAP_GENERATION
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

        img = pg.image.load(path)

        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

        self.rect.x = x
        self.rect.y = y



class WorldClass:
    def __init__(self, WORLD: MAP_GENERATION, floor_surface, wall_surface):
        self.FLOOR = pg.sprite.Group()
        self.WALL = pg.sprite.Group()
        self.WORLD = WORLD
        self.floor_surface = floor_surface
        self.wall_surface = wall_surface
        self.tiles_img = None

        self.x_coord = 0
        self.y_coord = 0

        self.x_centr = 0
        self.y_centr = 0

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
        self.check_centr()
        center0 = self.get_center_tile_corner()
        center = center0[0] + self.x_centr, center0[1] + self.y_centr

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
        self.check_centr()
        center0 = self.get_center_tile_corner()
        center = center0[0] + self.x_centr, center0[1] + self.y_centr
        TILEMAP = self.WORLD.get_map()


        render_list = TILEMAP.copy()
        render_list = render_list[int(self.y_coord) + self.draw_dist:][:self.draw_dist * 2 + 1]

        for n, row in enumerate(render_list):
            render_list[n] = row[int(self.x_coord) + self.draw_dist:][:self.draw_dist * 2 + 1]


        for row, x_c in enumerate(range(center[0], center[0] + (SIZE * self.draw_dist * 2) + 1, SIZE)):
            for col, y_c in enumerate(range(center[1], center[1] + (SIZE * self.draw_dist * 2) + 1, SIZE)):
                try:
                    tile = self.search_tile(row, col, render_list)
                    self.draw_tile(up_left_draw_corner=(x_c, y_c), tile_type=self.tiles_img[tile], wall=True)
                except IndexError:
                    pass
    
    @staticmethod
    def search_tile(row, col, render_list):
        for tile, data in TILES.items():
            if data["ej"] == render_list[col][row]:
                return tile

    def check_centr(self):
        center0 = self.get_center_tile_corner()
        center = (center0[0] + self.x_centr), (center0[1] + self.y_centr)

        if (center0[0] - center[0]) >= 32:
            self.x_centr = 0
            self.x_coord += 1
        if (center[0] - center0[0]) >= 32:
            self.x_centr = 0
            self.x_coord -= 1

        if (center0[1] - center[1]) >= 32:
            self.y_centr = 0
            self.y_coord += 1
        if (center[1] - center0[1]) >= 32:
            self.y_centr = 0
            self.y_coord -= 1

    def get_world(self):
        return self.WORLD

    def crop_tiles(self):
        image = Image.open("./DATA/reses/tileset/tileset.png")
        self.tiles_img = {}

        for tile, data in TILES.items():
            top_y, top_x = data['coord']
            top_x, top_y = (top_x - 1) * SIZE, (top_y - 1) * SIZE
            down_x, down_y = top_x + SIZE, top_y + SIZE

            nt = image.crop((top_x, top_y, down_x, down_y))

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

    def groups_clear(self):
        self.WALL = pg.sprite.Group()
        self.FLOOR = pg.sprite.Group()

    # def tile_point(self, x, y,
    #                  x_plus=False, y_plus=False,
    #                  x_minus=False, y_minus=False,
    #                  set_x=False, set_y=False):
    #     if x_minus:
    #         self.x_coord -= x
    #     elif x_plus:
    #         self.x_coord += x
    #
    #     if y_minus:
    #         self.y_coord -= y
    #     elif y_plus:
    #         self.y_coord += y
    #
    #     if set_x:
    #         self.x_coord = x
    #     if set_y:
    #         self.y_coord = y

    def center_point(self, other:int, operat:str):
        if operat == "+x":
            self.x_centr += other
        if operat == "-x":
            self.x_centr -= other

        if operat == "+y":
            self.y_centr += other
        if operat == "-y":
            self.y_centr -= other