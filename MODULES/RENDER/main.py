import pygame
import pygame as pg

from MODULES.Entitys.player import Player as Player_class
from MODULES.MAP.generate import MAP_GENERATION
from MODULES.RENDER.render_world import WorldClass
from MODULES.init import CONFIG, BLACK

FPS = int(CONFIG["pygame"]["FPS"])


def upd_map(World, screen, game_surf):
    World.draw_floor()
    World.draw_wall()

    FLOOR = World.sprite_list_Floor()
    FLOOR.draw(screen)
    FLOOR.update()

    WALL = World.sprite_list_Wall()
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


def create_obj(screen, game_surf):
    World = WorldClass(MAP_GENERATION(), screen, game_surf)
    Player = Player_class(x=int(game_surf.get_width() // 2), y=int(game_surf.get_height() // 2))

    return World, Player


def update_screen(screen, floor_surf, game_surf, gui_surf, clock):
    clock.tick(int(FPS))
    game_surf.blit(gui_surf, (0, 0))
    floor_surf.blit(game_surf, (0, 0))
    screen.blit(floor_surf, (0, 0))
    pygame.display.flip()


def clear_screen(screen, floor_surf, game_surf, gui_surf, World):
    screen.fill(BLACK)
    floor_surf.fill(BLACK)
    game_surf.fill(BLACK)
    gui_surf.fill(BLACK)
    World.groups_clear()


def main(screen, size):
    pg.event.set_allowed([pg.QUIT])

    clock = pg.time.Clock()

    center, floor_surf, game_surf, gui_surf = set_up_layers(size)

    World, Player = create_obj(floor_surf, game_surf)
    World.generate_worldmap()

    running = True
    while running:
        clear_screen(screen, floor_surf, game_surf, gui_surf, World)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if (Player.x - center[0]) >= 64:
            World.center_point(200//FPS, "-x")
        if (Player.y - center[1]) >= 64:
            World.center_point(200//FPS, "-y")
        if (center[0] - Player.x) >= 64:
            World.center_point(200//FPS, "+x")
        if (center[1] - Player.y) >= 64:
            World.center_point(200//FPS, "+y")

        Player.move(keys, center)

        upd_map(World, floor_surf, game_surf)
        Player.draw(game_surf)

        update_screen(screen, floor_surf, game_surf, gui_surf, clock)



