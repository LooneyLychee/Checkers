from logic.piece import CheckersPiece, Color, Name
from logic.position import Position
from enum import Enum


class CheckersVariant(Enum):
    CLASSIC = 8
    POLISH = 10


class GameInfo:
    def __init__(self, checkers_variant):
        self.checkers_variant = checkers_variant

        board_size = checkers_variant.value
        rows_for_pieces = (board_size - 2) / 2
        self.amount_of_pieces = [rows_for_pieces * board_size / 2, rows_for_pieces * board_size / 2]
        self.amount_of_dames = [0, 0]


class CheckersBoard:
    def __init__(self, checkers_variant):
        self.game_info = GameInfo(checkers_variant)
        board_size = checkers_variant.value

        # add first row
        self.board = [[CheckersPiece(Name.STONE, Color.WHITE) if column % 2 == 0 else None for column in range(board_size)]]

        # add other rows
        rows_for_pieces = (board_size - 2) / 2
        row = 1
        while row < board_size:
            if row < rows_for_pieces:
                white_pieces_row = [CheckersPiece(Name.STONE, Color.WHITE) if (row + column) % 2 == 0 else None for column in range(board_size)]
                self.board.append(white_pieces_row)
            elif row >= board_size - rows_for_pieces:
                black_pieces_row = [CheckersPiece(Name.STONE, Color.BLACK) if (row + column) % 2 == 0 else None for column in range(board_size)]
                self.board.append(black_pieces_row)
            else:
                empty_row = [None for _ in range(board_size)]
                self.board.append(empty_row)
            row += 1

    def clone_piece(self, position):
        if not self.is_valid_position(position):
            raise Exception("Position isn't on the board")

        piece = self.board[position.row][position.column]
        clone_piece = CheckersPiece.clone(piece)
        return clone_piece

    def get_piece(self, position):
        if not self.is_valid_position(position):
            raise Exception("Position isn't on the board")

        return self.board[position.row][position.column]

    def is_valid_position(self, position):  # is on the board
        return len(self.board) > position.row >= 0 and len(self.board) > position.column >= 0

    def is_empty(self, position):
        if not self.is_valid_position(position):
            raise Exception("Position isn't on the board")

        return self.board[position.row][position.column] is None

    def is_white_piece(self, position):
        if not self.is_valid_position(position):
            raise Exception("Position isn't on the board")

        return self.board[position.row][position.column] is not None and self.board[position.row][position.column].color == Color.WHITE

    def is_black_piece(self, position):
        if not self.is_valid_position(position):
            raise Exception("Position isn't on the board")

        return self.board[position.row][position.column] is not None and self.board[position.row][position.column].color == Color.BLACK

    def set_piece(self, position, piece):
        if not self.is_valid_position(position):
            raise Exception("Position isn't on the board")
        else:
            self.board[position.row][position.column] = piece

    def remove_piece(self, position):
        if not self.is_valid_position(position):
            raise Exception("Position isn't on the board")
        else:
            self.board[position.row][position.column] = None

    def capture_piece(self, position):
        captured_piece = self.get_piece(position)

        self.game_info.amount_of_pieces[captured_piece.color.value] -= 1

        if captured_piece.name == Name.DAME:
            self.game_info.amount_of_dames[captured_piece.color.value] -= 1

        self.remove_piece(position)

    def crown_piece(self, crowned_piece):
        crowned_piece.crown()
        self.game_info.amount_of_dames[crowned_piece.color.value] += 1

    def get_size(self):
        return len(self.board)

    @classmethod
    def clone_checkers_board(cls, board):
        new_board = cls(board.game_info.checkers_variant)
        new_board.board = [[board.clone_piece(Position(row, column)) for column in range(len(board.board))] for row in range(len(board.board))]

        new_board.game_info.amount_of_pieces = board.game_info.amount_of_pieces
        new_board.game_info.amount_of_dames = board.game_info.amount_of_dames

        return new_board

    def __str__(self):
        board = ""

        row = len(self.board) - 1
        while row >= 0:
            column = 0
            while column < len(self.board):
                if self.board[row][column] is None:
                    board += "."
                elif self.board[row][column].color == Color.BLACK:
                    if self.board[row][column].name == Name.DAME:
                        board += "B"
                    else:
                        board += "b"
                else:
                    if self.board[row][column].name == Name.DAME:
                        board += "W"
                    else:
                        board += 'w'  # str(Position(row, column))

                column += 1
            row -= 1
            board += "\n"

        return board
