from icecream import ic
from pydantic import BaseModel
import random
from MODULES.init import CONFIG

ELEMENTS = CONFIG['world_gen']['elements']
WIDTH = HEIGHT = CONFIG['world_gen']['size']
ITERATIONS = CONFIG['world_gen']['iterations']

MAP = [[ELEMENTS["empty"]["ej"]] * WIDTH for _ in range(HEIGHT)]

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


#  Точки спавна и выхода ↓↓↓↓↓↓↓↓


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


#  Открытие закрытых зон


def zone_fill(row, col, visited, open_zones):
    if (not (not (row < 0) and
             not (col < 0) and
             not (row >= HEIGHT) and
             not (col >= WIDTH)) or
            MAP[row][col] == ELEMENTS["wall"]["ej"] or
            visited[row][col]):
        return

    visited[row][col] = True
    open_zones.add((row, col))
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        zone_fill(row + dx, col + dy, visited, open_zones)


def identify_closed_zones():
    visited = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]
    open_zones, closed_zones = set(), []

    for row in range(HEIGHT):
        for col in range(WIDTH):
            if not visited[row][col] and MAP[row][col] == ELEMENTS["floor"]["ej"]:
                zone = set()
                zone_fill(row, col, visited, zone)
                if not (ELEMENTS["floor"]["ej"] in zone or
                        HEIGHT - 1 in [z[0] for z in zone] or
                        WIDTH - 1 in [z[1] for z in zone]):
                    closed_zones.append(zone)
                else:
                    open_zones.update(zone)

    return closed_zones, open_zones


def find_wall_candidates(closed_zones, open_zones):
    wall_candidates = []
    for zone in closed_zones:
        for row, col in zone:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = row + dx, col + dy
                if (0 <= nx < HEIGHT and
                    0 <= ny < WIDTH and
                    MAP[nx][ny] == ELEMENTS["wall"]["ej"] and
                    (nx, ny) not in zone and
                    (nx, ny) in open_zones):
                    wall_candidates.append((nx, ny))
    return wall_candidates


def rm_walls(wall_candidates):
    for wall_row, wall_col in wall_candidates:
        MAP[wall_row][wall_col] = ELEMENTS["floor"]["ej"]


def open_closed_zones():
    closed_zones, open_zones = identify_closed_zones()
    wall_candidates = find_wall_candidates(closed_zones, open_zones)
    return MAP


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

    MAP = open_closed_zones()

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
