from dataclasses import dataclass
from copy import deepcopy

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
        # Color: 'r' = Red, 'p' = Purple, 'g' = Green, 'h' = Horizontal Purple
        self.color = color

    def __str__(self) -> str:
        match self.color:
            case 'r':
                color = "Red"
            case 'p':
                color = "Purple"
            case 'g':
                color = "Green"
            case 'h':
                color = "Horizontal Purple"
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
                if space[0] + choice[0] >= gb.width or space[0] + choice[0] < 0:
                    is_valid = False
                    continue
                if space[1] + choice[1] >= gb.length or space[1] + choice[1] < 0:
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
        if (direction not in [[1,0], [0,1], [-1,0], [0,-1]]):
            raise ValueError(f"direction given was {direction}." +
                    "Direction must be in [[1,0], [0,1], [-1,0], [0,-1]]")
        self.location[0] += direction[0]
        for space in self.spaces_occupied:
            if space[0] not in range(gb.width):
                raise ValueError(f"\nMoving piece {str(self)} in direction " +
                        f"{direction} moves this piece past the edge.")
        self.location[1] += direction[1]
        for space in self.spaces_occupied:
            if space[1] not in range(gb.length):
                raise ValueError(f"\nMoving piece {str(self)} in direction " +
                        f"{direction} moves this piece past the edge.")
        for self_space in self.spaces_occupied:
            for piece in gb.pieces.values():
                for other_space in piece.spaces_occupied:
                    if piece != self and self_space == other_space:
                        raise ValueError(f"\nMoving piece {str(self)} in " +
                                f"direction {direction} moves this piece " + 
                                f"onto piece {str(piece)}.")

class GameBoard:
    def __init__(self):
        self.width = 4
        self.length = 5
        # Notice that we can't use e.g. [[0] * 4] * 5 because the * 5 produces
        #   shallow copies, i.e. 5 pointers to one list of length 4.
        self.board = [[0] * self.width for i in range(self.length)]
        self.p1 = GamePiece(1, 1, 2, 0, 1, 'p')
        self.p2 = GamePiece(2, 1, 2, 0, 3, 'p')
        self.p3 = GamePiece(3, 1, 2, 3, 1, 'p')
        self.p4 = GamePiece(4, 1, 2, 3, 3, 'p')
        self.h1 = GamePiece(1, 2, 1, 1, 2, 'h')
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
                self.h1.name: self.h1, 
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
    def valid_moves(self) -> list["Move"]:
        """Find all possible valid moves for the entire game board."""
        valid_moves = []
        for piece in self.pieces.values():
            moves = piece.valid_moves(self)
            if moves:
                for move in moves:
                    valid_moves.append(Move(piece.name, move))
        return valid_moves

    def move(self, move: "Move") -> None:
        """Carry out move for this piece on the current board."""
        piece = self.pieces[move.piece]
        piece.move(move.direction, self)
        self.re_read_board()

    def re_read_board(self) -> None:
        """Reset the board attribute so matches the current piece state."""
        self.board = [[0] * self.width for i in range(self.length)]
        for piece in self.pieces.values():
            for space in piece.spaces_occupied:
                self.board[space[1]][space[0]] = piece.name

    def delete_piece(self, piece_name: str) -> None:
        del self.pieces[piece_name]
        exec(f"del self.{piece_name}")
        self.re_read_board()

@dataclass
class Move:
    """Just a struct to represent a move"""
    piece: str
    # Intended: from [1,0], [-1,0], [0,1], [0,-1].  See GamePiece.move()
    direction: list[int]

    def __str__(self) -> str:
        return self.piece + " " + str(self.direction)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Move):
            return False
        return self.piece == other.piece and self.direction == other.direction

@dataclass
class State:
    """Just a struct to represent a state of the puzzle and how we got there."""
    board: list[list[int | str]]
    moves: list["Move"]

    def __str__(self) -> str:
        ret_str = str(self.board) + "["
        for move in self.moves: 
            ret_str += str(move) + ", "
        if self.moves:
            ret_str = ret_str[:-2]
        ret_str += "]\n"
        return ret_str

def deja_vu(
        current_board: "GameBoard", 
        # type is list of board states
        reached_states: list["State"],
) -> bool:
    """Check if state has been reached before.
    
    Notice that this includes swaps of pieces of same color."""
    reached_states_boards = [r.board for r in reached_states]
    if current_board.board in reached_states_boards:
        return True
    # First check if both empty squares are in the same spot.
    possible_matches = []
    cur_empties = []
    for i, row in enumerate(current_board.board):
        for j, entry in enumerate(row):
            if entry == 0:
                cur_empties.append([i, j])
    for board in reached_states_boards:
        no_match = False
        for i, row in enumerate(board.board):
            for j, entry in enumerate(row):
                if entry == 0:
                    if [i, j] not in cur_empties:
                        no_match = True
            if no_match: continue
        if not no_match:
            possible_matches.append(board)
    if not possible_matches:
        return False
    # So, now we have only boards with empty spaces in the same spot as current.
    # Now, check if pieces the same color are swapped.
    for board in possible_matches:
        no_match = False
        for hist_piece in board.pieces.values():
            if hist_piece.color == 'g' or hist_piece.color == 'h': continue
            match_found = False
            for cur_piece in current_board.pieces.values():
                if (hist_piece.color == cur_piece.color and 
                        hist_piece.location == cur_piece.location):
                    match_found = True
                    break
            if not match_found:
                no_match = True
                continue              
        if not no_match:
            return True
    return False

def main():
    total_moves = 0
    branches_ended = 0
    reached_states = []
    unexplored_moves = []
    gb = GameBoard()
    state = State(deepcopy(gb), [])
    reached_states.append(state)
    valid_moves = gb.valid_moves
    for move in valid_moves:
        unexplored_moves.append((state, move))
    while total_moves < 1000:
        total_moves += 1
        state, move = unexplored_moves.pop(0)
        board = deepcopy(state.board)
        board.move(move)
        if not deja_vu(board, reached_states):
            new_moves = state.moves + [move]
            new_state = State(deepcopy(board), new_moves)
            reached_states.append(new_state)
            for move in board.valid_moves:
                unexplored_moves.append((new_state, move))
        else:
            branches_ended += 1
            # TODO: Compare move sequences, save shorter
        print(f"Moves: {total_moves} Reached: {len(reached_states)} Unex: {len(unexplored_moves)} Ends: {branches_ended}", end="\r")
    print()

if __name__ == "__main__":
    main()