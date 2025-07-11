from math import sqrt, floor
from position import Position
from movement import Movement
from random import choice
import copy



class Board:
    """
    This class define the chess board and the game.
    It define the rules, the game state and allow convertion between PGN and
    Coordonate movement (PosA -> PosB)
        Exemple: e2 -> e4
    """

    WHITE = False
    BLACK = True

    def __init__(self) -> None:

        # NOTATION
        # W -> White & B -> Black
        # R -> Rook & N -> Knight & B -> Bishop & K -> King & Q -> Queen
        self.grid = [
            # h     g     f      e    d     c     b     a   y/x
            ['WR', 'WN', 'WB', 'WK', 'WQ', 'WB', 'WN', 'WR'], # 1
            ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'], # 2
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 3
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 4
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 5
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 6
            ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'], # 7
            ['BR', 'BN', 'BB', 'BK', 'BQ', 'BB', 'BN', 'BR']  # 8
        ]

        self.currentPlayer = self.WHITE
        self.turn = 0

    def getGrid(self):
        return self.grid
    
    def resetGrid(self):
        """
        Reset grid to default position.
        """
        self.grid = [
            # h     g     f      e    d     c     b     a   y/x
            ['WR', 'WN', 'WB', 'WK', 'WQ', 'WB', 'WN', 'WR'], # 1
            ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'], # 2
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 3
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 4
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 5
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 6
            ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'], # 7
            ['BR', 'BN', 'BB', 'BK', 'BQ', 'BB', 'BN', 'BR']  # 8
        ]

    def resetEmpty(self):
        """
        Reset grid to empty board.
        """
        self.grid = [
            # h     g     f      e    d     c     b     a   y/x
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 1
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 2
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 3
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 4
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 5
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 6
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 7
            ['00', '00', '00', '00', '00', '00', '00', '00']  # 8
        ]

    def setGrid(self, grid):
        self.grid = grid

    def makeVector(self):
        """
        Make a vector in the following form:
        [
            WPe1,
            WPe2,
            ...
            Wph7,
            WRe1,
            ...
            WRh8,
            ... 
        ]
        With boolean indication if the piece is, or not, in the speficied case
        Here is the order of the pieces:
        WP, WR, WN, WB, WQ, WK, BP, BR, BN, BB, BQ, BK
        """
        # Case vide déterminable après coup
        vector = [self.currentPlayer, self.turn]
        pieces = ['WP', 'WR', 'WN', 'WB', 'WQ', 'WK', 'BP', 'BR', 'BN', 'BB', 'BQ', 'BK']
        for n in range(len(pieces)):
            for i in range(8):
                for j in range(8):
                    if self.grid[i][j] == pieces[n]:
                        vector.append(True)
                    else:
                        vector.append(False)
        return vector

    def setGridFromVector(self, vector):
        pieces = ['WP', 'WR', 'WN', 'WB', 'WQ', 'WK', 'BP', 'BR', 'BN', 'BB', 'BQ', 'BK']
        self.resetEmpty()
        self.currentPlayer = vector.pop(0)
        for n in range(len(pieces)):
            for i in range(8):
                for j in range(8):
                        if vector[n*(8*8) + (i*8+j)]:
                            self.grid[i][j] = pieces[n]

    def nextTurn(self):
        self.currentPlayer = not self.currentPlayer
        self.turn += 1
        
    def isBlack(self, piece):
        """
        Return True if a give piece if black, False otherwise
        """
        if piece == None:
            return False
        else: return piece[0] == "B"

    def isWhite(self, piece):
        """
        Return True if a given piece is white, False otherwise
        """
        if piece == None:
            return False
        else: return piece[0] == "W"

    def isEnemy(self, piece):
        """
        Given a color (switch) describing the team of the player, and a piece
        Tell if the piece is enemie of the player
        """
        return [self.isBlack(piece), self.isWhite(piece)][self.currentPlayer]

    def convertPosition(self, square):
        """
        Convert chess position into grid coordonate
        return None if the coordonate are not correct
        a1 -> (0,0)
        a8 -> (7,0)
        h8 -> (7,7)
        """
        if(len(square) == 2):
            if(square[0] >= 'a' and square[0] <= 'h' and square[1] >= '1' and square[1] <= '8'):
                x = int(square[1]) -1
                y = (ord('h') - ord(square[0]))
                return Position(x,y)
        return None

    def getPiece(self, square):
        """
        Take chess position (cartesian) (0,0) and return the name of the piece at the given position
        return None if the coordonate are not correct
        """
        if square == None:
            return None
        return self.grid[square.x][square.y]
    
    def setPiece(self, pos, piece):
        """
        Take cartesian position, Position object and a piece
        Set the given piece and the given position
        """
        self.grid[pos.x][pos.y] = piece
        
    def movePiece(self, origin, dest):
        """
        Take 2 chess position (cartesian) and move the piece from origin to destination
        Replace the origin position by '00'
        Erase the destination piece if there was one
        Don't check move legality
        """
        originPos = self.convertPosition(origin)
        destPos = self.convertPosition(dest)
        if(originPos == None or destPos == None):
            return False
        
        self.grid[destPos.x][destPos.y] = self.getPiece(originPos)
        self.grid[originPos.x][originPos.y] = '00'
        return True
    
    def display(self):
        """
        Display the game board
        Use "GHost" pawn to show prise en passant possibilities.
        """
        symbol = {
            "BP": '♙',
            "BPG": 'X',     # Ghost black pawn
            "BN": '♘',
            "BB": '♗',
            "BR": '♖',
            "BQ": '♕',
            "BK": '♔',
            "WP": '♟', 
            "WPG": 'X',     # Ghost White Pawn
            "WN": '♞',
            "WB": '♝',
            "WR": '♜', 
            "WQ": '♛',
            "WK": '♚',
            "00": '□'

        }

        index = 1
        print("########################")
        print("h g f e d c b a")
        for line in self.grid:

            for piece in line:
                print(f"{symbol[piece]} ", end="")  
            print(index)
            index += 1
        print("########################") 

    def removeGhost(self):
        """
        Remove all Ghost pawn on the grid and replace it by empty square.
        """
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] == "WPG":
                    self.grid[i][j] = '00'
                elif self.grid[i][j] == "BPG":
                    self.grid[i][j] = '00'

    def checkDiagonal(self, origin, dest, max=100):
        """
        Check if a non linear movement is a corect diagonal.
        We compare the y and x delta, if there equal, the diagonal is correct
        """
        return abs(origin.x - dest.x) == abs(origin.y - dest.y) and abs(origin.y - dest.y) <= max   

    def checkOnMove(self, pos1, pos2, linear=True):
        """
        Check if there is piece on the way from pos1 to pos2
        use cartesian positions
        (x,y)
        """
        current = Position(pos1.x, pos1.y)
        dist = pos1.distance(pos2)

        if linear and (pos1.x != pos2.x and pos1.y != pos2.y):
            return False

        while dist > 0:
            nbMove = (not linear) + 1 # check if you can move diagonally
            if(current.x != pos2.x and nbMove > 0):
                nbMove -= 1
                if(current.x < pos2.x):
                    current.x += 1
                else:
                    current.x -= 1
            if(current.y != pos2.y and nbMove > 0):
                nbMove -= 1
                if(current.y < pos2.y):
                    current.y += 1
                else:
                    current.y -= 1
            
            # check if new position is empty
            if ((self.getPiece(current) != '00' and not self.getPiece(current) in ["WPG", "BPG"]) and not current.equal(pos2)):
                return False 
            dist = current.distance(pos2)
        
        return True


    def isLegalMove(self, move):
        """
        Take a move object describing chess movement (e2 -> e4)
        And tell, with the current board, if the move is legal or not
        Does not take in count check state
        """
        # Rock
        if(move.origin[1:]  == "O-O" or move.origin[1:] == "O-O-O"):
            if move.origin[0] == 'W':
                line = 1
            else:
                line = 8
            return ((
                    self.getPiece(self.convertPosition(f"e{line}")) == f"{move.origin[0]}K" and
                    self.getPiece(self.convertPosition(f"f{line}")) == "00" and
                    self.getPiece(self.convertPosition(f"g{line}")) == "00" and
                    self.getPiece(self.convertPosition(f"h{line}")) == f"{move.origin[0]}R" and 
                    move.origin[1:] == 'O-O')
                or 
                    (self.getPiece(self.convertPosition(f"e{line}")) == f"{move.origin[0]}K" and
                    self.getPiece(self.convertPosition(f"d{line}")) == "00" and
                    self.getPiece(self.convertPosition(f"c{line}")) == "00" and
                    self.getPiece(self.convertPosition(f"b{line}")) == "00" and 
                    self.getPiece(self.convertPosition(f"a{line}")) == f"{move.origin[0]}R" and 
                    move.origin[1:] == 'O-O-O')
                ) 

        # Covert to cartesian coordonate (0,0)
        origin = self.convertPosition(move.origin)
        dest = self.convertPosition(move.dest)

        # Get the piece from the grid
        originPiece = self.getPiece(origin)
        destPiece = self.getPiece(dest)

        # Check coordonates are in the board limits
        if (origin == None or dest == None):
            return False
        
        # Check if the piece go to a piece of the same color or to a King
        if((originPiece[0] == destPiece[0]) and not destPiece in ["WPG", "BPG"]):
            return False

        # Check if promotion exist
        color = ['W', 'B'][self.currentPlayer]
        if not move.promotion in [f'{color}R', f'{color}N', f'{color}B', f'{color}Q', None]:
            return False

        # Check of check
        tmpGrid = copy.deepcopy(self.grid)
        if color == originPiece[0]:    # get player's team
            self.play(move)              # Simulate movement

            if self.isCheck(): 
                self.grid = copy.deepcopy(tmpGrid)
                return False
            self.grid = copy.deepcopy(tmpGrid)


           

        # Piece are going to empty or enemie piece (except king)
        match originPiece:
            case '00':
                return False
            
            case 'WP':       # White Pawn
                # Check if pawn can walk 2 square
                if(origin.distance(dest) <= 2):
                    if(origin.distance(dest) == 2 and origin.x != 1):
                        return False
                    
                    # Check forward movement and piece take
                    if origin.y == dest.y  and origin.x < dest.x and self.checkOnMove(origin, dest) and destPiece == '00': # forward
                        return True
                    if destPiece[0] == "B" and origin.x < dest.x and self.checkOnMove(origin, dest, linear=False) and self.checkDiagonal(origin, dest, max=1):
                        return True
                    
            case 'BP':      # Black Pawn
                # Check if pawn can walk 2 square
                if(origin.distance(dest) <= 2):
                    if(origin.distance(dest) == 2 and origin.x != 6):
                        return False
                    
                    # Check forward movement and piece take
                    if origin.y == dest.y and self.checkOnMove(origin, dest) and origin.x > dest.x and destPiece == '00': # forward
                        return True
                    if destPiece[0] == "W" and origin.x > dest.x and self.checkOnMove(origin, dest, linear=False) and self.checkDiagonal(origin, dest, max=1):
                        return True
                
            case 'WR' | 'BR':       # Rook
                return self.checkOnMove(origin, dest, linear=True)
            
            case 'WN' | 'BN':       # Knight
                return (
                    dest.equal(Position(origin.x +2, origin.y +1)) or
                    dest.equal(Position(origin.x +2, origin.y -1)) or
                    dest.equal(Position(origin.x +1, origin.y +2)) or
                    dest.equal(Position(origin.x +1, origin.y -2)) or
                    dest.equal(Position(origin.x -2, origin.y +1)) or
                    dest.equal(Position(origin.x -2, origin.y -1)) or
                    dest.equal(Position(origin.x -1, origin.y +2)) or
                    dest.equal(Position(origin.x -1, origin.y -2)) 
                    )
            
            case 'WB' | 'BB':       # Bishop
                return self.checkOnMove(origin, dest, linear=False) and self.checkDiagonal(origin, dest)
            
            case 'WQ' | 'BQ':       # Queen
                if origin.x == dest.x or origin.y == dest.y:
                    return self.checkOnMove(origin, dest, linear=True)
                else:
                    return self.checkOnMove(origin, dest, linear=False) and self.checkDiagonal(origin, dest)
                
            case 'WK' | 'BK':        # King
                return floor(origin.distance(dest)) == 1
        return False

    def isCheck(self):
        """
        Check if the current color King is in a check situation.
        """
        color = ['W', 'B'][self.currentPlayer]
        kingPos = ""

        # Find ally king
        for x in range(8):
            for y in range(8):
                if(self.grid[x][y] == f"{color}K"):
                    kingPos = f"{chr(ord('h') - y)}{x + 1}"
                    break

        # For every piece
        for i in range(8):
            for j in range(8):

                # If the piece is an enemy
                if(self.isEnemy(self.grid[i][j])):

                    if(self.isLegalMove(Movement(origin=f"{chr(ord('h') - j)}{i + 1}", dest=kingPos))):
                        return True

        return False
    
    def isCheckMate(self):
        """
        Check if the current player is checkmate
        """
        issueFound = True
        if self.isCheck():
            issueFound = False
            color = ['W', 'B'][self.currentPlayer]
            kingPos = ""

            # Find ally king
            for x in range(8):
                for y in range(8):
                    if(self.grid[x][y] == f"{color}K"):
                        kingPos = f"{chr(ord('h') - y)}{x + 1}"
                        break

            # For every piece
            for i in range(8):
                for j in range(8):

                    # If the piece is an ally
                    # Check for every piece move if it can save the king from checkmate
                    piece = self.getPiece(Position(i,j))
                    if(piece[0] == color):
                        grid = copy.deepcopy(self.grid)


                        for x in range(8):
                            for y in range(8):
                                move = Movement(piece=piece, origin=f"{chr(ord('h') - j)}{i + 1}", dest=f"{chr(ord('h') - y)}{x + 1}")
                                if self.isLegalMove(move):
                                    self.play(move)
                                    if not self.isCheck():
                                        issueFound = True
                                    self.setGrid(copy.deepcopy(grid))
                            
                    
        return not issueFound
        

    def getLegalMoves(self):
        """
        Return a liste of legal move the current player can use
        color take a color constant, WHITE, BLACK
        """
        moves =[]
        color = ['W', 'B'][self.currentPlayer]

        # Find all the player pieces
        for i in range(8):
            for j in range(8):
                if(self.grid[i][j][0] == color):

                    # Check for every square if the move is legal
                    for x in range(8):
                        for y in range(8):
                            if(self.isLegalMove(Movement(f"{chr(ord('h') - j)}{i + 1}", f"{chr(ord('h') - y)}{x + 1}"))):
                                moves.append(Movement(f"{chr(ord('h') - j)}{i + 1}", f"{chr(ord('h') - y)}{x + 1}", None))
                    
        return moves
    
    def play(self, move):
        """
        Play a move is legal, use chess notation
        Return True if the move is played, false howerver.
        Rock is encoded: [color][small/big rock] in move.origin
        """
        # TODO VERIFY CHECK DURING ROCK
        # Small Rock
        if(move.origin[1:] == "O-O"):   
            if move.origin[0] == 'W':
                line = 1
            else:
                line = 8
            self.movePiece(f"e{line}", f"f{line}") # Move king
            self.movePiece(f"f{line}", f"g{line}")
            self.setPiece(self.convertPosition(f"f{line}"), f"{move.origin[0]}R")  # Move rook
            self.setPiece(self.convertPosition(f"h{line}"), '00')
            self.removeGhost()
        # Big Rock
        elif(move.origin[1:] == "O-O-O"):  
            if move.origin[0] == 'W':
                line = 1
            else:
                line = 8
            self.movePiece(f"e{line}", f"d{line}") # Move king
            self.movePiece(f"d{line}", f"c{line}")
            self.setPiece(self.convertPosition(f"d{line}"), f"{move.origin[0]}R") # Move rook
            self.setPiece(self.convertPosition(f"a{line}"), '00')
            self.removeGhost()
        # 2 step pawn movement
        # Add ghost piece when moving 2
        elif(self.convertPosition(move.origin).distance(self.convertPosition(move.dest)) == 2 and move.piece[1] == 'P'):
            self.movePiece(move.origin, move.dest)
            # Format to chess cause it's int here 
            self.setPiece(
                self.convertPosition(f"{move.origin[0]}{round((int(move.origin[1]) + int(move.dest[1])) / 2)}"),
                f"{move.piece[0]}PG"
            ) # Set ghost piece on pawn long start
        # Prise en passant
        elif(move.piece[1] == "P" and self.getPiece(self.convertPosition(move.dest)) in ["WPG", "BPG"]):
            pos = self.convertPosition(move.dest)
            match move.piece[0]:
                case 'W':
                    pos.x -= 1
                case 'B':
                    pos.x += 1
            self.setPiece(pos, '00')
            self.movePiece(move.origin, move.dest)
            self.removeGhost()
        # Promotion
        elif(move.promotion != None):
            self.movePiece(move.origin, move.dest)
            self.setPiece(
                self.convertPosition(move.dest),
                move.promotion
            )
        else:
            self.movePiece(move.origin, move.dest)
            self.removeGhost()
        return True

    def convertPgn(self, PGN):
        """
        Convert PGN formated move into classical chess move used in the rest of the program
        the switch paramater define the player playing, fakse for white, true for black
        We parcour all the piece that match the targeted type, and we check if the move is legal, the first piece with a legal move is moved.
        """
        # Piece analysis
        piece = ["W", "B"][self.currentPlayer]
        output = Movement()

        if PGN == "O-O" or PGN == 'O-O-O': # Small rock & big rock
            output.origin = piece + PGN
            return output    

        if(PGN[0] in ["R", "N", "B", "Q", "K"]):
            piece += PGN[0]
            PGN = PGN[1:]
        else:
            piece += "P"

        output.piece = piece

        ### PRECISION SI 2 PIECE PEUVENT FINIR AU MEME ENDROIT.
        #  la pièce vient de la colonne désigné par la lette
        if((PGN[0] >= 'a' and PGN[0] <= 'h') and ((PGN[1] >= 'a' and PGN[1] <= 'h') or PGN[1] == 'x')):
            column = PGN[0]
            PGN = PGN[1:]
            for i in range(1,9):
                if (self.getPiece(self.convertPosition(f"{column}{i}")) == piece and
                     self.isLegalMove(Movement(piece= piece, origin=f"{column}{i}", dest=f"{PGN[0]}{PGN[1]}"))):
                    output.origin = f"{column}{i}"
                    break

        # La pièce vient de la ligne désigné par le chiffre
        elif((PGN[0] >= '1' and PGN[0] <= '8')) and (PGN[1] == 'x' or (PGN[1] >= 'a' and PGN[1] <= 'h')):
            line = PGN[0]
            PGN = PGN[1:]
            for i in range(1,9):
                if (self.getPiece(self.convertPosition(f"{chr(ord('h') - (i-1))}{line}")) == piece and
                        self.isLegalMove(Movement(piece=piece, origin=f"{chr(ord('h') - (i-1))}{line}", dest=f"{PGN[0]}{PGN[1]}"))
                        ):
                    output.origin = f"{chr(ord('h') - (i-1))}{line}"
                    break

        # La pièce vient de la case désigné par la lettre et le chiffre  
        elif(PGN[0] >= 'a' and PGN[0] <= 'h') and (PGN[1] >= '1' and PGN[1] <= '8') and len(PGN) > 2 and ((PGN[2] >= 'a' and PGN[2] <= 'h') or PGN[1] == 'x'):
                column = PGN[0]
                line = PGN[1]
                PGN = PGN[2:]
                if(self.isLegalMove(Movement(piece=piece, origin=f"{column}{line}", dest=f"{PGN[0]}{PGN[1]}"))):
                    output.origin = f"{column}{line}"

        # Analyse des coordonées du déplacement
        else:
            for i in range(8):
                for j in range(8):
                    if(self.grid[i][j] == piece):
                        if self.isLegalMove(Movement(piece=piece, origin=f"{chr(ord('h') - j)}{i + 1}", dest=f"{PGN[0]}{PGN[1]}")):
                            output.origin = f"{chr(ord('h') - j)}{i + 1}"

        output.dest = f"{PGN[0]}{PGN[1]}"
        PGN = PGN[2:]

        if len(PGN) != 0:
            if PGN[0] == '=':
                output.promotion = f"{output.piece[0]}{PGN[1]}"

        return output
