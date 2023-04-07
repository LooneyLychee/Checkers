from enum import Enum


class Name(Enum):
    DAME = 0
    STONE = 1


class Color(Enum):
    WHITE = 0
    BLACK = 1

    @classmethod
    def opposite(cls, color):
        return cls((color.value + 1) % 2)


class CheckersPiece:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    @classmethod
    def clone(cls, piece):
        if piece is None:
            return None

        return cls(piece.name, piece.color)

    # @classmethod
    # def create_a_piece_of_a_different_color(cls, piece):
    #    if piece.color is Color.BLACK:
    #        return cls(piece.name, Color.WHITE)
    #    else:
    #        return cls(piece.name, Color.BLACK)

    def change_color(self):
        if self.color == Color.BLACK:
            self.color = Color.WHITE
        else:
            self.color = Color.BLACK

    def crown(self):
        self.name = Name.DAME

    def __eq__(self, obj):
        return self.color == obj.color and self.name == obj.name
