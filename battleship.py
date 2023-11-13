import sys

BOARD_LENGTH = 10

EMPTY = 0
SHIP_PRESENT = 1
MISS = 2
HIT = 3

def InitBoard( ):
  return [ [ 0 ] * 10 ] * 10

def Display( MyBoard, OpponentBoard ):
  print( "      Your Board         " )
  print( "-------------------------" )
  for i in range( len( MyBoard ) ):
    print( "--------------------------------------------------")
    for j in range( len( MyBoard[0] ) ):
      print( "| " + str( MyBoard[i][j] ) + " |" )
    print("\n")

  print( "       Opponent's Board        " )
  print( "-------------------------------" )
  for i in range( len( OpponentBoard ) ):
    print( "--------------------------------------------------")
    for j in range( len( OpponentBoard[0] ) ):
      print( "| " + str( OpponentBoard[i][j] ) + " |" )
    print("\n")

def ValidCoordinates(shipSize, startX, startY, endX, endY, board):
  startInBounds = (startX >= 0) and (startX < BOARD_LENGTH) and (startY >= 0) and (startY < BOARD_LENGTH)
  endInBounds = (endX >= 0) and (endX < BOARD_LENGTH) and (endY >= 0) and (endY < BOARD_LENGTH)
  if(startInBounds and endInBounds):
    if((endX - startX == shipSize) and (endY == startY)):
      for Index in range(shipSize):
        if (board[startX + Index][startY] != EMPTY):
          return False
        
      for Index in range(shipSize):
        board[startX + Index][startY] = SHIP_PRESENT
      return True
    
    elif((endX == startX) and (endY - startY == shipSize)):
      for Index in range(shipSize):
        if (board[startX][startY + Index] != EMPTY):
          return False
        
      for Index in range(shipSize):
        board[startX][startY + Index] = SHIP_PRESENT
      return True
    
    else:
      return False
    
  else:
    return False


def ShipAdded(shipSize, start, end, board):
  startX = int(start[0])
  startY = int(start[2])
  endX = int(end[0])
  endY = int(end[2])
  if (ValidCoordinates(shipSize, startX, startY, endX, endY, board)): 
    return True
  else:
    return False


def PlaceShips(board):
  shipsArray = [ 5, 4, 3, 3, 2 ]
  carrier = 5
  battleship = 4
  destroyer = 3
  submarine = 3
  patrolBoat = 2

  while ( len(shipsArray) > 0 ):
    print("Ship sizes remaining: " + str(shipsArray) + "\n")
    shipSize = input("Enter size of ship to place on board: ")
    if (shipSize not in shipsArray):
      print("Invalid ship size")
    else:
      start = input("Enter starting coordinates for ship: ")
      end = input("Enter ending coordinates for the ship: ")
      if (ShipAdded(shipSize, start, end, board) == True):
        shipsArray.remove(shipSize)
      else:
        print("Invalid coordinates for adding ship")
  return


class HumanPlayer:
  def __init__( self ):
    self.action = None
    self.defeated = False
    self.myBoard = InitBoard( )       # Player's board with ships
    self.opponentBoard = InitBoard( ) # Opponent's board, initially empty
                                      # This will hold the actions this player
                                      # calls against the opponent
  
  def get_myBoard(self):
    return self.myBoard
  
  def get_opponentBoard(self):
    return self.opponentBoard
  
  def is_defeated(self):
    return self.defeated
  
  def declare_defeat(self):
    self.defeated = True


def main( ):  
  player1 = None
  player2 = None
  
  if (len(sys.argv) < 2):
    player1 = HumanPlayer()
    player2 = HumanPlayer() # Switch to a random player once game is functional
  
  PlaceShips(player1.get_myBoard())
  PlaceShips(player2.get_myBoard())

  while (True):
    if (player1.is_defeated()):
      print("Player 2 has won")
      return 0
    
    player1.Turn()

    if (player2.is_defeated()):
      print("Player 1 has won")
      return 0

    player2.Turn()


if __name__ == '__main__':
  main()