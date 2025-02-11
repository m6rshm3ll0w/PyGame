import os

from MODULES.MAP.generate import MapGeneration
from MODULES.RENDER.MAP2IMG import map_visualise
import pygame as pg
from MODULES.init import CONFIG
from PIL import Image
from MODULES.init import BLACK

TILES = CONFIG['world_gen']['tile_set']["tiles"]
SIZE = CONFIG['world_gen']['tile_set']["size"]


class Tile_entity(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, path: str) -> None:
        pg.sprite.Sprite.__init__(self)

        img = pg.image.load(path)

        self.image = img
        self.image.set_colorkey(BLACK)
        
        mask = pg.image.load(CONFIG["world_gen"]["tile_set"]["mask"]).convert_alpha()
        self.mask = pg.mask.from_surface(mask)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) 
        
    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)
        self.mask = pg.mask.from_surface(self.image)


class WorldClass:
    def __init__(self, WORLD: MapGeneration, floor_surface: pg.Surface, wall_surface: pg.Surface) -> None:
        self.floor: Tile_entity
        self.wall = pg.sprite.Group()
        # self.start_point: Tile_entity
        self.exit_point = None
        self.WORLD = WORLD
        self.floor_surface = floor_surface
        self.wall_surface = wall_surface

        self.x_coord:int = 20
        self.y_coord:int = 20

        self.x_end: int = 25
        self.y_end: int = 25
        
        self.x_centr = 0
        self.y_centr = 0

        self.tiles_img: dict[str,str]

        self.DRAW_DIST = CONFIG["pygame"]["distance"]
        self.crop_tiles()

    def change_start_point(self) -> None:
        self.data = self.WORLD.get_data()
        self.x_start = self.data.start_point["col"] 
        self.y_start = self.data.start_point["row"] 

        self.x_coord = self.x_start
        self.y_coord = self.y_start

        self.x_end = self.data.end_point["col"]
        self.y_end = self.data.end_point["row"]

    def generate_world_map(self, vis:bool=False) -> None:
        self.WORLD.generate_world()
        if vis:
            MAP = self.WORLD.get_map()
            map_visualise(MAP)

    def draw_points(self, surface: pg.Surface):
        self.draw_end(surface=surface)
        self.draw_start(surface)

    def _draw_point(self, surface: pg.Surface, x_tile: int, y_tile: int, image_path: str, exit_p=False) -> None:
        coords_tiled = (x_tile - self.x_coord, y_tile - self.y_coord)
        center = self.get_center_tile_corner()
        corner_coord = (self.x_centr + center[0], self.y_centr + center[1])
        
        coords = (coords_tiled[0] + self.DRAW_DIST, 
                coords_tiled[1] + self.DRAW_DIST)

        if 0 <= coords[0] <= self.DRAW_DIST * 2 and 0 <= coords[1] <= self.DRAW_DIST * 2:
            resized = (coords[0] * SIZE + corner_coord[0], coords[1] * SIZE + corner_coord[1])
            point_sprite = Tile_entity(resized[0], resized[1], image_path)
            if exit_p:
                self.exit_point = point_sprite
            point_sprite.draw(surface)

    def draw_end(self, surface: pg.Surface):
        self._draw_point(surface, self.x_end, self.y_end, "./DATA/tmp/tiles/end-point.png", exit_p=True)

    def draw_start(self, surface: pg.Surface):
        self._draw_point(surface, self.x_start, self.y_start, "./DATA/tmp/tiles/start-point.png")

    def get_center_tile_corner(self) -> tuple[int, int]:
        center = self.floor_surface.get_rect().center
        up_left_draw_corner = center[0] - SIZE // 2, center[1] - SIZE // 2

        return (up_left_draw_corner[0] - (SIZE * self.DRAW_DIST + 1),
                up_left_draw_corner[1] - (SIZE * self.DRAW_DIST + 1))

    def draw_floor(self) -> None:
        center0 = self.get_center_tile_corner()
        center = center0[0] + self.x_centr, center0[1] + self.y_centr

        self.draw_tile(up_left_draw_corner=(center[0], center[1]), tile_type="./DATA/tmp/floor_sprite.png")

    def draw_tile(self, up_left_draw_corner: tuple[int, int], tile_type: str, wall: bool=False) -> None:
        if not wall:
            try:
                obj_ = Tile_entity(up_left_draw_corner[0],
                                   up_left_draw_corner[1], tile_type)
                self.floor = obj_
            except AttributeError:
                raise AttributeError("error")

        if wall:
            try:
                obj_ = Tile_entity(up_left_draw_corner[0],
                                   up_left_draw_corner[1], tile_type)
                self.wall.add(obj_)
            except AttributeError:
                raise AttributeError("error")
            
    def draw_minimap(self, surface: pg.Surface):
        width = height = 150
        margin = 20
        img = pg.image.load("./DATA/tmp/wall_sprite.png").convert_alpha()
        new_img = self.image = pg.transform.scale(img, (width, height))
        
        surface.blit(new_img, (surface.get_width()-(width+margin), margin))

    def draw_wall(self) -> None:
        self.wall = pg.sprite.Group()
        center = self.get_center_tile_corner()
        center = center[0] + self.x_centr, center[1] + self.y_centr

        TILEMAP = self.WORLD.get_map()

        render_list = TILEMAP[:]

        self.anti_allise()

        render_list = render_list[self.y_coord - self.DRAW_DIST:self.y_coord + self.DRAW_DIST + 1]

        for n, row in enumerate(render_list):
             render_list[n] = row[self.x_coord - self.DRAW_DIST:self.x_coord + self.DRAW_DIST + 1]

        for row, x_c in enumerate(range(center[0], center[0] + (SIZE * self.DRAW_DIST* 2) + 1, SIZE)):
            for col, y_c in enumerate(range(center[1], center[1] + (SIZE * self.DRAW_DIST * 2) + 1, SIZE)):
                try:
                    tile = self.search_tile(col, row, render_list)
                    if row < 0 or col < 0:
                        raise IndexError
                    elif tile != "floor":
                        self.draw_tile(up_left_draw_corner=(x_c, y_c), tile_type=self.tiles_img[tile], wall=True)
                except IndexError:
                    pass

    @staticmethod
    def search_tile(row: int, col: int, render_list: list[list[str]]) -> TILES:
        for tile, data in TILES.items():
            if data["ej"] == render_list[row][col]:
                return tile

    def get_world(self) -> MapGeneration:
        return self.WORLD

    def crop_tiles(self) -> None:
        image = Image.open("./DATA/reses/tileset/tileset.png")
        self.tiles_img: dict[str, str]= {}

        for tile, data in TILES.items():
            top_y, top_x = data['coord']
            top_x, top_y = (top_x - 1) * SIZE, (top_y - 1) * SIZE
            down_x, down_y = top_x + SIZE, top_y + SIZE

            nt = image.crop((top_x, top_y, down_x, down_y))

            tmppath = "\\DATA\\tmp\\tiles\\"

            if not os.path.exists(os.getcwd() + tmppath):
                os.mkdir(os.getcwd() + tmppath)

            path = f"./DATA/tmp/tiles/{tile}.png"
            nt.save(path)

            self.tiles_img[tile] = path

    def render_floor(self) -> None:
        dist = self.DRAW_DIST * 2 + 1

        print("Pre-Render Floor > ", end="")

        img_floor = Image.new('RGB', (SIZE * dist, SIZE * dist), 'black')
        for row in range(dist):
            for col in range(dist):
                tile = Image.open(self.tiles_img["floor"])
                img_floor.paste(tile, (col * 32, row * 32))

        img_floor.save("./DATA/tmp/floor_sprite.png")

        print("DONE!!!")

    def render_wall(self) -> None:
        WIDTH = HEIGHT = CONFIG['world_gen']['size']
        print("Pre-Render Wall  > ", end="")
        tilemap = self.WORLD.tilemap

        img_wall = Image.new('RGBA', (SIZE * WIDTH, SIZE * HEIGHT), (255, 0, 0, 0))
        for row in range(HEIGHT):
            for col in range(WIDTH):
                tile = self.search_tile(row, col, tilemap)
                if tile != "floor":
                    tile_img = Image.open(self.tiles_img[tile])
                    thresh = 3
                    r = tile_img.convert('L').point(lambda x : 255 if x > thresh else 0, mode='1')
                    img_wall.paste(r, (col * 32, row * 32))

        img_wall.save("./DATA/tmp/wall_sprite.png")

        print("DONE!!!")

    def pre_render_textures(self) -> None:
        print(">> PRE RENDERING:")
        self.render_wall()
        self.render_floor()
        print(">> DONE!!!")

    def center_point(self, other: int, operat: str) -> None:
        if operat == "+x" and self.x_coord > self.DRAW_DIST:
            self.x_centr += other
        if operat == "-x" and self.x_coord < (len(self.WORLD.get_map())-self.DRAW_DIST-1):
            self.x_centr -= other

        if operat == "+y" and self.y_coord > self.DRAW_DIST:
            self.y_centr += other
        if operat == "-y" and self.y_coord < (len(self.WORLD.get_map())-self.DRAW_DIST-1):
            self.y_centr -= other
        

        center0 = self.get_center_tile_corner()
        center = (center0[0] + self.x_centr), (center0[1] + self.y_centr)

        if (center0[0] - center[0]) > 32:
            self.x_centr = 0
            self.x_coord += 1
        if (center[0] - center0[0]) > 32:
            self.x_centr = 0
            self.x_coord -= 1

        if (center0[1] - center[1]) > 32:
            self.y_centr = 0
            self.y_coord += 1
        if (center[1] - center0[1]) > 32:
            self.y_centr = 0
            self.y_coord -= 1

        self.anti_allise()

    def anti_allise(self, get=False):
        if not get:
            if self.y_coord > (len(self.WORLD.get_map())-self.DRAW_DIST-1):
                self.y_coord = len(self.WORLD.get_map())-self.DRAW_DIST-1
            if self.y_coord < self.DRAW_DIST:
                self.y_coord = self.DRAW_DIST
            
            if self.x_coord > (len(self.WORLD.get_map())-self.DRAW_DIST-1):
                self.x_coord = len(self.WORLD.get_map())-self.DRAW_DIST-1
            if self.x_coord < self.DRAW_DIST:
                self.x_coord = self.DRAW_DIST
        
        if get:
            if self.y_coord >= (len(self.WORLD.get_map())-self.DRAW_DIST-1):
                return "y+"
            if self.y_coord <= self.DRAW_DIST:
                return "y-"
            
            if self.x_coord >= (len(self.WORLD.get_map())-self.DRAW_DIST-1):
                return "x+"
            if self.x_coord <= self.DRAW_DIST:
                return "x-"