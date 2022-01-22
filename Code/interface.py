import pygame
from login import *
from menu import *


class Interface():
    def __init__(self):
        pygame.init()
        self.SCREEN_W = 1000
        self.SCREEN_H = 800
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)

        self.mouse_pos = None

        self.sign_in = SignIn(self)
        self.register = Register(self)
        self.current_screen = self.sign_in  # Starts on the sign-in screen
        self.main_menu = MainMenu(self)
        self.options = Options()
        self.game_mode = GameMode()

        self.clicked = False
        self.pressed = False
        self.key = None

        self.ENTER_KEY = False
        self.BACK_KEY = False
        self.DOWN_KEY = False
        self.UP_KEY = False

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            self.mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = True

            if event.type == pygame.KEYDOWN:  # Press a key
                self.pressed = True
                self.key = event

                if event.key == pygame.K_RETURN:
                    self.ENTER_KEY = True
                elif event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                elif event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                elif event.key == pygame.K_UP:
                    self.UP_KEY = True


interface = Interface()
while True:
    interface.current_screen.display()

