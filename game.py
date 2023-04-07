from logic.board import CheckersBoard, Color, Position
from logic.move import Move
from front.game_screen import GameScreen
from enum import Enum


class Answer(Enum):
    YES = True
    NO = False


class ClientGame:
    def __init__(self, checkers_variant, player):
        self.player = player
        self.game_screen = GameScreen(player, checkers_variant)
        self.from_server = ServerToClient(checkers_variant)

    def actualize(self, from_server):
        self.from_server = from_server
        self.game_screen.actualize(from_server)


class ServerGame:
    def __init__(self, checkers_variant):
        self.checkers_variant = checkers_variant
        self.to_client = ServerToClient(checkers_variant)
        self.moves = Move(self.to_client.player_turn, self.to_client.board)

    def connected(self):
        self.to_client.connected = True

    def __change_player(self):
        self.to_client.player_turn = Color.opposite(self.to_client.player_turn)
        self.to_client.turn_started = False

        self.moves.crowning(self.to_client.board)
        self.moves = Move(self.to_client.player_turn, self.to_client.board)

        if len(self.moves.legal_moves.next_moves) == 0:
            self.__game_over()

    def __game_over(self):
        self.to_client.winner = Color.opposite(self.to_client.player_turn)
        self.to_client.end = True

    def pick_a_piece(self, position, player):
        if player == self.to_client.player_turn and not self.to_client.turn_started and self.to_client.questioning is None:
            self.moves.pick_a_piece(position)
            if self.moves.move_exist:
                if self.to_client.current_position is not None:
                    self.to_client.previous_position = Position(self.to_client.current_position.row, self.to_client.current_position.column)
                self.to_client.turn_started = True

                self.to_client.current_position = Position(position.row, position.column)

    def make_a_move(self, position, player):
        if player == self.to_client.player_turn and self.to_client.turn_started and self.to_client.questioning is None:
            self.moves.make_a_move(self.to_client.board, position)
            if self.moves.move_allowed:
                self.to_client.previous_position = Position(self.to_client.current_position.row, self.to_client.current_position.column)
                self.to_client.current_position = Position(position.row, position.column)
                self.to_client.captured_piece_position = self.moves.captured_piece_position

            if not self.moves.move_exist:
                self.__change_player()

    def give_up(self, player):
        self.to_client.winner = Color.opposite(player)
        self.to_client.end = True

    def tie(self, player):
        self.to_client.questioning = player

    def answer(self, player, answer):
        if player != self.to_client.questioning:
            if answer.value:
                self.to_client.tie = True
            else:
                self.to_client.questioning = None


class ServerToClient:
    def __init__(self, checkers_variant):
        self.board = CheckersBoard(checkers_variant)
        self.previous_position = None
        self.current_position = None
        self.captured_piece_position = None
        self.player_turn = Color.WHITE
        self.connected = False
        self.turn_started = False
        self.winner = None
        self.end = False
        self.questioning = None
        self.tie = False
