import pygame
import pygame as pg

from MODULES.MAP.generate import MAP_GENERATION
from MODULES.RENDER.render_world import WorldClass
from MODULES.init import CONFIG, BLACK

FPS = int(CONFIG["pygame"]["FPS"])


def main(screen, size):

    clock = pg.time.Clock()
    game_surf = pygame.surface.Surface((int(size[0]), int(size[1])))
    gui_surf = pygame.surface.Surface((int(size[0]), int(size[1])))

    game_surf.set_colorkey(BLACK)
    gui_surf.set_colorkey(BLACK)

    WLD = MAP_GENERATION()
    World = WorldClass(WLD, screen, game_surf)

    World.generate_worldmap()

    running = True
    while running:
        screen.fill(BLACK)
        game_surf.fill(BLACK)
        gui_surf.fill(BLACK)
        World.groups_clear()


        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    World.center_point(0, 1, y_minus=True)
                if event.key == pg.K_s:
                    World.center_point(0, 1, y_plus=True)
                if event.key == pg.K_a:
                    World.center_point(1, 0, x_minus=True)
                if event.key == pg.K_d:
                    World.center_point(1, 0, x_plus=True)

        World.draw_floor()
        World.draw_wall()

        FLOOR = World.sprite_list_Floor()
        FLOOR.draw(screen)
        FLOOR.update()


        WALL = World.sprite_list_Wall()
        WALL.draw(game_surf)
        WALL.update()

        clock.tick(FPS)
        game_surf.blit(gui_surf, (0, 0))
        screen.blit(game_surf, (0, 0))
        pygame.display.flip()


