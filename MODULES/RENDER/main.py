import pygame
import pygame as pg
from pygame.time import Clock
import time

from MODULES.ENTITYES.player import Player
from MODULES.RENDER.fog import fog_of_game
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


def load_images():
    keys = ['w', 't', 'a', 's', 'd']
    images = {}
    for key in keys:
        img = pygame.image.load(CONFIG['dirs']['pictures'][f'white_key_{key}'])
        images[key] = pygame.transform.scale(img, (40, 40))
    return images


def main_game_loop(screen: pygame.Surface, size: tuple[int, int], audio: AudioPlayer = AudioPlayer()) -> tuple[str , float, float]:
    clock = pg.time.Clock()
    center, floor_surf, game_surf, gui_surf = set_up_layers(size)

    world, player = create_object(floor_surf, game_surf)
    world.generate_world_map()
    world.render_floor()
    world.render_wall()

    fog = FogOfGame("./DATA/reses/fog/fog.png")
    draw_fog(fog, gui_surf)
    world.draw_minimap(gui_surf)

    images = load_images()

    font1 = pygame.font.Font(CONFIG["dirs"]["fonts"]["agat8"], 20)
    moving_surface = font1.render(CONFIG['main_game']['moving'], True, 'white')
    sound_surface = font1.render(CONFIG['main_game']['sound'], True, 'white')

    audio.run(CONFIG['dirs']['sounds']['game'])

    img = pygame.image.load(CONFIG['dirs']['pictures']['button'])
    img = pygame.transform.scale(
        img, (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"]))

    font2 = pygame.font.Font(CONFIG['dirs']['fonts']['agat8'], 30)
    menu = CONFIG['best_results']['menu']
    menu_surface = font2.render(menu, True, 'white')
    menu_rect = menu_surface.get_rect(topleft=(415, 530))
    menu_click_area = pygame.Rect(390, 518, 120, 50)

    start_time = time.time()

    running = True
    while running:

        clear_screen(screen, floor_surf, game_surf, gui_surf)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit", start_time, time.time()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t and pg.time.get_ticks() - st_time > 800:
                    audio.pause_unpause_music()
                    st_time = pg.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu_click_area.collidepoint(event.pos):
                        audio.stop_music()
                        return 'menu'

        keys = pygame.key.get_pressed()

        move_speed = CONFIG["player"]["speed"] // FPS

        if player.x - center[0] >= 64:
            world.center_point(move_speed, "-x")
        if player.y - center[1] >= 64:
            world.center_point(move_speed, "-y")
        if center[0] - player.x >= 64:
            world.center_point(move_speed, "+x")
        if center[1] - player.y >= 64:
            world.center_point(move_speed, "+y")

        # if keys[pygame.K_t] and audio.is_running and pg.time.get_ticks() - st_time > 500:
        #     audio.pause_unpause_music()
        #     st_time = pg.time.get_ticks()
        # elif keys[pygame.K_y] and not audio.is_running and pg.time.get_ticks() - st_time > 500:
        #     audio.pause_unpause_music()
        #     st_time = pg.time.get_ticks()

        update_map(world, floor_surf, game_surf)

        player.update(keys, center, world.wall)
        player.draw(game_surf)

        if player.exit_now(world.exit_point) == "win":
            return "win", start_time, time.time()

        update_screen(screen, floor_surf, game_surf, gui_surf, clock)
        guide_for_user(screen, images, moving_surface, sound_surface)

        screen.blit(img, (0, 0))
        screen.blit(menu_surface, menu_rect)

        pygame.display.flip()
    return "quit", start_time, time.time()
