import unittest

import slidey_puzzle

class TestGamePiece(unittest.TestCase):
    def test_str(self):
        self.board = slidey_puzzle.GameBoard()
        self.assertIn("Purple", str(self.board.p1))
        self.assertIn("Red", str(self.board.r1))
        self.assertIn("Green", str(self.board.g1))
        self.assertIn("Horizontal", str(self.board.h1))
        self.assertIn("Purple", str(self.board.h1))
    
    def test_repr(self):
        self.board = slidey_puzzle.GameBoard()
        self.assertIsInstance(eval(f"slidey_puzzle.{repr(self.board.r1)}"), 
                slidey_puzzle.GamePiece)

    def test_spaces_occupied(self):
        self.board = slidey_puzzle.GameBoard()
        self.board.p1.location = [0, 0]
        self.assertEqual(len(self.board.p1.spaces_occupied), 2)
        self.assertIn([0, 0], self.board.p1.spaces_occupied)
        self.assertIn([0, 1], self.board.p1.spaces_occupied)
        self.board.delete_piece("p1")
        self.board.g1.location = [0, 0]
        self.assertEqual(len(self.board.g1.spaces_occupied), 4)
        self.assertIn([0, 0], self.board.g1.spaces_occupied)
        self.assertIn([1, 0], self.board.g1.spaces_occupied)
        self.assertIn([0, 1], self.board.g1.spaces_occupied)
        self.assertIn([1, 1], self.board.g1.spaces_occupied)
        self.board.delete_piece("g1")
        self.board.h1.location = [0, 0]
        self.assertEqual(len(self.board.h1.spaces_occupied), 2)
        self.assertIn([0, 0], self.board.h1.spaces_occupied)
        self.assertIn([1, 0], self.board.h1.spaces_occupied)
        self.board.delete_piece("h1")
        self.board.r1.location = [0, 0]
        self.assertEqual(len(self.board.r1.spaces_occupied), 1)
        self.assertIn([0, 0], self.board.r1.spaces_occupied)

    def test_move(self):
        self.board = slidey_puzzle.GameBoard()
        # Check that pieces can't move off the edges
        with self.assertRaises(ValueError):
            self.board.p1.move([-1,0], self.board)
        with self.assertRaises(ValueError): 
            self.board.g1.move([0,-1], self.board)
        with self.assertRaises(ValueError): 
            self.board.p3.move([1,0], self.board)
        with self.assertRaises(ValueError): 
            self.board.p4.move([0,1], self.board)

    def test_valid_moves(self):
        # This also tests GameBoard.delete_piece() and, through that, 
        #   also tests GameBoard.re_read_board().
        self.board = slidey_puzzle.GameBoard()
        self.assertEqual(1, len(self.board.p1.valid_moves(self.board)))
        self.assertIn([0,-1], self.board.p1.valid_moves(self.board))
        self.assertEqual(1, len(self.board.p3.valid_moves(self.board)))
        self.assertIn([0,-1], self.board.p3.valid_moves(self.board))
        self.assertEqual(0, len(self.board.p2.valid_moves(self.board)))
        self.assertEqual(0, len(self.board.p4.valid_moves(self.board)))
        self.assertEqual(0, len(self.board.g1.valid_moves(self.board)))
        self.assertEqual(0, len(self.board.h1.valid_moves(self.board)))
        self.assertEqual(0, len(self.board.r1.valid_moves(self.board)))
        self.assertEqual(0, len(self.board.r2.valid_moves(self.board)))
        self.assertEqual(0, len(self.board.r3.valid_moves(self.board)))
        self.assertEqual(0, len(self.board.r4.valid_moves(self.board)))
        self.board.delete_piece("p1")
        self.assertEqual(1, len(self.board.h1.valid_moves(self.board)))
        self.assertIn([-1,0], self.board.h1.valid_moves(self.board))
        self.assertEqual(1, len(self.board.p2.valid_moves(self.board)))
        self.assertIn([0,-1], self.board.p2.valid_moves(self.board))
        self.board.move('p2', [0,-1])
        self.assertEqual(1, len(self.board.g1.valid_moves(self.board)))
        self.assertIn([-1,0], self.board.g1.valid_moves(self.board))
        self.assertEqual(2, len(self.board.p2.valid_moves(self.board)))
        self.assertIn([0,-1], self.board.p2.valid_moves(self.board))
        self.assertIn([0,1], self.board.p2.valid_moves(self.board))
        self.assertEqual(1, len(self.board.r2.valid_moves(self.board)))
        self.assertIn([-1,0], self.board.r2.valid_moves(self.board))
        self.assertEqual(0, len(self.board.r1.valid_moves(self.board)))
        self.assertEqual(0, len(self.board.r3.valid_moves(self.board)))
        self.assertEqual(0, len(self.board.r4.valid_moves(self.board)))
        self.assertEqual(0, len(self.board.h1.valid_moves(self.board)))

class TestBoard(unittest.TestCase):
    def test_str(self):
        self.board = slidey_puzzle.GameBoard()
        self.assertEqual(2, str(self.board).count("xx"))
        self.assertEqual(2, str(self.board).count("p1"))
        self.assertEqual(2, str(self.board).count("p2"))
        self.assertEqual(2, str(self.board).count("p3"))
        self.assertEqual(2, str(self.board).count("p4"))
        self.assertEqual(2, str(self.board).count("h1"))
        self.assertEqual(4, str(self.board).count("g1"))
        self.assertEqual(1, str(self.board).count("r1"))
        self.assertEqual(1, str(self.board).count("r2"))
        self.assertEqual(1, str(self.board).count("r3"))
        self.assertEqual(1, str(self.board).count("r4"))

    def test_valid_moves(self):
        # This also tests some valid moves for GameBoard.move()
        self.board = slidey_puzzle.GameBoard()
        self.assertEqual(2, len(self.board.valid_moves.items()))
        self.assertIn("p1", self.board.valid_moves.keys())
        self.assertIn("p3", self.board.valid_moves.keys())
        self.assertEqual([[0,-1]], list(self.board.valid_moves.values())[0])
        self.assertEqual([[0,-1]], list(self.board.valid_moves.values())[1])
        self.board.move("p1", [0, -1])
        self.board.move("h1", [-1, 0])
        valid_moves = self.board.valid_moves
        self.assertEqual(3, len(valid_moves.items()))
        self.assertIn("r3", valid_moves.keys())
        self.assertIn("h1", valid_moves.keys())
        self.assertIn("p3", valid_moves.keys())
        self.assertEqual([[0, -1]], valid_moves["r3"])
        self.assertEqual([[1, 0]], valid_moves["h1"])
        self.assertEqual([[0, -1]], valid_moves["p3"])

    def test_move(self):
        # Only testing invalud moves here because we've already tested valid
        self.board = slidey_puzzle.GameBoard()
        # Move off edges
        with self.assertRaises(ValueError):
            self.board.move("p1", [-1, 0])
        self.board = slidey_puzzle.GameBoard()
        with self.assertRaises(ValueError):
            self.board.move("g1", [0, -1])
        self.board = slidey_puzzle.GameBoard()
        with self.assertRaises(ValueError):
            self.board.move("p4", [1, 0])
        self.board = slidey_puzzle.GameBoard()
        with self.assertRaises(ValueError):
            self.board.move("p4", [0, 1])
        # Move onto other pieces
        self.board = slidey_puzzle.GameBoard()
        with self.assertRaises(ValueError):
            self.board.move("g1", [-1, 0])
        self.board = slidey_puzzle.GameBoard()
        with self.assertRaises(ValueError):
            self.board.move("g1", [1, 0])
        self.board = slidey_puzzle.GameBoard()
        with self.assertRaises(ValueError):
            self.board.move("g1", [0, 1])
        self.board = slidey_puzzle.GameBoard()
        with self.assertRaises(ValueError):
            self.board.move("r1", [-1, 0])
        self.board = slidey_puzzle.GameBoard()
        with self.assertRaises(ValueError):
            self.board.move("r1", [1, 0])
        self.board = slidey_puzzle.GameBoard()
        with self.assertRaises(ValueError):
            self.board.move("r1", [0, -1])
        self.board = slidey_puzzle.GameBoard()
        with self.assertRaises(ValueError):
            self.board.move("r1", [0, 1])