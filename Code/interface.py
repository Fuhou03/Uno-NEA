import pygame
from login import *
from menu import *
from game_screen import GameScreen


class Interface:
    def __init__(self):
        pygame.init()
        self.SCREEN_W = 1200
        self.SCREEN_H = 1000
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))

        pygame.display.set_caption("Uno")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.running = True

        self.mouse_pos = None

        self.sign_in = SignIn(self)     # Self is a parameter so the menu can change the variables in this interface
        self.register = Register(self)

        self.main_menu = MainMenu(self)
        self.options = Options(self)
        self.game_screen = GameScreen(self)
        self.current_screen = self.main_menu  # Starts on the main_menu screen
        # Changes depending on what the user navigates to

        self.game_mode = GameMode(self)
        self.game_mode_choice = 0

        self.clicked = False
        self.pressed = False
        self.key = None
        self.card_chosen = False

        self.ENTER_KEY = False
        self.BACK_KEY = False
        self.DOWN_KEY = False
        self.UP_KEY = False
        self.LEFT_KEY = False
        self.RIGHT_KEY = False

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            self.mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = True

            elif event.type == pygame.KEYDOWN:  # Press a key
                self.pressed = True
                self.key = event

                if event.key == pygame.K_RETURN:    # If they click these keys the variable becomes True
                    self.ENTER_KEY = True           # This is used to navigate through the Menu
                elif event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                elif event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                elif event.key == pygame.K_UP:
                    self.UP_KEY = True
                elif event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                elif event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True



