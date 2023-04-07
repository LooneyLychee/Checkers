from logic.board import *


class MoveType(Enum):
    CAPTURING = 1
    NORMAL = 0


class Direction(Enum):
    NORTH_WEST = 1
    NORTH_EAST = 2
    SOUTH_WEST = 3
    SOUTH_EAST = 4


class LegalMoves(object):

    __create_key = object()

    def __init__(self, create_key, position, move_type):
        assert (create_key == self.__create_key), \
            "OnlyCreatable objects must be created using LegalMoves.find"
        self.current_position = position
        self.captured_piece_position = None  # in previous move
        self.amount_of_captured_pieces = 0
        self.next_moves = []
        self.move_type = move_type

    def __str__(self):
        text = self.__convert_to_string(self, "")
        if text is not None:
            return text

        return ""

    @classmethod
    def __convert_to_string(cls, legal_moves, text):
        if legal_moves.current_position is not None:
            text = text + str(legal_moves.current_position) + " " + str(
                legal_moves.amount_of_captured_pieces) + " -> \n"

        for next_position in legal_moves.next_moves:
            text = cls.__convert_to_string(next_position, text)

        text = text + " <- \n"

        return text

    @classmethod
    def find(cls, board, color):
        legal_moves = cls(cls.__create_key, None, None)

        row = 0
        while row < len(board.board):
            column = 0
            while column < len(board.board):
                position = Position(row, column)
                # actualize_moves, without forced maximum capturing
                cls.__actualize_moves(board, position, color, legal_moves)
                column += 1
            row += 1
        # remove if not maximum capturing
        legal_moves.__remove_not_allowed_moves()
        return legal_moves

    @classmethod
    # actualize_moves, without forced maximum capturing
    def __actualize_moves(cls, board, position, color, moves):
        if not board.is_empty(position) and board.get_piece(position).color == color:
            next_move = cls(cls.__create_key, position, None)
            moves.next_moves.append(next_move)

            if board.get_piece(position).name == Name.STONE:
                cls.__normal_moves_for_stone(board, next_move, position)
                work_board = CheckersBoard.clone_checkers_board(board)
                cls.__capturing_for_stone(board, work_board, next_move, position, position, color)
            else:
                cls.__normal_moves_for_dame(board, next_move, position)
                working_board = CheckersBoard.clone_checkers_board(board)
                cls.__capturing_for_dame(board, working_board, next_move, position, position, color)

            if next_move.move_type is not None and moves.move_type != MoveType.CAPTURING:
                moves.move_type = next_move.move_type

            moves.amount_of_captured_pieces = max(moves.amount_of_captured_pieces, next_move.amount_of_captured_pieces + 1)

    @classmethod
    def __normal_moves_for_stone(cls, board, moves, position):
        if board.is_white_piece(position):
            possible_positions = [Position(position.row+1, position.column-1),
                                  Position(position.row+1, position.column+1)]
        else:
            possible_positions = [Position(position.row - 1, position.column - 1),
                                  Position(position.row - 1, position.column + 1)]

        for possible_position in possible_positions:
            if board.is_valid_position(possible_position) and board.is_empty(possible_position):
                next_moves = cls(cls.__create_key, possible_position, MoveType.NORMAL)
                moves.next_moves.append(next_moves)
                moves.move_type = MoveType.NORMAL

    @classmethod
    def __capturing_for_stone(cls, board, work_board, current_moves, current_position, start_position, color):
        captured_pieces_positions = [
            Position(current_position.row + 1, current_position.column - 1),
            Position(current_position.row + 1, current_position.column + 1),
            Position(current_position.row - 1, current_position.column - 1),
            Position(current_position.row - 1, current_position.column + 1)
        ]

        next_positions = [
            Position(current_position.row + 2, current_position.column - 2),
            Position(current_position.row + 2, current_position.column + 2),
            Position(current_position.row - 2, current_position.column - 2),
            Position(current_position.row - 2, current_position.column + 2)
        ]

        for next_position, captured_position in zip(next_positions, captured_pieces_positions):
            if work_board.is_valid_position(next_position) and work_board.is_empty(next_position):
                captured_piece = work_board.get_piece(captured_position)

                if not work_board.is_empty(captured_position) and captured_piece.color != color:
                    # simulation move on the working board
                    work_board.remove_piece(captured_position)
                    work_board.set_piece(next_position, work_board.get_piece(current_position))
                    work_board.remove_piece(current_position)

                    # creation new possible move and connected it with currentMove.
                    next_move = cls(cls.__create_key, next_position, MoveType.CAPTURING)
                    next_move.captured_piece_position = captured_position

                    current_moves.next_moves.append(next_move)
                    current_moves.move_type = MoveType.CAPTURING

                    cls.__capturing_for_stone(board, work_board, next_move, next_position, start_position, color)

                    # recursion is back, so we're fixing the working board.
                    work_board.set_piece(captured_position, captured_piece)
                    work_board.set_piece(current_position, board.clone_piece(start_position))
                    work_board.remove_piece(next_position)

                    current_moves.amount_of_captured_pieces = max(next_move.amount_of_captured_pieces + 1, current_moves.amount_of_captured_pieces)

    @classmethod
    def __normal_moves_for_dame(cls, board, moves, position):
        possible_directions = [
            Direction.NORTH_EAST,
            Direction.NORTH_WEST,
            Direction.SOUTH_EAST,
            Direction.SOUTH_WEST
        ]

        for direction in possible_directions:
            next_position = cls.__move(direction, position)
            while board.is_valid_position(next_position) and board.is_empty(next_position):
                next_move = cls(cls.__create_key, next_position, MoveType.NORMAL)
                moves.next_moves.append(next_move)
                moves.move_type = MoveType.NORMAL

                next_position = cls.__move(direction, next_position)

    @classmethod
    def __capturing_for_dame(cls, board, work_board, current_moves, current_position, start_position, color):
        possible_directions = [
            Direction.NORTH_EAST,
            Direction.NORTH_WEST,
            Direction.SOUTH_EAST,
            Direction.SOUTH_WEST
        ]

        for direction in possible_directions:
            next_position = cls.__move(direction, current_position)

            # find the first enemy piece
            while work_board.is_valid_position(next_position) and work_board.is_empty(next_position):
                next_position = cls.__move(direction, next_position)

            captured_piece_position = Position(next_position.row, next_position.column)
            next_position = cls.__move(direction, next_position)

            while work_board.is_valid_position(next_position) and work_board.is_empty(next_position) and work_board.get_piece(captured_piece_position).color != color:
                captured_piece = work_board.get_piece(captured_piece_position)
                if captured_piece.color != color:
                    while board.is_valid_position(next_position) and work_board.is_empty(next_position):
                        # on captured_piece_position insert Piece in other color, we want to avoid standing on the square with a previously captured piece
                        piece = board.clone_piece(captured_piece_position)
                        piece.change_color()
                        work_board.set_piece(captured_piece_position, piece)

                        # on next_position insert current_piece
                        piece = work_board.get_piece(current_position)
                        work_board.set_piece(next_position, piece)
                        work_board.remove_piece(current_position)

                        next_move = cls(cls.__create_key, next_position, MoveType.CAPTURING)
                        next_move.captured_piece_position = captured_piece_position
                        current_moves.next_moves.append(next_move)
                        current_moves.move_type = MoveType.CAPTURING

                        cls.__capturing_for_dame(board, work_board, next_move, next_position, start_position, color)

                        work_board.set_piece(captured_piece_position, board.clone_piece(captured_piece_position))
                        work_board.set_piece(current_position,  board.clone_piece(start_position))
                        work_board.remove_piece(next_position)

                        current_moves.amount_of_captured_pieces = max(next_move.amount_of_captured_pieces + 1, current_moves.amount_of_captured_pieces)
                        next_position = cls.__move(direction, next_position)

    @staticmethod
    def __move(direction, position):
        if direction == Direction.NORTH_EAST:
            return Position(position.row + 1, position.column + 1)
        elif direction == Direction.NORTH_WEST:
            return Position(position.row + 1, position.column - 1)
        elif direction == Direction.SOUTH_EAST:
            return Position(position.row - 1, position.column - 1)
        else:
            return Position(position.row - 1, position.column + 1)

    def __remove_not_allowed_moves(self):
        if self.move_type == MoveType.CAPTURING:
            self.__remove_not_maximum_moves()
            self.__remove_normal_moves()

            for legal_position in self.next_moves:
                legal_position.__remove_not_allowed_moves()
        else:
            index = 0
            while index < len(self.next_moves):
                player_possibilities = self.next_moves[index]
                if len(player_possibilities.next_moves) == 0:
                    self.next_moves.remove(player_possibilities)
                else:
                    index = index + 1

    def __remove_normal_moves(self):
        index = 0
        while index < len(self.next_moves):
            player_possibilities = self.next_moves[index]
            if player_possibilities.move_type == MoveType.NORMAL:
                self.next_moves.remove(player_possibilities)
            else:
                index = index + 1

    def __remove_not_maximum_moves(self):
        index = 0
        while index < len(self.next_moves):
            player_possibilities = self.next_moves[index]
            if player_possibilities.amount_of_captured_pieces != self.amount_of_captured_pieces - 1:
                self.next_moves.remove(player_possibilities)
            else:
                index = index + 1

    def find_for_position(self, position):
        for move in self.next_moves:
            if move.current_position == position:
                return move
