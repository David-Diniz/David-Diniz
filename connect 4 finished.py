import pygame,sys #imports pygame and system so i can use them later
import numpy as np #i use numpy to set up a board of zeros and as a result i need to import it
pygame.init() #initializing pygame allows me to actually use it

#these are all just variables that i set now for reuse later
WIDTH = 700
HEIGHT = 600
LINECOLOUR = (0,0,255)
LINEWIDTH = 10
BLUE = (60,60,215)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
PLAYERONECOLOUR=(255,255,0)
PLAYERTWOCOLOUR = (255,0,0)
WINCOLOUR = (0,255,0)
BOARDROWS = 6 #height
BOARDCOLS = 7 #width

pygame.display.set_caption('Connect 4')
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #this command actually sets up my display where i will now be able to draw things later
board = np.zeros((BOARDROWS,BOARDCOLS))#this is my board of zeros that i use numpy to set up i use this board to check what squares are taken and by who.
#while it may not be seen by the player this is where all of the win checks and and square marking happens and as a result this is an integral part of the program

#this program uses a lot of functions to be more efficient and this is the part of the program where i define them

def drawLines(): #this is the function which draws the game grid
    screen.fill(BLUE)#dyes the whole screen blue
    for row in range(BOARDROWS):
        for col in range(BOARDCOLS):#these two for loops will run through every square, drawing a white circle where the circles can be placed 
            pygame.draw.circle(screen, WHITE, (col *100 + 50, row*100 + 50), 45)#this command draws white circles

def markSquare(row, col, player):#this function marks the square on my numpy board assuming the square isn't taken
    board[row][col] = player #sets the board at index row and col to the value of player(either on or two) indicating which colour of circle is on that square

def checkSquare(row, col): #this function will check if a square is already taken or not
    if board[row][col] == 0:#if the board at the given indexes is free then it's value will be zero so return True
        return True

    else: #if it isn't zero then its taken and so we return false
        return False

def isBoardFull(): #this function checks if the board is full
    for row in range (BOARDROWS):
        for col in range(BOARDCOLS):#two for loops will go through each and every square on the board
            if board[row][col] == 0: #if even one cell is found with value 0 then it returns false
                return False
    return True#if no empty squares are found it returns false


def drawFigures(player): #this function will draw the circles in the square that the player chooses
    for row in range(BOARDROWS): 
        for col in range(BOARDCOLS): #the two for loops will run through every square on the grid
            if player == 1: #if the player is one then it will draw a circle of player one's colour in the square that player clicked
                pygame.draw.circle(screen, PLAYERONECOLOUR, (clickedCol*100 + 50, gravity(clickedCol, clickedRow) *100 + 50), 45)
            elif player == 2:  #does the same for player two
                pygame.draw.circle(screen, PLAYERTWOCOLOUR, (clickedCol*100 + 50, gravity(clickedCol, clickedRow)*100 + 50),45)

def gravity(clickedCol, clickedRow): # this is the function for gravity which makes the circles fall if there is nothing beneath them
    while clickedRow < 5: #gravity doesn't apply if you're in the 5th row so if they're already in the 5th row then they don't enter the loop, by making this a while loop it will happen over and over until the circle can no longer fall
        if board[clickedRow + 1][clickedCol] == 0: #by adding one to the row we are checking if the space directly below it is equal to zero
            clickedRow += 1 #if the square is free than it adds one to the value of the row and this causes the circle to drop down one, this keeps happening until it either hits the bottom or the aquare below it is taken 
        else:
            break #if the square below is taken it breaks from the loop
    return (clickedRow)#the clicked row now equals whatever it is after gravity happens, this essentially updates the variable for later use


def checkWin(Row, clickedCol, player): #this entire function covers checking for a win in all possible directions
    #horizontal win check
    for row in range(BOARDROWS):
        for col in range(BOARDCOLS - 3): #to avoid an index error i don't check the last three columns, if there is a win then it will be detected in the first 4 columns.
            if board[row][col] == player and board[row][col+1] == player and board[row][col +2] == player and board[row][col + 3] == player: #checks the board at index of whatever the for loops are at and the three squares to the right of that.
                drawHorizontalWin(row, col, player)#if the next three squares are all occupied by the same player, it will draw the horizontal win line in the spot that the player won 
                return True #returns true for checks with if statements later
    #vertical win check
    for row in range(BOARDROWS - 3): #similar to checking for a horizontal win we don't have to check the bottom 3 rows as they would only serve to break the program(index error)
        for col in range(BOARDCOLS):
            if board[row][col] ==player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player: #if a spot is detected which belongs to the player, it will also check the three below it to see if they also belong to the player
                drawVerticalWin(row, col, player)#if they do then it draws a vertical win line 
                return True #Returns true for later checks
    #descending diagonal win check
    for row in range(BOARDROWS-3): #for a descending diagonal we only need to check a 4x3 grid in the top right, anymore than that will produce and index error as it will attempt to check a square which doesn't actually exist
        for col in range(BOARDCOLS -3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player: #checks for a diagonal win on the board
                drawDescendingDiagonalWin(row, col, player) #if they have won, this will draw the appropriate win line
                return True #returns true for later checks
    #ascending diagonal win check
    for row in range(3,BOARDROWS): #if we are going to check for ascending diagonal wins then we need to check all the squares in a 4x3 grid in the bottom left, for this we require the different dtarting value of the for loop, in this case 3
        for col in range(BOARDCOLS-3): #no change is required in the columns for loop however as we still start at the 0th index. 
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col +2] == player and board[row -3][col +3] == player: #checks for an ascending diagonal win
                drawAscendingDiagonalWin(row, col, player)#draws ascending diagonal win line
                return True#return true for later checks
    return False #If nobody has won yet the program returns false which we will use later when we call on the function to see if anybody has won

    # had trouble with win algoritm, this site made me see that i need to run my for loop 3 less times in order to avoid an index error with myboard
    #https://stackoverflow.com/questions/29949169/python-connect-4-check-win-function

#thewese are the functions for drawing the win lines, they all draw a line in the appropriate spot using pygame
#they pass whatever index the for loops are at for row and col so it starts drawing the line in whichever the first square detected was in the win
def drawVerticalWin(Row, col, player):
    pygame.draw.line(screen, WINCOLOUR, (col*100 +50,Row*100 +50),(col*100+50,(Row+3)*100 +50), 10)
def drawHorizontalWin(Row, col, player):
    pygame.draw.line(screen, WINCOLOUR, (col*100 + 50, Row *100 +50), ((col+3)*100 +50, Row * 100 +50), 10)
def drawAscendingDiagonalWin(Row, col, player):
    pygame.draw.line(screen, WINCOLOUR, (col*100 + 50, Row *100 +50), (((col+3)*100 +50), (Row-3)*100+50), 10)
def drawDescendingDiagonalWin(Row, col, player):
    pygame.draw.line(screen, WINCOLOUR, (col*100 + 50, (Row)*100 +50), ((col+3)*100 +50, (Row+3)*100 + 50), 10)

#this is the restart function it will be triggered later when the user types r
def restart():
    screen.fill(BLUE)#refills the screen with blue
    drawLines()#redraws the game lines
    player = 2 #sets the player equal to 2, if you win you don't get to go first assuming you stay the same colour
    for row in range(BOARDROWS):
        for col in range(BOARDCOLS):
            board[row][col] = 0 #resets the numpy board to set all values to zero


    
drawLines()#just before entering the game loop we draw the game lines
player = 1 #initializes the player variable, setting it to one
gameOver = False #this variable is used to detect whether the game is over later


#below is the main game loop, it's where all events take place and where inputs are taken from
while True:
    for event in pygame.event.get(): #this block is where it reads your input so anytiome you do something, this executes
        if event.type == pygame.QUIT: #this is for if you press the red X in the top right corner, then this code executes
            pygame.display.quit()#closes the pygame window, without this the program would stop and the game would still be on your screen, but you wouldn't be able to clickl stuff
            sys.exit()#stops the program
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not gameOver: #detects a left mouse button click, (josh almost broke it by clicking both mouse buttons at once so i chose to implement this) also checks if the gameover variable is True, if all conditions are met the code executes
            posX = event.pos[0]#this gives the x pixel value of where you clicked on the screen, if you clicked the bottom right this value would be 700
            posY = event.pos[1]#this grabs the y pixel value of where you clicked on the screen, if you clicked the bottom right this value would be 600
            clickedCol = int(posX/100) #by dividing it by 100 it gives me which column you clicked, set to an int so it automatically rounds down. i.e clicked 674, gives me 6.74 which is rounded to 6 
            clickedRow = int(posY/100) #same process as clickedCol
            Row = gravity(clickedCol, clickedRow) #had to have this predefined so i could use it in my functions earlier

            if checkSquare(clickedRow, clickedCol): #puts clickedCol and clickedRow throught the check square function and checks if it returns true, if statements automatically check for the value true so there is no need for == True at the end
                if player == 1: #if the square is free it then checks what players turn it is
                    drawFigures(player)#draws a circle in the players colour on the screen, only requires me to pass the player variable through it from there it detects which player's turn it is and draws the correct figure
                    markSquare(Row, clickedCol, 1)#Passes the row with gravity applied clicked column and the player through the markSquare function which will mark my numpy board accoringly
                    if checkWin(Row, clickedCol, player): #checks for a win by passing the Row clicked column and player through that function automatically checks if it returns True
                        gameOver = True #if the player has won then gameover is set to True which no longer allows the if statement to execute which happens after you click the left mouse button
                    player = 2 #following player one's turn it is set to be player 2's turn
                elif player == 2: #same logic as previous if statement but for player 2 instead
                    drawFigures(player)
                    markSquare(Row, clickedCol, 2)
                    if checkWin(Row, clickedCol, player):
                        gameOver = True
                    player = 1 

            
        if event.type == pygame.KEYDOWN:#this will detect if the user has pressed a key on their keyboard
            if event.key == pygame.K_r:#checks if the pressed key was r
                restart()#if the user did press r then the game restarts
                gameOver = False #almost forgot to add this, it allows the game to be replayed, without it gameOver is still true and so the if statement which detects a mouse button going down will never execute
    
    pygame.display.update()#happens on every iteration of the for loop this updates the screen to display what has happened, without it the screenb would be black and nothing would appear in the pygame window
