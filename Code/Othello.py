## Written By Suicheng Su

from random import randint
import os
LEFT_BOUNDARY = - 200; RIGHT_BOUNDARY = 200
TOP_BOUNDARY = 200; BOTTOM_BOUNDARY = -200
SQUARE = 50

## SIGNATURE
# This function creates a new game state upon starting new game. 
# Four initial tiles are created at the center of the baord.
## Test
# new_game_state(8) => create a 8x8 matrix with center four tiles being 0 and 1 alternatively.

def new_game_state(n):
    # Create nxn matrix for data storage
    global storage, PLAYER1, PLAYER2, PLAYERS, WHOSE_TURN, player_name
    storage = [[None for i in range(n)] for i in range(n)]  # initial state with 
    PLAYER1 = '0'; PLAYER2 = '1' # PLAYER1 is the actual player, PLAYER2 is the computer
    PLAYERS = [PLAYER1, PLAYER2] 
    player_name = '' # pre-allocate storage for user name
    WHOSE_TURN = 0  # The player plays the first turn
    # Initial State when game begins: Place two tiles for each player at center of the board
    storage[int(n/2) - 1][int(n/2) - 1] = storage[int(n/2)][int(n/2)] = PLAYER2
    storage[int(n/2) - 1][int(n/2)] = storage[int(n/2)][int(n/2) - 1] = PLAYER1
    return storage


## SIGNATURE
# Given game state storage, matrix index, and assigned val, this function assign the corresponding
# value to the corresponding matrix index.
## Test
# insert_move(storage, 0,0, '1') => assign '1' to storage[0][0]

def insert_move(storage, m, n, val):
    try:
        storage[m][n] = val
    except IndexError:
        pass


## SIGNATURE
# Given a matrix index (mth row and nth column), and player's turn, return the validity of that position
# and a list of valid directions. 
## Test
# legal_move(2,4,PLAYER1) => return validity for assigning PLAYER1 to global storage[2][4] and a list of
# valid directions

def legal_move(m, n, who):
    '''the tile on upperleft of the board is m=0, n=0, first row first column enter either PLAYER1 OR PLAYER2 for who'''
    global storage, PLAYERS, WHOSE_TURN
    validity = False; valid_direction = [] # pre-allocate storage for valid direction
    # check whether the matrix position is empty or not, if it is not empty, return False
    if storage[m][n] != None:
        return validity, valid_direction
    
    # Direction Vector in form of [m_increment, n_increment, direction]
    DIRECTION = [[-1, 0, "North"], [-1, 1, "Northeast"], [0, 1, 'East'], [1, 1, 'Southeast'], [1, 0, 'South'],[
        1, -1, 'Southwest'], [0, -1, 'West'], [-1, -1, 'Northwest']]
    for vector in DIRECTION:
        # assign next position in current direction
        temp_m = m + vector[0]; temp_n = n + vector[1]
        try:
            # if next position is other player's tile, and is own tile before reaching empty tile, then it's valid in that direction 
            if storage[temp_m][temp_n] not in [None, who]: # if the next tile is opponent tile
                while storage[temp_m + vector[0]][temp_n + vector[1]] in PLAYERS and temp_m + vector[
                    0] >= 0 and temp_n + vector[1] >= 0: 
                    if storage[temp_m + vector[0]][temp_n + vector[1]] == who:
                        validity = True
                        valid_direction.append(vector) if vector not in valid_direction else None
                        break
                    else:
                        temp_m += vector[0]; temp_n += vector[1]
        except IndexError: # when the next position is out of boundary
            pass # Do nothing
    return validity, valid_direction


######################## Draw Board - Begin ########################
import turtle
## SIGNATURE
# Given size of the board, it returns a turtle graphic with proper screen size and grid
## Test
# draw_board(8) => return a turtle graphic with 8x8 grid, with four tiles at the center

def draw_board(n):
    wn = turtle.Screen()
    wn.setup(n * SQUARE + 1.5 *SQUARE, n * SQUARE + 1.5* SQUARE), wn.screensize(n * SQUARE, n * SQUARE), wn.bgcolor('white')
    # Create the turtle to draw the board
    othello = turtle.Turtle(); othello.penup(), othello.speed(0), othello.hideturtle()
    othello.goto(-4*SQUARE, 4.2*SQUARE), othello.write("Othello Challenge", False, font=("Arial", 16, "bold"))
    othello.goto(SQUARE, 4.3*SQUARE), othello.write("You have:                   tiles. ", False, font=("Arial", 12, "bold"))
    othello.goto(SQUARE, 4*SQUARE), othello.write("Computer has:          tiles.  ", False, font=("Arial", 12, "bold"))
    
    # Turtle to display score on Screen
    global turtle_1, turtle_2
    turtle_1, turtle_2 = turtle.Turtle(), turtle.Turtle()
    turtle_1.speed(0), turtle_2.speed(0)
    turtle_1.hideturtle(), turtle_2.hideturtle()
    turtle_1.pu(), turtle_2.pu()
    turtle_1.goto(2.8*SQUARE, 4.3*SQUARE), turtle_2.goto(2.8*SQUARE, 4*SQUARE)
    turtle_1.pd(), turtle_2.pd()
    turtle_1.color("Red"), turtle_2.color("Red")
    turtle_1.write("2", False, font=("Arial", 13, "bold")), turtle_2.write("2", False, font=("Arial", 13, "bold"))
    
    # Line color is black, fill color is flat dark earth
    othello.color("black", "#787828")

    # Move the turtle to the lower left corner
    corner = -n * SQUARE / 2; othello.setposition(corner, corner)

    #Draw the green background
    othello.begin_fill()
    for i in range(4):
        othello.pendown(); othello.forward(SQUARE * n); othello.left(90)
    othello.end_fill()
    
    #Draw the horizontal lines
    for i in range(n + 1):
        othello.setposition(corner, SQUARE * i + corner); draw_lines(othello, n)
    
    # Draw the vertical lines
    othello.left(90)
    for i in range(n+1):
        othello.setposition(SQUARE * i + corner, corner); draw_lines(othello, n)
    
    # Draw initial four circles
    othello.right(90)
    coord = [[25, 25-SQUARE/3, "Black"], [-25, -25-SQUARE/3, "Black"], [-25, 25-SQUARE/3, "White"],[25, -25-SQUARE/3, "White"]]
    for i in coord:
        othello.goto(i[0], i[1]), othello.begin_fill(), othello.color(i[2], i[2])
        othello.pd(), othello.circle(SQUARE/3), othello.pu(), othello.end_fill()
    return othello


## SIGNATURE
# It draws a line in turtle graphic in length of n
## Test
# draw_lines(turt, 50) => a line of length 50 will be drawn

def draw_lines(turt, n):
    turt.pendown(), turt.forward(SQUARE * n), turt.penup()
turtle.hideturtle()
######################## Draw Board - The End ########################


## SIGNATURE
# It takes in x, y coordinates on board (where -175 <= x or y <= 175), 
# returns the corresponding position on the 8x8 matrix with square = 50 
## Test
# transXY_to_MN((-175, 175)) => (0, 0)

def transXY_to_MN(pos):
    MAXIMUM_X = MAXIMUM_Y = 175; SQUARE = 50
    pos_x, pos_y = pos
    m = (MAXIMUM_Y - pos_y) // SQUARE # square 50, n = 8
    n = (MAXIMUM_X + pos_x) // SQUARE 
    return m, n


## SIGNATURE
# It creates a onclick listern for turtle screen

def create_game_listern():
    turtle.speed(0) # FASTEST speed
    print("You take the first turn: ")
    turtle.onscreenclick(execute_move)


## SIGNATURE
# Given a storage of game state, it checks for a winner or end game state for this storage
## Test
# evaluate_for_winner(storage) => Boolean, str(winner)

def evaluate_for_winner(storage):
    global PLAYERS, count_player1, count_player2, WHOSE_TURN, turtle_1, turtle_2
    count_player1 = count_player2 = 0
    result = True
    for ele in storage:
        for each_item in ele:
            if each_item == None:
                result = False    # Board is not full if there's an empty tile
            elif each_item == PLAYERS[0]:
                count_player1 += 1
            elif each_item == PLAYERS[1]:
                count_player2 += 1
    # Draw Score on Screen
    turtle_1.undo(), turtle_2.undo()
    turtle_1.write(str(count_player1), False, font=("Arial", 13, "bold"))
    turtle_2.write(str(count_player2), False, font=("Arial", 13, "bold"))
    # assign string for announcing winner in end game state
    winner = "No winner, it's a tie!" if count_player1 == count_player2 else "You Win!" if count_player1 > count_player2 else "You lose. :("
    return result, winner


## SIGNATURE
# It takes in a matrix position of global storage of game state, it returns the number of potential flips if 
# this position is being placed
## Test
# test_best_AI_move(2,3) => the number of flips if storage[2][3] is assigned as Computer's tile.

def test_best_AI_move(m,n):
    global storage
    DIRECTION = [[-1, 0, "North"], [-1, 1, "Northeast"], [0, 1, 'East'], [1, 1, 'Southeast'], [1, 0, 'South'],[
        1, -1, 'Southwest'], [0, -1, 'West'], [-1, -1, 'Northwest']]
    for vector in DIRECTION:
        temp_m = m + vector[0]; temp_n = n + vector[1]
        num_flip = 0
        try:
            if storage[temp_m][temp_n] not in [None, PLAYER2]: # if the next tile is player's tile
                while storage[temp_m + vector[0]][temp_n + vector[1]] in PLAYERS and temp_m + vector[
                    0] >= 0 and temp_n + vector[1] >= 0: 
                    if storage[temp_m + vector[0]][temp_n + vector[1]] == PLAYER2:
                        num_flip += 1
                        temp_m += vector[0]; temp_n += vector[1]
                    else:
                        temp_m += vector[0]; temp_n += vector[1]
        except IndexError:
            pass # Do nothing
    return num_flip


## SIGNATURE
# Given a list of valid move positions of the board, it return the best next move for computer 
## Test
# Given a list of valid move positions, it should returns the one valid move that results in winning the most tiles flipped

def pick_best_AI_move(valid_move):
    num_flip_each_valid_move = []
    for ele in valid_move:
        num_flip = test_best_AI_move(ele[0], ele[1])
        num_flip_each_valid_move.append(num_flip)
    best_move_index = num_flip_each_valid_move.index(max(num_flip_each_valid_move))
    return valid_move[best_move_index]


## SIGNATURE
# It allows computer to place a tile base on its own thinking
## Test
# computer should execute a move upon this function called

def computer_move():
    global WHOSE_TURN
    valid_move = [] # store m, n informatin for valid movements for computer
    for m in range(8):
        for n in range(8):
            if legal_move(m, n, PLAYER2)[0] == True:
                valid_move.append([m, n])
    ## Easy AI Mode - Uncomment next 3 lines and comment out the other section to switch mode
    # random_pick = randint(0, len(valid_move)-1)
    # m = valid_move[random_pick][0] 
    # n = valid_move[random_pick][1]
    ## Hard AI Mode - Uncomment next 3 lines and comment out the other section above to switch mode
    m = pick_best_AI_move(valid_move)[0]; n = pick_best_AI_move(valid_move)[1]
    execute_move(-175 + n * SQUARE, 175 - m * SQUARE)


## SIGNATURE
# Base on who is playing the next move, it returns a list of valid move positions in the storage matrix
## Test
# num_valid_move(PLAYER1) => it should returns a list of possible valid moves for PLAYER1

def num_valid_move(who):
    global storage
    valid_move = []
    for m in range(8):
        for n in range(8):
            if storage[m][n] != None:
                continue
            elif legal_move(m, n, who)[0] == True:
                valid_move.append([m, n])
            else:
                continue
    return valid_move


### Developer feature for improving testing/debugging efficiency.
## SIGNATURE
# This is made so that computer can play against computer, it doesnt hurt to add more fun :)

def auto_player_move():
    global WHOSE_TURN
    valid_move = num_valid_move(PLAYERS[WHOSE_TURN])
    if valid_move != []:
        random_pick = randint(0, len(valid_move)-1)
        m = valid_move[random_pick][0]; n = valid_move[random_pick][1]
        execute_move(-175 + n * SQUARE, 175 - m * SQUARE)


######## Core Function - Begin ########
## SIGNATURE
# Given a coordinate (x,y) of the board, it places tiles base on validity. Opponent tiles will be flipped in appropriate directions.
# Game state will be checked after every move to determine if end game condition is met. 
## Test
# execute_move(25,25) => coordinate(25, 25) will be converted to matrix position; validity will be checked and corresponding tiles
# will be flipped and updated in game state, game board will be checked if there is a winner.

def execute_move(x, y):
    # Edge case where user clicks outside of screen but within the window.
    if x <= LEFT_BOUNDARY or x >= RIGHT_BOUNDARY or y >= TOP_BOUNDARY or y <= BOTTOM_BOUNDARY:
        print("Out of bound")
        return None
    global storage, WHOSE_TURN, player_name
    # Calibrating the clicked corodinate to coordinate of the center of its located tile
    pos_x = int((x // SQUARE) * SQUARE + SQUARE/2); pos_y = int((y // SQUARE) * SQUARE + SQUARE/2)
    # translate the coordinate to a matrix position (m, n) in the storage matrix
    pos_m, pos_n = transXY_to_MN((pos_x, pos_y))
    
    # store validity and a list of valid direction for that matrix position 
    temp = legal_move(pos_m, pos_n, PLAYERS[WHOSE_TURN])
    validity = temp[0] # True if it is a legal move, False if otherwise.
    valid_direction = temp[1] # A list of legal directions.
    
    # if the matrix position is a valid position, draw new tile and flip oponent's tiles
    if validity == True and valid_direction != []:
        # Insert move to storage and draw corresponding tile
        insert_move(storage, pos_m, pos_n, PLAYERS[WHOSE_TURN]); draw_tile(pos_x, pos_y)
        # flip opponent's tiles in valid directions
        for vector in valid_direction:
            temp_mm = pos_m; temp_nn = pos_n
            while storage[temp_mm + vector[0]][temp_nn + vector[1]] not in [None, PLAYERS[WHOSE_TURN]]:
                if 0 <= temp_mm + vector[0] <= 7 and 0 <= temp_nn + vector[1] <= 7:
                    flip_tiles(temp_mm + vector[0], temp_nn + vector[1], PLAYERS[WHOSE_TURN])
                    insert_move(storage, temp_mm + vector[0], temp_nn + vector[1], PLAYERS[WHOSE_TURN])
                    temp_mm += vector[0]; temp_nn += + vector[1]
                else:
                    break
        
        # then check for any winner and annouce winner if found
        current_result = evaluate_for_winner(storage) 
        player1_valid_move, player2_valid_move = num_valid_move(PLAYERS[0]), num_valid_move(PLAYERS[1])
        if current_result[0] != False: # if there is a winner, annouce it and end game
            print(current_result[1])
            player_name = turtle.textinput('Enter Your Name: ', current_result[1])
            end_game()
            return None
        elif player1_valid_move == [] and player2_valid_move == []: # if neither side has no valid move to make, then end game
            print("No more valid move for you or computer.")
            player_name = turtle.textinput('Enter Your Name: ', current_result[1])
            print(current_result[1])
            end_game()
            return None
        else: # if no winner yet, continue game
            WHOSE_TURN = (WHOSE_TURN + 1) % 2 # switch to next player
            if PLAYERS[WHOSE_TURN] == PLAYER2: # if it is computer's turn
                if num_valid_move(PLAYERS[WHOSE_TURN]) != []: #check if any valid move
                    print("It's computer's turn."); computer_move() # if theres a valid move then computer makes a move
                elif num_valid_move(PLAYERS[WHOSE_TURN]) == []: # else if no valid move
                    print("No valid move for computer."); WHOSE_TURN = (WHOSE_TURN + 1) % 2 # switch to next player
                    # # Comment out next line for auto_play version (1/2) 
                    # auto_player_move()
            elif PLAYERS[WHOSE_TURN] == PLAYER1: # if it is player's turn
                if num_valid_move(PLAYERS[WHOSE_TURN]) == []: # if no valid move for player
                    print("No valid move for you."); WHOSE_TURN = (WHOSE_TURN + 1) % 2 # switch to computer's turn
                    computer_move() 
                else:
                    print("It's your turn.")
                # # Comment out below section for auto_player version (2/2)
                # else: #else if there is valid move for player
                #     auto_player_move() # auto_mode for player/computer vs computer
######## Core Function - The End ########


## SIGNATURE
# given coordinate of a position on the board, it draws a tile base on current player
## Test
# draw_tile(25, 25) => it draws a circle of radius of 1/3 of SQUARE on turtle graphic screen at (25,25)

def draw_tile(pos_x, pos_y):
    turtle.pu()
    turtle.color("Black") if PLAYERS[WHOSE_TURN] == PLAYER1 else turtle.color("White") # Check again
    turtle.goto(pos_x, pos_y - SQUARE/3); turtle.pd()
    turtle.begin_fill(); turtle.circle(SQUARE/3); turtle.end_fill()


## SIGNATURE
# given matrix position of storage of game state, and current player, it flipped the corresponding tile
# to the current player's color
## Test
# flip_tiles(0,0, PLAYER!) => it flips the current tile at storage[0][0] to black color (represents player1)

def flip_tiles(m, n, to_who):
    turtle.pu(), turtle.goto(LEFT_BOUNDARY + SQUARE/2 + n * SQUARE, TOP_BOUNDARY - SQUARE/2 - m * SQUARE - SQUARE/3), turtle.pd()
    if to_who == PLAYER1:
        turtle.color("Black")
    elif to_who == PLAYER2:
        turtle.color("White")
    turtle.begin_fill(), turtle.circle(SQUARE/3), turtle.end_fill()


## SIGNATURE
# it ends the game but keeps turtle graphic in the mainloop

def end_game():
    turtle.done()


## SIGNATURE
# given scores.txt file directory, it stores the player name and num of tiles for that game into the file
## Test
# it should append player's name and number of tiles into scores.txt and sort the list in descending order

def store_score(file_path):
    global count_player1, player_name
    # First insert new entry and sort the list in Descending order
    if player_name == '': # if game is forced to end half way, do not save entry
        return None
    with open(file_path, 'r') as f:
        lst = f.readlines()
        new_lst = []
        for entry in lst:
            new_lst.append(entry.strip("\n").split(" "))
        new_lst.append([player_name, str(count_player1)])
        new_lst.sort(key= lambda x: x[1], reverse = True)
        f.close()
    # Then overwrite on file
    with open(file_path, "w+") as f:
        lines = ''
        for entry in new_lst:
            lines += entry[0] + ' ' + entry[1] + "\n"
        f.writelines(lines)
        f.close()


def main():
    draw_board(8)
    new_game_state(8) # n = 8
    create_game_listern()
    end_game()
    # Change file path in order to save your score
    # file_path = '/Users/Casparsu/Documents/CS5001/GitHub_GitHub/student_repo_casparsu/HW6 & 7/scores.txt'
    file_path = os.getcwd()+"score.txt"
    store_score(file_path)

main() # Comment out for pytest


#### Tests ####
def test_new_game_state():
    assert(new_game_state(4) == [[None, None, None, None],[
        None, '1', '0', None],[None, '0', '1', None],[None, None, None, None]])
def test_transXY_to_MN():
    assert(transXY_to_MN((-175, 175)) == [0, 0])