def welcome():
    print(
    '+------------------------------------------------+'+
    '\nWELCOME TO TIC TAC TOE\n'+
    '+------------------------------------------------+\n')

def board(p):
    print(
'+-------+-------+-------+\n'+
'|       |       |       |\n'+
'|   {}   |   {}   |   {}   |\n'.format(p[0], p[1], p[2])+
'|       |       |       |\n'+
'+-------+-------+-------+\n'+
'|       |       |       |\n'+
'|   {}   |   {}   |   {}   |\n'.format(p[3], p[4], p[5])+
'|       |       |       |\n'+
'+-------+-------+-------+\n'+
'|       |       |       |\n'+
'|   {}   |   {}   |   {}   |\n'.format(p[6], p[7], p[8])+
'|       |       |       |\n'+
'+-------+-------+-------+')

def instructions():
    print(
    '+------------------------------------------------+'+
    '\nINSTRUCTIONS\n'+
    '+------------------------------------------------+'+
    '\nUsing a numpad as a reference, place your X or O'+
    '\non the board using the numbers 1-9 corresponding'+
    '\nto the grid from left to right and top to bottom.'+
    '\nThe player who chooses X will start the game.'+
    '\n+------------------------------------------------+\n')

placement = [' ']*9
x = True
o = False
player_1 = ' '

#outputs blank board and instructions. Player 1 ch
def player_start():
    welcome()
    board(placement)
    instructions()
    global player_1
    try:
        player_type = input('\nWould you like to be X or O? ')
        if player_type.lower() == 'x':
            print('\nOkay, Player 1 will go first as X')
            print ('\nPlayer 1, ') 
            player_1 = 'x'   
        elif player_type.lower() == 'o':
            print('Okay, Player 2 will go first as X')
            print ('\nPlayer 2, ')
            player_1 = 'o'
        else:
            raise ValueError
    except ValueError:
        print('Try that again. Please enter X or O to start the game: ')

#plays game while no winners detected
def player_input():
    global x
    global o
    global placement
    try:
        while x == True or o == True:
            try:
                while x:
                    place_x = int(input('Where would you like to place your X? '))
                    if 1 <= place_x <= 9:
                        try:
                            if placement[place_x-1] == ' ':
                                placement[place_x-1] = 'X'
                                board(placement)
                                x = False
                                o = True
                                win_game(placement)
                            else:
                                raise ValueError
                        except ValueError:
                            print('Try that again. Someone has already played there.')
                    else:
                        x = True
                        raise ValueError
            except ValueError:
                print('Try again. Please enter a number 1-9.')
            try:
                while o:
                    place_o = int(input('Where would you like to place your O? '))
                    if 1 <= place_o <= 9:
                        try:
                            if placement[place_o-1] == ' ':
                                placement[place_o-1] = 'O'
                                board(placement)
                                o = False
                                x = True
                                win_game(placement)
                            else:
                                raise ValueError
                        except ValueError:
                            print('Try that again. Someone has already played there.')
                    else:
                        o = True
                        raise ValueError
            except ValueError:
                print('Try again. Please enter a number 1-9.')
    except ValueError:
            print('Try again.')

def win_game(p):
    global x
    global o
    global placement
    #winning tuple patterns
    wins = (
    (p[0], p[1], p[2]),
    (p[3], p[4], p[5]),
    (p[6], p[7], p[8]),
    (p[2], p[5], p[8]),
    (p[1], p[4], p[7]),
    (p[0], p[3], p[6]),
    (p[6], p[4], p[2]),
    (p[0], p[4], p[8])
    )
    #checks if someone won, if not continues playing
    if ('X','X','X') in wins:
        x = False
        o = False
        if player_1 == 'x':
            print('Player 1 wins as X!')
        else:
            print('Player 2 wins as X!')
        placement = [' ']*9
        play_again()
    elif ('O','O','O') in wins:
        x = False
        o = False
        if player_1 == 'x':
            print('Player 2 wins as O!')
        else:
            print('Player 1 wins as O!') 
        placement = [' ']*9
        play_again()
    elif ' ' not in placement:
        x = False
        o = False
        print("It's a tie!")
        placement = [' ']*9
        play_again()

    else:
        pass

#clears board if player wants a rematch
def play_again():
    global x
    while x == False and o == False:
        try:
            again = input('Do you want a rematch? Y/N: ')
            if again.lower() == 'y' or again.lower() == 'yes':
                x = True
                board(placement)
                break
            elif again.lower() == 'n' or again.lower() == 'no':
                print('Thanks for Playing!')
                break
            else:
                raise ValueError
        except ValueError:
            print('Try that again. Please enter Y for yes or N for no.')


player_start()
player_input()