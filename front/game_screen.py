from front.properties import *
from logic.piece import Color, Name
from logic.position import Position
import pygame
from logic.board import CheckersBoard


class GameScreen:
    def __init__(self, player_color, checkers_variant):
        board = CheckersBoard(checkers_variant)
        self.board = Board(board, player_color)
        self.info = Info(board, player_color)
        self.background = ColorRGB.BACKGROUND.value
        self.buttons = []

        square_size = min(Size.WINDOW_SIZE.value[0] - 2 * Coordinators.BOARD_COORDINATORS.value[0],
                          Size.WINDOW_SIZE.value[1] - 2 * Coordinators.BOARD_COORDINATORS.value[1])
        square_size /= len(board.board)

        self.__create_buttons(checkers_variant.value, square_size)

    def draw(self, win, tie_screen):
        win.fill(self.background)
        self.board.draw(win)
        self.info.draw(win)

        for button in self.buttons:
            pygame.draw.rect(win, button.color, button.rect)
            win.blit(button.text, button.text_rect)
        if tie_screen is not None:
            tie_screen.draw(win)

        pygame.display.update()

    def actualize(self, from_server):
        if from_server.previous_position is not None:
            self.board.board_update(from_server.board, from_server.previous_position)
            self.board.uncheck_position(from_server.previous_position)
        if from_server.current_position is not None:
            self.board.board_update(from_server.board, from_server.current_position)
            self.board.uncheck_position(from_server.current_position)
        if from_server.captured_piece_position is not None:
            self.board.board_update(from_server.board, from_server.captured_piece_position)

        if from_server.turn_started:
            self.board.chose_position(from_server.current_position)

        self.info.actualize_pieces_info(from_server.board)
        self.info.actualize_turn(from_server.player_turn)

    def __create_buttons(self, number_of_rows, square_size):
        board_size = min(Size.WINDOW_SIZE.value[0] - 2 * Coordinators.BOARD_COORDINATORS.value[0],
                         Size.WINDOW_SIZE.value[1] - 2 * Coordinators.BOARD_COORDINATORS.value[1])

        width = (Size.WINDOW_SIZE.value[0] - board_size - 2 * Coordinators.BOARD_COORDINATORS.value[0]) * 3/4
        height = int(((number_of_rows - 4) * square_size) / 5)

        x = Coordinators.BOARD_COORDINATORS.value[0] + board_size + square_size
        y = Coordinators.BOARD_COORDINATORS.value[1] + 2 * square_size + height
        button = Button((x, y), (width, height), "Give Up")
        self.buttons.append(button)

        y += 2 * height
        button = Button((x, y), (width, height), "Tie")
        self.buttons.append(button)

    def get_button(self, mouse_position):
        for button in self.buttons:
            button.color = ColorRGB.BUTTON.value
            if button.coordinators[0] <= mouse_position[0] <= button.coordinators[0] + button.size[0]:
                if button.coordinators[1] <= mouse_position[1] <= button.coordinators[1] + button.size[1]:
                    button.color = ColorRGB.BUTTON_CLICK.value
                    return button


class Board:
    def __init__(self, board, player_color):
        self.player = player_color

        square_size = min(Size.WINDOW_SIZE.value[0] - 2 * Coordinators.BOARD_COORDINATORS.value[0],
                          Size.WINDOW_SIZE.value[1] - 2 * Coordinators.BOARD_COORDINATORS.value[1])
        square_size /= len(board.board)

        self.board = [[Square(square_size) for _ in range(len(board.board))] for _ in range(len(board.board))]
        if player_color == Color.BLACK:
            self.__board_for_black(board, square_size)
        else:
            self.__board_for_white(board, square_size)

    def __board_for_black(self, board, square_size):
        #  first square coordinator - left up corner
        y = Coordinators.BOARD_COORDINATORS.value[1]
        for row in range(len(board.board)):
            x = Coordinators.BOARD_COORDINATORS.value[0] + (len(board.board) - 1) * square_size
            for column in range(len(board.board[row])):
                self.board[row][column].set_coordinators((x, y))
                if (row + column) % 2 == 0:
                    self.board[row][column].color = ColorRGB.DARK_SQUARE.value
                else:
                    self.board[row][column].color = ColorRGB.LIGHT_SQUARE.value

                piece = board.get_piece(Position(row, column))
                if piece is None:
                    pass
                elif piece.name == Name.STONE:
                    if piece.color == Color.BLACK:
                        self.board[row][column].set_piece_color(ColorRGB.DARK_STONE.value)
                    else:
                        self.board[row][column].set_piece_color(ColorRGB.LIGHT_STONE.value)
                else:
                    if piece.color == Color.BLACK:
                        self.board[row][column].set_piece_color(ColorRGB.DARK_DAME.value)
                    else:
                        self.board[row][column].set_piece_color(ColorRGB.LIGHT_DAME.value)

                x = x - square_size
            y = y + square_size

    def __board_for_white(self, board, square_size):
        #  first square coordinator - left up corner
        y = Coordinators.BOARD_COORDINATORS.value[1] + (len(board.board) - 1) * square_size
        for row in range(len(board.board)):
            x = Coordinators.BOARD_COORDINATORS.value[0]
            for column in range(len(board.board[row])):
                self.board[row][column].set_coordinators((x, y))
                if (row + column) % 2 == 0:
                    self.board[row][column].color = ColorRGB.DARK_SQUARE.value
                else:
                    self.board[row][column].color = ColorRGB.LIGHT_SQUARE.value

                piece = board.get_piece(Position(row, column))
                if piece is None:
                    pass
                elif piece.name == Name.STONE:
                    if piece.color == Color.BLACK:
                        self.board[row][column].set_piece_color(ColorRGB.DARK_STONE.value)
                    else:
                        self.board[row][column].set_piece_color(ColorRGB.LIGHT_STONE.value)
                else:
                    if piece.color == Color.BLACK:
                        self.board[row][column].set_piece_color(ColorRGB.DARK_DAME.value)
                    else:
                        self.board[row][column].set_piece_color(ColorRGB.LIGHT_DAME.value)

                x = x + square_size
            y = y - square_size

    def board_update(self, board, position):
        piece = board.get_piece(position)
        r = position.row
        c = position.column

        if piece is None:
            self.board[r][c].set_piece_color(None)
        elif piece.name == Name.STONE:
            if piece.color == Color.WHITE:
                self.board[r][c].set_piece_color(ColorRGB.LIGHT_STONE.value)
            else:
                self.board[r][c].set_piece_color(ColorRGB.DARK_STONE.value)
        else:
            if piece.color == Color.WHITE:
                self.board[r][c].set_piece_color(ColorRGB.LIGHT_DAME.value)
            else:
                self.board[r][c].set_piece_color(ColorRGB.DARK_DAME.value)

    def get_position(self, coordinators):
        row = 0
        while row < len(self.board):
            column = 0
            while column < len(self.board[row]):
                square = self.board[row][column]
                if square.coordinators[0] <= coordinators[0] <= square.coordinators[0] + square.size:
                    if square.coordinators[1] <= coordinators[1] <= square.coordinators[1] + square.size:
                        return Position(row, column)
                column = column + 1
            row = row + 1

    def chose_position(self, position):
        r = position.row
        c = position.column

        self.board[r][c].color = ColorRGB.CHOSEN_SQUARE.value

    def uncheck_position(self, position):
        r = position.row
        c = position.column

        if (r + c) % 2 == 0:
            self.board[r][c].color = ColorRGB.DARK_SQUARE.value
        else:
            self.board[r][c].color = ColorRGB.LIGHT_SQUARE.value

    def draw(self, win):
        for row in self.board:
            for cell in row:
                pygame.draw.rect(win, cell.color, cell.react)
                if cell.piece.color is not None:
                    pygame.draw.circle(win, cell.piece.color, cell.piece.center, cell.piece.diameter, 0)


class Square:
    def __init__(self, size):
        self.coordinators = None
        self.color = None
        self.size = size
        self.react = None
        self.piece = Piece(self.size)

    def set_coordinators(self, coordinators):
        self.coordinators = (coordinators[0], coordinators[1])
        self.react = (coordinators[0], coordinators[1], self.size, self.size)  # self.square_size, self.square_size)
        self.piece.center = (coordinators[0] + self.size / 2, coordinators[1] + self.size / 2)

    def set_piece_color(self, color):
        self.piece.color = color


class Piece:
    def __init__(self, square_size):
        self.color = None
        self.center = None
        self.diameter = int(square_size * 9 / 20)


class Info:
    def __init__(self, board, player_color):
        self.player = player_color
        self.opponent = Color.opposite(player_color)

        self.__square_size = min(Size.WINDOW_SIZE.value[0] - 2 * Coordinators.BOARD_COORDINATORS.value[0],
                                 Size.WINDOW_SIZE.value[1] - 2 * Coordinators.BOARD_COORDINATORS.value[1])
        self.__square_size /= len(board.board)

        # pieces
        self.stones = [Piece(self.__square_size), Piece(self.__square_size)]
        self.dames = [Piece(self.__square_size), Piece(self.__square_size)]
        self.__set_pieces(len(board.board))

        # info about pieces
        self.dames_exist = [False, False]
        self.__text_font = pygame.font.SysFont(FontStyle.TEXT_STYLE.value, int(self.__square_size * 18 / 20))
        self.__amount_stones = [str(int(board.game_info.amount_of_pieces[0] - board.game_info.amount_of_dames[0])),
                                str(int(board.game_info.amount_of_pieces[1] - board.game_info.amount_of_dames[1]))]
        self.__amount_dames = [str(int(board.game_info.amount_of_dames[0])),
                               str(int(board.game_info.amount_of_dames[1]))]

        self.stones_info = [self.__text_font.render(self.__amount_stones[0], True, ColorRGB.TEXT.value),
                            self.__text_font.render(self.__amount_stones[1], True, ColorRGB.TEXT.value)]
        self.dames_info = [self.__text_font.render(self.__amount_dames[0], True, ColorRGB.TEXT.value),
                           self.__text_font.render(self.__amount_dames[1], True, ColorRGB.TEXT.value)]

        (x_white, y_white) = self.stones[0].center
        (x_black, y_black) = self.stones[1].center
        x_white += self.__square_size
        x_black += self.__square_size
        self.stones_info_react = [self.stones_info[0].get_rect(center=(x_white, y_white)),
                                  self.stones_info[0].get_rect(center=(x_black, y_black))]

        (x_white, y_white) = self.dames[0].center
        (x_black, y_black) = self.dames[1].center
        x_white += self.__square_size
        x_black += self.__square_size
        self.dames_info_react = [self.dames_info[0].get_rect(center=(x_white, y_white)),
                                 self.dames_info[1].get_rect(center=(x_black, y_black))]

        # info about turn
        self.turn = ["Your turn", "Opponent turn"]
        self.info_turn = self.__text_font.render(self.turn[self.player.value], True, ColorRGB.TEXT.value)
        x = (Size.WINDOW_SIZE.value[0] - self.info_turn.get_width()) / 2
        y = Coordinators.BOARD_COORDINATORS.value[1] / 2
        self.info_turn_rect = self.info_turn.get_rect(center=(x, y))

    def __set_pieces(self, number_of_rows):
        self.stones[0].color = ColorRGB.LIGHT_STONE.value
        self.stones[1].color = ColorRGB.DARK_STONE.value
        self.dames[0].color = ColorRGB.LIGHT_DAME.value
        self.dames[1].color = ColorRGB.DARK_DAME.value

        (x, y) = Coordinators.BOARD_COORDINATORS.value
        x += self.__square_size * (number_of_rows + 1)
        x += self.__square_size / 2
        y += self.__square_size / 2
        self.stones[self.opponent.value].center = (x, y)
        self.dames[self.opponent.value].center = (x, y + self.__square_size)

        y += self.__square_size * (number_of_rows - 1)
        self.dames[self.player.value].center = (x, y)
        self.stones[self.player.value].center = (x, y - self.__square_size)

    def draw(self, win):
        pygame.draw.circle(win, self.stones[0].color, self.stones[0].center, self.stones[0].diameter, 0)
        pygame.draw.circle(win, self.stones[1].color, self.stones[1].center, self.stones[1].diameter, 0)

        win.blit(self.stones_info[0], self.stones_info_react[0])
        win.blit(self.stones_info[1], self.stones_info_react[1])

        win.blit(self.info_turn, self.info_turn_rect)

        if self.dames_exist[0]:
            pygame.draw.circle(win, self.dames[0].color, self.dames[0].center, self.dames[0].diameter, 0)
            win.blit(self.dames_info[0], self.dames_info_react[0])

        if self.dames_exist[1]:
            pygame.draw.circle(win, self.dames[1].color, self.dames[1].center, self.dames[1].diameter, 0)
            win.blit(self.dames_info[1], self.dames_info_react[1])

    def actualize_turn(self, player_turn):
        self.turn[player_turn.value] = "Your turn"
        self.turn[Color.opposite(player_turn).value] = "Opponent turn"

        self.info_turn = self.__text_font.render(self.turn[self.player.value], True, ColorRGB.TEXT.value)
        x = (Size.WINDOW_SIZE.value[0] - self.info_turn.get_width()) / 2
        y = Coordinators.BOARD_COORDINATORS.value[1] / 2
        self.info_turn_rect = self.info_turn.get_rect(center=(x, y))

    def actualize_pieces_info(self, board):
        self.__amount_stones = [str(int(board.game_info.amount_of_pieces[0] - board.game_info.amount_of_dames[0])),
                                str(int(board.game_info.amount_of_pieces[1] - board.game_info.amount_of_dames[1]))]
        self.__amount_dames = [str(int(board.game_info.amount_of_dames[0])),
                               str(int(board.game_info.amount_of_dames[1]))]

        self.stones_info = [self.__text_font.render(self.__amount_stones[0], True, ColorRGB.TEXT.value),
                            self.__text_font.render(self.__amount_stones[1], True, ColorRGB.TEXT.value)]
        self.dames_info = [self.__text_font.render(self.__amount_dames[0], True, ColorRGB.TEXT.value),
                           self.__text_font.render(self.__amount_dames[1], True, ColorRGB.TEXT.value)]

        (x_white, y_white) = self.stones[0].center
        (x_black, y_black) = self.stones[1].center
        x_white += self.__square_size
        x_black += self.__square_size
        self.stones_info_react = [self.stones_info[0].get_rect(center=(x_white, y_white)),
                                  self.stones_info[0].get_rect(center=(x_black, y_black))]

        (x_white, y_white) = self.dames[0].center
        (x_black, y_black) = self.dames[1].center
        x_white += self.__square_size
        x_black += self.__square_size
        self.dames_info_react = [self.dames_info[0].get_rect(center=(x_white, y_white)),
                                 self.dames_info[1].get_rect(center=(x_black, y_black))]

        if self.__amount_dames[0] != '0':
            self.dames_exist[0] = True
        else:
            self.dames_exist[0] = False

        if self.__amount_dames[1] != '0':
            self.dames_exist[1] = True
        else:
            self.dames_exist[1] = False

        if self.dames_exist[self.player.value]:
            self.stones[self.player.value].center = (self.dames[self.player.value].center[0],
                                                     self.dames[self.player.value].center[1] - self.__square_size)
        else:
            self.stones[self.player.value].center = self.dames[self.player.value].center


class Button:
    def __init__(self, coordinators, size, caption):  # size, coordinators = (width, height)
        self.color = ColorRGB.BUTTON.value
        self.coordinators = coordinators
        self.size = size
        self.rect = (self.coordinators[0], self.coordinators[1], size[0], size[1])

        self.text_font = pygame.font.SysFont(FontStyle.TEXT_STYLE.value, int(size[1] * 4/9))
        self.text = self.text_font.render(caption, True, ColorRGB.TEXT.value)
        self.text_rect = self.text.get_rect(
            center=(self.coordinators[0] + size[0] / 2, self.coordinators[1] + size[1] / 2))
        self.caption = caption
