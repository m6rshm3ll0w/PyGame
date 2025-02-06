import pygame
import pygame as pg
import time


from MODULES.ENTITYES.player import Player
from MODULES.RENDER.fog import fog_of_game
from MODULES.MAP.generate import MapGeneration
from MODULES.RENDER.render_world import WorldClass
from MODULES.init import CONFIG, BLACK

FPS = int(CONFIG["pygame"]["FPS"])


def update_map(World, screen, game_surf):
    World.draw_floor()
    World.draw_wall() 
    FLOOR = World.FLOOR
    FLOOR.draw(screen)

    WALL = World.WALL
    WALL.draw(game_surf)
    WALL.update()


def set_up_layers(size):
    floor_surf = pygame.surface.Surface((int(size[0]), int(size[1])))
    game_surf = pygame.surface.Surface((int(size[0]), int(size[1])))
    gui_surf = pygame.surface.Surface((int(size[0]), int(size[1])))
    game_surf.set_colorkey(BLACK)
    gui_surf.set_colorkey(BLACK)
    floor_surf.set_colorkey(BLACK)

    center = game_surf.get_rect().center

    return center, floor_surf, game_surf, gui_surf


def create_object(screen, game_surf):
    world = WorldClass(MapGeneration(), screen, game_surf)
    player = Player(x=int(game_surf.get_width() // 2), y=int(game_surf.get_height() // 2))

    return world, player


def update_screen(screen, floor_surf, game_surf, gui_surf, clock):
    clock.tick(int(FPS))
    game_surf.blit(gui_surf, (0, 0))
    floor_surf.blit(game_surf, (0, 0))
    screen.blit(floor_surf, (0, 0))
    pygame.display.flip()


def clear_screen(screen, floor_surf, game_surf, gui_surf, world):
    screen.fill(BLACK)
    floor_surf.fill(BLACK)
    game_surf.fill(BLACK)
    gui_surf.fill(BLACK)
    world.groups_clear()

def draw_fog(obj, screen):
    obj.draw(screen)



def main_game_loop(screen, size):
    pg.event.set_allowed([pg.QUIT])

    clock = pg.time.Clock()

    center, floor_surf, game_surf, gui_surf = set_up_layers(size)

    world, player = create_object(floor_surf, game_surf)
    world.generate_world_map()
    world.render_floor()
    world.render_wall()

    fog = fog_of_game("./DATA/reses/fog/fog.png")

    running = True
    while running:
        time_start = time.time()
        clear_screen(screen, floor_surf, game_surf, gui_surf, world)
        draw_fog(fog, gui_surf)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if (player.x - center[0]) >= 64:
            world.center_point(200//FPS, "-x")
        if (player.y - center[1]) >= 64:
            world.center_point(200//FPS, "-y")
        if (center[0] - player.x) >= 64:
            world.center_point(200//FPS, "+x")
        if (center[1] - player.y) >= 64:
            world.center_point(200//FPS, "+y")


        update_map(world, floor_surf, game_surf)

        player.update(keys, center, world.WALL)
        player.draw(game_surf)

        update_screen(screen, floor_surf, game_surf, gui_surf, clock)

        time_end = time.time()
        # print(f"FPS {1//(time_end - time_start):.1f}")



