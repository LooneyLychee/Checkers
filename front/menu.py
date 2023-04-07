from front.properties import *
from logic.board import CheckersVariant
import pygame


class MenuScreen:
    def __init__(self):
        self.background = ColorRGB.BACKGROUND.value

        variants = []
        for variant in CheckersVariant:
            variants.append(variant)

        #  first button
        button_coordinators = Coordinators.FIRST_BUTTON_COORDINATORS.value

        button_width = (Size.WINDOW_SIZE.value[0] - 2 * button_coordinators[0])

        button_height = (Size.WINDOW_SIZE.value[1] - 2 * button_coordinators[1])
        button_height -= (Size.SPACE_BETWEEN_BUTTONS.value * (len(variants)-1))
        button_height /= len(variants)
        button_height = int(button_height)

        button_size = (button_width, button_height)

        self.buttons = []

        for i in range(len(variants)):
            button = Button(button_coordinators, button_size, str(variants[i].name))
            self.buttons.append(button)

            button_coordinators = (button_coordinators[0], button_coordinators[1] + button_size[1] + Size.SPACE_BETWEEN_BUTTONS.value)

    def get_button(self, mouse_position):
        for button in self.buttons:
            button.color = ColorRGB.BUTTON.value
            if button.coordinators[0] <= mouse_position[0] <= button.coordinators[0] + button.size[0]:
                if button.coordinators[1] <= mouse_position[1] <= button.coordinators[1] + button.size[1]:
                    button.color = ColorRGB.BUTTON_CLICK.value
                    return button

    def draw(self, win):
        win.fill(self.background)
        for button in self.buttons:
            pygame.draw.rect(win, button.color, button.rect)
            win.blit(button.text, button.text_rect)

        pygame.display.update()


class Button:
    def __init__(self, coordinators, size, caption):  # size, coordinators = (width, height)
        self.color = ColorRGB.BUTTON.value
        self.coordinators = coordinators
        self.size = size
        self.rect = (self.coordinators[0], self.coordinators[1], size[0], size[1])

        self.text_font = pygame.font.SysFont(FontStyle.TEXT_STYLE.value, int(size[1]/3))
        self.text = self.text_font.render(caption, True, ColorRGB.TEXT.value)
        self.text_rect = self.text.get_rect(center=(self.coordinators[0] + size[0]/2, self.coordinators[1] + size[1]/2))
        self.caption = caption
