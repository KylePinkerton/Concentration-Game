import random

def create_space():
    """() -> None
    Prints 51 lines of white space
    """
    print('\n'*50)
        
def shuffle_deck(deck):
    '''(list of str)->None
       Shuffles the given list of strings representing the playing deck    
    '''
    print('Shuffling the deck...\n')
    
    random.shuffle(deck)
    
def create_board(size):
    '''int->list of str
       Precondition: size is even positive integer between 2 and 52
       Returns a rigorous deck (i.e. board) of a given size.
    '''
    board = [None]*size 

    letter='A'
    for i in range(len(board)//2):
          board[i]=letter
          board[i+len(board)//2 ]=board[i]
          letter=chr(ord(letter)+1)
    return board

def print_board(a):
    '''(list of str)->None
       Prints the current board in a nicely formated way
    '''
    for i in range(len(a)):
        print('{0:4}'.format(a[i]), end=' ')
    print()
    for i in range(len(a)):
        print('{0:4}'.format(str(i+1)), end=' ')


def wait_for_player():
    '''()->None
    Pauses the program/game until the player presses enter
    '''
    input("\nPress enter to continue. ")
    print()

def print_revealed(discovered, p1, p2, original_board):
    '''(list of str, int, int, list of str)->None
    Prints the current board with the two new positions (p1 & p2) revealed from the original board
    Preconditions: p1 & p2 must be integers ranging from 1 to the length of the board
    '''
    #saving values of discovered that we will be altering
    a = discovered[p1-1]
    b = discovered[p2-1]

    #changing values of discovered to corresponding values of original board
    #as dictated by p1, p2 
    discovered[p1 -1] = original_board[p1-1]
    discovered[p2 -1] = original_board[p2-1]

    #printing discovered
    print_board(discovered)

    #changing discovered back to its original form
    discovered[p1-1] = a
    discovered[p2-1] = b 

    
    

#############################################################################
#   FUNCTIONS FOR OPTION 2 (with the board being read from a given file)    #
#############################################################################

def read_raw_board(file):
    '''str->list of str
    Returns a list of strings represeniting a deck of cards that was stored in a file. 
    The deck may not necessarifly be playable
    '''
    raw_board = open(file).read().splitlines()
    for i in range(len(raw_board)):
        raw_board[i]=raw_board[i].strip()
    return raw_board


def clean_up_board(l):
    '''list of str->list of str

    The functions takes as input a list of strings representing a deck of cards. 
    It returns a new list containing the same cards as l except that
    one of each cards that appears odd number of times in l is removed
    and all the cards with a * on their face sides are removed
    '''
    print("\nRemoving one of each cards that appears odd number of times and removing all stars ...\n")
    playable_board=[]

    #create a board (new_board) equivalent to l in which we can change the
    #individual elements, as we don't want to alter the values contained in l
    new_board = [None]*len(l)
    
    for i in range(len(l)):
        new_board[i] = l[i]
    
    # check number of times a card appears in the list,
    # if it appears odd times, turn the first occurance
    # into a 0, also turn all *'s into 0's
    # we will not append these 0's to the new list 
    for i in range(len(l)):
        if new_board[i] in '*':
            new_board[i] = 0
        if new_board.count(l[i])%2 == 1:
            new_board[i] = 0 
        
    # list should now be able to be copied into playable board

    h = 0
    while h<len(l):
        #don't append the 0's 
        if new_board[h] == 0:
            h +=1
        #append everything else 
        else:
            playable_board.append(new_board[h])
            h += 1 
            
    return sorted(playable_board)

def is_rigorous(l):
    '''list of str->bool
    Returns True if every element in the list appears exactlly 2 times or the list is empty.
    Otherwise, it returns False.

    Precondition: Every element in the list appears even number of times
    '''
    
    for i in range(len(l)): #for loop runs O(n) times 
        if l.count(l[i]) == 2: #runtime of l.count O(n) +1 (for comparision) => total runtime O(n) e.g. the +1 is insignificant
            pass
        else:
            return False

    #this entire for loop does O(n)*O(n) operations => O(n^2) operations in total

    return True                
        

####################################################################

def play_game(board):
    '''(list of str)->None
    Plays a concentration game using the given board
    Precondition: board a list representing a playable deck
    '''

    print("Ready to play ...\n")

    #creating a hidden board of the same length as the original board
    #it will have *'s representing face down cards, e.g. the cards are "hidden" 

    hidden_board = [None]*(len(board))

    for i in range(len(board)):
        hidden_board[i] = '*'
        
    #initializing variables we will need for the following two while loops (nested)
    first_position = 0
    second_position = 0
    q = 1
    guesses = 0 
    board_size = len(hidden_board)

    while hidden_board != board:
        #the below will only execute once positions are given from the next, inner loop
        #because these values are initialized to 0
        if first_position > 0 and second_position > 0:
            print_revealed(hidden_board, first_position, second_position, board)
            print()
            #if the revealed positions match, save their values to the hidden board
            #so they are shown from now on 
            if board[first_position - 1] == board[second_position - 1]:
                hidden_board[first_position-1] = board[first_position-1]
                hidden_board[second_position-1] = board[second_position-1]
                #if the hidden board is equal to the original board, the game is
                #complete, so break out of the loop
                if hidden_board == board:
                    break                
            wait_for_player()
            create_space()

        #print the hidden board in its current state 
        print_board(hidden_board)
        print()           
                
        while q:
            print('\nEnter two distinct positions on the board that you want revealed.')
            print('i.e. two integers in the range [1, {}]' .format(board_size))
            first_position = int(input('Enter position 1: '))
            second_position = int(input('Enter position 2: '))

            
            #if one of the positions given are not in the correct range, inform the user of this
            #and go through the loop again to get new positions, without increasing the number of guesses 
            if 1 > first_position or first_position > board_size or 1 > second_position or second_position > board_size:
                print('One or both of your positions do not have a corresponding value on the board.')

            #if one of the positions given has already been paired, and both of the positions given are the same,
            #inform the user of this and go through the loop again to get new positions, without increasing the number
            #of guesses
            elif (hidden_board[first_position - 1] != '*' or hidden_board[second_position - 1] != '*') and first_position == second_position:
                print('One or both of your chosen positions has already been paired.')
                print('You chose the same positions.')
        
            #if one of the positions given has already been paired, inform the user of this and go through the
            #loop again to get new positions, without incrementing number of guesses 
            elif hidden_board[first_position - 1] != '*' or hidden_board[second_position - 1] != '*':
                print('One or both of your chosen positions has already been paired.')

            #if both of the positions given are the same, inform the user of this and go through the loop again
            #to get new positions, without incrementing number of guesses 
            elif first_position == second_position:
                print('You chose the same positions.')

            #if none of the above hold true, the given positions are satisfactory, so increment 
            #the number of guesses and break out of the loop
            else:
                guesses += 1
                break

            print('Please try again. This guess did not count. Your current number of guesses is {}.' .format(guesses))


    #the following executes when the board is fully discovered
    wait_for_player()
    create_space()
    relative_score = int(guesses - len(board)/2)
    print('Congratulations! you completed the game with {} guesses. That is {} more than the best possible.' .format(guesses, relative_score))
    


    # this is the funciton that plays the game
 

####################################################################################################################################
#main
####################################################################################################################################

if __name__ == "__main__":
        

    #WELCOME MESSAGE
    print('*'*42)
    print('*' + ' '*40 + '*')
    print('*' + ' '*2 + '__Welcome to my Concentration game__' + ' '*2 + '*')
    print('*' + ' '*40 + '*')
    print('*'*42)
    print()
    print()

    #printing the available options for the user
    print('Would you like (enter 1 or 2 to indicate your choice):')
    print('(1) me to generate a rigorous deck of cards for you')
    print('(2) or, would you like me to read a deck from a file?')

    #the following loop will ask the user what option they want,
    #and will continue to ask until an appropriate answer is given 

    i = 1 
    while i:
        choice = int(input())

        if choice == 1:
            i = 0

        elif choice == 2:
            i = 0
            
        else: 
            print(choice, 'is not exisiting option. Please try again. Enter 1 or 2 to indicate your choice')

    
    
    ####################################### OPTION 1 — Generating a Rigorous Deck ##################################################
    if choice == 1:
        print('You chose to have a rigorous deck generated for you')
        
        p = 1
        while p:
            print('\nHow many cards do you want to play with?')
            requested_size = int(input('Enter an even number between 2 and 52: '))

            #if the following evaluates to true, the inputs are satisfactory and the
            #program can continue, if the following evaluates to false, the user
            #will be prompted for another input
            if requested_size %2 == 0 and 2 <= requested_size <= 52:
                p = 0

        #create a board of the given size 
        board = create_board(requested_size)

        #shuffle the board
        shuffle_deck(board)       

        #wait for player
        wait_for_player()
        create_space()

        #play the game 
        play_game(board)

       

    ####################################### OPTION 2 — Loading a deck of cards from a File #########################################
    if choice == 2:
        print('You chose to load a deck of cards from a file')
        file = input('Enter the name of the file: ')
        file = file.strip()
        board = read_raw_board(file)
        board = clean_up_board(board)
        board_from_file_size = str(len(board))
        string_size = len(board_from_file_size)

        
        if is_rigorous(board):
            #create a message telling the user that the deck is playable, rigorous,
            #and informing the user about the total number of cards in the deck
            #top line
            print('*'*55, end='')
            print('*'*string_size, end='')
            print('*'*12)
            #second line
            print('*', end='')
            print(' '*54, end='')
            print(' '*string_size, end='')
            print(' '*11, end='')
            print('*')
            #third line
            print('*', end='')
            print(' '*2, end='')
            print('__This deck is now playable and rigorous and it has {} cards.__' .format(board_from_file_size), end='')
            print(' '*2, end='')
            print('*')
            #fourth line
            print('*', end='')
            print(' '*54, end='')
            print(' '*string_size, end='')
            print(' '*11, end='')
            print('*')
            #fifth line
            print('*'*55, end='')
            print('*'*string_size, end='')
            print('*'*12)

            #message has been printed

            #wait for the player
            print()
            wait_for_player()
            create_space()

            #shuffle the deck
            shuffle_deck(board)
            wait_for_player()
            create_space()

            #check if the board is empty, because if it is, it is not possible to play the game
            if len(board) == 0:
                print('The resulting board is empty.')
                print('Playing Concentration game with an empty board is impossible.')
                print('Good bye')

                    
            #if the board isn't empty, play the game 
            else:
                play_game(board)
        
               
        else:
            #create a message telling the user that the deck is playable, not rigorous,
            #and informing the user about the total number of cards in the deck
            #top line
            print('*'*59, end='')
            print('*'*string_size, end='')
            print('*'*12)
            #second line
            print('*', end='')
            print(' '*58, end='')
            print(' '*string_size, end='')
            print(' '*11, end='')
            print('*')
            #third line
            print('*', end='')
            print(' '*2, end='')
            print('__This deck is now playable but not rigorous and it has {} cards.__' .format(board_from_file_size), end='')
            print(' '*2, end='')
            print('*')
            #fourth line
            print('*', end='')
            print(' '*58, end='')
            print(' '*string_size, end='')
            print(' '*11, end='')
            print('*')
            #fifth line
            print('*'*59, end='')
            print('*'*string_size, end='')
            print('*'*12)

            #message has been printed

            #wait for the player
            print()
            wait_for_player()
            create_space()

            #shuffle the deck
            shuffle_deck(board)
            wait_for_player()
            create_space()


            #we don't have to check if the board is empty before playing the game here,
            #because if the board is empty is_rigorous would have returned true
            #and we are in the conditional case where is_rigorous returned false 
            #therefore, play the game 
            play_game(board)
               
        

