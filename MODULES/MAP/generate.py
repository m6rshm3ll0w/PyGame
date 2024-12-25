from icecream import ic
from pydantic import BaseModel
import random
from MODULES.init import CONFIG

ELEMENTS = CONFIG['world_gen']['elements']
WIDTH = HEIGHT = CONFIG['world_gen']['size']
ITERATIONS = CONFIG['world_gen']['iterations']

MAP = [[ELEMENTS["empty"]["ej"]] * WIDTH for _ in range(HEIGHT)]
START_POINT: tuple = (0, 0)


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


def get_neighbors(row, col):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < HEIGHT and 0 <= nc < WIDTH:
                neighbors.append(MAP[nr][nc])
    return neighbors


def check_rules(row, col):
    current_tile = MAP[row][col]
    neighbors = get_neighbors(row, col)

    if current_tile == ELEMENTS["empty"]["ej"]:
        if random.randint(1, 2) == 1 and random.randint(1, 100) <= ELEMENTS["floor"]["perc"]:
            return ELEMENTS["floor"]["ej"]
        elif random.randint(1, 2) == 2 and random.randint(1, 100) <= ELEMENTS["wall"]["perc"]:
            return ELEMENTS["wall"]["ej"]

    elif current_tile == ELEMENTS["wall"]["ej"]:
        if neighbors.count(ELEMENTS["wall"]["ej"]) >= 5 or neighbors.count(ELEMENTS["floor"]["ej"]) == 8:
            return ELEMENTS["floor"]["ej"]
        elif neighbors.count(ELEMENTS["wall"]["ej"]) >= 3 and neighbors.count(ELEMENTS["floor"]["ej"]) < 4:
            return ELEMENTS["floor"]["ej"]

    elif current_tile == ELEMENTS["floor"]["ej"]:
        if neighbors.count(ELEMENTS["wall"]["ej"]) == 2 and neighbors.count(ELEMENTS["floor"]["ej"]) == 5:
            return ELEMENTS["wall"]["ej"]

    return current_tile


def search_sp(_MAP) -> dict[str, int]:
    points_of_start = []

    for row in range(HEIGHT):
        for col in range(WIDTH):
            neighbors = get_neighbors(row, col)
            if neighbors.count(ELEMENTS["wall"]["ej"]) >= 5:
                points_of_start.append((row, col))

    total_points = len(points_of_start)
    random.shuffle(points_of_start)

    r_p = random.randint(a=0, b=total_points)

    sr = points_of_start[r_p][0]
    sc = points_of_start[r_p][1]

    return {"row": sr, "col": sc}


def search_ep(_MAP) -> dict[str, int]:
    points_of_end = []

    for row in range(HEIGHT):
        for col in range(WIDTH):
            neighbors = get_neighbors(row, col)
            if neighbors.count(ELEMENTS["floor"]["ej"]) == 8:
                points_of_end.append((row, col))

    total_points = len(points_of_end)
    random.shuffle(points_of_end)

    r_p = random.randint(a=0, b=total_points)

    sr = points_of_end[r_p][0]
    sc = points_of_end[r_p][1]

    return {"row": sr, "col": sc}


def generate_iteration():
    new_map = [row_[:] for row_ in MAP]
    for row in range(HEIGHT):
        for col in range(WIDTH):
            new_map[row][col] = check_rules(row, col)
    return new_map


def generate_world():
    global MAP
    for _ in range(ITERATIONS):
        MAP = generate_iteration()

    start_p = search_sp(MAP)
    MAP[start_p["row"]][start_p["col"]] = ELEMENTS["start_point"]["ej"]

    end_p = search_ep(MAP)
    MAP[end_p["row"]][end_p["col"]] = ELEMENTS["end_point"]["ej"]

    with open("./DATA/world/map.txt", "w", encoding="UTF-8") as map_file:
        for row in range(HEIGHT):
            map_file.write("".join(MAP[row]) + "\n")

    with open("./DATA/world/world.json", "w", encoding="UTF-8") as conf:
        conf.write(World(size=10, elements=ELEMENTS, start_point=start_p, end_point=end_p).model_dump_json())


generate_world()