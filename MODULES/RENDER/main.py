import pygame
import pygame as pg
from pygame.time import Clock
import time

from MODULES.ENTITYES.player import Player
from MODULES.RENDER.fog import FogOfGame
from MODULES.MAP.generate import MapGeneration
from MODULES.RENDER.render_world import WorldClass
from MODULES.init import CONFIG, BLACK, logger
from MODULES.AUDIO.audio import AudioPlayer

FPS = int(CONFIG["pygame"]["FPS"])
SIZE = CONFIG['world_gen']['tile_set']["size"]


class MainGameLoop:
    def __init__(self, screen: pygame.Surface, size: tuple[int, int], audio: AudioPlayer):
        self.screen = screen
        self.size = size
        self.clock = pg.time.Clock()
        self.running = True
        self.start_time = time.time()
        self.audio = audio
        self.center, self.floor_surf, self.game_surf, self.gui_surf = self.set_up_layers()
        self.world, self.player = self.create_objects()
        self.fog = FogOfGame("./DATA/reses/fog/fog.png")
        self.menu_click_area = pygame.Rect(390, 518, 120, 50)

    def set_up_layers(self) -> tuple[tuple[int, int], pygame.Surface, pygame.Surface, pygame.Surface]:
        floor_surf = pygame.Surface(self.size)
        game_surf = pygame.Surface(self.size)
        gui_surf = pygame.Surface(self.size)

        for surf in (floor_surf, game_surf, gui_surf):
            surf.set_colorkey(BLACK)

        center = (game_surf.get_rect().center[0] - SIZE / 2,
                  game_surf.get_rect().center[1] - SIZE / 2)
        logger.info("Surfaces set up")
        return center, floor_surf, game_surf, gui_surf

    def create_objects(self) -> tuple[WorldClass, Player]:
        world = WorldClass(MapGeneration(), self.screen, self.game_surf)
        world.generate_world_map()
        world.render_floor()
        world.render_wall()
        world.change_start_point()
        
        center = world.get_center_tile_corner()
        center = (world.DRAW_DIST * SIZE + center[0], world.DRAW_DIST * SIZE + center[1])
        player = Player(x=center[0], y=center[1])

        logger.info("World and Player classes created")
        return world, player

    def update_screen(self):
        self.clock.tick(FPS)
        self.game_surf.blit(self.gui_surf, (0, 0))
        self.floor_surf.blit(self.game_surf, (0, 0))
        self.screen.blit(self.floor_surf, (0, 0))
        self.timer()
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill(BLACK)
        self.floor_surf.fill(BLACK)
        self.game_surf.fill(BLACK)

    def timer(self):
        font_over = pygame.font.Font(CONFIG["dirs"]["fonts"]["fontover"], 25)
        now_time = time.time() - self.start_time
        mins, secs = divmod(int(now_time), 60)
        ms = int((now_time * 1000) % 1000)
        timer_txt = font_over.render(f"{mins}:{secs:02}.{ms:03}", True, 'white')
        self.screen.blit(timer_txt, (740, 550))

    def guide_for_user(self):
        logger.info("creating tips")
        logger.info("setup fonts")
        agat8_20 = pygame.font.Font(CONFIG["dirs"]["fonts"]["agat8"], 20)
        agat8_30 = pygame.font.Font(CONFIG['dirs']['fonts']['agat8'], 30)
        agat8_15 = pygame.font.Font(CONFIG['dirs']['fonts']['agat8'], 15)

        logger.info("render text")
        menu_txt = agat8_30.render(CONFIG['best_results']['menu'], True, 'white')
        moving_txt =agat8_20.render(CONFIG['main_game']['moving'], True, 'white')
        sound_txt = agat8_20.render(CONFIG['main_game']['sound'], True, 'white')

        map_txt = agat8_15.render("MAP", True, 'white')
        todo_txt = agat8_15.render("Tasks:", True, 'white')
        task_txt = agat8_15.render("> Find exit!", True, 'white')

        # M.F.D: if you see a bug, simply restart the level, check your luck
        logger.info("loading pictures")

        keys = ['w', 't', 'a', 's', 'd']
        images = {}
        for key in keys:
            img = pygame.image.load(CONFIG['dirs']['pictures'][f'white_key_{key}'])
            images[key] = pygame.transform.scale(img, (40, 40))

        key_positions = {'w': (55, 10), 't': (55, 150), 'a': (
            10, 55), 's': (55, 55), 'd': (100, 55)}
        for key, pos in key_positions.items():
            self.gui_surf.blit(images[key], pos)

        img = pygame.image.load(CONFIG['dirs']['pictures']['button']).convert_alpha()
        img = pygame.transform.scale(
            img, (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"]))
        
        logger.info("blit tips to screen")
        self.gui_surf.blit(img, (0, 0))

        self.gui_surf.blit(moving_txt, (40, 110))
        self.gui_surf.blit(sound_txt, (20, 205))
        self.gui_surf.blit(menu_txt, (415, 530))
        
        self.gui_surf.blit(map_txt, (650+80, 20))
        self.gui_surf.blit(todo_txt, (650+80, 180+20))
        self.gui_surf.blit(task_txt, (655+80, 195+20))

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                self.audio.pause_unpause_music()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_click_area.collidepoint(event.pos):
                    self.audio.stop_music()
                    return "menu"
        return None

    def run(self):
        logger.info("Game is running")
        self.audio.run(CONFIG['dirs']['sounds']['game'])

        self.fog.draw(self.gui_surf)
        self.world.draw_minimap(self.gui_surf)
        self.guide_for_user()
        
        while self.running:
            self.clear_screen()
            action = self.handle_events()
            if action:
                return action, self.start_time, time.time()

            keys = pygame.key.get_pressed()
            move_speed = CONFIG["player"]["speed"] // FPS
            error = (self.player.x + SIZE / 2 - self.center[0],
                     self.player.y + SIZE / 2 - self.center[1])
            
            if error[0] <= 12:
                self.world.center_point(move_speed, "+x")
            if error[0] >= -12:
                self.world.center_point(move_speed, "-x")
            if error[1] <= 12:
                self.world.center_point(move_speed, "+y")
            if error[1] >= -12:
                self.world.center_point(move_speed, "-y")

            self.world.draw_floor()
            self.world.draw_wall()
            self.world.floor.draw(self.floor_surf)
            self.world.wall.draw(self.game_surf)
            self.world.wall.update()
            self.world.draw_points(self.game_surf)

            self.player.update(keys, self.center, self.world)
            self.player.draw(self.game_surf)

            if self.player.exit_now(self.world.exit_point) == "win":
                logger.info("Game won!")
                return "win", self.start_time, time.time()

            self.update_screen()
        
        return "quit", self.start_time, time.time()