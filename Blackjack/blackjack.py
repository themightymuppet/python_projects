import random
import time


class Card:
    # class to define single card
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def show(self):
        # print single card
        print(f'{self.suit}{self.rank}')

    def __repr__(self):
        return self.suit + self.rank

# example tests using card class
# mycard = Card(suit = 'Spades',rank = '5')
# print(mycard.suit)
# print(mycard.rank)

class Deck:
    # class to define full 52 card deck
    suits = ['♥︎','♦︎','♣︎','♠︎']
    ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    cards = []

    def __init__(self):
        # default build deck, auto build on initialize
        self.build()

    def build(self):
        # for loop to create a list of 52 cards for each suit/rank
        for s in self.suits:
            for r in self.ranks:
                self.cards.append(Card(s,r))
        return self.cards

    def show(self):
        # reveal deck
        for c in self.cards:
            c.show()

    def shuffle(self):
        # grab random integer within the length of remaining cards and shuffle self.cards
        for i in range(len(self.cards)):
            r = random.randint(0,i)
            #swap with card in random generated int position
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def draw(self):
        # draw card and remove from deck(self.cards)
        return self.cards.pop()

    def __len__(self):
        # magic method to define current length of deck
        return len(self.cards)

    def __repr__(self):
        # magic method to print/represent current deck
        return self.cards

    def __del__(self):
        # magic method to clear deck and restart
        while len(self.cards)-1 > 0:
            self.cards.pop()
        self.build()

# class to define player moves
class Player:
    def __init__(self,name):
        self.name = name
        self.hand = [] #creates empty hand
        
    def draw(self, deck):
        # draw card using deck.draw()
        # remove card from deck
        # add to hand
        self.hand.append(deck.draw())
        return self

    def showHand(self):
        # show cards in hand
        for card in self.hand:
            card.show()
        
    def handCount(self):
        return self.hand

    def __len__(self):
        return len(self.hand)
    
    def __repr__(self):
        return self.hand

# redundant class to bandaid issues with
# multi-player instance
# will revist later :) 
class Dealer:
    def __init__(self,name='Dealer'):
        self.name = name
        self.hand = []
        # self.value = 0

    def draw(self, deck):
        self.hand.append(deck.draw())
        return self

    def showHand(self):
        for card in self.hand:
            card.show()

    def __len__(self):
        return len(self.hand)

    def __repr__(self):
        return self.hand

#global settings, initiate player
print(
" W E L C O M E   T O   B L A C K J A C K \n" +
"          _____\n" +
"         |A .  | _____\n" +
"         | /.\ ||A ^  | _____\n" +
"         |(_._)|| / \ ||A _  | _____\n" +
"         |  |  || \ / || ( ) ||A_ _ |\n" +
"         |____V||  .  ||(_'_)||( v )|\n" +
"                |____V||  |  || \ / |\n" +
"                       |____V||  .  |\n" +
"                              |____V|\n")
player_name = input("Hello player 1, what's your name? ")

def deal():
    deck = Deck()
    deck.shuffle()

    # players
    p = Player(player_name)
    d = Dealer()
    print('\n\nOkay, dealing the cards.')
    time.sleep(1)

    # dealers starting hand
    # draws a hidden card after show hand
    d.draw(deck)
    print(f'\n\nDealer: ')
    d.showHand()
    d.draw(deck)

    #players starting hand
    p.draw(deck)
    p.draw(deck)
    print(f'\nYour hand: ')
    p.showHand()
    turn = 'player'
    while turn == 'player':
        p_sum = 0
        p_hand = []
        p_hand.append(p.hand)
        hitme = input('Do you want to Hit or Stay? ')
        if hitme.lower() == 'hit' or hitme.lower() == 'h':
            # if hit, draw a card, show hand, and count
            p.draw(deck)
            p.showHand()
            for s,r in enumerate(p_hand):
                for x, y in enumerate(r):
                    if y.rank == 'J' or y.rank == 'Q' or y.rank == 'K':
                         p_sum += 10
                    elif y.rank == 'A':
                        if p_sum >= 11:
                            p_sum += 1
                        else:
                            p_sum += 10
                    else:
                        p_sum += int(y.rank)
            if p_sum > 21:
                print(f'{p_sum} - Bust!')
                turn = 'dealer'
            elif p_sum == 21:
                print(f'{p_sum} - Blackjack! {player_name} wins.')
                turn = 'End Game'
                return p_sum
            else:
                print(f'{p_sum}')
                continue
        elif hitme.lower() == 'stay' or hitme.lower() == 's':
            # if stay, count cards and set turn to dealer
            for s,r in enumerate(p_hand):
                for x, y in enumerate(r):
                    if y.rank == 'J' or y.rank == 'Q' or y.rank == 'K':
                         p_sum += 10
                    elif y.rank == 'A':
                        if p_sum >= 11:
                            p_sum += 1
                        else:
                            p_sum += 10
                    else:
                        p_sum += int(y.rank)
            turn = 'dealer'
            print(f"{turn}'s turn")
            break
        else:
            print('Try again, please enter hit or stay.')
    # play dealers hand
    print(f'{p_sum}\n')
    print("\nDealer's Turn")
    while turn == 'dealer':
        d_sum = 0
        d_hand = []
        d_hand.append(d.hand)
        print(f"\n\nDealer's Hand: ")
        d.showHand()
        if len(d_hand) != 0:
            # count cards
            for a,b in enumerate(d_hand):
                for w, z in enumerate(b):
                    if z.rank == 'J' or z.rank == 'Q' or z.rank == 'K':
                        d_sum += 10
                    elif z.rank == 'A':
                        if d_sum >= 11:
                            d_sum += 1
                        else:
                            d_sum += 10
                    else:
                        d_sum += int(z.rank)
        if d_sum <= 15:
            # if card count is <= 15, hit.
            d.draw(deck)
            print(f"\n\nDealer hits.\nDealer's Hand: ")
            time.sleep(1)
            d.showHand()
        elif 15 < d_sum <= 21 and d_sum < p_sum:
            d.draw(deck)
            print(f"\n\nDealer hits.\nDealer's Hand: ")
            time.sleep(1)
            d.showHand()
        elif d_sum < p_sum and p_sum <= 21:
            print(f'{d_sum} - {player_name} Wins.')
            turn = 'End Game'
        elif p_sum > d_sum and p_sum <= 21:
            print(f'{d_sum} - {player_name} Wins.')
            turn = 'End Game'
        elif 15 < d_sum <=21 and d_sum > p_sum:
            print(f'{d_sum} - Dealer Wins.')
            turn = 'End Game'
        elif d_sum == p_sum:
            print(f'{d_sum} - Tie Game.')
            turn = 'End Game'
        elif d_sum > p_sum and d_sum <= 21 :
            print(f'{d_sum} - Dealer Wins.')
            turn = 'End Game'
        elif d_sum > 21 and p_sum > 21:
            print(f'{d_sum} - Dealer busts too. Tie Game.')
            turn = 'End Game'
        elif d_sum > 21 and p_sum < 21:
            print(f'{d_sum} - Bust! {player_name} wins.')
            turn = 'End Game'
        else:
            break

def play_again():
    again = input("Rematch? Y/N: ")
    if again.lower() == 'y' or again.lower() == 'yes':
        # restart class instances and play again
        deal()
        play_again()
    elif again.lower() == 'n' or again.lower() == 'no':
        # end game
        print('Thanks for playing!')
    else:
        print("I didn't quite get that. Please enter Y/N to play again.")



deal()
play_again()