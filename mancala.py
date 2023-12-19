import random
import copy
import sys
import math

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
  if player_one >= 49:
    player_one += 20
    player_two -= 20
  elif player_two >= 49:
    player_two += 20
    player_one += 20
  # Check how close a player and their opponents is to winning, we multiply the difference of the opponent winning by 0.5 because we should be mainly focused on moves that will g
  else:
    player_one -= (49 - player_one)
    # player_one_copy = copy.copy(player_one)
    # player_one -= (49 - player_two)
    player_two -= (49 - player_two)
    # player_two -= (49 - player_one_copy)

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

  if player.get_zone() == PLAYER_ONE_ZONE:
    score = player_one - player_two
  elif player.get_zone() == PLAYER_TWO_ZONE:
    score = player_two - player_one_copy
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
    def __init__(self, state, zone, untried_actions, depth, action=None, parent=None):
        self.state = state
        self.zone = zone
        self.action = action
        self.untried_actions = untried_actions
        self.depth = depth
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0

    def is_fully_expanded(self, actions):
        # Check if all possible actions have child nodes
        return len(self.children) == len(actions)

    def get_remaining_moves(self):
        # Return a list of moves that haven't been tried yet
        if self.untried_actions == None:
          self.untried_actions = actions(self.state)
        return self.untried_actions

    def select(self, constant):


        max_value = -999999
        best_node = None
          
        for child in self.children:
          print("CHILD")
          curr_value = child.value / child.visits + constant * (2 * ((math.log(self.visits) / child.visits) ** 0.5))
          if curr_value > max_value:
            max_value = curr_value
            best_node = child
        if best_node == None:
          print(self.children)
        return best_node

    def expand(self, child_state, curr_action=None):
        # Add a child node with the given action and state
        if actions(child_state) == []:
          return self
        curr_action = random.choice(actions(child_state))
        result(child_state, curr_action)
        child = Node(state=child_state, zone=self.zone, action=curr_action, parent=self, untried_actions=actions(child_state), depth=self.depth-1)
        self.children.append(child)
        return child

    def back_propogate(self, node, i):
      result_state = node.state
      print("BACKING")
      print(i)
      if node.parent == None:
        return
      if (node.zone == PLAYER_ONE_ZONE):
        if (result_state.mancala_board[0] > result_state.mancala_board[7]):
          node.value += 1
      elif (node.zone == PLAYER_TWO_ZONE):
        if (node.state.mancala_board[7] > node.state.mancala_board[0]):
          node.value += 1
      node.visits += 1

      self.back_propogate(node.parent, i+1)

    # def best_child(self):
    #   best_node = None
    #   max_playouts = 0
    #   for child in self.children:
    #     if child.num_playout > max_playout:
    #       best_node = child
    #       max_playout = child.num_playout

    #   return best_node.action

def search(root):
  root.untried_actions = actions(root.state)
  if len(root.untried_actions) == 1:
    return root.untried_actions[0]
  # Initializing first layer of leaf nodes
  if root.children == []:
    for action in root.untried_actions:
      child_state = copy.deepcopy(root.state)
      result(child_state, action)
      root.expand(child_state, action)
    root.untried_actions = []
  print("SEARCHING")
  print(root.children)
  
  # Simulating a game for each initial node
  for child in root.children:
    game_result = SimulateMancala(child, child.state)
    if (game_result == True):
      child.value += 1
      root.value += 1
    child.visits += 1
    root.visits += 1


  root.depth -= 1
      
  while root.depth != 0:
    new_state = copy.deepcopy(root.state)
    leaf = root.select(1.414)
    print("Visits")
    print(leaf.visits)
    child = leaf.expand(new_state)
    simulated_result = SimulateMancala(child, child.state)
    root.back_propogate(child, 0)
    root.depth -= 1
  
  best_child = None
  max_visits = -99999
  for child in root.children:
    if child.visits > max_visits and child.action in actions(root.state):
      max_visits = child.visits
      best_child = child

  # print(best_child.action)
  return best_child.action


## SELECTION
    

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
        returnTuple = alpha_beta_search(self, state, self.zone, self.depthlimit)
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
        returnTuple = minimax(self, state, self.zone, self.depthlimit)
        Display(state)
        return returnTuple[1]

class RandomPlayer(MancalaPlayerTemplate):
  def __init__(self, myzone):
    self.zone = myzone

  def get_zone(self):
    return self.zone

  def make_move(self, state):
    legal = actions(state)
    if legal != []:
      decision = random.choice(legal)
    else:
      decision = -1
    # Display(state)
    return decision

class MonteCarloPlayer(MancalaPlayerTemplate):
  def __init__(self, myzone, depth):
    self.zone = myzone
    self.depthlimit = depth

  def get_zone(self):
    return self.zone
    
  def get_depthlimit(self):
    return self.depthlimit
    
  def make_move(self, state):
    node = Node(state, self.get_zone(), untried_actions=actions(state), depth=self.get_depthlimit())
    decision = search(node)
    print(decision)
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

def SimulateMancala(child, state):
  playerOne = RandomPlayer(PLAYER_ONE_ZONE)
  playerTwo = RandomPlayer(PLAYER_TWO_ZONE)

  while True:

    action = playerOne.make_move(state)
    if action not in actions(state) and action != -1:
      # print("Illegal move made by Player One")
      # print("Player Two wins!")
      if (child.zone == PLAYER_TWO_ZONE):
        return True
      else:
        return False
    elif action not in actions(state) and action == -1 and terminal_test(state):
      # print("Game Over")
      # Display(state)
      # DisplayFinal(state)
      if (state.mancala_board[0] >= 49 and child.zone == PLAYER_ONE_ZONE):
        return True
      elif (state.mancala_board[0] >= 49 and child.zone == PLAYER_TWO_ZONE):
        return False
      elif (state.mancala_board[7] >= 49 and child.zone == PLAYER_ONE_ZONE):
        return False
      elif (state.mancala_board[7] >= 49 and child.zone == PLAYER_TWO_ZONE):
        return True
    moving = TAKE_ANOTHER_MOVE
    while (moving != END_MOVE):
      moving = result(state, action)
      if (moving == ERROR_MOVE):
        # print("Illegal move made by Player One")
        # print("Player Two wins!")
        if (child.zone == PLAYER_TWO_ZONE):
          return True
        else:
          return False
      elif (moving == TAKE_ANOTHER_MOVE):
        action = playerOne.make_move(state)
    
    newState = MancalaState(state.other, state.current, copy.deepcopy(state.mancala_board))
    state = MancalaState(newState.current, newState.other, copy.deepcopy(newState.mancala_board))
    
    if terminal_test(state):
      # print("Game Over")
      # Display(state)
      # DisplayFinal(state)
      if (state.mancala_board[0] >= 49 and child.zone == PLAYER_ONE_ZONE):
        return True
      elif (state.mancala_board[0] >= 49 and child.zone == PLAYER_TWO_ZONE):
        return False
      elif (state.mancala_board[7] >= 49 and child.zone == PLAYER_ONE_ZONE):
        return False
      elif (state.mancala_board[7] >= 49 and child.zone == PLAYER_TWO_ZONE):
        return True
    action = playerTwo.make_move(state)
    if action not in actions(state) != -1:
      # print("Illegal move made by Player Two")
      # print("Player One wins!")
      if (child.zone == PLAYER_ONE_ZONE):
        return True
      else:
        return False
    elif action not in actions(state) and action == -1 and terminal_test(state):
      # print("Game Over")
      # Display(state)
      # DisplayFinal(state)
      if (state.mancala_board[0] >= 49 and child.zone == PLAYER_ONE_ZONE):
        return True
      elif (state.mancala_board[0] >= 49 and child.zone == PLAYER_TWO_ZONE):
        return False
      elif (state.mancala_board[7] >= 49 and child.zone == PLAYER_ONE_ZONE):
        return False
      elif (state.mancala_board[7] >= 49 and child.zone == PLAYER_TWO_ZONE):
        return True
    moving = TAKE_ANOTHER_MOVE
    while (moving != END_MOVE):
      moving = result(state, action)
      if (moving == ERROR_MOVE):
        # print("Illegal move made by Player One")
        # print("Player Two wins!")
        if (child.zone == PLAYER_ONE_ZONE):
          return True
        else:
          return False
      elif (moving == TAKE_ANOTHER_MOVE):
        action = playerTwo.make_move(state)
    
    newState = MancalaState(state.other, state.current, copy.deepcopy(state.mancala_board))
    state = MancalaState(newState.current, newState.other, copy.deepcopy(newState.mancala_board))
    if terminal_test(state):
      # print("Game Over")
      # Display(state)
      # DisplayFinal(state)
      if (state.mancala_board[0] >= 49 and child.zone == PLAYER_ONE_ZONE):
        return True
      elif (state.mancala_board[0] >= 49 and child.zone == PLAYER_TWO_ZONE):
        return False
      elif (state.mancala_board[7] >= 49 and child.zone == PLAYER_ONE_ZONE):
        return False
      elif (state.mancala_board[7] >= 49 and child.zone == PLAYER_TWO_ZONE):
        return True

def PlayMancala(playerOne=None, playerTwo=None):
  if playerOne == None:
    playerOne = HumanPlayer(PLAYER_ONE_ZONE)
  elif playerOne == 'h':
    playerOne = HumanPlayer(PLAYER_ONE_ZONE)
  elif playerOne == 'r':
    playerOne = RandomPlayer(PLAYER_ONE_ZONE)
  elif playerOne == 'mm':
    playerOne = MinimaxPlayer(PLAYER_ONE_ZONE, 4)
  elif playerOne == 'ab':
    playerOne = AlphabetaPlayer(PLAYER_ONE_ZONE, 6)
  elif playerOne == 'mc':
    playerOne = MonteCarloPlayer(PLAYER_ONE_ZONE, 2)
  if playerTwo == None:
    playerTwo = RandomPlayer(PLAYER_TWO_ZONE)
  elif playerTwo == 'h':
    playerTwo = HumanPlayer(PLAYER_TWO_ZONE)
  elif playerTwo == 'r':
    playerTwo = RandomPlayer(PLAYER_TWO_ZONE)
  elif playerTwo == 'mm':
    playerTwo = MinimaxPlayer(PLAYER_TWO_ZONE, 4)
  elif playerTwo == 'ab':
    playerTwo = AlphabetaPlayer(PLAYER_TWO_ZONE, 6)
  elif playerTwo == 'mc':
    playerTwo = MonteCarloPlayer(PLAYER_TWO_ZONE, 2)

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
  playerOne = None
  playerTwo = None

  if (len(sys.argv) > 1):
    if (sys.argv[1] == "help"):
      print("To execute the mancala.py program with select agents, ")
      print("the user must specify them using the following symbol correlations:")
      print()
      print("h: human agent")
      print("r: random agent")
      print("mm: minimax agent")
      print("ab: alpha-beta agent")
      print("mc: monte carlo agent")
      print()
      print("If the user does not select the agents for players one and two,")
      print("the default will become:")
      print("Player One = human agent")
      print("Player Two = random agent")
      print()
      print("Example execution for the program with user-determined agents:")
      print()
      print("python mancala.py mm ab")
      print()
      print("This will result in the following matchup for a game of Mancala:")
      print("Player One = minimax agent")
      print("Player Two = alpha-beta agent")
      return
    
    elif (len(sys.argv) == 2):
      if (sys.argv[1] == 'h' or sys.argv[1] == 'r' or sys.argv[1] == 'mm' or sys.argv[1] == 'ab' or sys.argv[1] == 'mc'):
        playerOne = sys.argv[1]
      else:
        print("Invalid arguments. To see available arguments, execute 'python mancala.py help'")
        return
    elif (len(sys.argv) > 2):
      if ((sys.argv[1] == 'h' or sys.argv[1] == 'r' or sys.argv[1] == 'mm' or sys.argv[1] == 'ab' or sys.argv[1] == 'mc') and \
          (sys.argv[2] == 'h' or sys.argv[2] == 'r' or sys.argv[2] == 'mm' or sys.argv[2] == 'ab' or sys.argv[2] == 'mc')):
        playerOne = sys.argv[1]
        playerTwo = sys.argv[2]
      else:
        print("Invalid arguments. To see available arguments, execute 'python mancala.py help'")
        return
    else:
      print("Invalid arguments. To see available arguments, execute 'python mancala.py help'")
      return
  PlayMancala(playerOne, playerTwo)

if __name__ == '__main__':
  main()