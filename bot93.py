# Description: This includes all game logic of the bot.
import copy



# Constants
RED_PLAYER = 2
BLACK_PLAYER = 3
BOARD_SIZE = 5
PLAYER = None   # This will be set to RED_PLAYER or BLACK_PLAYER in main.py

TILE = 1
EMPTY_SQUARE = 0

DIRECTIONS = [
    (-1, 0),  # Up
    (1, 0),   # Down
    (0, -1),  # Left
    (0, 1),   # Right
    (-1, -1), # Up-Left
    (-1, 1),  # Up-Right
    (1, -1),  # Down-Left
    (1, 1)    # Down-Right
]


# give each possible stack of token(s) an ID
# // Indiviual fields are encoded in the following way:
# //                 R B R  B  R  B  R  B
# //         R B R B R R B  B  R  R  B  B
# //     R B R R B B R R R  R  B  B  B  B
# //   - - - - - - - - - -  -  -  -  -  -
# // 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
# // R(ed) is the first player, B(lack) is the second player and "-" denotes a tile of the game board.

id_to_stack_dict = {
    0: [], 
    1: ['tile'], 
    2: ['tile', 'R'], 
    3: ['tile', 'B'], 
    4: ['tile', 'R', 'R'],
    5: ['tile', 'R', 'B'],
    6: ['tile', 'B', 'R'],
    7: ['tile', 'B', 'B'],
    8: ['tile', 'R', 'R', 'R'],
    9: ['tile', 'R', 'R', 'B'],
    10: ['tile', 'R', 'B', 'R'],
    11: ['tile', 'R', 'B', 'B'],
    12: ['tile', 'B', 'R', 'R'],
    13: ['tile', 'B', 'R', 'B'],
    14: ['tile', 'B', 'B', 'R'],
    15: ['tile', 'B', 'B', 'B']
}

stack_to_id_dict = {tuple(v): k for k, v in id_to_stack_dict.items()}

def IdToStack(ID):
    assert 0 <= ID <= 15, f"ID {ID} is out of range"
    stack = id_to_stack_dict.get(ID, [])
    return stack

def stackToID(stack):
    id = stack_to_id_dict.get(tuple(stack), None)
    assert id is not None, f"Stack {stack} is not valid"
    return id



def findWinningMove(board, player):
    '''
    Helper func for findAllLegalMoves(). Finds the winning move if there is one, else returns None
    This simply checks which row is the opponent's last piece, and if we also have a piece on that row
    then we have a winning move. This includes going off the board, or going onto a tile that was removed
    Returns:
        tuple: of tuple:
          ((old_row, old_col), (new_row, new_col)) if winning move is found, else None
    '''

    if player == RED_PLAYER:
        # find the lowest piece of opponent
        lowest_black = None
        for row in range(BOARD_SIZE - 1, -1, -1):
            for col in range(BOARD_SIZE):
                stack = board[row][col]
                if stack > 1 and (stack % 2 == 1): # or stack in [6, 10, 12, 14]):
                    lowest_black = row
                    break
            if lowest_black is not None:
                break
        
        # find the winning move if there is one
        if lowest_black is not None: 
            # if there is an active red piece on the same row with the lowest black piece, then we have a winning move
            for col in range(BOARD_SIZE):
                stack = board[lowest_black][col]
                if stack > 1 and stack % 2 == 0:
                    winning_move = ((lowest_black, col), (lowest_black + 1, col))
                    return winning_move
        return None
    
    # Exact same code as above but for black player
    else:
        # find the lowest piece of opponent
        lowest_red = None
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                stack = board[row][col]
                if stack > 1 and (stack % 2 == 0): # or stack in [5, 9, 11, 13]):
                    lowest_red = row
                    break
            if lowest_red is not None:
                break
        
        # find the winning move if there is one
        if lowest_red is not None: 
            # if there is an active black piece on the same row with the lowest red piece, then we have a winning move
            for col in range(BOARD_SIZE):
                stack = board[lowest_red][col]
                if stack > 1 and stack % 2 == 1:
                    winning_move = ((lowest_red, col), (lowest_red - 1, col))
                    return winning_move
        return None

def findAllLegalMoves(board, PLAYER):
    '''
    Goes through every player's pieces on the given board position and finds all legal moves
    First checks if the player has a winning move, if so, returns that move
    Else, check for all normal legal moves: within the board range, and the new square has less than 3 pieces
    Args:
        board (list of lists): The layout of the game board.
        PLAYER (int): The player ID (2 for Red, 3 for Black).

    Returns:
        Dictionary (key: tuple, value: list of tuples):
            A dictionary of all legal moves for the current player.
            The dictionary is in the format {(old_row, old_col): [(new_row_1, new_col_1), (new_row_2, new_col_2), ...], ...}
        
        Boolean: True if a winning move is found, else false'''

    
    all_legal_moves = {}
    fortress_moves = {}
    for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] <= 1:
                    continue
                if (board[row][col] % 2 == PLAYER % 2):
                    
                    legal_moves = []
                    for direction_row, direction_col in DIRECTIONS:
                        new_col, new_row = col + direction_col, row + direction_row
                        if 0 <= new_col < 5 and 0 <= new_row < 5 and board[new_row][new_col] in range(1, 8):
                            legal_moves.append((new_row, new_col))
                    all_legal_moves[(row, col)] = legal_moves
        # return all_legal_moves, False

    # for old_pos, moves in all_legal_moves.items():
    #     if (PLAYER == RED_PLAYER and old_pos == (0, 1)) or (PLAYER == BLACK_PLAYER and old_pos == (4, 1)):
    #         fortress_moves[old_pos] = moves
    #     else:
    #         all_legal_moves[old_pos] = moves
    
    # # Only include fortress moves if there are no other moves available
    # if not all_legal_moves:
    #     all_legal_moves = fortress_moves

    # Check for winning move, AND VALIDATE IF THE WINNING MOVE IS LEGAL!
    winning_move = findWinningMove(board, PLAYER)
    if winning_move is not None:
        # print("Winning move found: ", winning_move)
        (old_row, old_col), (new_row, new_col) = winning_move
        return {(old_row, old_col): [(new_row, new_col)]}, True
    return all_legal_moves, False

def isRowEmpty(board, row):
    """
    THIS CAN BE FURTHER IMPROVED, bcs we can also consider a row with only TILES (1) as effectively empty 
    for the sake of 'jumping' concerns
    """
    if row < 0 or row >= BOARD_SIZE:
        return False
    for col in range(BOARD_SIZE):
        if board[row][col] > 1:
            return False
    return True
#####################################################
# Minimax Algorithm with Alpha-Beta Pruning
# Note: red player is always the maximizer, black is always the minimizer 
#   (positive points is good for red, negative points is good for black)

######### TWEAKS ##########:
MAX_DEPTH = 5       # max depth for analysis

# Points to help evaluate the total score of a board. Important for calculateScore().
PTS_TOKEN = 5               # Points for each token (+3 for each token we have, -3 for each token opponent has)
PTS_WINNING = 5000          # Points for winning position
PTS_TOP_STACK_2 = 2         # Points for being on top of a stack of 2 tokens
PTS_TOP_STACK_3 = 5        # Points for being on top of a stack of 3 tokens
# BONUS_FORM_WALL = 10
# PENALTY_SAME_PIECE_TWICE = 5
BONUS_JUMP_ON_ENEMY = 30
PROGRESS_FACTOR_RED = 20   
PROGRESS_FACTOR_BLACK = 20
# EMPTY_ROW_PENALTY = 200
KEEP_FORTRESS_BUILT = 4000

_last_move_global = None

class Minimax:

    def __init__(self, player):
        """
        Parameters:
            player (int): The user player (us). 2 for Red, 3 for Black.
        """
        self.maximizer = True if player == RED_PLAYER else False
        self.last_move = None
        self.corner_fortress_built = False
        global PLAYER
        PLAYER = player

    def breaks_fortress(self, board, old_pos, new_pos):
        if PLAYER == RED_PLAYER:
            return old_pos == (0, 1) and board[0][1] == 8
        else:
            return old_pos == (4, 1) and board[4][1] == 15
        
    def evaluate(self, board, alpha=float('-inf'), beta=float('inf'), maximizer=None, depth=MAX_DEPTH):
        """
        start Minimax algorithm with Alpha-Beta pruning.

        Parameters:
            board (2d list): The layout of the game board.
            alpha (float): The best score the maximizer is assured of. Default is negative infinity.
            beta (float): The best score the minimizer is assured of. Default is positive infinity.
            maximizer (bool): True if the current player is maximizing, False otherwise. Default is the user player.
            depth (int): The depth to which the algorithm will search. Default is MAX_DEPTH.

        Returns:
            tuple: (best_score, best_move) where best_score is the score of the best move,
                   and best_move is a tuple of tuple ( (old_row, old_col) , (new_row, new_col) ).
        """
        assert board is not None, "Board is None"
        if maximizer is None:
            maximizer = self.maximizer
        

        # 1. leaf level/bottom level: return the score of this position using calculateScore()
        if depth == 0:
            return self.calculateScore(board), None

        ####### BUILDING FULL STACK IN THE CORNER #######
        if not self.corner_fortress_built:
            best_move = self.buildFortress(board, maximizer)
            new_board = self.simulateMove(board, *best_move)
            if self.corner_fortress_built:
                print("nice fortress is built!!!")
            return self.calculateScore(new_board), best_move

        # 2. If reach here then we not yet at the bottom level, so find all nodes of the next level
        legal_moves, found_winning_move = findAllLegalMoves(board, RED_PLAYER if maximizer else BLACK_PLAYER)
        # If no legal moves, return evaluation
        if not legal_moves:
            return self.calculateScore(board), None
        # else if we found the winning move, return with the winning move
        elif found_winning_move:
            pts = PTS_WINNING if maximizer else -PTS_WINNING
            old_pos, new_pos_list = next(iter(legal_moves.items()))
            new_pos = new_pos_list[0]
            winning_move = (old_pos, new_pos)
            return pts, winning_move

        # 3. Finding the best move for current node
        best_move = None        # tuple of tuple ( (old_row, old_col) , (new_row, new_col) )

        if maximizer:   # current node is maximizing player's turn
            # go through each child node
            for old_pos, new_pos_list in legal_moves.items():
                for new_pos in new_pos_list:
                    # simulate the move and get the score of that move
                    # if self.breaks_fortress(board, old_pos, new_pos): # CHECK WHETHER THIS MOVE BREAKS THE FORTRESS
                    #     continue

                    new_board = self.simulateMove(board, old_pos, new_pos)
                    alpha_temp, _ = self.evaluate(new_board, alpha, beta, not maximizer, depth - 1)     # 'not maximizer' switch state between maximizing and minimizing (works both ways)
                    
                    # if we found a better move, update the best move
                    if alpha_temp > alpha:
                        alpha = alpha_temp
                        best_move = (old_pos, new_pos)
                        
                    # alpha-beta pruning
                    if beta <= alpha:
                        return beta, best_move
            # After going through all child node and we didnt prune anything, return the best score with best move
            return alpha, best_move

        # Same code as above, but for Minimizing player
        else:
            for old_pos, new_pos_list in legal_moves.items():
                for new_pos in new_pos_list:

                    # if self.breaks_fortress(board, old_pos, new_pos): # CHECK WHETHER THIS MOVE BREAKS THE FORTRESS
                    #     continue

                    new_board = self.simulateMove(board, old_pos, new_pos)
                    beta_temp, _ = self.evaluate(new_board, alpha, beta, not maximizer, depth - 1)
                    if beta_temp < beta:
                        beta = beta_temp
                        best_move = (old_pos, new_pos)
                    if beta <= alpha:
                        return alpha, best_move
            return beta, best_move

    def buildFortress(self, board, maximizer):
        if maximizer: # moves for red
            # We want to move like this: 2 2 2 2 2 --> 2 4 0 2 2 --> 0 8 0 2 2
            if board[0][0] == RED_PLAYER and board[0][1] == RED_PLAYER and board[0][2] == RED_PLAYER: # move from board[0][2] to board[0][1]
                return ((0, 2), (0, 1))
            if board[0][0] == RED_PLAYER and board[0][1] == 4 and board[0][2] == 0: # move from board[0][0] to board[0][1]
                self.corner_fortress_built = True
                return ((0, 0), (0, 1))
            else: 
                assert False
        else: 
            # We want to move like this: 3 3 3 3 3 --> 3 7 0 3 3 --> 0 15 0 3 3
            if board[4][0] == BLACK_PLAYER and board[4][1] == BLACK_PLAYER and board[4][2] == BLACK_PLAYER: # move from board[4][2] to board[4][1]
                return ((4, 2), (4, 1))
            if board[4][0] == BLACK_PLAYER and board[4][1] == 7 and board[4][2] == 0: # move from board[4][0] to board[4][1]
                self.corner_fortress_built = True
                return ((4, 0), (4, 1))
            else: 
                assert False
    
    def simulateMove(self, board, old_pos, new_pos):
        """
        Helper_1 for evaluate(). Simulates making a given move on the given board.

        Parameters:
            board (2d list): The current board.
            old_pos (tuple): Coordinates of the old position. (old_row, old_col)
            new_pos (tuple): Coordinates of the new position. (new_row, new_col)

        Returns:
            2d list: The new board after making the move.
        """
        global _last_move_global
        (old_row, old_col) = old_pos
        (new_row, new_col) = new_pos
        old_id = board[old_row][old_col]        # ID/value on the old position
        new_id = board[new_row][new_col]        # ID/value on the new position

        # Error handling: The move should already be valid, but we do small check to be sure
        # only check that we dont move from empty field or to a field with already 3 tokens
        if old_id <= 1 or new_id >= 8:
            raise ValueError(f"Invalid move from ({old_row}, {old_col}) to ({new_row}, {new_col})")

        # Make the move and update the board
        new_board = copy.deepcopy(board)
        old_stack = IdToStack(old_id).copy()
        new_stack = IdToStack(new_id).copy()
        
        moving_token = old_stack.pop()
        assert moving_token != 'tile', "invalid moving_token, can not move a tile"
        new_stack.append(moving_token)
        new_board[old_row][old_col] = stackToID(old_stack)
        new_board[new_row][new_col] = stackToID(new_stack)

        # Remove old tile if theres now no token left on that tile (according to rule of Passo). 
        # Also remove any Island (stack with no tile around it)
        if new_board[old_row][old_col] == TILE:
            new_board[old_row][old_col] = EMPTY_SQUARE
            self.removeIsland(new_board, (old_row, old_col))

        _last_move_global = (old_row, old_col)
        self.last_move = (old_row, old_col)

        return new_board

    def removeIsland(self, board, deleted_pos):
        """
        Helper for simulateMove(). After a tile is deleted, there could be some stacks that becomes
        an island (no tile around it). This function removes all islands.
        Parameters:
            board (2d list): The game board.
            deleted_pos (tuple): (row, col) of the newly deleted tile.
        """
        (deleted_row, deleted_col) = deleted_pos

        # check all neighbors of the deleted tile
        for direction_row, direction_col in DIRECTIONS:
            neighbor_row, neighbor_col = deleted_row + direction_row, deleted_col + direction_col

            #if the neighbor is an active token/stack
            if 0 <= neighbor_row < BOARD_SIZE and 0 <= neighbor_col < BOARD_SIZE and board[neighbor_row][neighbor_col] > 1:
                # check if this neighbor is now an island. If so, remove it
                is_island = True
                for direction_row2, direction_col2 in DIRECTIONS:
                    neighbor_row2, neighbor_col2 = neighbor_row + direction_row2, neighbor_col + direction_col2
                    if 0 <= neighbor_row2 < BOARD_SIZE and 0 <= neighbor_col2 < BOARD_SIZE and board[neighbor_row2][neighbor_col2] > 1:
                        is_island = False
                        break
                if is_island:
                    board[neighbor_row][neighbor_col] = EMPTY_SQUARE
    def calculateScore(self, board):
        """
        Helper_2 for evaluate(). Evaluates the score of the given board. Positive is good for red, negative is good for black.
        The score is based on:
        - The number of tokens of each player on the board
        - Token on top of a stack gives points to owner of that token
        Note: this func does not calculate pts for winning position, it is already done in evaluate()

        Parameters:
            board (2d list): The game board.

        Returns:ans it has a Red top token)
            int: The evaluation score (Positive is good for red, negative is good for black).
        """
        global _last_move_global
        score = 0

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                id = board[row][col]
                if id <= 1:         # skip empty square or tile
                    continue
                stack = IdToStack(id)

                # add pts for each token in the stack
                for token in stack[1:]:          
                    if token == 'R':
                        score += PTS_TOKEN
                    else:
                        score -= PTS_TOKEN

                # add bonus for being on top of a stack (5 pts for each stack of 2 tokens, 10 pts for 3 tokens)
                if 4 <= id <= 7:                    # Stack height of 2
                    if id % 2 == 0:                 # red token on top
                        score += PTS_TOP_STACK_2
                    else:
                        score -= PTS_TOP_STACK_2
                elif 8 <= id <= 11:                 # Stack height of 3
                    if id % 2 == 0:                 # red token on top
                        score += PTS_TOP_STACK_3
                    else:
                        score -= PTS_TOP_STACK_3

                # award fortress if built, for red player it is built on board[0][1] and there is 8 to be checked
                if PLAYER == RED_PLAYER and row == 0 and col == 1 and id == 8:
                    score += KEEP_FORTRESS_BUILT
                if PLAYER == BLACK_PLAYER and row == 4 and col == 1 and id == 15:
                    score -= KEEP_FORTRESS_BUILT
                
        # #################### ENCOURAGE MOVING FORWARD ###############################
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell_id = board[row][col]
                if cell_id <= 1:
                    continue
                if cell_id % 2 == 0:
                    score += (row * PROGRESS_FACTOR_RED)
                else:
                    score -= ((BOARD_SIZE - 1 - row) * PROGRESS_FACTOR_BLACK)


        ############### JUMPING ONTO ENEMY ########################
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                top_id = board[row][col]
                if top_id <= 1:
                    continue
                for (dr, dc) in DIRECTIONS:
                    nr = row + dr
                    nc = col + dc
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                        neighbor_id = board[nr][nc]
                        # Only meaningful if neighbor has a top token and not already full
                        if neighbor_id > 1 and neighbor_id < 8:
                            # If current top is Red
                            if top_id % 2 == 0:
                                # If neighbor top is Black, we can jump onto them
                                if neighbor_id % 2 == 1:
                                    score += BONUS_JUMP_ON_ENEMY
                            else:
                                # If current top is Black
                                # If neighbor top is Red, that's good for Black => negative for Red
                                if neighbor_id % 2 == 0:
                                    score -= BONUS_JUMP_ON_ENEMY

        return score


