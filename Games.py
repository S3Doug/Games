
import random as rand

from TicTacToeTrain import AI
 
CARDS = ['K','Q','J','T','9','8','7','6','5','4','3','2','A']
DECK = []
for suit in "DHCS":
    for card in range(len(CARDS)):
        DECK.append(suit+CARDS[card])


class BlackJack:
    def __init__(self, hand='', players=1, acescore=11):
        self.score = 0
        self.cut = 60 + rand.randint(0,15)
        self.acescore = acescore
        
        self.deck = []
        for _ in range(24):
            self.deck.extend(CARDS)
        rand.shuffle(self.deck)
        
        self.hand = hand
        self.players = players
        self.player_hands = []
        self.player_scores = []
        self.dealer_hand = ""
        self.dealer_score = 0
        
        self.bets = []
        self.player_pot = []
        for _ in range(self.players):
            self.bets.append(0)
            self.player_pot.append(0)
            
        self.turn = 0
        
    def Score(self):
        self.score = 0
        for h in self.hand:
            if h == "A":
                acechoice_invalid = True
                while acechoice_invalid:
                    print(f"Player {self.turn+1}: Your current score is {self.score}")
                    acechoice = input("Do you want to count this ace as 11 points or 1 point? ")
                    try:
                        acechoice = int(acechoice)
                        assert acechoice == 11 or acechoice == 1
                        if acechoice == 11:
                            self.score += 11
                            acechoice_invalid = False
                        else:
                            self.score += 1
                            acechoice_invalid = False
                    except:
                        print("Please input 11 or 1")

            elif h in "KQJT":
                self.score += 10
            else:
                self.score += int(h)
        
        if self.score > 21:
            self.score = -1
        
        return
    
    def Scorer(self):
        self.score = 0
        for h in self.hand:
            if h == "A":
                if self.acescore == 11:
                    self.score += 11
                else:
                    self.score += 1

            elif h in "KQJT":
                self.score += 10
            else:
                self.score += int(h)
        
        if self.score > 21:
            self.score = -1
        
        return self.score
    
    def Dealer_Score(self):
        while True:
            self.dealer_score = 0
            aces = 0
            for h in self.dealer_hand:
                if h == "A":
                    self.dealer_score += 11
                    aces += 1
                elif h in "KQJT":
                    self.dealer_score += 10
                else:
                    self.dealer_score += int(h)
            if (self.dealer_score >= 17) and (self.dealer_score <= 21):
                print(f"The Dealer's score is {self.dealer_score}.")
                return
            elif self.dealer_score > 21 and aces == 0:
                self.dealer_score = -1
                print(f"The Dealer went bust.")
                return
            elif self.dealer_score > 21 and aces > 0:
                while self.dealer_score > 21:
                    if aces > 0:
                        aces -= 1
                        self.dealer_score -= 10
                    else:
                        self.dealer_score = -1
                        print(f"The Dealer went bust.")
                        return
                return
                    
            elif self.dealer_score < 17:
                print(f"The Dealer's score is {self.dealer_score}. \nThey must hit.")
                self.Dealer_Hit()
            
    def Game(self):

        self.turn = 0
        while self.turn < self.players:
            self.player_pot[self.turn] = input(f"Player {self.turn+1}: How much money would you like to start with? ")
            try:
                self.player_pot[self.turn] = float(self.player_pot[self.turn])
                self.turn += 1
            except TypeError:
                if "$" in self.player_pot[self.turn] and (self.player_pot[self.turn].strip("$.").isnumeric()):
                    print("Input an amount without the dollar sign.")
                else:
                    print("Please input an amount with only numbers.")
                    
        while True:
            self.turn = 0
            while self.turn < self.players:
                self.bets[self.turn] = input(f"Player {self.turn+1}: You have ${self.player_pot[self.turn]:.2f} in your pot. How much would you like to bet? ($2.00-$500.00) ")
                try:
                    self.bets[self.turn] = float(self.bets[self.turn])
                    assert (self.bets[self.turn] <= 500) and (self.bets[self.turn] >= 2)
                    if self.bets[self.turn] > self.player_pot[self.turn]:
                        raise Exception
                    print(f"You bet ${self.bets[self.turn]:.2f}")
                    self.turn += 1
                except TypeError:
                    if "$" in self.bets[self.turn] and (self.bets[self.turn].strip("$.").isnumeric()):
                        print("Input a bet without the dollar sign.")
                    else:
                        print("Please bet with only numbers.")
                except AssertionError:
                    print("Please bet an amount between 2.00 and 500.00 dollars.")
                except:
                    print("Please bet an amount less than or equal to your pot.")
            
            for _ in range(self.players):
                self.player_hands.append("")
            
            for _ in range(2):
                self.Deal()
            
            self.turn = 0
            while self.turn < self.players:
                print(f"Player {(self.turn + 1)}: Your hand is {self.player_hands[self.turn]}")
                print(f"Dealer's Hand: {self.dealer_hand[0]} ?")
                self.hand = self.player_hands[self.turn]
                self.Score()
                print(f"Your hand's score is {self.score}")
                choice = input("Do you hit or stand? ")
                try:
                    assert choice in " hit Hit stand Stand "
                    if choice in " hit Hit ":
                        self.Hit()
                        print(f"Player {self.turn+1}: Your hand is now {self.player_hands[self.turn]}.")
                        self.hand = self.player_hands[self.turn]
                        self.Score()
                        if self.score == -1:
                            print("You went bust.")
                            self.player_pot[self.turn] -= self.bets[self.turn]
                            print(f"You now have ${self.player_pot[self.turn]} left in your pot.")
                            self.player_scores.append(self.score)
                            self.turn += 1  
                    else:
                        self.player_scores.append(self.score)
                        print(f"Player {self.turn+1}: Your final score is {self.player_scores[self.turn]}.")
                        self.turn += 1
                except:
                    print("That wasn't an expected input. Try again.")
                    
            self.Dealer_Turn()
            self.turn = 0
            remove_players = 0
            while self.turn < self.players:
                if self.player_scores[self.turn] > self.dealer_score:
                    self.player_pot[self.turn] += self.bets[self.turn]
                    print(f"Player {self.turn+1}: You beat the Dealer this round. Congratulations!")
                elif (self.player_scores[self.turn] < self.dealer_score) and (self.player_scores[self.turn] != -1):
                    self.player_pot[self.turn] -= self.bets[self.turn]
                    print(f"Player {self.turn+1}: You did NOT beat the Dealer this round.")
                else:
                    print(f"Player {self.turn+1}: You did NOT beat the Dealer this round.")
                
                print(f"You have ${self.player_pot[self.turn]} left in your pot.")
                if self.player_pot[self.turn] > 2:
                    play = input(f"Do you want to continue playing? (Y/N) ")
                    try:
                        assert play == "Y" or play == "y" or play == "N" or play == "n"
                        if play == "N" or play == "n":
                            remove_players += 1
                            self.player_pot.pop(self.turn)
                            print("Ok, goodbye")
                        self.turn += 1
                    except:
                        print("That's not the input that was expected. Try again")
                else: 
                    print(f"You do not have enough money left to continue betting. Goodbye")
                    remove_players += 1
                    self.player_pot.pop(self.turn)
                    self.turn += 1
            
            self.players -= remove_players
            
            if self.players == 0:
                return
            
            if len(self.deck) <= self.cut:
                self.Shuffle()
            
            self.Reset()
    
    def Deal(self):
        for p in range(self.players):
            card_index = rand.randrange(0,len(self.deck))
            self.player_hands[p] = self.player_hands[p] + self.deck[card_index]
            self.deck.remove(self.deck[card_index])
        card_index = rand.randrange(0,len(self.deck))
        self.dealer_hand += self.deck[card_index]
        self.deck.remove(self.deck[card_index])
        return
        
    def Hit(self):
        card_index = rand.randrange(0,len(self.deck))
        self.player_hands[self.turn] = self.player_hands[self.turn] + self.deck[card_index]
        self.deck.remove(self.deck[card_index])
        return
            
    def Dealer_Hit(self):
        card_index = rand.randrange(0,len(self.deck))
        self.dealer_hand += self.deck[card_index]
        self.deck.remove(self.deck[card_index])
        print(f"The Dealer's hand is {self.dealer_hand}")
        return
    
    def Dealer_Turn(self):
        print(f"The Dealer's hand is {self.dealer_hand}")
        self.Dealer_Score()
    
    def Shuffle(self):
        self.deck = []
        for _ in range(24):
            self.deck.extend(CARDS)
        rand.shuffle(self.deck)
        self.cut = 60 + rand.randint(1,15)
        
    def Reset(self):
        self.player_hands = []
        self.player_scores = []
        self.dealer_hand = ""
        self.bets = []
        for _ in range(self.players):
            self.bets.append(0)

class TicTacToe:
    def __init__(self):
        self.state = [["","",""],["","",""],["","",""]]
        self.not_win = True
        self.not_lose = True
        self.turn = True
        
    def Display(self):
        print(f"   |   |   \n{self.state[0][0]:^3}|{self.state[0][1]:^3}|{self.state[0][2]:^3}\n___|___|___")
        print(f"   |   |   \n{self.state[1][0]:^3}|{self.state[1][1]:^3}|{self.state[1][2]:^3}\n___|___|___")
        print(f"   |   |   \n{self.state[2][0]:^3}|{self.state[2][1]:^3}|{self.state[2][2]:^3}\n   |   |   \n")
        
    def Check_Win(self):
        for rows in range(3):
            if self.state[rows][0] == self.state[rows][1] and self.state[rows][0] == self.state[rows][2] and self.state[rows][0] != "":
                return True
        
        for columns in range(3):
            if self.state[0][columns] == self.state[1][columns] and self.state[0][columns] == self.state[2][columns] and self.state[0][columns] != "":
                return True
        
        
        if self.state[0][0] == self.state[1][1] and self.state[0][0] == self.state[2][2] and self.state[0][0] != "":
            return True
        
        
        if self.state[0][2] == self.state[1][1] and self.state[0][2] == self.state[2][0] and self.state[0][2] != "":
            return True
            
        return False
    
    def Game(self):
        while self.not_win and self.not_lose:
            self.Display()
            while not(self.turn):
                row, column = AI(self.state).Choose_Move()
                if self.state[row][column] == "":
                    self.state[row][column] = "X"
                    if self.Check_Win():
                        self.not_lose = False
                    self.turn = True
            if not(self.not_lose):
                break
            
            self.Display()
            while self.turn:
                row = input("What row would you like to mark? (1,2,3) > ")
                column = input("What column would you like to mark? (1,2,3) > ")
                try:
                    row = int(row)
                    column = int(column)
                    if row > 3 or row < 1 or column > 3 or column < 1:
                        raise Exception
                except:
                    print("Either your row or column isn't valid, try again.")
                else:
                    if self.state[row-1][column-1] == "":
                        self.state[row-1][column-1] = "O"
                        if self.Check_Win():
                            self.not_win = False
                        self.turn = False
                    else:
                        print("That spot has already been claimed, try again.")
                        
                    
        self.Display()
        if not(self.not_win):
            print("You Won!")
        else:
            print("You Lose")
        return
        


if __name__ == "__main__":
    TicTacToe().Game()
    #BlackJack().Game()
