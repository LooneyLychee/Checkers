from enum import Enum


class Size(Enum):
    WINDOW_SIZE = (800, 600)
    SPACE_BETWEEN_BUTTONS = 50
    TIE_SCREEN = (500, 300)


class ColorRGB(Enum):
    BACKGROUND = (146, 166, 91)
    BUTTON = (51, 51, 51)
    BUTTON_CLICK = (128, 32, 0)
    TEXT = (230, 230, 230)
    LIGHT_SQUARE = (244, 164, 96)
    DARK_SQUARE = (160, 82, 45)
    CHOSEN_SQUARE = (150, 150, 150)
    LIGHT_STONE = (225, 225, 225)
    LIGHT_DAME = (148, 209, 200)
    DARK_STONE = (30, 30, 30)
    DARK_DAME = (130, 10, 1)
    TIE_SCREEN = (77, 77, 77)


class FontStyle(Enum):
    TEXT_STYLE = 'Calibri'


class Coordinators(Enum):  # upper left corner
    FIRST_BUTTON_COORDINATORS = (100, 100)
    BOARD_COORDINATORS = (50, 100)
