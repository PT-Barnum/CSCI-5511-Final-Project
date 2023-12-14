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




def DisplayBoard():
  pass

def PlayMancala(playerOne=None, playerTwo=None):
  pass

def main():
  # TODO: instantiate the board
  PlayMancala()
  pass


if __name__ == '__main__':
  main()