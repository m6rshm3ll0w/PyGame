import pygame
import pygame as pg
from pygame.time import Clock
import time

from MODULES.ENTITYES.player import Player
from MODULES.RENDER.fog import FogOfGame
from MODULES.MAP.generate import MapGeneration
from MODULES.RENDER.render_world import WorldClass
from MODULES.init import CONFIG, BLACK
from MODULES.audio import AudioPlayer

FPS = int(CONFIG["pygame"]["FPS"])
SIZE = CONFIG['world_gen']['tile_set']["size"]


def update_map(World: WorldClass, screen: pygame.Surface, game_surf: pygame.Surface) -> None:
    World.draw_floor()
    World.draw_wall() 

    FLOOR = World.floor
    FLOOR.draw(screen)

    WALL = World.wall
    WALL.draw(game_surf)
    WALL.update()

    World.draw_points(game_surf)

def set_up_layers(size: tuple[int, int]) -> tuple[tuple[int, int], pygame.Surface, pygame.Surface, pygame.Surface]:
    floor_surf = pygame.surface.Surface((int(size[0]), int(size[1])))
    game_surf = pygame.surface.Surface((int(size[0]), int(size[1])))
    gui_surf = pygame.surface.Surface((int(size[0]), int(size[1])))
    game_surf.set_colorkey(BLACK)
    gui_surf.set_colorkey(BLACK)
    floor_surf.set_colorkey(BLACK)

    center = game_surf.get_rect().center

    return center, floor_surf, game_surf, gui_surf


def create_object(screen: pygame.Surface, 
                  game_surf: pygame.Surface) -> tuple[WorldClass, Player]:
    world = WorldClass(MapGeneration(), screen, game_surf)
    
    coords_tiled = (0, 0)
    corner = world.get_center_tile_corner()
    center = (coords_tiled[0] * SIZE + corner[0] + (world.DRAW_DIST) * SIZE, 
                coords_tiled[1] * SIZE + corner[1] + (world.DRAW_DIST) * SIZE)

    player = Player(x=center[0], y=center[1])

    return world, player


def update_screen(screen: pygame.Surface, 
                  floor_surf: pygame.Surface, 
                  game_surf: pygame.Surface, 
                  gui_surf: pygame.Surface, 
                  clock: Clock) -> None:
    clock.tick(int(FPS))
    game_surf.blit(gui_surf, (0, 0))
    floor_surf.blit(game_surf, (0, 0))
    screen.blit(floor_surf, (0, 0))
    pygame.display.flip()


def clear_screen(screen: pygame.Surface, 
                 floor_surf: pygame.Surface, 
                 game_surf: pygame.Surface, 
                 gui_surf: pygame.Surface) -> None:
    screen.fill(BLACK)
    floor_surf.fill(BLACK)
    game_surf.fill(BLACK)
    # gui_surf.fill(BLACK)


def draw_fog(obj: FogOfGame, screen: pygame.Surface) -> None:
    obj.draw(screen)



def main_game_loop(screen: pygame.Surface, size: tuple[int, int], audio: AudioPlayer) -> tuple[str , float, float]:
    # audio.unpause_music()

    pg.event.set_allowed([pg.QUIT])

    clock = pg.time.Clock()

    center, floor_surf, game_surf, gui_surf = set_up_layers(size)

    world, player = create_object(floor_surf, game_surf)
    world.generate_world_map()
    world.change_start_point()
    world.pre_render_textures()

    fog = FogOfGame("./DATA/reses/fog/fog.png")
    draw_fog(fog, gui_surf)
    world.draw_minimap(gui_surf)

    start_time = time.time()
    running = True
    while running:
        clear_screen(screen, floor_surf, game_surf, gui_surf)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit", start_time, time.time()

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


        player.update(keys, center, world.wall)


        player.draw(game_surf)

        if player.exit_now(world.exit_point) == "win":
            return "win", start_time, time.time()

        update_screen(screen, floor_surf, game_surf, gui_surf, clock)

        # print(f"FPS {1//(time_end - time_start):.1f}")

    return "quit", start_time, time.time()


