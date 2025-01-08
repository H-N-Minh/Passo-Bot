import grpc
import time
import sys

sys.path.append('./netcode')

from netcode.pso_pb2 import *
from netcode.netcode_pb2 import *
from netcode.netcode_pb2_grpc import GameComStub

from bot93 import *


# AI mode
MINIMAX_ACTIVATED = True

# settings
userToken = 'cbed7183f4dc01d4b19e5d55acb3ab5e35d10883d376c756142c56046249cde8'  # TODO: Insert your user token here
gameserverAddress = 'gameserver.ist.tugraz.at:80'

# Vars
matchToken = ""

# Setup comms
channel = grpc.insecure_channel(gameserverAddress)
stub = GameComStub(channel)


# Query your userToken to be able to start a new match
def getUserToken(matr_number, secret):
    auth = AuthPacket()
    auth.matr_number = matr_number
    auth.secret = secret
    response = stub.GetUserToken(auth)
    return response.user_token


# Request a new match for pso
def newMatch(length):
    params = GameParameter()
    request = MatchRequest(user_token=userToken,
                           game_token='pso',
                           timeout_suggestion_seconds=5,
                           pso_game_parameters=params)
    response = stub.NewMatch(request)

    print("New Match:", response.match_token)
    print("First player?", response.beginning_player)
    global PLAYER
    PLAYER = RED_PLAYER if response.beginning_player else BLACK_PLAYER

    global matchToken
    matchToken = response.match_token


# Helper to create the MatchIDPacket
def createMatchId():
    return MatchIDPacket(user_token=userToken,
                         match_token=matchToken)


# Let's get started
def queryGameState():
    response = stub.GetGameState(createMatchId())
    return response.pso_game_state, response.game_status


# Sleepy time
def waitMatchStarted():
    while queryGameState()[1] == GameStatus.MATCH_NOT_STARTED:
        time.sleep(1)


# Identify yourself!
def queryOpponentInfo():
    response = stub.GetOpponentInfo(createMatchId())
    print("Opponent:", response.user_pseudonym, "(" + str(response.elo.user_elo) + "),",
          "from group:", response.group_pseudonym, "(" + str(response.elo.group_elo) + ")")
    pass


# What did we agree on? 2 Timeout, keine mehr?
def queryTimeout():
    response = stub.GetTimeout(createMatchId())
    print("Negotiated timeout:", response.timeout_seconds, "sec")
    pass


def findChangedSquares(board_a, board_b):
    changes = []
    for r in range(len(board_a)):
        for c in range(len(board_a[0])):
            if board_a[r][c] != board_b[r][c]:
                changes.append(((r, c), board_a[r][c], board_b[r][c]))
    return changes


# Submit a turn and evaluate the turn status info. Also returns the Tak board state.
def submitTurn(turn):
    request = TurnRequest(match_id=createMatchId(),
                          pso_game_turn=turn)
    response = stub.SubmitTurn(request)
    if response.turn_status == TurnStatus.INVALID_TURN:
        print("Error: Invalid turn submitted.")
        exit(1)
    if response.turn_status == TurnStatus.MATCH_OVER:
        printGameOutcome(response.turn_status) # added here!
        
        print("\n---------Match info---------")
        queryOpponentInfo()
        queryTimeout()
        exit(0)
    if response.turn_status == TurnStatus.NOT_YOUR_TURN:
        print("This isn't the time to use that!")
    return response.pso_game_state


# Helper
def isMatchOver(game_status):
    return game_status in [GameStatus.MATCH_WON,
                           GameStatus.MATCH_LOST,
                           GameStatus.DRAW,
                           GameStatus.MATCH_ABORTED]


# Helper
def isTurnPlayable(game_status):
    return game_status == YOUR_TURN



#############################################################
# Our code starts here


def printBoard():
    """
    Print the current board layout and game status (whose turn it is, or who won)
    Returns:
        state (str): The current game state.
        status (str): The current game status.
    """
    state, status = queryGameState()
    
    str_state = str(state)
    values = [int(line.split(": ")[1]) for line in str_state.splitlines()]
    board = [[None for _ in range(5)] for _ in range(5)]
    
    print("\nCurrent Board State:")
    counter = 0
    # print("col1 col2 x3 x4 x5")

    for i in range(5):
        print("row " + str(i), end="|  ")
        for j in range(5):
            board[i][j] = values[counter]
            symbol =  str(board[i][j])
            print(symbol, end="  ")
            counter += 1
        print()  # '\n'

    print()
    printGameOutcome(status)
    
    return state, status



def printGameOutcome(status):
    """print whose turn it is, or how did the game end"""
    status_mapping = {
        0: "YOUR_TURN" , # YOUR_TURN = 0;
        1: "OPPONENTS_TURN" , # OPPONENTS_TURN = 1;
        3: "Victoria Belli - MATCH_WON" , # MATCH_WON = 3;
        4: "Clades Belli - MATCH_LOST" , # MATCH_LOST = 4;
        5: "Bellum Inconclusium - DRAW" , # DRAW = 5;
        6: "Bellum Non Inceptum - MATCH_NOT_STARTED" , # MATCH_NOT_STARTED = 6;
        7: "Bellum Interruptum - MATCH_ABORTED" # MATCH_ABORTED = 7;
    }
    status_message = status_mapping.get(status, "UNKNOWN_STATUS")
    if status > 1:
        print(f"GAME OVER! Outcome: {status_message}")
        # printBoard()
    else:
        player = "RED" if PLAYER == RED_PLAYER else "BLACK"
        print(f"Game is still ongoing. You are {player}. Currently it is {status_message}")



def getBoard(state):
    """convert the grpc board into 2d array (row, col) in range 0-4"""
    board_state = list(state.board)
    return [
        board_state[0:5],
        board_state[5:10],
        board_state[10:15],
        board_state[15:20],
        board_state[20:25],
    ]


def autoPlay():
    """Automatically play the game. Make the move, then print the board.
    Moved is calculated using Minimax if activated, else just random legal move."""
    state, status = printBoard()
    old_board = getBoard(state)
    
    minimax_bot = Minimax(PLAYER)

    while not isMatchOver(status):
        # If its our turn then submit a move
        if isTurnPlayable(status):
            # print("--------------- NEW TURN. START FINDING MOVES:  ---------------")
            board = getBoard(state)

            if MINIMAX_ACTIVATED:
                best_score, best_move = minimax_bot.evaluate(board)
                print("Minimax has returned the following: Best score:", best_score, ", best move: ", best_move)
                # In order to not trigger this assert, I have made in this case just a legal move, to not terminate the whole game: # assert best_move is not None, "Minimax did not return a valid move"
                if best_move is None:
                    legal_moves, _ = findAllLegalMoves(board, PLAYER)
                    print("These are legal moves: ", legal_moves)

                    for (row_old, col_old), moves in legal_moves.items():
                        if moves:
                            row_new, col_new = moves[0]
                            print(f"Moving from (row, col): ({row_old}, {col_old}) to ({row_new}, {col_new})")
                            submitTurn(GameTurn(x1=col_old + 1, y1=row_old + 1, x2=col_new + 1, y2=row_new + 1))
                            break
                else:
                    (old_pos, new_pos) = best_move
                    assert old_pos is not None and new_pos is not None, "Old position or new position is None"
                    (row_old, col_old) = old_pos
                    (row_new, col_new) = new_pos
                    assert row_old is not None and col_old is not None, "Old row or old col is None"
                    assert row_new is not None and col_new is not None, "New row or new col is None"

                    print(f"Moving from (row, col): ({row_old}, {col_old}) to ({row_new}, {col_new})")
                    submitTurn(GameTurn(x1=col_old + 1, y1=row_old + 1, x2=col_new + 1, y2=row_new + 1))

            else:   # Play Random legal move

                legal_moves, _ = findAllLegalMoves(board, PLAYER)
                print("These are legal moves: ", legal_moves)

                for (row_old, col_old), moves in legal_moves.items():
                    if moves:
                        row_new, col_new = moves[0]
                        print(f"Moving from (row, col): ({row_old}, {col_old}) to ({row_new}, {col_new})")
                        submitTurn(GameTurn(x1=col_old + 1, y1=row_old + 1, x2=col_new + 1, y2=row_new + 1))
                        break

        new_state, new_status = printBoard()
        new_board = getBoard(new_state)

        changed_squares = findChangedSquares(old_board, new_board)
        if changed_squares:
            print("Squares changed:", changed_squares)
        
        old_board = new_board
        state = new_state
        status = new_status

        time.sleep(1)
    
    
def main():
    # stub.SetGroupPseudonym("")
    print("UserToken:", userToken)
    newMatch(5)
    waitMatchStarted()
    print("Opponent found.")

    print("---------Match info---------")
    queryOpponentInfo()
    queryTimeout()

    autoPlay()

    print("\n---------Match info---------")
    queryOpponentInfo()
    queryTimeout()


if __name__ == "__main__":
    main()
