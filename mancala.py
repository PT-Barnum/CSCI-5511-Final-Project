# TOTAL_SPACES = PLAYABLE_SPACES + 2 player zones
TOTAL_SPACES = 14
PLAYABLE_SPACES = 12
PLAYER_ONE_ZONE = 0   # Index of Player One's Zone
PLAYER_TWO_ZONE = 7   # Index of Player Two's Zone
LAST_ZONE = 13

VALID_MOVE = 0
INVALID_MOVE = 1

class MancalaPlayerTemplate:
    '''Template class for an Othello Player

    An othello player *must* implement the following methods:

    get_color(self) - correctly returns the agent's color

    make_move(self, state) - given the state, returns an action that is the agent's move
    '''
    def __init__(self, myzone):
        self.zone = myzone

    def get_zone(self):
        return self.zone

    def make_move(self, state):
        '''Given the state, returns a legal action for the agent to take in the state
        '''
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
            display(state)
            if self.zone == PLAYER_ONE_ZONE:
                print("White ", end='')
            else:
                print("Black ", end='')
            print(" to play.")
            print("Legal moves are " + str(legals))
            move = input("Enter your move as a r,c pair:")
            if move == "":
                return legals[0]

            # if move == SKIP and SKIP in legals:
            #     return move

            # try:
            #     movetup = int(move.split(',')[0]), int(move.split(',')[1])
            # except:
            #     movetup = None
            # if movetup in legals:
            #     curr_move = movetup
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
        display(state)
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
        display(state)
        return returnTuple[1]

class RandomPlayer(MancalaPlayerTemplate):
    def __init__(self, myzone):
        self.zone = myzone

    def get_zone(self):
        return self.zone

    def make_move(self, state):
        '''Given the state, returns a legal action for the agent to take in the state
        '''
        legal = actions(state)
        decision = random.choice(legal)
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
      self.current_player = current_player
      self.other_player = other_player


# def DistributeMarbles(index, player_zone):
#   initialMarbles = mancala_board[index]
#   mancala_board[index] = 0
#   newIndex = index
#   while (initialMarbles):
#     if (TerminalTest(initialMarbles, newIndex, player_zone)):
#       return newIndex
#     elif (newIndex == PLAYER_ONE_ZONE):
#       if (player_zone == PLAYER_ONE_ZONE):
#         # place marble in this zone
#         initialMarbles -= 1
#         newIndex += 1
#       else:
#         newIndex += 1
#     elif (newIndex == PLAYER_TWO_ZONE):
#       if (player_zone == PLAYER_TWO_ZONE):
#         # place marble in this zone
#         initialMarbles -= 1
#         newIndex += 1
#       else:
#         newIndex += 1
#     else:
#       # place marble in this zone
#       initialMarbles -= 1
#       if (newIndex == LAST_ZONE):
#         newIndex = 0
#       else:
#         newIndex += 1
#   return -1


# def MakeMove(index, player_zone):
#   if ((mancala_board[index] == 0) or (index == PLAYER_ONE_ZONE) or (PLAYER_TWO_ZONE)):
#     return INVALID_MOVE
   
#   moving = 1
#   newIndex = index
#   while (moving):
#     if (mancala_board[newIndex] == 0):
#       moving = 0
#     else:
#       newIndex = DistributeMarbles(newIndex, player_zone)
#       if (newIndex == -1):
#         return INVALID_MOVE
#   return VALID_MOVE

def player(state):
    return state.current

def actions(state):
    pass
    # '''Return a list of possible actions given the current state
    # '''
    # legal_actions = []
    # for i in range(SIZE):
    #     for j in range(SIZE):
    #         if result(state, (i,j)) != None:
    #             legal_actions.append((i,j))
    # if len(legal_actions) == 0:
    #     legal_actions.append(SKIP)
    # return legal_actions

def result(state, action):
    pass
    # '''Returns the resulting state after taking the given action

    # (This is the workhorse function for checking legal moves as well as making moves)

    # If the given action is not legal, returns None

    # '''
    # # first, special case! an action of SKIP is allowed if the current agent has no legal moves
    # # in this case, we just skip to the other player's turn but keep the same board
    # if action == SKIP:
    #     newstate = RandOthelloState(state.other, state.current, copy.deepcopy(state.board_array), state.num_skips + 1)
    #     return newstate

    # if state.board_array[action[0]][action[1]] != EMPTY:
    #     return None

    # color = state.current.get_color()
    # # create new state with players swapped and a copy of the current board
    # newstate = RandOthelloState(state.other, state.current, copy.deepcopy(state.board_array))

    # newstate.board_array[action[0]][action[1]] = color
    
    # flipped = False
    # directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    # for d in directions:
    #     i = 1
    #     count = 0
    #     while i <= SIZE:
    #         x = action[0] + i * d[0]
    #         y = action[1] + i * d[1]
    #         if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
    #             count = 0
    #             break
    #         elif newstate.board_array[x][y] == -1 * color:
    #             count += 1
    #         elif newstate.board_array[x][y] == color:
    #             break
    #         else:
    #             count = 0
    #             break
    #         i += 1

    #     if count > 0:
    #         flipped = True

    #     for i in range(count):
    #         x = action[0] + (i+1) * d[0]
    #         y = action[1] + (i+1) * d[1]
    #         newstate.board_array[x][y] = color

    # if flipped:
    #     return newstate
    # else:  
    #     # if no pieces are flipped, it's not a legal move
    #     return None

def terminal_test(state):
    for Index in range(TOTAL_SPACES):
        if ((Index != PLAYER_ONE_ZONE) and (Index != PLAYER_TWO_ZONE)):
            if (state.mancala_board[Index] != 0):
                return False
    return True


def display(state):
    pass
    # '''Displays the current state in the terminal window
    # '''
    # print('  ', end='')
    # for i in range(SIZE):
    #     print(i,end='')
    # print()
    # for i in range(SIZE):
    #     print(i, '', end='')
    #     for j in range(SIZE):
    #         if state.board_array[j][i] == WHITE:
    #             print('W', end='')
    #         elif state.board_array[j][i] == BLACK:
    #             print('B', end='')
    #         elif state.board_array[j][i] == BLOCKED:
    #             print('X', end='')
    #         else:
    #             print('-', end='')
    #     print()

def PlayMancala(playerOne=None, playerTwo=None):
  pass

def main():
  # TODO: instantiate the board
  PlayMancala()
  pass


if __name__ == '__main__':
  main()