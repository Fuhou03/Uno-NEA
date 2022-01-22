import pygame
from login import *

class Interface():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)

        self.mouse_pos = None

        self.sign_in = SignIn(self)
        self.register = Register(self)
        self.current_screen = self.sign_in  # Starts on the sign-in screen

        self.clicked = False
        self.pressed = False
        self.key = None


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


interface = Interface()
while True:
    interface.current_screen.display()
