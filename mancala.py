import random
import copy

# TOTAL_SPACES = PLAYABLE_SPACES + 2 player zones
TOTAL_SPACES = 14
PLAYABLE_SPACES = 12
PLAYER_ONE_ZONE = 0   # Index of Player One's Zone
PLAYER_TWO_ZONE = 7   # Index of Player Two's Zone
FIRST_ZONE = 0
LAST_ZONE = 13

VALID_MOVE = 0
INVALID_MOVE = 1
TAKE_ANOTHER_MOVE = 2
END_MOVE = 3
ERROR_MOVE = 4
MOVING = 5

# TODO: Make utility function
def Utility(zone, state):
  pass

def alpha_beta_search(state, zone, depthlimit):
  if ((depthlimit == 0) or terminal_test(state)):
    val = Utility(zone, state)
    legalActions = actions(state)
    move = random.choice(legalActions)
    return val, move
  return max_value_ab(state, zone, depthlimit, -999999, 999999)


def max_value_ab(state, zone, depthlimit, alpha, beta):
  val = None
  move = None
  if ((depthlimit == 0) or (terminal_test(state))):
    val = Utility(zone, state)
    legalActions = actions(state)
    move = random.choice(legalActions)
    return val, move
  val = -999999
  for action in actions(state):
    v2, a2 = min_value_ab(result(state, action), zone, depthlimit-1, alpha, beta)
    if (v2 > val):
      val, move = v2, action
      alpha = max(val, alpha)
    if (val >= beta):
      return val, move
  return val, move

def min_value_ab(state, zone, depthlimit, alpha, beta):
  val = None
  move = None
  if ((depthlimit == 0) or terminal_test(state)):
    val = Utility(zone, state)
    legalActions = actions(state)
    move = random.choice(legalActions)
    return val, move
  val = 999999
  for action in actions(state):
    v2, a2 = max_value_ab(result(state, action), zone, depthlimit-1, alpha, beta)
    if (v2 < val):
      val, move = v2, action
      beta = min(val, beta)
    if (val <= alpha):
      return val, move
  return val, move


def minimax(state, zone, depthlimit):
  if ((depthlimit == 0) or terminal_test(state)):
    val = Utility(zone, state)
    legalActions = actions(state)
    move = random.choice(legalActions)
    return val, move
  return max_value(state, zone, depthlimit)

def max_value(state, zone, depthlimit):
  if ((depthlimit == 0) or terminal_test(state)):
    val = Utility(zone, state)
    legalActions = actions(state)
    move = random.choice(legalActions)
    return val, move
  val = -999999
  move = None
  for action in actions(state):
    v2, a2 = min_value(state, zone, depthlimit-1)
    if (v2 > val):
      val, move = v2, action
  return val, move

def min_value(state, zone, depthlimit):
  if ((depthlimit == 0) or terminal_test(state)):
    val = Utility(zone, state)
    legalActions = actions(state)
    move = random.choice(legalActions)
    return val, move
  val = 999999
  move = None
  for action in actions(state):
    v2, a2 = max_value(state, zone, depthlimit-1)
    if (v2 < val):
      val, move = v2, action
  return val, move



class MancalaPlayerTemplate:
    def __init__(self, myzone):
        self.zone = myzone

    def get_zone(self):
        return self.zone

    def make_move(self, state):
        return None

class HumanPlayer(MancalaPlayerTemplate):
    def __init__(self, myzone):
        self.zone = myzone

    def get_zone(self):
        return self.zone

    def make_move(self, state):
        curr_move = None
        legals = actions(state)
        while curr_move == None:
            Display(state)
            if self.zone == PLAYER_ONE_ZONE:
                print("Player One ", end='')
            else:
                print("Player Two ", end='')
            print(" to play.")
            print("Legal moves are " + str(legals))
            move = int(input("Enter your move as the index to start at:"))
            if move in legals:
                return move
            else:
                print("That doesn't look like a legal action to me")
        return curr_move

class AlphabetaPlayer(MancalaPlayerTemplate):
    def __init__(self, myzone, depthlimit):
        self.zone = myzone
        self.depthlimit = depthlimit

    def get_zone(self):
        return self.zone
    
    def get_depthlimit(self):
        return self.depthlimit

    def make_move(self, state):
        returnTuple = alpha_beta_search(state, self.zone, self.depthlimit)
        Display(state)
        return returnTuple[1]

class MinimaxPlayer(MancalaPlayerTemplate):
    def __init__(self, myzone, depthlimit):
        self.zone = myzone
        self.depthlimit = depthlimit

    def get_zone(self):
        return self.zone
    
    def get_depthlimit(self):
        return self.depthlimit
    
    def make_move(self, state):
        returnTuple = minimax(state, self.zone, self.depthlimit)
        Display(state)
        return returnTuple[1]

class RandomPlayer(MancalaPlayerTemplate):
  def __init__(self, myzone):
    self.zone = myzone

  def get_zone(self):
    return self.zone

  def make_move(self, state):
    legal = actions(state)
    decision = random.choice(legal)
    Display(state)
    return decision


class MancalaState:
    def __init__(self, current_player, other_player, mancala_board = None):
      if mancala_board != None:
          self.mancala_board = mancala_board
      else:
         self.mancala_board = [0] * 14
         for Index in range(TOTAL_SPACES):
            if ((Index != PLAYER_ONE_ZONE) and (Index != PLAYER_TWO_ZONE)):
              # Index 0 = Player 1 Zone
              # Index 7 = Player 2 Zone
              self.mancala_board[Index] = 8
      self.current = current_player
      self.other = other_player


def player(state):
    return state.current


def actions(state):
  legal_actions = []
  if (state.current.get_zone() == PLAYER_ONE_ZONE):
    for Index in range(1, 7):
      if (state.mancala_board[Index] > 0):
        legal_actions.append(Index)
  else:
    for Index in range(8, 14):
      if (state.mancala_board[Index] > 0):
        legal_actions.append(Index)
    
  return legal_actions


def result(state, action):
  zone = state.current.get_zone()
  marbles = state.mancala_board[action]
  state.mancala_board[action] = 0
  if (action == LAST_ZONE):
    index = PLAYER_ONE_ZONE
  else:
    index = action + 1
  
  while (marbles):
    if (marbles == 1):
      if ((index == PLAYER_ONE_ZONE) and (zone == PLAYER_ONE_ZONE)):
        state.mancala_board[index] += 1
        marbles -= 1
        return TAKE_ANOTHER_MOVE
      elif ((index == PLAYER_TWO_ZONE) and (zone == PLAYER_TWO_ZONE)):
        state.mancala_board[index] += 1
        marbles -= 1
        return TAKE_ANOTHER_MOVE
      elif ((index == PLAYER_ONE_ZONE) and (zone != PLAYER_ONE_ZONE)):
        index += 1
      elif ((index == PLAYER_TWO_ZONE) and (zone != PLAYER_TWO_ZONE)):
        index += 1
      else:
        state.mancala_board[index] += 1
        marbles -= 1
        if (state.mancala_board[index] == 1):
          if ((index < PLAYER_TWO_ZONE) and (zone == PLAYER_ONE_ZONE)):
            if (index == 1):
              state.mancala_board[zone] += state.mancala_board[1]
              state.mancala_board[zone] += state.mancala_board[13]
              state.mancala_board[1] = 0
              state.mancala_board[13] = 0
            elif (index == 2):
              state.mancala_board[zone] += state.mancala_board[2]
              state.mancala_board[zone] += state.mancala_board[12]
              state.mancala_board[2] = 0
              state.mancala_board[12] = 0
            elif (index == 3):
              state.mancala_board[zone] += state.mancala_board[3]
              state.mancala_board[zone] += state.mancala_board[11]
              state.mancala_board[3] = 0
              state.mancala_board[11] = 0
            elif (index == 4):
              state.mancala_board[zone] += state.mancala_board[4]
              state.mancala_board[zone] += state.mancala_board[10]
              state.mancala_board[4] = 0
              state.mancala_board[10] = 0
            elif (index == 5):
              state.mancala_board[zone] += state.mancala_board[5]
              state.mancala_board[zone] += state.mancala_board[9]
              state.mancala_board[5] = 0
              state.mancala_board[9] = 0
            elif (index == 6):
              state.mancala_board[zone] += state.mancala_board[6]
              state.mancala_board[zone] += state.mancala_board[8]
              state.mancala_board[6] = 0
              state.mancala_board[8] = 0
            else:
              return ERROR_MOVE
          elif ((index > PLAYER_TWO_ZONE) and (zone == PLAYER_TWO_ZONE)):
            if (index == 8):
              state.mancala_board[zone] += state.mancala_board[6]
              state.mancala_board[zone] += state.mancala_board[8]
              state.mancala_board[6] = 0
              state.mancala_board[8] = 0
            elif (index == 9):
              state.mancala_board[zone] += state.mancala_board[5]
              state.mancala_board[zone] += state.mancala_board[9]
              state.mancala_board[5] = 0
              state.mancala_board[9] = 0
            elif (index == 10):
              state.mancala_board[zone] += state.mancala_board[4]
              state.mancala_board[zone] += state.mancala_board[10]
              state.mancala_board[4] = 0
              state.mancala_board[10] = 0
            elif (index == 11):
              state.mancala_board[zone] += state.mancala_board[3]
              state.mancala_board[zone] += state.mancala_board[11]
              state.mancala_board[3] = 0
              state.mancala_board[11] = 0
            elif (index == 12):
              state.mancala_board[zone] += state.mancala_board[2]
              state.mancala_board[zone] += state.mancala_board[12]
              state.mancala_board[2] = 0
              state.mancala_board[12] = 0
            elif (index == 13):
              state.mancala_board[zone] += state.mancala_board[1]
              state.mancala_board[zone] += state.mancala_board[13]
              state.mancala_board[1] = 0
              state.mancala_board[13] = 0
            else:
              return ERROR_MOVE
        else:
          return END_MOVE
        
    else:
      if ((index == PLAYER_ONE_ZONE) and (zone != PLAYER_ONE_ZONE)):
        index += 1
      elif ((index == PLAYER_TWO_ZONE) and (zone != PLAYER_TWO_ZONE)):
        index += 1
      elif (index == LAST_ZONE):
        state.mancala_board[index] += 1
        marbles -= 1
        index = PLAYER_ONE_ZONE
      else:
        state.mancala_board[index] += 1
        marbles -= 1
        index += 1
      
  return END_MOVE


def terminal_test(state):
  if (state.current.get_zone() == PLAYER_ONE_ZONE):
    for Index in range(1, PLAYER_TWO_ZONE):
      if (state.mancala_board[Index] != 0):
        return False
  else:
    for Index in range(8, 14):
      if (state.mancala_board[Index] != 0):
        return False

  return True


def Display(state):
  zoneZero = f'{state.mancala_board[0]:02d}'      # PLAYER_ONE_ZONE
  zoneOne = f'{state.mancala_board[1]:02d}'
  zoneTwo = f'{state.mancala_board[2]:02d}'
  zoneThree = f'{state.mancala_board[3]:02d}'
  zoneFour = f'{state.mancala_board[4]:02d}'
  zoneFive = f'{state.mancala_board[5]:02d}'
  zoneSix = f'{state.mancala_board[6]:02d}'
  zoneSeven = f'{state.mancala_board[7]:02d}'     # PLAYER_TWO_ZONE
  zoneEight = f'{state.mancala_board[8]:02d}'
  zoneNine = f'{state.mancala_board[9]:02d}'
  zoneTen = f'{state.mancala_board[10]:02d}'
  zoneEleven = f'{state.mancala_board[11]:02d}'
  zoneTwelve = f'{state.mancala_board[12]:02d}'
  zoneThirteen = f'{state.mancala_board[13]:02d}'

  print()
  print()
  print("==================================================================================")
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("||        ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||        ||" % (zoneOne, zoneTwo, zoneThree, zoneFour, zoneFive, zoneSix))
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("||   %s   ==============================================================   %s   ||" % (zoneZero, zoneSeven))
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("||        ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||        ||" % (zoneThirteen, zoneTwelve, zoneEleven, zoneTen, zoneNine, zoneEight))
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("==================================================================================")
  print()
  print()


def DisplayFinal(state):
  zoneZero = f'{state.mancala_board[0]:02d}'      # PLAYER_ONE_ZONE
  zoneOne = f'{state.mancala_board[1]:02d}'
  zoneTwo = f'{state.mancala_board[2]:02d}'
  zoneThree = f'{state.mancala_board[3]:02d}'
  zoneFour = f'{state.mancala_board[4]:02d}'
  zoneFive = f'{state.mancala_board[5]:02d}'
  zoneSix = f'{state.mancala_board[6]:02d}'
  zoneSeven = f'{state.mancala_board[7]:02d}'     # PLAYER_TWO_ZONE
  zoneEight = f'{state.mancala_board[8]:02d}'
  zoneNine = f'{state.mancala_board[9]:02d}'
  zoneTen = f'{state.mancala_board[10]:02d}'
  zoneEleven = f'{state.mancala_board[11]:02d}'
  zoneTwelve = f'{state.mancala_board[12]:02d}'
  zoneThirteen = f'{state.mancala_board[13]:02d}'

  print()
  print()
  print("==================================================================================")
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("||        ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||        ||" % (zoneOne, zoneTwo, zoneThree, zoneFour, zoneFive, zoneSix))
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("||   %s   ==============================================================   %s   ||" % (zoneZero, zoneSeven))
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("||        ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||        ||" % (zoneThirteen, zoneTwelve, zoneEleven, zoneTen, zoneNine, zoneEight))
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("==================================================================================")
  print()
  print()
  
  print("Player One marbles: " + str(state.mancala_board[PLAYER_ONE_ZONE]))
  print("Player Two marbles: " + str(state.mancala_board[PLAYER_TWO_ZONE]))
  print()

  if (state.mancala_board[PLAYER_ONE_ZONE] > state.mancala_board[PLAYER_TWO_ZONE]):
    print("Player One Wins!")

  elif (state.mancala_board[PLAYER_ONE_ZONE] < state.mancala_board[PLAYER_TWO_ZONE]):
    print("Player Two Wins!")

  else:
    print("It's a Draw!")


def PlayMancala(playerOne=None, playerTwo=None):
  if playerOne == None:
    playerOne = HumanPlayer(PLAYER_ONE_ZONE)
  if playerTwo == None:
    playerTwo = HumanPlayer(PLAYER_TWO_ZONE)

  state = MancalaState(playerOne, playerTwo)
  while True:
    action = playerOne.make_move(state)
    if action not in actions(state):
      print("Illegal move made by Player One")
      print("Player Two wins!")
      return
    moving = TAKE_ANOTHER_MOVE
    while (moving != END_MOVE):
      moving = result(state, action)
      if (moving == ERROR_MOVE):
        print("Illegal move made by Player One")
        print("Player Two wins!")
        return
      elif (moving == TAKE_ANOTHER_MOVE):
        action = playerOne.make_move(state)
    
    newState = MancalaState(state.other, state.current, copy.deepcopy(state.mancala_board))
    state = MancalaState(newState.current, newState.other, copy.deepcopy(newState.mancala_board))
    
    if terminal_test(state):
      print("Game Over")
      Display(state)
      DisplayFinal(state)
      return
    action = playerTwo.make_move(state)
    if action not in actions(state):
      print("Illegal move made by Player Two")
      print("Player One wins!")
      return
    moving = TAKE_ANOTHER_MOVE
    while (moving != END_MOVE):
      moving = result(state, action)
      if (moving == ERROR_MOVE):
        print("Illegal move made by Player One")
        print("Player Two wins!")
        return
      elif (moving == TAKE_ANOTHER_MOVE):
        action = playerTwo.make_move(state)
    
    newState = MancalaState(state.other, state.current, copy.deepcopy(state.mancala_board))
    state = MancalaState(newState.current, newState.other, copy.deepcopy(newState.mancala_board))
    if terminal_test(state):
      print("Game Over")
      Display(state)
      DisplayFinal(state)
      return

def main():
  # TODO: instantiate the board
  PlayMancala()

if __name__ == '__main__':
  main()