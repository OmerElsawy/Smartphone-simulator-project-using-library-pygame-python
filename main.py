import pygame
from core.lock_screen import LockScreen
from core.ui import HomeScreen
from core.app_manager import AppManager
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Smartphone Smulator")


lock_screen = LockScreen(screen)
if lock_screen.run():

    app_manager = AppManager(screen)
    home_screen = HomeScreen(screen, app_manager)
    home_screen.run()

pygame.quit()
