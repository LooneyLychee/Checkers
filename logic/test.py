import unittest
from logic.legal_moves import LegalMoves
from logic.move import Move
from logic.piece import CheckersPiece, Name, Color
from logic.board import CheckersBoard, CheckersVariant
from logic.position import Position
from front.game_screen import *
# można już robić Possible  Moves
class MyTestCase(unittest.TestCase):
    def test_something(self):
        board = CheckersBoard(CheckersVariant.CLASSIC)
        #board.set_piece_on_position(Position('a5'), CheckersPiece(Name.STONE, Color.WHITE))
        #board.set_piece_on_position(Position('c5'), CheckersPiece(Name.STONE, Color.WHITE))
        #board.set_square_empty(Position('e3'))
        #board.set_square_empty(Position('b2'))
        #board.set_piece_on_position(Position('b6'), CheckersPiece(Name.DAME, Color.BLACK))

        print(board)
        a = Move(Color.WHITE, board)
        a.pick_a_piece(Position("c3"))
        a.make_a_move(board, Position("b4"))

        print("1")

        a = Move(Color.BLACK, board)
        a.pick_a_piece(Position("d6"))
        a.make_a_move(board, Position("c5"))
        board.crown_piece(board.get_piece(Position("b4")))
        print("2")
        print(board)
        a = Move(Color.WHITE, board)
        print(a.legal_moves)

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
