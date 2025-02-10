import pygame
import pygame as pg

from MODULES.ENTITYES.player import Player
from MODULES.RENDER.fog import fog_of_game
from MODULES.MAP.generate import MapGeneration
from MODULES.RENDER.render_world import WorldClass
from MODULES.init import CONFIG, BLACK
from MODULES.audio import AudioPlayer

FPS = int(CONFIG["pygame"]["FPS"])


def update_map(World, screen, game_surf):
    World.draw_floor()
    World.draw_wall()
    World.FLOOR.draw(screen)
    World.WALL.draw(game_surf)
    World.WALL.update()


def set_up_layers(size):
    layers = {name: pygame.Surface(size).convert_alpha()
              for name in ["floor", "game", "gui"]}
    for surf in layers.values():
        surf.set_colorkey(BLACK)
    return layers["game"].get_rect().center, layers["floor"], layers["game"], layers["gui"]


def create_object(screen, game_surf):
    return WorldClass(MapGeneration(), screen, game_surf), Player(game_surf.get_width() // 2, game_surf.get_height() // 2)


def update_screen(screen, floor_surf, game_surf, gui_surf, clock):
    clock.tick(FPS)
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


def load_images():
    keys = ['w', 't', 'a', 's', 'd']
    images = {}
    for key in keys:
        img = pygame.image.load(CONFIG['dirs']['pictures'][f'white_key_{key}'])
        images[key] = pygame.transform.scale(img, (40, 40))
    return images


def guide_for_user(screen, images, moving_surface, sound_surface):
    key_positions = {'w': (55, 10), 't': (55, 150), 'a': (
        10, 55), 's': (55, 55), 'd': (100, 55)}
    for key, pos in key_positions.items():
        screen.blit(images[key], pos)
    screen.blit(moving_surface, (40, 110))
    screen.blit(sound_surface, (20, 205))


def main_game_loop(screen, size):
    pg.event.set_allowed([pg.QUIT])

    clock = pg.time.Clock()

    center, floor_surf, game_surf, gui_surf = set_up_layers(size)
    world, player = create_object(floor_surf, game_surf)
    world.generate_world_map()
    world.render_floor()
    world.render_wall()

    fog = fog_of_game("./DATA/reses/fog/fog.png")
    st_time = pg.time.get_ticks()

    images = load_images()

    font1 = pygame.font.Font(CONFIG["dirs"]["fonts"]["agat8"], 20)
    moving_surface = font1.render(CONFIG['main_game']['moving'], True, 'white')
    sound_surface = font1.render(CONFIG['main_game']['sound'], True, 'white')

    audio = AudioPlayer()
    audio.run(CONFIG['dirs']['sounds']['game'])

    img = pygame.image.load(CONFIG['dirs']['pictures']['button'])
    img = pygame.transform.scale(
        img, (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"]))

    font2 = pygame.font.Font(CONFIG['dirs']['fonts']['agat8'], 30)
    menu = CONFIG['best_results']['menu']
    menu_surface = font2.render(menu, True, 'white')
    menu_rect = menu_surface.get_rect(topleft=(415, 530))
    menu_click_area = pygame.Rect(390, 518, 120, 50)

    running = True
    while running:

        clear_screen(screen, floor_surf, game_surf, gui_surf, world)
        draw_fog(fog, gui_surf)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return 'quit'
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
        move_speed = 200 // FPS

        if player.x - center[0] >= 64:
            world.center_point(move_speed, "-x")
        if player.y - center[1] >= 64:
            world.center_point(move_speed, "-y")
        if center[0] - player.x >= 64:
            world.center_point(move_speed, "+x")
        if center[1] - player.y >= 64:
            world.center_point(move_speed, "+y")

        if keys[pygame.K_t] and audio.is_running and pg.time.get_ticks() - st_time > 500:
            audio.pause_unpause_music()
            st_time = pg.time.get_ticks()

        elif keys[pygame.K_y] and not audio.is_running and pg.time.get_ticks() - st_time > 500:
            audio.pause_unpause_music()
            st_time = pg.time.get_ticks()

        update_map(world, floor_surf, game_surf)

        player.update(keys, center, world.WALL)
        player.draw(game_surf)

        update_screen(screen, floor_surf, game_surf, gui_surf, clock)

        guide_for_user(screen, images, moving_surface, sound_surface)

        screen.blit(img, (0, 0))
        screen.blit(menu_surface, menu_rect)

        pygame.display.flip()
