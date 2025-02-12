from csv import Error
import math

from pydantic import BaseModel
import random

from MODULES.init import CONFIG
from MODULES.MAP.tileset_use import MAP2TILEMAP
from MODULES.MAP.check_runble import check_labirint


class World(BaseModel):
    size: int
    elements: dict[str, dict[str, str | int]]
    start_point: dict[str, int] = {"row": 10, "col": 10}
    end_point: dict[str, int] = {"row": 20, "col": 20}

#  Генерация карты ↓↓↓↓↓↓↓
class MapGeneration:
    def __init__(self):
        self.data: World

        self.tilemap: list[list[str]] = []
        self.ELEMENTS = CONFIG['world_gen']['elements']
        self.WIDTH = self.HEIGHT = CONFIG['world_gen']['size']
        self.ITERATIONS = CONFIG['world_gen']['iterations']
        self.DIST = CONFIG['world_gen']['s-p_dist']

        self.map: list[list[str]] = [[self.ELEMENTS["empty"]["ej"]] * self.WIDTH for _ in range(self.HEIGHT)]

    def get_neighbors(self, row: int, col: int) -> list[str]:
        neighbors:list[str] = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.HEIGHT and 0 <= nc < self.WIDTH:
                    neighbors.append(self.map[nr][nc])
        return neighbors

    def check_rules(self, row: int, col: int) -> str:
        current_tile = self.map[row][col]
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

    def search_points(self) -> tuple[dict[str, int], dict[str, int]]:
        points_of_end: list[tuple[int, int]] = []

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

        points_of_start: list[tuple[int, int]] = []

        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                neighbors = self.get_neighbors(row, col)

                d = math.sqrt(abs((er - row) ** 2 - (ec - col) ** 2))
                if neighbors.count(self.ELEMENTS["wall"]["ej"]) >= 5 and d >= self.DIST:
                    points_of_start.append((row, col))

        total_points = len(points_of_start)-1
        random.shuffle(points_of_start)

        r_p = random.randint(a=0, b=total_points)

        sr: int = points_of_start[r_p][0]
        sc: int = points_of_start[r_p][1]

        return {"row": er, "col": ec}, {"row": sr, "col": sc}

    def generate_iteration(self) -> list[list[str]]:
        new_map = [_row[:] for _row in self.map]
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                new_map[row][col] = self.check_rules(row, col)
        return new_map


    def add_borders(self) -> None:
        self.map[0] = [self.ELEMENTS["wall"]["ej"]] * self.WIDTH
        self.map[-1] = [self.ELEMENTS["wall"]["ej"]] * self.WIDTH

        for row in range(self.HEIGHT):
            self.map[row][0] = self.ELEMENTS["wall"]["ej"]
            self.map[row][-1] = self.ELEMENTS["wall"]["ej"]

        self.generate_iteration()


    def generate_all_iters(self) -> None:
        for _ in range(self.ITERATIONS):
            self.map = self.generate_iteration()


    def generate_world(self):

        try_ = 1
        check = False
        while not check:
            self.map: list[list[str]] = [[self.ELEMENTS["empty"]["ej"]] * self.WIDTH for _ in range(self.HEIGHT)]
            self.add_borders()
            self.generate_all_iters()

            end_p, start_p = self.search_points()
            self.map[end_p["row"]][end_p["col"]] = self.ELEMENTS["end-point"]["ej"]
            self.map[start_p["row"]][start_p["col"]] = self.ELEMENTS["start-point"]["ej"]
            
            check = check_labirint(self.map)

            print(try_, check)
            try_ += 1

        self.data = World(size=self.WIDTH, elements=self.ELEMENTS, start_point=start_p,
                          end_point=end_p)
        
        for r in [-1,0,1]:
            for c in [-1,0,1]:
                if r == 0 and c == 0:
                    pass
                else:
                    self.map[start_p["row"] + r][start_p["col"] + c] = self.ELEMENTS["floor"]["ej"]

        self.add_borders()

        ref = MAP2TILEMAP()
        ref.reformat(self.map)

        self.tilemap = ref.get_tilemap()

        with open("./DATA/world/map-simple.dat", "w", encoding="UTF-8") as map_file:
            for row in range(self.HEIGHT):
                map_file.write("".join(self.map[row]) + "\n")

        with open("./DATA/world/map-tiled.dat", "w", encoding="UTF-8") as map_file:
            for row in range(self.HEIGHT):
                map_file.write("$".join(self.tilemap[row]) + "\n")

        with open("./DATA/world/world.json", "w", encoding="UTF-8") as conf:
            conf.write(self.data.model_dump_json())

    def get_map(self) -> list[list[str]]:
            try:
                return self.tilemap
            except Error:
                raise ValueError("Tilemap not generated yet!")

    def get_data(self) -> World:
        try:
            return self.data
        except Error:
            raise ValueError("You don't generated the map!!!!")