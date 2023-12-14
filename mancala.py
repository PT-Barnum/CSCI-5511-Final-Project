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

def alpha_beta_search(one, two, three):
  pass

def minimax(one, two, three):
  pass

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
    for Index in range(TOTAL_SPACES):
        if ((Index != PLAYER_ONE_ZONE) and (Index != PLAYER_TWO_ZONE)):
            if (state.mancala_board[Index] > 0):
                legal_actions.append(Index)
    
    return legal_actions


def result(state, action):
  zone = state.current.get_zone()
  newState = MancalaState(state.other, state.current, copy.deepcopy(state.mancala_board))
  marbles = newState.mancala_board[action]
  
  index = action

  if (action == LAST_ZONE):
    index = PLAYER_ONE_ZONE
  elif (action == 6):
    index = PLAYER_TWO_ZONE
  else:
    index += 1

  while (marbles):
    if (index == PLAYER_ONE_ZONE):
      if (index == zone):
        newState.mancala_board[index] += 1
        marbles -= 1
      index += 1
    elif (index == PLAYER_TWO_ZONE):
      if (index == zone):
        newState.mancala_board[index] += 1
        marbles -= 1
      index += 1
    elif (index == LAST_ZONE):
      newState.mancala_board[index] += 1
      marbles -= 1
      index = FIRST_ZONE
    else:
      newState.mancala_board[index] += 1
      marbles -= 1
      index += 1

    if (marbles == 0):
      marbles = newState.mancala_board[index]
  
  return newState


def terminal_test(state):
    for Index in range(TOTAL_SPACES):
        if ((Index != PLAYER_ONE_ZONE) and (Index != PLAYER_TWO_ZONE)):
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
    state = result(state, action)
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
    state = result(state, action)
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