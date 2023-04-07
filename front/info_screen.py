from front.properties import *
import pygame
from enum import Enum


class Message(Enum):
    QUESTIONING = "Waiting for answer"
    RESPONDING = "Tie?"


class WaitingScreen:
    def __init__(self):
        self.background = ColorRGB.BACKGROUND.value
        text_height = int(Size.WINDOW_SIZE.value[1]/10)
        font = pygame.font.SysFont(FontStyle.TEXT_STYLE.value, text_height)
        self.text = font.render("Waiting for Player...", True, ColorRGB.TEXT.value)
        self.text_rect = self.text.get_rect(center=(Size.WINDOW_SIZE.value[0] / 2, Size.WINDOW_SIZE.value[1] / 2))

    def draw(self, win):
        win.fill(self.background)
        win.blit(self.text, self.text_rect)

        pygame.display.update()


class EndScreen:
    def __init__(self, result):
        self.background = ColorRGB.BACKGROUND.value
        text_height = int(Size.WINDOW_SIZE.value[1] / 5)
        font = pygame.font.SysFont(FontStyle.TEXT_STYLE.value, text_height)
        self.text = font.render(result, True, ColorRGB.TEXT.value)
        self.text_rect = self.text.get_rect(center=(Size.WINDOW_SIZE.value[0] / 2, Size.WINDOW_SIZE.value[1] * 3/8))
        x = Size.WINDOW_SIZE.value[0] / 4
        y = Size.WINDOW_SIZE.value[1] * 5/8
        width = Size.WINDOW_SIZE.value[0] / 2
        height = Size.WINDOW_SIZE.value[1] / 4
        self.menu_button = Button((x, y), (width, height), "MENU")

    def draw(self, win):
        win.fill(self.background)
        win.blit(self.text, self.text_rect)
        pygame.draw.rect(win, self.menu_button.color, self.menu_button.rect)
        win.blit(self.menu_button.text, self.menu_button.text_rect)

        pygame.display.update()

    def get_button(self, mouse_position):
        self.menu_button.color = ColorRGB.BUTTON.value
        if self.menu_button.coordinators[0] <= mouse_position[0] <= self.menu_button.coordinators[0] + self.menu_button.size[0]:
            if self.menu_button.coordinators[1] <= mouse_position[1] <= self.menu_button.coordinators[1] + self.menu_button.size[1]:
                self.menu_button.color = ColorRGB.BUTTON_CLICK.value
                return self.menu_button

    @staticmethod
    def get_result(player, winner):
        if winner is None:
            return "Tie"
        elif winner == player:
            return "Winner"
        else:
            return "Looser"


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


class TieScreen:
    def __init__(self, message):
        self.message = message
        #  background
        self.background = ColorRGB.TIE_SCREEN.value
        x = (Size.WINDOW_SIZE.value[0] - Size.TIE_SCREEN.value[0]) / 2
        y = (Size.WINDOW_SIZE.value[1] - Size.TIE_SCREEN.value[1]) / 2
        self.screen_react = (x, y, Size.TIE_SCREEN.value[0], Size.TIE_SCREEN.value[1])

        #  message
        text_height = int(Size.TIE_SCREEN.value[1] / 9)
        font = pygame.font.SysFont(FontStyle.TEXT_STYLE.value, text_height)
        self.text = font.render(message.value, True, ColorRGB.TEXT.value)
        self.text_rect = self.text.get_rect(center=(x + Size.TIE_SCREEN.value[0] / 2, y + Size.TIE_SCREEN.value[1] * 3 / 8))

        #  buttons
        self.buttons = []
        width = Size.TIE_SCREEN.value[0] / 5
        height = Size.TIE_SCREEN.value[1] / 4
        self.buttons.append(Button((x + width, y + Size.TIE_SCREEN.value[1] * 5 / 8), (width, height), "YES"))
        self.buttons.append(Button((x + 3 * width, y + Size.TIE_SCREEN.value[1] * 5 / 8), (width, height), "NO"))

    def draw(self, win):
        pygame.draw.rect(win, self.background, self.screen_react)
        win.blit(self.text, self.text_rect)

        if self.message == Message.RESPONDING:
            for button in self.buttons:
                pygame.draw.rect(win, button.color, button.rect)
                win.blit(button.text, button.text_rect)

    def get_button(self, mouse_position):
        if self.message == Message.RESPONDING:
            for button in self.buttons:
                button.color = ColorRGB.BUTTON.value
                if button.coordinators[0] <= mouse_position[0] <= button.coordinators[0] + button.size[0]:
                    if button.coordinators[1] <= mouse_position[1] <= button.coordinators[1] + button.size[1]:
                        button.color = ColorRGB.BUTTON_CLICK.value
                        return button
