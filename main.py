import pygame
from MODULES.init import CONFIG
from MODULES.RENDER.main import main_game_loop
from MODULES.BEST_RESULTS.best_results import ScoreTable
from MODULES.START_SCREEN.start_screen import start_screen
from MODULES.audio import AudioPlayer

size = (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"])
f_size = (CONFIG["pygame"]["f_width"], CONFIG["pygame"]["f_height"])

if __name__ == "__main__":
    pygame.init()
    audio = AudioPlayer()

    if CONFIG["pygame"]["fullscreen"] == "Yes":
        scr = pygame.display.set_mode(
            (int(f_size[0]), int(f_size[1])), pygame.FULLSCREEN)
    else:
        scr = pygame.display.set_mode((int(size[0]), int(size[1])))

    size = scr.get_size()

    while True:
        flag = start_screen(scr, size, audio)
        flag = "main_game"

        if flag == "error" or flag == "quit":
            break

        if flag == "main_game":
            game_flag = main_game_loop(scr, size, audio)
            if game_flag == "quit":
                break
            else:
                print(f"you win the game to {round(float(game_flag[2] - game_flag[1]), 3)}secs!!!!")
                break
        elif flag == "best_results":
            flag = ScoreTable().run()
            if flag == 'quit':
                break

    audio.stop_music()
    pygame.quit()
