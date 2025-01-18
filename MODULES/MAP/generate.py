import math

from pydantic import BaseModel
import random
from MODULES.init import CONFIG
from MODULES.MAP.tileset_use import MAP2TILEMAP


#  Классы обьектов ↓↓↓↓↓↓↓↓↓
class Item(BaseModel):
    name: str
    ej: str


class Enemy(BaseModel):
    name: str
    health: int
    speed: int
    perc: int


class Chest(BaseModel):
    loot: list[Item]
    coord: dict[str, int]


class Spawner(BaseModel):
    enemies: list[Enemy]
    timeout: float
    coord: dict[str, int]


class World(BaseModel):
    size: int
    elements: dict
    start_point: dict[str, int] = {"row": 10, "col": 10}
    end_point: dict[str, int] = {"row": 10, "col": 10}
    chests: list[Chest] = None
    spawners: list[Spawner] = None


#  Генерация карты ↓↓↓↓↓↓↓
class MAP_GENERATION:
    def __init__(self):
        self.data = None
        self.TILEMAP = None
        self.ELEMENTS = CONFIG['world_gen']['elements']
        self.WIDTH = self.HEIGHT = CONFIG['world_gen']['size']
        self.ITERATIONS = CONFIG['world_gen']['iterations']
        self.MAP = [[self.ELEMENTS["empty"]["ej"]] * self.WIDTH for _ in range(self.HEIGHT)]
        self.DIST = CONFIG['world_gen']['s-p_dist']

    def get_neighbors(self, row, col):
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.HEIGHT and 0 <= nc < self.WIDTH:
                    neighbors.append(self.MAP[nr][nc])
        return neighbors

    def check_rules(self, row, col):
        current_tile = self.MAP[row][col]
        neighbors = self.get_neighbors(row, col)

        if current_tile == self.ELEMENTS["empty"]["ej"]:
            if (random.randint(1, 2) == 1 and
                    random.randint(1, 100) <= self.ELEMENTS["floor"]["perc"]):
                return self.ELEMENTS["floor"]["ej"]
            elif (random.randint(1, 2) == 2 and
                  random.randint(1, 100) <= self.ELEMENTS["wall"]["perc"]):
                return self.ELEMENTS["wall"]["ej"]

        elif current_tile == self.ELEMENTS["wall"]["ej"]:
            if (neighbors.count(self.ELEMENTS["wall"]["ej"]) >= 5 or
                    neighbors.count(self.ELEMENTS["floor"]["ej"]) == 8):
                return self.ELEMENTS["floor"]["ej"]
            elif (neighbors.count(self.ELEMENTS["wall"]["ej"]) >= 3 and
                  neighbors.count(self.ELEMENTS["floor"]["ej"]) < 4):
                return self.ELEMENTS["floor"]["ej"]

        elif current_tile == self.ELEMENTS["floor"]["ej"]:
            if (neighbors.count(self.ELEMENTS["wall"]["ej"]) == 2 and
                    neighbors.count(self.ELEMENTS["floor"]["ej"]) == 5):
                return self.ELEMENTS["wall"]["ej"]

        return current_tile

    def search_points(self):
        points_of_end = []

        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                neighbors = self.get_neighbors(row, col)
                if neighbors.count(self.ELEMENTS["floor"]["ej"]) == 8:
                    points_of_end.append((row, col))

        total_points = len(points_of_end)
        random.shuffle(points_of_end)

        r_p = random.randint(a=0, b=total_points)-1

        er = points_of_end[r_p][0]
        ec = points_of_end[r_p][1]

        points_of_start = []
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                neighbors = self.get_neighbors(row, col)

                d = math.sqrt(abs((er - row) ** 2 - (ec - col) ** 2))
                if neighbors.count(self.ELEMENTS["wall"]["ej"]) >= 5 and d >= self.DIST:
                    points_of_start.append((row, col))

        total_points = len(points_of_start)-1
        random.shuffle(points_of_start)

        r_p = random.randint(a=0, b=total_points)

        sr = points_of_start[r_p][0]
        sc = points_of_start[r_p][1]

        return {"row": er, "col": ec}, {"row": sr, "col": sc}

    def generate_iteration(self):
        new_map = [_row[:] for _row in self.MAP]
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                new_map[row][col] = self.check_rules(row, col)
        return new_map


    def add_borders(self):
        self.MAP[0] = [self.ELEMENTS["wall"]["ej"]] * self.WIDTH
        self.MAP[-1] = [self.ELEMENTS["wall"]["ej"]] * self.WIDTH

        for row in range(self.HEIGHT):
            self.MAP[row][0] = self.ELEMENTS["wall"]["ej"]
            self.MAP[row][-1] = self.ELEMENTS["wall"]["ej"]

        self.generate_iteration()


    def generate_world(self):
        for _ in range(self.ITERATIONS):
            self.MAP = self.generate_iteration()

        self.add_borders()

        end_p, start_p = self.search_points()
        self.MAP[end_p["row"]][end_p["col"]] = self.ELEMENTS["end_point"]["ej"]
        self.MAP[start_p["row"]][start_p["col"]] = self.ELEMENTS["start_point"]["ej"]
        self.data = World(size=self.WIDTH, elements=self.ELEMENTS, start_point=start_p,
                          end_point=end_p)


        ref = MAP2TILEMAP()
        ref.reformat(self.MAP)

        self.TILEMAP = ref.get_tilemap()

        with open("./DATA/world/map-simple.dat", "w", encoding="UTF-8") as map_file:
            for row in range(self.HEIGHT):
                map_file.write("".join(self.MAP[row]) + "\n")

        with open("./DATA/world/map-tiled.dat", "w", encoding="UTF-8") as map_file:
            for row in range(self.HEIGHT):
                map_file.write("$".join(self.TILEMAP[row]) + "\n")

        with open("./DATA/world/world.json", "w", encoding="UTF-8") as conf:
            conf.write(self.data.model_dump_json())

    def get_map(self):
        if self.MAP is None and self.TILEMAP is None:
            raise ValueError("You dont generated the map!!!!")
        else:
            return self.TILEMAP

    def get_data(self):
        if self.data is None:
            raise ValueError("You dont generated the map!!!!")
        else:
            return self.data