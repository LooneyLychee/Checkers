class Position:
    def __init__(self, *args):  # row, column or 'a1'...
        if len(args) == 1:
            position = args[0]

            if len(position) != 2:
                raise Exception("Wrong Position. Except 'a1', 'a2' ... 'a8'. 'b1' ... 'h8'")

            row = ord(position[1])
            self.row = row - ord('1')

            column = ord(position[0])
            self.column = column - ord('a')
        elif len(args) == 2:

            self.row = args[0]
            self.column = args[1]

        else:
            raise Exception("Wrong Position. Too many arguments")

    def __str__(self):
        column = chr(self.column + 97)
        row = chr(self.row + 49)

        return column + row

    def __eq__(self, obj):
        return self.row == obj.row and self.column == obj.column
