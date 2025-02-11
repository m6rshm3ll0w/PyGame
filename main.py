import pygame
from MODULES.init import CONFIG
from MODULES.RENDER.main import main_game_loop
from MODULES.BEST_RESULTS.best_results import ScoreTable
from MODULES.START_SCREEN.start_screen import start_screen
from MODULES.END_SCREEN.end_screen import EndScreen
from MODULES.audio import AudioPlayer

size = (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"])
f_size = (CONFIG["pygame"]["f_width"], CONFIG["pygame"]["f_height"])


if __name__ == "__main__":
    pygame.init()
    audio = AudioPlayer()
    audio.run()

    if CONFIG["pygame"]["fullscreen"] == "Yes":
        scr = pygame.display.set_mode(
            (int(f_size[0]), int(f_size[1])), pygame.FULLSCREEN)
    else:
        scr = pygame.display.set_mode((int(size[0]), int(size[1])))

    size = scr.get_size()
    flag = "menu"

    while True:
        if flag == "menu":
            flag = start_screen(scr, size, audio)

        if flag == "error" or flag == "quit":
            break

        if flag == "main_game":
            flag, time1, time2 = main_game_loop(scr, size, audio)
            if flag == "quit":
                break
            elif flag == 'win':
                flag = EndScreen(int(float(time2) - float(time1))).run(audio)
                if flag == 'quit':
                    break
            else:
                audio = AudioPlayer()
                audio.run()

        elif flag == "best_results":
            flag = ScoreTable().run(audio)
            if flag == 'quit':
                break

    audio.stop_music()
    pygame.quit()
