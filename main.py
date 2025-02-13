import pygame
from MODULES.init import CONFIG, check_tmp, set_logging, logger
from MODULES.RENDER.main import MainGameLoop
from MODULES.BEST_RESULTS.best_results import ScoreTable
from MODULES.START_SCREEN.start_screen import StartScreen
from MODULES.END_SCREEN.end_screen import EndScreen
from MODULES.AUDIO.audio import AudioPlayer


size = (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"])
f_size = (CONFIG["pygame"]["f_width"], CONFIG["pygame"]["f_height"])


if __name__ == "__main__":
    check_tmp()
    set_logging()

    pygame.init()
    audio = AudioPlayer()
    audio.run()
    logger.info("Audio configured")

    if CONFIG["pygame"]["fullscreen"] == "Yes":
        scr = pygame.display.set_mode(
            (int(f_size[0]), int(f_size[1])), pygame.FULLSCREEN)
    else:
        scr = pygame.display.set_mode((int(size[0]), int(size[1])))

    size = scr.get_size()
    flag = "menu"

    while True:
        if flag == "menu":
            flag = StartScreen(scr, size, audio).run()

        if flag == "error" or flag == "quit":
            break

        if flag == "main_game":
            flag, time1, time2 = MainGameLoop(scr, size, audio).run()
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

    check_tmp(clear=True)
    



