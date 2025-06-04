import unittest
from chessgame import Board

class testNodeClass(unittest.TestCase):

    def test_getPiece(self):
        board = Board()
        board.setTestGrid()
        self.assertEqual(board.getPiece(board.convertPosition("a4")), "BP")
        self.assertEqual(board.getPiece(board.convertPosition("d1")), "WQ")
        self.assertEqual(board.getPiece(board.convertPosition("e4")), "WK")
        self.assertEqual(board.getPiece(board.convertPosition("g5")), "BP")
        #self.assertEqual(board.getPiece("notacase"), None)
        
    def test_movePiece(self):
        board = Board()
        board.movePiece('a2', 'a3')
        self.assertEqual(board.getPiece(board.convertPosition('a3')), 'WP')

        board.movePiece('a3', 'h8')
        self.assertEqual(board.getPiece(board.convertPosition('h8')), 'WP')
        self.assertEqual(board.getPiece(board.convertPosition('a3')), '00')

    def test_legalMove(self):
        board = Board()
        board.setTestGrid()

        # TODO verifier si la prise en passant est en tounois et l'ajouter si oui 

        # Pawn
        self.assertTrue(board.isLegalMove("c2", "c3")) # Walk one
        self.assertTrue(board.isLegalMove("c2", "c4")) # Walk 2 from start
        self.assertTrue(board.isLegalMove("h4", 'g5')) # take diagonally
        self.assertFalse(board.isLegalMove("b3", "b3")) # take forward
        self.assertFalse(board.isLegalMove("h4", "h6")) # walk 2 from not start
        self.assertFalse(board.isLegalMove("c2", "c1")) # walk backward
        self.assertFalse(board.isLegalMove("c2", "d3")) # walk diagonaly

        # Rook
        self.assertTrue(board.isLegalMove("a1", "a3")) # Move
        self.assertTrue(board.isLegalMove("a1", "a4")) # Take
        self.assertFalse(board.isLegalMove("a1", "a5")) # Jump
        self.assertFalse(board.isLegalMove("h1", "h4")) # Take ally piece
    
        # Queen
        self.assertTrue(board.isLegalMove("d1", "g4")) # Walk diagonally
        self.assertTrue(board.isLegalMove("d1", "d4")) # walk forward
        self.assertFalse(board.isLegalMove("d1", "e3")) # walk like a Knight
        self.assertFalse(board.isLegalMove("d1", "c2")) # take ally piece

        # King
        self.assertTrue(board.isLegalMove("e4", "f5"))  # move 1 diagonaly
        self.assertTrue(board.isLegalMove("e4", "d4")) # move 1 linera
        self.assertFalse(board.isLegalMove("e4", "e6")) # move 2 linera
        self.assertFalse(board.isLegalMove("e4", "c6")) # move 2 diagonally
        self.assertFalse(board.isLegalMove("e4", "g3")) # move like a knight

        # Bishop
        self.assertTrue(board.isLegalMove("f1", "c4")) # Move 3 diagonaly
        self.assertFalse(board.isLegalMove("f1", "f4")) # move forward

        # Knight 
        self.assertTrue(board.isLegalMove("c5", "d7")) # take oponent piece
        self.assertTrue(board.isLegalMove("c5", "a6")) # move
        self.assertFalse(board.isLegalMove("c5","e4")) # jump on ally piece


if __name__ == "__main__":
    unittest.main()