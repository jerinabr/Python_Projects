import random

def DrawBoard(Board):
    # This function prints out the board that it was passed
    # "Board" is a list of 10 strings representing the board (ignore index 0)
    print('   |   |')
    print(' ' + Board[7] + ' | ' + Board[8] + ' | ' + Board[9])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + Board[4] + ' | ' + Board[5] + ' | ' + Board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + Board[1] + ' | ' + Board[2] + ' | ' + Board[3])
    print('   |   |')

def InputPlayerLetter():
    # Let's the player type which letter they want to be
    # Returns a list with the player's letter as the first item, and the computer's letter as the second
    Letter = ""
    while (not (Letter == "X" or Letter == "O")):
        print("Do you want to be X or O")
        Letter = raw_input().upper()

    # The first element in the tuple is the player's letter, the second is the computer's letter
    return (Letter == "X" and ["X","O"] or ["O","X"])

def WhoGoesFirst():
    # Randomly choose the player who goes first
    return (random.randint(0,1) == 0 and "Computer" or "Player")

def PlayAgain():
    # This function returns True if the player wants to play again, otherwise it returns False
    print("Do you want to play again? (yes or no)")
    return raw_input().lower().startswith("y")

def MakeMove(Board,Letter,Move):
    Board[Move] = Letter

def IsWinner(Board,Letter):
    # Given a board and a player's letter, this function returns True if that player won
    return (
        (Board[7] == Letter and Board[8] == Letter and Board[9] == Letter) or # Across the top
        (Board[4] == Letter and Board[5] == Letter and Board[6] == Letter) or # Across the middle
        (Board[1] == Letter and Board[2] == Letter and Board[3] == Letter) or # Across the bottom
        (Board[7] == Letter and Board[4] == Letter and Board[1] == Letter) or # Down the left
        (Board[8] == Letter and Board[5] == Letter and Board[2] == Letter) or # Down the middle
        (Board[9] == Letter and Board[6] == Letter and Board[3] == Letter) or # Down the right
        (Board[7] == Letter and Board[5] == Letter and Board[3] == Letter) or # Diagonal negative slope
        (Board[9] == Letter and Board[5] == Letter and Board[1] == Letter))   # Diagonal positive slope

def GetBoardCopy(Board):
    # Make a duplicate of the board list and return it the duplicate
    DuplicateBoard = []
    for index in Board:
        DuplicateBoard.append(index)
    return DuplicateBoard

def IsSpaceFree(Board,Move):
    # Return True if the passed move is free on the passed board
    return Board[Move] == " "

def GetPlayerMove(Board):
    # Let the player type in his/her move
    Move = 0
    while Move not in [1,2,3,4,5,6,7,8,9] or not IsSpaceFree(Board,Move):
        print("What is your next move? (1 - 9)")
        Move = input()
    return Move

def ChooseRandomMoveFromList(Board,MovesList):
    # Returns a valid move from the passed list on the passed board
    # Returns None if there is no valid move
    PossibleMoves = []
    for index in MovesList:
        if IsSpaceFree(Board,index):
            PossibleMoves.append(index)
    if len(PossibleMoves) != 0:
        return random.choice(PossibleMoves)
    else:
        return None

def GetComputerMove(Board,ComputerLetter):
    # Given a board and the computer's letter, determine where to move and return that move
    if ComputerLetter == "X":
        PlayerLetter = "O"
    else:
        PlayerLetter = "X"
    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for index in range(1,10):
        Copy = GetBoardCopy(Board)
        if IsSpaceFree(Copy,index):
            MakeMove(Copy,ComputerLetter,index)
            if IsWinner(Copy,ComputerLetter):
                return index
    # Check if the player could win on his next move, and block them
    for index in range(1,10):
        Copy = GetBoardCopy(Board)
        if IsSpaceFree(Copy,index):
            MakeMove(Copy,PlayerLetter,index)
            if IsWinner(Copy,PlayerLetter):
                return index
    # Try to take one of the corners, if they are free
    Move = ChooseRandomMoveFromList(Board,[1,3,7,9])
    if Move != None:
        return Move
    # Try to take the center, if it is free
    if IsSpaceFree(Board,5):
        return 5
    # Move on one of the sides
    return ChooseRandomMoveFromList(Board,[2,4,6,8])

def IsBoardFull(Board):
    # Return True if every space on the board has been taken. Otherwise return False
    for index in range(1,10):
        if IsSpaceFree(Board,index):
            return False
    return True

print("Welcome to Tic Tac Toe!")

while True:
    # Reset the board
    Board = [" "] * 10
    PlayerLetter,ComputerLetter = InputPlayerLetter()
    Turn = WhoGoesFirst()
    print("The " + Turn + " will go first.")
    GameIsPlaying = True
    while GameIsPlaying:
        if Turn == "Player":
            # Player's turn
            DrawBoard(Board)
            Move = GetPlayerMove(Board)
            MakeMove(Board,PlayerLetter,Move)
            if IsWinner(Board,PlayerLetter):
                DrawBoard(Board)
                print("Hooray! You have won the game!")
                GameIsPlaying = False
            else:
                if IsBoardFull(Board):
                    DrawBoard(Board)
                    print("The game is a tie!")
                    break
                else:
                    Turn = "Computer"
        else:
            # Computer's turn
            Move = GetComputerMove(Board,ComputerLetter)
            MakeMove(Board,ComputerLetter,Move)
            if IsWinner(Board,ComputerLetter):
                DrawBoard(Board)
                print("The Computer has beaten you! You lose!")
                GameIsPlaying = False
            else:
                if IsBoardFull(Board):
                    DrawBoard(Board)
                    print("The game is a tie!")
                    break
                else:
                    Turn = "Player"
    if (not PlayAgain()):
        break
