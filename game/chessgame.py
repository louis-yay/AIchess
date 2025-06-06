from math import sqrt, floor
from position import Position
from movement import Movement
from random import choice



class Board:

    def __init__(self) -> None:

        # NOTATION
        # W -> White & B -> Black
        # R -> Rook & N -> Knight & B -> Bishop & K -> King & Q -> Queen
        self.grid = [
            # a     b    c       d     e     f     g     h   y/x
            ['WR', 'WN', 'WB', 'WK', 'WQ', 'WB', 'WN', 'WR'], # 1
            ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'], # 2
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 3
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 4
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 5
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 6
            ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'], # 7
            ['BR', 'BN', 'BB', 'BK', 'BQ', 'BB', 'BN', 'BR']  # 8
        ]

    def getGrid(self):
        return self.grid
    
    def resetGrid(self):
        self.grid = [
            # a     b    c       d     e     f     g     h   y/x
            ['WR', 'WN', 'WB', 'WK', 'WQ', 'WB', 'WN', 'WR'], # 1
            ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'], # 2
            ['00', '00', '00', '00', '00', '00', 'BP', '00'], # 3
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 4
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 5
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 6
            ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', '00', 'BP'], # 7
            ['BR', 'BN', 'BB', 'BK', 'BQ', 'BB', 'BN', 'BR']  # 8
        ]

    def setTestGrid(self):
        self.grid = [
            # a     b    c       d     e     f     g     h   y/x
            ['WR', '00', '00', 'WQ', '00', 'WB', '00', '00'], # 1
            ['00', '00', 'WP', '00', '00', 'WP', '00', '00'], # 2
            ['00', 'WP', '00', '00', '00', '00', '00', '00'], # 3
            ['BP', 'BP', '00', '00', 'WK', '00', '00', 'WP'], # 4
            ['00', '00', 'WN', '00', '00', '00', 'BN', '00'], # 5
            ['00', '00', '00', '00', 'WR', '00', '00', '00'], # 6
            ['00', '00', '00', 'BR', '00', '00', '00', '00'], # 7
            ['00', '00', '00', '00', '00', '00', '00', '00']  # 8
        ]

    def setConvertGrid(self):
        self.grid = [
            # a     b    c       d     e     f     g     h   y/x
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 1
            ['00', 'WN', '00', '00', '00', 'WN', '00', 'WP'], # 2
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 3
            ['00', '00', '00', 'WR', '00', '00', '00', '00'], # 4
            ['00', '00', '00', '00', '00', '00', '00', '00'], # 5
            ['WQ', '00', '00', '00', '00', '00', '00', '00'], # 6
            ['00', '00', '00', 'WR', '00', '00', 'WP', '00'], # 7
            ['00', '00', '00', '00', '00', '00', '00', '00']  # 8
        ]

    def Sign(self, value):
        if value < 0:
            return -1
        else:
            return 1
        
    def isBlack(self, piece):
        if piece == None:
            return False
        else: return piece[0] == "B"

    def isWhite(self, piece):
        if piece == None:
            return False
        else: return piece[0] == "W"

    def isEnemy(self, piece, switch=False):
        """
        Switch false = player play white
        Switch true = player play black
        Switch tell about player team
        """
        return [self.isBlack(piece), self.isWhite(piece)][switch]

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
                y = (ord(square[0]) - ord('a'))
                return Position(x,y)
        return None

    def getPiece(self, square):
        """
        Take chess position (cartesian) and return the name of the piece at the given position
        return None if the coordonate are not correct
        """
        if square == None:
            return None
        return self.grid[square.x][square.y]
        
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
        """
        index = 1
        print("########################")
        print("a  b  c  d  e  f  g  h")
        for line in self.grid:

            for piece in line:
                print(f"{piece} ", end="")  
            print(index)
            index += 1
        print("########################") 

    def checkDiagonal(self, origin, dest, max=100):
        return abs(origin.x - dest.x) == abs(origin.y - dest.y) and abs(origin.y - dest.y) <= max   

    def checkOnMove(self, pos1, pos2, linear=True):
        """
        Check if there is piece on the way from pos1 to pos2
        use cartesian positions
        (x,y)
        """
        current = Position(pos1.x, pos1.y)
        dist = pos1.distance(pos2)

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
            if (self.getPiece(current) != '00' and not current.equal(pos2)):
                return False 
            dist = current.distance(pos2)
        
        return True

            

    def isLegalMove(self, origin, dest):
        # TODO ADD promotion system

        """
        Take 2 chess position and check if the move is legal or not.
        """
        
        origin = self.convertPosition(origin)
        dest = self.convertPosition(dest)

        originPiece = self.getPiece(origin)
        destPiece = self.getPiece(dest)

        # Check coordonates are in the board limits
        if (origin == None or dest == None):
            return False
        
        # Check if the piece go to a piece of the same color or to a King
        if(originPiece[0] == destPiece[0] or destPiece[1] == 'K'):
            return False


        # Piece are going to empty or enemie piece (except king)
        # TODO finish the rules of the game
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
                
            case 'WK' | 'BK':       # King
                  return floor(origin.distance(dest)) == 1
        return False
    
    def getLegalMoves(self, color):
        """
        Return a liste of legal move the current player can use
        Color: 'W' or 'B' for White and Black current player team
        """
        moves =[]
        for i in range(8):
            for j in range(8):
                if(self.grid[i][j][0] == color):
                    for x in range(8):
                        for y in range(8):
                            if(self.isLegalMove(f"{chr(ord('a') + j)}{i + 1}", f"{chr(ord('a') + y)}{x + 1}")):
                                moves.append(Movement(f"{chr(ord('a') + j)}{i + 1}", f"{chr(ord('a') + y)}{x + 1}", None))
                    
        return moves
    
    def play(self, origin, dest):
        if(self.isLegalMove(origin, dest)):
            self.movePiece(origin, dest)

    def convertPgn(self, PGN, switch=False):
        """
        Convert PGN formated move into classical chess move used in the rest of the program
        the switch paramater define the player playing, fakse for white, true for black
        We parcour all the piece that match the targeted type, and we check if the move is legal, the first piece with a legal move is moved.
        """
        if PGN == "O-O":
            pass    # Small rock
        if PGN == "O-O-O":
            pass    # Big rock

        # Piece analysis
        piece = ["W", "B"][switch]
        output = Movement()
        if(PGN[0] in ["R", "N", "B", "Q", "K"]):
            piece += PGN[0]
            PGN = PGN[1:]
        else:
            piece += "P"
        
        ### PRECISION SI 2 PIECE PEUVENT FINIR AU MEME ENDROIT.
        #  la pièce vient de cette colonne
        if((PGN[0] >= 'a' and PGN[0] <= 'h') and ((PGN[1] >= 'a' and PGN[1] <= 'h') or PGN[1] == 'x')):
            for i in range(1,9):
                if self.getPiece(self.convertPosition(f"{PGN[0]}{i}")) == piece:
                    output.origin = f"{PGN[0]}{i}"
                    PGN = PGN[1:]
                    break
        elif((PGN[0] >= '1' and PGN[0] <= '8')) and (PGN[1] == 'x' or (PGN[1] >= 'a' and PGN[1] <= 'h')):
            for i in range(1,9):
                if self.getPiece(self.convertPosition(f"{chr(ord('a') + i)}{PGN[0]}")) == piece:
                    output.origin = f"{chr(ord('a') + i)}{PGN[0]}"
                    PGN = PGN[1:]
                    break
        elif((PGN[0] >= 'a' and PGN[0] <= 'h') and (PGN[1] >= '1' and PGN[1] <= '8') and len(PGN) > 2 and ((PGN[2] >= 'a' and PGN[2] <= 'h') or PGN[1] == 'x')):
                output.origin = f"{PGN[0]}{PGN[1]}"
                PGN = PGN[2:]
        else:
            for i in range(8):
                for j in range(8):
                    if(self.grid[i][j] == piece):
                        if self.isLegalMove(f"{chr(ord('a') + j)}{i + 1}", f"{PGN[0]}{PGN[1]}"):
                            output.origin = f"{chr(ord('a') + j)}{i + 1}"

        output.dest = f"{PGN[0]}{PGN[1]}"
        PGN = PGN[2:]


        PGN.replace('x', "")
        if len(PGN) != 0:
            if PGN[0] == '=':
                output.promotion == PGN[1]

        return output


        



            

                    



board = Board()
turn = False

while True:
    board.display()
    input(">>>")
    move = choice(board.getLegalMoves('W'))
    print(f"PLAYER: {move.origin} -> {move.dest}")
    board.play(move.origin, move.dest)

