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
        self.location = [x, y]
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
    def name(self) -> str:
        return self.color + str(self.number)

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

    def valid_moves(self, gb: "GameBoard") -> list[list[int]]:
        """Produce list of valid moves for this piece.
        
        [1, 0] means can move this piece one square to the right.
        [0, 1] means can move this piece one square down (towards exit)
        [-1, 0] and [0, -1] are same but left/up."""
        choices = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        valid = []
        for choice in choices:
            is_valid = True
            for space in self.spaces_occupied:
                if space[0] + choice[0] >= gb.width:
                    is_valid = False
                    continue
                if space[1] + choice[1] >= gb.length:
                    is_valid = False
                    continue
                if (gb.board[space[1] + choice[1]][space[0] + choice[0]] != 0
                        and (gb.board[space[1] + choice[1]][space[0] + 
                        choice[0]] != self.name)):
                    is_valid = False
            if is_valid:
                valid.append(choice)
        return valid

    def move(self, direction: list[int], gb: "GameBoard") -> None:
        """Move this piece in given direction, with validity checking."""
        print(self.location)
        assert(direction in [[1,0], [0,1], [-1,0], [0,-1]])
        self.location[0] += direction[0]
        assert(self.location[0] in range(gb.width))
        self.location[1] += direction[1]
        assert(self.location[1] in range(gb.length))
        print(self.location)

class GameBoard:
    def __init__(self):
        self.width = 4
        self.length = 5
        # Notice that we can't use e.g. [[0] * 4] * 5 because the * 5 produces
        #   shallow copies, i.e. 5 pointers to one list of length 4.
        self.board = [[0] * self.width for i in range(self.length)]
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
        self.pieces = {
                self.p1.name: self.p1, 
                self.p2.name: self.p2, 
                self.p3.name: self.p3, 
                self.p4.name: self.p4, 
                self.p5.name: self.p5, 
                self.r1.name: self.r1, 
                self.r2.name: self.r2, 
                self.r3.name: self.r3, 
                self.r4.name: self.r4, 
                self.g1.name: self.g1,
        }
        for piece in self.pieces.values():
            for space in piece.spaces_occupied:
                self.board[space[1]][space[0]] = piece.name

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

    @property
    def valid_moves(self) -> dict:
        """Find all possible valid moves for the entire game board."""
        valid_moves = {}
        for piece in self.pieces.values():
            moves = piece.valid_moves(self)
            if moves:
                valid_moves[piece.name] = moves
        return valid_moves

    def move(self, piece: "GamePiece", move: list[int]) -> None:
        """Carry out move for this piece on the current board."""
        piece.move(move, self)
        self.board = [[0] * self.width for i in range(self.length)]
        for piece in self.pieces.values():
            for space in piece.spaces_occupied:
                self.board[space[1]][space[0]] = piece.name

def main():
    gb = GameBoard()
    # This isn't quite what I want because it applies the second move to the
    #   board after the first move is finished, and I really want to branch
    #   and have one board with the first move applied and another board with
    #   with only the second move applied.
    for piece_name in gb.valid_moves.keys():
        for move in gb.valid_moves[piece_name]:
            gb.move(gb.pieces[piece_name], move)
            print(gb)


if __name__ == "__main__":
    main()