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
def Utility(player, zone, state):
  copy_state = copy.copy(state)
  player_one = state.mancala_board[0]
  num_on_side_one = 0
  player_two = state.mancala_board[7]
  num_on_side_two = 0
  score = 0

  # If a player has 49 marbles then they automatically win
  # if player_one >= 49:
  #   player_one += 20
  #   player_two -= 20
  # elif player_two >= 49:
  #   player_two += 20
  #   player_one += 20
  # # Check how close a player and their opponents is to winning, we multiply the difference of the opponent winning by 0.5 because we should be mainly focused on moves that will g
  # else:
  # #   player_one -= (49 - player_one)
  #   player_one_copy = copy.copy(player_one)
  #   player_one = (49 - player_two)
  # #   player_two -= (49 - player_two)
  #   player_two = (49 - player_one_copy)


  for i in range(1,7):
    # This means that they have the chance to steal
    if (state.mancala_board[i] == 0):
      player_one += 3
      player_two -= 3
    num_on_side_one += state.mancala_board[i]

  for i in range(8, 14):
    # This means that they have the chance to steal
    if (state.mancala_board[i] == 0):
      player_two += 3
      player_one -= 3
    num_on_side_two += state.mancala_board[i]

  player_one = (num_on_side_one * 0.5)
  player_two = (num_on_side_two * 0.5)

  player_one_copy = copy.copy(player_one)

  if player.get_player() == "1":
    score = player_one - player_two
  elif player.get_player() == "2":
    score = player_two - player_one_copy

  # Encourages agent to make the move that will get it another turn

  # if player.get_player() == "1":

  #   if state.mancala_board[1] == 1:
  #     player_one -= 3
  #   elif state.mancala_board[2] == 2:
  #     player_one -= 3
  #   elif state.mancala_board[3] == 3:
  #     player_one -= 3
  #   elif state.mancala_board[4] == 4:
  #     player_one -= 3
  #   elif state.mancala_board[5] == 5:
  #     player_one -= 3
  #   elif state.mancala_board[6] == 6:
  #     player_one -= 3

  #   score = player_one - player_two
  # elif player.get_player() == "2":

  #   if state.mancala_board[8] == 1:
  #     player_two -= 3
  #   elif state.mancala_board[9] == 2:
  #     player_two -= 3
  #   elif state.mancala_board[10] == 3:
  #     player_two -= 3
  #   elif state.mancala_board[11] == 4:
  #     player_two -= 3
  #   elif state.mancala_board[12] == 5:
  #     player_two -= 3
  #   elif state.mancala_board[13] == 6:
  #     player_two -= 3
      
  #   score = player_two - player_one

  return score
  
  

def alpha_beta_search(player, state, zone, depthlimit):
  if ((depthlimit == 0) or terminal_test(state)):
    val = Utility(player, zone, state)
    legalActions = actions(state)
    move = random.choice(legalActions)
    return val, move
  return max_value_ab(player, state, zone, depthlimit, -999999, 999999)


def max_value_ab(player, state, zone, depthlimit, alpha, beta):
  val = None
  move = None
  if ((depthlimit == 0) or (terminal_test(state))):
    val = Utility(player, zone, state)
    legalActions = actions(state)
    if (legalActions == []): 
      return val, None
    move = random.choice(legalActions)
    return val, move
  val = -999999
  for action in actions(state):
    new_state = copy.deepcopy(state)
    result(new_state, action)
    v2, a2 = min_value_ab(player, new_state, zone, depthlimit-1, alpha, beta)
    if (v2 > val):
      val, move = v2, action
      alpha = max(val, alpha)
    if (val >= beta):
      return val, move
  return val, move

def min_value_ab(player, state, zone, depthlimit, alpha, beta):
  val = None
  move = None
  if ((depthlimit == 0) or terminal_test(state)):
    val = Utility(player, zone, state)
    legalActions = actions(state)
    if (legalActions == []): 
      return val, None
    move = random.choice(legalActions)
    return val, move
  val = 999999
  for action in actions(state):
    new_state = copy.deepcopy(state)
    result(new_state, action)
    v2, a2 = max_value_ab(player, new_state, zone, depthlimit-1, alpha, beta)
    if (v2 < val):
      val, move = v2, action
      beta = min(val, beta)
    if (val <= alpha):
      return val, move
  return val, move


def minimax(player, state, zone, depthlimit):
  if ((depthlimit == 0) or terminal_test(state)):
    val = Utility(player, zone, state)
    legalActions = actions(state)
    move = random.choice(legalActions)
    return val, move
  return max_value(player, state, zone, depthlimit)

def max_value(player, state, zone, depthlimit):
  if ((depthlimit == 0) or terminal_test(state)):
    val = Utility(player, zone, state)
    legalActions = actions(state)
    if (legalActions == []): 
      return val, None
    move = random.choice(legalActions)
    return val, move
  val = -999999
  move = None
  for action in actions(state):
    new_state = copy.deepcopy(state)
    result(new_state, action)
    v2, a2 = min_value(player, new_state, zone, depthlimit-1)
    if (v2 > val):
      val, move = v2, action
  return val, move

def min_value(player, state, zone, depthlimit):
  if ((depthlimit == 0) or terminal_test(state)):
    val = Utility(player, zone, state)
    legalActions = actions(state)
    if (legalActions == []): 
      return val, None
    move = random.choice(legalActions)
    return val, move
  val = 999999
  move = None
  for action in actions(state):
    new_state = copy.deepcopy(state)
    result(new_state, action)
    v2, a2 = max_value(player, new_state, zone, depthlimit-1)
    if (v2 < val):
      val, move = v2, action
  return val, move

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.num_playout = 0
        self.value = 0.0

    def is_fully_expanded(self):
        # Check if all possible actions have child nodes
        return len(self.children) == len(self.get_untried_actions())

    def get_untried_actions(self):
        # Return a list of moves that haven't been tried yet
        pass

    def select(self, constant=1.414):
        # Select a child node based on the UCB1 formula
        # UCB1 = value / visits + exploration_weight * sqrt(log(parent_visits) / visits)
        # You may need to adjust the formula based on your specific requirements

        if not self.children:
            return None

        max_value = -99999
          
        for child in self.children:
          curr_value = child.value / child.num_playout + constant * (2 * sqrt(math.log(self.num_playout) / child.num_playout))
          max_value = max(curr_value, max_value)

        return max_value

    def expand(self, action, child_state):
        # Add a child node with the given action and state
        child = Node(state=child_state, parent=self)
        self.children.append(child)
        return child

class MancalaPlayerTemplate:
    def __init__(self, myzone, player):
        self.zone = myzone

    def get_player(self):
      return self.player

    def get_zone(self):
        return self.zone

    def make_move(self, state):
        return None

class HumanPlayer(MancalaPlayerTemplate):
    def __init__(self, myzone, player):
        self.zone = myzone
        self.player = player

    def get_player(self):
      return self.player

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
    def __init__(self, myzone, depthlimit, player):
        self.zone = myzone
        self.depthlimit = depthlimit
        self.player = player

    def get_player(self):
      return self.player

    def get_zone(self):
        return self.zone
    
    def get_depthlimit(self):
        return self.depthlimit

    def make_move(self, state):
        returnTuple = alpha_beta_search(self, state, self.zone, self.depthlimit)
        Display(state)
        return returnTuple[1]

class MinimaxPlayer(MancalaPlayerTemplate):
    def __init__(self, myzone, depthlimit, player):
        self.zone = myzone
        self.depthlimit = depthlimit
        self.player = player

    def get_player(self):
      return self.player

    def get_zone(self):
        return self.zone
    
    def get_depthlimit(self):
        return self.depthlimit
    
    def make_move(self, state):
        returnTuple = minimax(self, state, self.zone, self.depthlimit)
        Display(state)
        return returnTuple[1]

class MonteCarloPlayer(MancalaPlayerTemplate):
    def __init__(self, myzone, depthlimit, player):
        self.zone = myzone
        self.depthlimit = depthlimit
        self.player = player

    def get_player(self):
      return self.player

    def get_zone(self):
        return self.zone
    
    def get_depthlimit(self):
        return self.depthlimit
    
    def make_move(self, state):
        returnTuple = minimax(self, state, self.zone, self.depthlimit)
        Display(state)
        return returnTuple[1]

class RandomPlayer(MancalaPlayerTemplate):
  def __init__(self, myzone, player):
    self.zone = myzone
    self.player = player

  def get_player(self):
    return self.player

  def get_zone(self):
    return self.zone

  def make_move(self, state):
    legal = actions(state)
    if legal != []:
      decision = random.choice(legal)
    else:
      decision = -1
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
  if (action == PLAYER_ONE_ZONE):
    index = LAST_ZONE
  else:
    index = action - 1
  
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
        index = LAST_ZONE
      elif ((index == PLAYER_TWO_ZONE) and (zone != PLAYER_TWO_ZONE)):
        index -= 1
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
        index = LAST_ZONE
      elif ((index == PLAYER_TWO_ZONE) and (zone != PLAYER_TWO_ZONE)):
        index -= 1
      elif ((index == PLAYER_ONE_ZONE) and (zone == PLAYER_ONE_ZONE)):
        state.mancala_board[index] += 1
        marbles -= 1
        index = LAST_ZONE
      else:
        state.mancala_board[index] += 1
        marbles -= 1
        index -= 1
      
  return END_MOVE


def terminal_test(state):
  if (state.current.get_zone() == PLAYER_ONE_ZONE):
    for Index in range(1, PLAYER_TWO_ZONE):
      if (state.mancala_board[Index] != 0):
        return False
    for Index in range(8, LAST_ZONE+1):
      state.mancala_board[PLAYER_TWO_ZONE] += state.mancala_board[Index]
      state.mancala_board[Index] = 0
  else:
    for Index in range(8, LAST_ZONE+1):
      if (state.mancala_board[Index] != 0):
        return False
    for Index in range(1, PLAYER_TWO_ZONE):
      state.mancala_board[PLAYER_ONE_ZONE] += state.mancala_board[Index]
      state.mancala_board[Index] = 0

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
  print("          ||                       Bins on P1 Side                    ||          ")
  print("  Player 1      1         2         3         4         5         6")
  print("==================================================================================")
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("||   P1   ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||   P2   ||" % (zoneOne, zoneTwo, zoneThree, zoneFour, zoneFive, zoneSix))
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("||   %s   ==============================================================   %s   ||" % (zoneZero, zoneSeven))
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("||        ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||        ||" % (zoneThirteen, zoneTwelve, zoneEleven, zoneTen, zoneNine, zoneEight))
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("==================================================================================")
  print("          ||                       Bins on P2 Side                    ||          ")
  print()
  print("               13        12        11        10        9          8     Player 2")
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
  print("          ||                       Bins on P1 Side                    ||          ")
  print("==================================================================================")
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("||   P1   ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||   P2   ||" % (zoneOne, zoneTwo, zoneThree, zoneFour, zoneFive, zoneSix))
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("||   %s   ==============================================================   %s   ||" % (zoneZero, zoneSeven))
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("||        ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||   %s   ||        ||" % (zoneThirteen, zoneTwelve, zoneEleven, zoneTen, zoneNine, zoneEight))
  print("||        ||        ||        ||        ||        ||        ||        ||        ||")
  print("==================================================================================")
  print("          ||                       Bins on P2 Side                    ||          ")
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
    # playerOne = HumanPlayer(PLAYER_ONE_ZONE, "1")
    # playerOne = RandomPlayer(PLAYER_ONE_ZONE, "1")
    playerOne = MinimaxPlayer(PLAYER_ONE_ZONE, 1, "1")
    # playerOne = AlphabetaPlayer(PLAYER_ONE_ZONE, 4, "1")
  if playerTwo == None:
    # playerTwo = HumanPlayer(PLAYER_TWO_ZONE, "2")
    # playerTwo = MinimaxPlayer(PLAYER_TWO_ZONE, 4, "2")
    # playerTwo = RandomPlayer(PLAYER_ONE_ZONE, "2")
    playerTwo = AlphabetaPlayer(PLAYER_TWO_ZONE, 1, "2")

  state = MancalaState(playerOne, playerTwo)
  while True:
    if terminal_test(state):
      print("Game Over")
      Display(state)
      DisplayFinal(state)
      return

    action = playerOne.make_move(state)
    if action not in actions(state) and action != -1:
      print("Illegal move made by Player One")
      print("Player Two wins!")
      return
    elif action not in actions(state) and action == -1 and terminal_test(state):
      print("Game Over")
      Display(state)
      DisplayFinal(state)
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
    if action not in actions(state) != -1:
      print("Illegal move made by Player Two")
      print("Player One wins!")
      return
    elif action not in actions(state) and action == -1 and terminal_test(state):
      print("Game Over")
      Display(state)
      DisplayFinal(state)
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