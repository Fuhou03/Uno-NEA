import pygame
from button import Button


class SignIn:
    def __init__(self, interface):
        # Creating the labels
        self.interface = interface
        self.font = pygame.font.Font(None, 30)

        self.username_label = self.font.render("Username", True, (255, 255, 255))
        self.password_label = self.font.render("Password", True, (255, 255, 255))
        self.register_label = self.font.render("Register", True, (255, 255, 255))
        self.login_label = self.font.render("Login", True, (255, 255, 255))

        self.button_list = []  # So we can loop through all buttons easily
        self.user_rect = Button(210, 90, 140, 32)  # (x, y, width, height)
        self.pass_rect = Button(210, 140, 140, 32)  # width becomes 200 later
        self.register_rect = Button(100, 210, 210, 32)
        self.login_rect = Button(350, 210, 210, 32)

        self.run_display = True

    def create_button_list(self):
        self.button_list.append(self.user_rect)
        self.button_list.append(self.pass_rect)
        self.button_list.append(self.register_rect)
        self.button_list.append(self.login_rect)

    def draw_label(self):
        # Put labels onto screen
        self.interface.screen.blit(self.username_label, (100, 100))
        self.interface.screen.blit(self.password_label, (100, 150))
        self.interface.screen.blit(self.register_label, (157, 217))
        self.interface.screen.blit(self.login_label, (417, 217))

    def draw_buttons(self):
        for b in self.button_list:
            if b == self.register_rect or b == self.login_rect:      # So you can't input text into these rectangles
                pygame.draw.rect(self.interface.screen, b.colour, b.rect, 2)
            else:
                b.draw(self.interface.screen)  # To put the rectangles onto the screen

    def display(self):
        self.create_button_list()

        while self.run_display:
            self.interface.screen.fill((0, 0, 0))  # Reset screen - Put it before you blit, so it doesn't cover the elements
            self.draw_label()

            self.interface.check_events()

            if self.interface.clicked:
                for button in self.button_list:  # Goes through all buttons
                    button.change_colour(self.interface.mouse_pos)  # Colour of box will be grey until clicked on
                    if button == self.register_rect and button.active and\
                            self.interface.current_screen != self.interface.register:
                        # If they click on the register button while on the login screen
                        self.interface.current_screen = self.interface.register
                        self.run_display = False

            if self.interface.pressed:
                for button in self.button_list:
                    if button.active:  # If the button has been clicked on
                        button.get_text(self.interface.key)


            self.draw_buttons()

            pygame.display.update()
            self.interface.clock.tick(60)   # 60 fps
            self.reset_keys()

    def reset_keys(self):
        self.interface.clicked = False
        self.interface.pressed = False
        self.interface.key = None



class Register(SignIn):
    def __init__(self, interface):
        super().__init__(interface)
        self.email_label = self.font.render("Email", True, (255, 255, 255))
        #font = pygame.font.Font(None, 28)   # Just for the confirm box
        self.confirm1_label = self.font.render("Confirm", True, (255, 255, 255))
        self.confirm2_label = self.font.render("Password", True, (255, 255, 255))

        self.confirm_rect = Button(210, 190, 140, 32)
        self.email_rect = Button(210, 240, 140, 32)

        self.register_rect = Button(350, 310, 210, 32)
        self.login_rect = Button(100, 310, 210, 32)

    def create_button_list(self):
        super().create_button_list()
        self.button_list.append(self.confirm_rect)
        self.button_list.append(self.email_rect)

    def draw_label(self):
        self.interface.screen.blit(self.username_label, (100, 100))
        self.interface.screen.blit(self.password_label, (100, 150))
        self.interface.screen.blit(self.confirm1_label, (100, 185))
        self.interface.screen.blit(self.confirm2_label, (100, 208))
        self.interface.screen.blit(self.email_label, (100, 250))

        self.interface.screen.blit(self.register_label, (400, 317))
        self.interface.screen.blit(self.login_label, (167, 317))


    def draw_buttons(self):
        super().draw_buttons()

    def display(self):
        super().display()
