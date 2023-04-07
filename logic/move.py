from logic.legal_moves import *


class Move:
    def __init__(self, color, board):  # legal_moves, start_position):
        self.legal_moves = LegalMoves.find(board, color)
        self.move_exist = False
        self.move_allowed = False
        self.position = None
        self.turn_started = False
        self.captured_piece_position = None

    def pick_a_piece(self, position):
        possible_moves = self.legal_moves.find_for_position(position)
        if not self.move_exist and possible_moves is not None and len(possible_moves.next_moves) != 0:
            self.move_exist = True
            self.legal_moves = possible_moves
            self.position = position

    def make_a_move(self, board, next_position):
        possible_moves = self.legal_moves.find_for_position(next_position)

        if possible_moves is None:
            self.move_allowed = False
            self.captured_piece_position = None
        else:
            self.__update_board(board, self.position, next_position, possible_moves.captured_piece_position)
            self.captured_piece_position = possible_moves.captured_piece_position
            self.move_allowed = True
            self.legal_moves = possible_moves
            self.position = next_position

        if len(self.legal_moves.next_moves) == 0:
            self.move_exist = False

    def crowning(self, board):
        piece = board.get_piece(self.position)
        last_row = len(board.board) - 1

        if piece.color == Color.WHITE and self.position.row == last_row:
            board.crown_piece(piece)
        elif self.position.row == 0 and piece.color == Color.BLACK:
            board.crown_piece(piece)

        # board.set_piece_on_position(self.position, piece)

    @staticmethod
    def __update_board(board, position, next_position, captured_piece_position):
        board.set_piece(next_position, board.get_piece(position))
        board.remove_piece(position)

        if captured_piece_position is not None:
            board.capture_piece(captured_piece_position)
