import pygame


class Button():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 30)
        self.colour_active = pygame.Color("lightskyblue3")
        self.colour_passive = pygame.Color("gray15")
        self.colour = self.colour_passive
        self.active = False
        self.text = ""

    def change_colour(self, pos):
        ''' Changes colour of button if you clicked on it'''
        if self.rect.collidepoint(pos):  # Check the pos of mouse click and see if it's inside the rect
            self.active = True  # So that we can start typing inside user_rect
            self.colour = self.colour_active
        else:
            self.active = False  # Click outside of box
            self.colour = self.colour_passive

    def get_text(self, key):
        ''' Gets your inputted text and stores it into the text variable '''

        if key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]  # Till 2nd last character
        else:   # To add the letter you pressed onto screen later
            self.text += key.unicode  # Unicode is the info of the button pressed.


    def draw(self, surface):  # surface = screen
        ''' Draw the rectangle onto screen '''

        self.input_text = self.font.render(self.text, True, (255, 255, 255))  # Put inputted text onto screen
        surface.blit(self.input_text, (self.rect.x + 5, self.rect.y + 5))

        self.rect.w = max(350, self.input_text.get_width() + 10)  # Set rect width
        #   Max uses the largest argument, so width is 350 initially. Becomes bigger after text width > 350.

        pygame.draw.rect(surface, self.colour, self.rect, 2)  # Include a borderwidth (2) to blit the border only


