"""
War Game
------------
Further development will be to set number of games and record data
no of games / rounds played / wins vs losses
report finding in a table with pandas and plot to graphic using plotly
"""
import random
import os
import time

# CLASSES
class card():
    def __init__(self,card_name):
        #unpack the tuple values into 2 variables
        self.suit,self.rank = card_name
        # use the supplied value to index further values
        self.value =  card_values[self.rank]
        self.prelogo = card_prelogo[self.rank]
        self.logo = card_suits[self.suit]
        self.name = f'{self.rank} of {self.suit}'

    def __str__(self):
        return f' ________\n|        |\n| {self.prelogo:<2} {self.logo}   | {self.name}\n|        |\n|________|'

class deck():
    def __init__(self):
        self.cards = []

        for suit in card_suits:
            for rank in card_ranks:
                # Create each card and add to the deck
                # pass the card class a tuple with the required variable values
                this_card = card((suit,rank))
                self.cards.append(this_card)
    
    def __len__(self):
        # This should return 52 at the start (no jokers)
        return len(self.cards)

    def __str__(self):
        return (f'Deck of {len(self.cards)} cards')

    def shuffle(self):
        return random.shuffle(self.cards)

    def deal_one(self):
        # remove and return the last card of the deck
        return self.cards.pop()

class player():
    def __init__(self,name):
        self.name = name
        self.hand = []

    def remove_one(self):
        # remove and return the first card in the players hand
        return self.hand.pop(0)

    def add_cards(self,new_cards):
        if type(new_cards) == type([]):
            self.hand.extend(new_cards)
        else:
            self.hand.append(new_cards)

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.hand)

# FUNCTIONS
def clear():
    # clear the terminal display
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def new_game():
    clear()
    # Create a new deck and shuffle it for the game
    game_deck = deck()
    game_deck.shuffle()
    print('\n*** WAR IS UPON US ***\n')
    # Capture names and create players
    players = []
    i = 1
    while i < 3:
        try:
            name = input(f'Enter player {i} name : ')
            if len(name) <= 2:
                print('Name must be 3 charactors or longer')
                continue
            players.append(player(name))
            i += 1
        except:
            print('Name must have min 3 charactors')
    # As long as there are cards keep dealing 1 card to alternating players
    cards = len(game_deck)
    x = 1
    while x <= cards:
        card = game_deck.deal_one()
        if x%2==0:
            players[0].add_cards(card)
        else:
            players[1].add_cards(card)
        x += 1
    # New Game Setup is now complete and we ready to play
    p1 = players[0]
    p2 = players[1]
    rounds = 1

    print(f'\n{p1.name} : {len(p1.hand)} vS {len(p2.hand)} : {p2.name}\n')
    input('ENTER to play cards')
    
    while len(p1.hand) > 0 and len(p2.hand) > 0:
        try:
            round_cards = []
            clear()
            print(f'\n{p1.name} : {len(p1.hand)} vS {len(p2.hand)} : {p2.name}\n')
            print(f'round {rounds}')
            card1 = p1.remove_one()
            round_cards.append(card1)
            card2 = p2.remove_one()
            round_cards.append(card2)
            for item in round_cards:
                print(item)
                print('')
                time.sleep(slow)
            
            if card1.value == card2.value:
                war_card_list = [card1,card2]
                war_card_values = []

                # Need to check if each player has enough cards to enter a war
                # If not that player looses all cards and the game
                if len(p1.hand) < 3:
                    for card in p1.hand:
                        war_card_list.append(p1.remove_one())
                elif len(p2.hand) < 3:
                    for card in p2.hand:
                        war_card_list.append(p2.remove_one())

                else:
                    for p in players:
                        clear()
                        x = 0 # Counter for 3 war cards
                        print(f'\n3 cards {p.name} will take to war\n')
                        while x < 3:
                            next_card = p.remove_one()
                            print(next_card)
                            time.sleep(slow)
                            war_card_list.append(next_card)
                            war_card_values.append(next_card.value)
                            x += 1

                    p1_war_cards = war_card_values[:3]
                    p2_war_cards = war_card_values[3:]

                    war = True
                    while war:
                        if max(p1_war_cards) > max(p2_war_cards):
                            # p1 wins
                            print(f'\n{p1.name} wins the war!\n')
                            p1.add_cards(war_card_list)
                            time.sleep(slow)
                            war = False
                        elif max(p1_war_cards) < max(p2_war_cards):
                            # p2 wins
                            print(f'\n{p2.name} wins the war!\n')
                            p2.add_cards(war_card_list)
                            time.sleep(slow)
                            war = False                    
                        else:
                            # that card is a draw
                            # find and remove the highest card and compare the second highest card
                            a = max(p1_war_cards)
                            p1_war_cards.remove(a)
                            b = max(p2_war_cards)
                            p2_war_cards.remove(b)

                        # here we need to code what to do if all 3 war cards are also equal 

            elif card1.value > card2.value:
                print(f'{p1.name} has won this battle!')
                p1.add_cards(round_cards)
                #input('ENTER to end battle')
                time.sleep(slow)
            else:
                print(f'{p2.name} has won this battle!')
                p2.add_cards(round_cards)
                #input('ENTER to end battle')
                time.sleep(slow)

            rounds += 1

        except Exception as e:
            print('Error in card play : {}'.format(e))
            input('ENTER to continue')

    
    if len(p1.hand) == 0:
        clear()
        print('**********************************')
        print(f'{p2.name} is the winner!!')
        print(f'{rounds} rounds were played')
        print('**********************************')
        input('ENTER to end the game')
    elif len(p2.hand) == 0:
        clear()
        print('**********************************')
        print(f'{p1.name} is the winner!!')
        print(f'{rounds} rounds were played')
        print('**********************************')
        input('ENTER to end the game')
        
def rules():
    clear()
    print('\n*** THIS IS WAR RULES ***\n')
    print('War is a card game played between 2 players\n')
    # Pause moments added for smaller text digestion
    input('press ENTER to continue\n')
    print('1 - A deck of 52 cards is shuffles and delt evenly between the players')
    print('2 - Each player presents his/her first card - this is a "battle"')
    print('3 - The cards are compard and the larger card will win the "battle"\n')
    # Pause moments added for smaller text digestion
    input('press ENTER to continue\n')
    print('4 - The player that won the "battle" adds those cards to their own hand')
    print('5 - Ace is lowest[1] and King is highest[13]')
    print('6 - If the cards are of equal value then this is "War"\n')
    # Pause moments added for smaller text digestion
    input('press ENTER to continue\n')
    print('7 - During "War" each player presents 3 cards from the top of their hand')
    print('8 - There are now 8 cards in play')
    print('9 - The largest unequaled card wins the "War" and that player adds all 8 cards to their hand')
    print('10 - The winner is the player with all the cards')
    # Pause moments added for smaller text digestion
    input('press ENTER to continue')

# VARIABLES
card_suits = {'Hearts':'\U00002665','Spades':'\U00002660','Diamonds':'\U00002666','Clubs':'\U00002663'}
card_values = {'Ace':1,'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':11,'Queen':12,'King':13}
card_prelogo = {'Ace':'A','Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':'J','Queen':'Q','King':'K'}
card_ranks = ('Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King')
slow = 0 # set the running speed of the game


# MAIN
def menu1():
    using_menu1 = True
    menu1_list = ['New Game','Rules']
    while using_menu1:
        clear()
        print('\n*** THIS IS WAR ***\n')
        for index,item in enumerate(menu1_list):
            print(f'[{index}] - {item}')
        print('[999] - EXIT\n')
        try:
            op = int(input('--> : '))
            if op == 999:
                print('Good Bye')
                using_menu1 = False
            elif op == 0:
                new_game()
            elif op == 1:
                rules()
            else:
                print('Invalid Selection')
        except:
            print('Only numbers may be entered')

if __name__ == '__main__':
    menu1()