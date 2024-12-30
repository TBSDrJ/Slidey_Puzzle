class GamePiece:
    def __init__(self, number: int, width: int, length: int, 
                x: int, y: int, color: str) -> None:
        # Used for identification of piece in board
        self.number = number
        # x-direction: The direction that starts with 4 spaces
        self.width = width
        # y-direction: The direction that starts with 5 spaces
        self.length = length
        # Upper-Left corner: x in 0 -> 3, y in 0 -> 4.
        self.location = (x, y)
        # Color: 'r' = Red, 'p' = Purple, 'g' = Green
        self.color = color

    def __str__(self) -> str:
        match self.color:
            case 'r':
                color = "Red"
            case 'p':
                color = "Purple"
            case 'g':
                color = "Green"
        return f"{color} Piece covering {self.spaces_occupied}"

    def __repr__(self) -> str:
        repr_str = f"GamePiece({self.number}, {self.width}, {self.length}, "
        repr_str += f"{self.location[0]}, {self.location[1]}, '{self.color}')"
        return repr_str

    @property
    def spaces_occupied(self):
        """Produce list of spaces covered by this piece."""
        spaces = []
        tmp_spaces = []
        for i in range(self.width):
            spaces.append([self.location[0] + i, self.location[1]])
        for i in range(1, self.length):
            for space in spaces:
                tmp_spaces.append([space[0], space[1] + i])
        spaces += tmp_spaces
        return spaces
    
class GameBoard:
    def __init__(self):
        self.board = [[0 for i in range(4)] for i in range(5)]
        self.p1 = GamePiece(1, 1, 2, 0, 1, 'p')
        self.p2 = GamePiece(2, 1, 2, 0, 3, 'p')
        self.p3 = GamePiece(3, 2, 1, 1, 2, 'p')
        self.p4 = GamePiece(4, 1, 2, 3, 1, 'p')
        self.p5 = GamePiece(5, 1, 2, 3, 3, 'p')
        self.r1 = GamePiece(1, 1, 1, 1, 3, 'r')
        self.r2 = GamePiece(2, 1, 1, 1, 4, 'r')
        self.r3 = GamePiece(3, 1, 1, 2, 3, 'r')
        self.r4 = GamePiece(4, 1, 1, 2, 4, 'r')
        self.g1 = GamePiece(1, 2, 2, 1, 0, 'g')
        self.pieces = [self.p1, self.p2, self.p3, self.p4, self.p5, 
                self.r1, self.r2, self.r3, self.r4, self.g1]
        for piece in self.pieces:
            for space in piece.spaces_occupied:
                self.board[space[1]][space[0]] = piece.color + str(piece.number)

    def __str__(self) -> str:
        board_str = ""
        for row in self.board:
            for entry in row:
                if entry != 0:
                    board_str += entry + " "
                else:
                    board_str += "xx "
            board_str += "\n"
        return board_str

    def __repr__(self) -> str:
        return "GameBoard()"

def main():
    gb = GameBoard()

if __name__ == "__main__":
    main()