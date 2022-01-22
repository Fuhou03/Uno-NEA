import pygame
from button import Button
from login import SignIn

class MainMenu:
    def __init__(self, interface):
        #super().__init__(interface)
        self.interface = interface
        self.state = None
        self.run_display = True
        
        self.MID_W, self.MID_H = 400, 350

        self.font = pygame.font.Font(None, 90)
        self.play_label = self.font.render("Play", True, (255, 255, 255))
        self.option_label = self.font.render("Option", True, (255, 255, 255))


        self.PLAY_X, self.PLAY_Y = self.MID_W, self.MID_H - 70
        self.play_button = Button(self.PLAY_X, self.PLAY_Y, 270, 85)

        self.OPTION_X, self.OPTION_Y = self.MID_W, self.MID_H + 70
        self.option_button = Button(self.OPTION_X, self.OPTION_Y, 270, 85)

        self.cursor = Button(self.PLAY_X, self.PLAY_Y, 270, 85)
        self.cursor.colour = self.cursor.colour_active

        self.button_list = [self.play_button, self.option_button, self.cursor]

    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))
            self.interface.screen.blit(self.play_label, (self.MID_W + 62, self.MID_H - 60))
            self.interface.screen.blit(self.option_label, (self.MID_W + 35, self.MID_H + 82))

            self.interface.check_events()
            self.check_input()

            for b in self.button_list:
                b.draw_rect(self.interface.screen)

            pygame.display.update()
            self.interface.clock.tick(60)   # 60 fps
            self.reset_keys()

    def move_cursor(self):
        if self.interface.DOWN_KEY:     # To select a button
            self.cursor.rect.y += 140

        elif self.interface.UP_KEY:
            self.cursor.rect.y -= 140

    def check_input(self):
        self.move_cursor()
        if self.interface.ENTER_KEY:    # If they pressed enter
            for button in self.button_list:     # Finds the button selected
                if button.rect.y == self.cursor.rect.y:     # If the cursor rect overlaps with that button

                    if button == self.play_button:
                        # Move onto game_mode screen
                        print("Play")
                    elif button == self.option_button:
                        print("Option")
                        # Move onto option screen


    def reset_keys(self):
        self.interface.ENTER_KEY = False
        self.interface.BACK_KEY = False
        self.interface.DOWN_KEY = False
        self.interface.UP_KEY = False

class Options:
    pass

class GameMode:
    pass



