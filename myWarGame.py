import random
import sys

#Usage & user inputs
NUM_ARGS = 2
USAGE = 'Usage: python myWarGame.py <User Name>\nEg: python myWarGame.py Batman'

# Restrict number of rounds to 10,000
# to avoid undeterministic rounds
MAX_ROUNDS = 10000


'''
This is Deck class, used for creating the playing deck,
shuffling the cards, dividing the cards and comparing card
face values to determine winner of the round.
'''
class Deck():
    Diamond = 1
    Heart = 2
    Spade = 3
    Club = 4
    SUITE = [Diamond, Heart, Spade, Club]

    def __init__(self):
        self.cards = []
        self.cards = [(suite, value) for suite in Deck.SUITE for value in range(2,15)]

    def shuffle(self):
        random.shuffle(self.cards, random.random)

    def divideCards(self):
        self.shuffle()
        return (self.cards[:26], self.cards[26:])

    #Compare player's top cards
    @staticmethod
    def compareCards(userCard, compCard):
        if userCard[1] > compCard[1]:
            return True
        else:
            return False

'''
This is Player class, used to initiate players and their decks.
Also facilitates methods to retrieve top cards, get number of 
cards in user's deck, adding winning cards to bottom of deck and 
provide Cards during a 'War' situation
'''
class Player():

    def __init__(self, name, deck):
        self.name = name
        self.deck = deck

    # Player play card from top of deck
    def playCard(self):
        return self.deck.pop(0)

    def getTopCard(self):
        return self.playCard()

    def getNumCards(self):
        return len(self.deck)

    # Player wins & adds Winning card
    # to bottom of their deck
    def addCard(self, addedCards):
        self.deck.extend(addedCards)

    def giveWarCard(self):
        warCard = []
	# Check if player can place 2 cards. 
	# One facedown & One face up
        if self.getNumCards() < 2:
            return self.deck
        else:
            for give in range(2):
                warCard.append(self.getTopCard())
        return warCard

    def handsNotEmpty(self):
        return (len(self.deck) != 0)

'''
This is warGame class, which initiates the game and contains
method to run the game. It handles each dealing round and 'War' situations.
Also takes care of Multi-war scenario and determines the game winner.
'''
class warGame():

    def __init__(self):
        self.roundsCount = 0
        self.warRoundsCount = 0

    def playGame(self, name):
        deck = Deck()
        userDeck, computerDeck = deck.divideCards()
        userName = name
        comp = Player("Computer", computerDeck)
        user = Player(userName, userDeck)

        while user.handsNotEmpty() and comp.handsNotEmpty() and self.roundsCount < MAX_ROUNDS:
            self.roundsCount += 1

            tableCards = []
            userCard = user.playCard()
            compCard = comp.playCard()

            # Add cards to table 
            tableCards.append(userCard)
            tableCards.append(compCard)
                

            # War scenario
            if userCard[1] == compCard[1]:

                uC, cC = userCard[1], compCard[1]

                # Now check for multi-war scenario
                # Check for tie & if yes, add cards 
                # to table until tie breaks or one of
                # the players' deck gets exhausted
                while(uC == cC):
                    self.warRoundsCount += 1

                    # Add cards to top of table
                    userWarCards = user.giveWarCard()
                    compWarCards = comp.giveWarCard()
                    tableCards = userWarCards + tableCards
                    tableCards = compWarCards + tableCards
                    try:
                        uC, cC = userWarCards[0][1], compWarCards[0][1]
                    except IndexError:
                        # One of players' deck is exhausted
                        break

                # Last card scenario - If a player does 
                # not have cards to play War,the opponent wins
                if(len(userWarCards) >= 1 and len(compWarCards) >= 1):

                    # Compare value and add cards to player's deck
                    if deck.compareCards(userWarCards[0], compWarCards[0]):
                        user.addCard(tableCards)
                    else:
                        comp.addCard(tableCards)
                else:
                    # Victory to opponent
                    break

            else:
                # Non-War scenario
                if deck.compareCards(userCard, compCard):
                    user.addCard(tableCards)
                else:
                    comp.addCard(tableCards)

        if (user.getNumCards() > comp.getNumCards()):
            print("%s won the game of 'War'" %userName)
        else:
            print("Computer won the game of 'War'")

'''
Driver function: main()
Verifies program usage, fetches user name from 
commandline and intiates the game using warGame class
'''
def main():

    numInputs = len(sys.argv)

    if numInputs != NUM_ARGS:
        print(USAGE)
        return

    userName = sys.argv[1]
    game = warGame()
    game.playGame(userName)

    print("# of rounds: %d" % (game.roundsCount))
    print("# of war rounds: %d" % (game.warRoundsCount))


if __name__ == "__main__":
    main()
