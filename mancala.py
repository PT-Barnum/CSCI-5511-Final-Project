# TOTAL_SPACES = PLAYABLE_SPACES + 2 player zones
TOTAL_SPACES = 14
PLAYABLE_SPACES = 12
PLAYER_ONE_ZONE = 0   # Index of Player One's Zone
PLAYER_TWO_ZONE = 7   # Index of Player Two's Zone


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