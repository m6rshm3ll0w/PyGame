from collections import deque
from MODULES.init import CONFIG, logger

def find_position(maze, char):
    logger.debug("searching position")
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == char:
                logger.debug("Sucsessful search position")
                return i, j
    logger.debug("point dont searched")
    return None

def is_valid_move(maze, x, y, visited):
    rows, cols = len(maze), len(maze[0])
    return 0 <= x < rows and 0 <= y < cols and maze[x][y] != CONFIG["world_gen"]["elements"]["wall"]["ej"] and not visited[x][y]

def bfs(maze, start, end):
    queue = deque([start])
    visited = [[False] * len(maze[0]) for _ in range(len(maze))]
    visited[start[0]][start[1]] = True

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            return True
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid_move(maze, new_x, new_y, visited):
                visited[new_x][new_y] = True
                queue.append((new_x, new_y))
    
    return False

def check_labirint(maze):
    logger.debug("check runable")
    start = find_position(maze, "X")
    end = find_position(maze, "Y")
    
    if not start or not end:
        logger.error("cant find start or end )")
        return "error"
    
    if bfs(maze, start, end):
        logger.debug("labirinnt is runble")
        return True
    else:
        logger.debug("labirinnt isnt runble")
        return False