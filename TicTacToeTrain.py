
import random as rand
import csv


Q_TABLE = {} #{"State":{"Move":Reward}}

LEARNING_RATE = 0.05
DISCOUNT = 0.5


class TicTacToeTrain:
    def __init__(self):
        self.state = [["","",""],["","",""],["","",""]]
        self.done = False
        self.turn = True
        self.row = 0
        self.column = 0
    
    def Game(self):
        while True:
            while self.turn:
                self.row, self.column = AI(self.state).Train_Move()
                self.moves = [self.row, self.column]
                self.x_state = [x[:] for x in self.state]
                self.state[self.row][self.column] = "X"
                self.done = Check_Win(self.state)
                if self.done == True:
                    AI(self.x_state).Reward_Win_Lose_Draw("win", self.moves)
                    return
                else:
                    self.done = Check_Draw(self.state)
                    if self.done == True:
                        AI(self.x_state).Reward_Win_Lose_Draw("draw", self.moves)
                        return
                self.turn = False
                        
            while not(self.turn) and not(self.done):
                moves = Check_Moves(self.state)
                move = rand.choice(moves)
                row = move[0]
                column = move[1]
                self.state[row][column] = "O"
                self.done = Check_Win(self.state)
                if self.done == True:
                    AI(self.x_state).Reward_Win_Lose_Draw("lose", self.moves)
                    return
                else:
                    self.done = Check_Draw(self.state)
                    if self.done == True:
                        AI(self.x_state).Reward_Win_Lose_Draw("draw", self.moves)
                        return
                    else:
                        AI(self.x_state).Reward(self.state, self.moves)
                self.turn = True
        
class AI:
    def __init__(self, state):
        self.state = [item[:] for item in state]

    def Train_Move(self):
        self.moves = []
        for x in Q_TABLE[str(self.state)].keys():
            if x != "x":
                self.moves.append([int(x[1]),int(x[4])])
        self.move = rand.choice(self.moves)
        self.row = self.move[0]
        self.column = self.move[1]
        return self.row, self.column
    
    def Choose_Move(self):
        q_table = {}
        with open("TicTacToeQTable.csv", newline="") as file:
            f = csv.reader(file)
            for line in f:
                q_table.update({line[0]:{}})
                for m in range(1,len(line),2):
                    if line[m] == "x":
                        move_list = line[m]
                    else:
                        move_list = [int(line[m][1]), int(line[m][4])]
                    q_table[line[0]].update({str(move_list):line[m+1]})
        max_score = 0
        for x in q_table[str(self.state)]:
            if int(q_table[str(self.state)][x]) > max_score:
                max_score = int(q_table[str(self.state)][x])
                max_score_move = [int(x[1]), int(x[4])]
        return max_score_move[0], max_score_move[1]
                
    def Reward(self, next_state, move):
        self.move = move
        self.next_state = [x[:] for x in next_state]
        values = []
        for value in Q_TABLE[str(self.next_state)].values():
            values.append(float(value))
        reward = float(Q_TABLE[str(self.state)][str(self.move)]) + LEARNING_RATE*(DISCOUNT * max(values) - float(Q_TABLE[str(self.state)][str(self.move)]))
        Q_TABLE[str(self.state)].update({str(self.move):reward})
    
    def Reward_Win_Lose_Draw(self, outcome, move):
        self.move = move
        if outcome == "win":
            reward = float(Q_TABLE[str(self.state)][str(self.move)]) + LEARNING_RATE*(DISCOUNT * 100 - float(Q_TABLE[str(self.state)][str(self.move)]))
        elif outcome == "lose":
            reward = float(Q_TABLE[str(self.state)][str(self.move)]) + LEARNING_RATE*(DISCOUNT * -100 - float(Q_TABLE[str(self.state)][str(self.move)]))
        else:
            reward = float(Q_TABLE[str(self.state)][str(self.move)]) + LEARNING_RATE*(DISCOUNT * -20 - float(Q_TABLE[str(self.state)][str(self.move)]))
        Q_TABLE[str(self.state)].update({str(self.move):reward})


def Train():
    with open("TicTacToeQTable.csv", newline="") as file:
        f = csv.reader(file)
        for line in f:
            Q_TABLE.update({line[0]:{}})
            for m in range(1,len(line),2):
                if line[m] == "x":
                    move_list = line[m]
                else:
                    move_list = [int(line[m][1]), int(line[m][4])]
                Q_TABLE[line[0]].update({str(move_list):line[m+1]})
                
    for _ in range(1000):
        TicTacToeTrain().Game()
        
    with open("TicTacToeQTable.csv", "w", newline="") as file:
        f = csv.writer(file)
        for state, move_dict in Q_TABLE.items():
            move_score = []
            for move, score in move_dict.items():
                move_score.append(move)
                move_score.append(score)
            f.writerow([state] + move_score)


def Check_Moves(state):
    moves = []
    for rows in range(3):
        for columns in range(3):
            if state[rows][columns] == "":
                moves.append([rows,columns])
    return moves

def Check_Win(state):
    for rows in range(3):
        if state[rows][0] == state[rows][1] and state[rows][0] == state[rows][2] and state[rows][0] != "":
            return True
    
    for columns in range(3):
        if state[0][columns] == state[1][columns] and state[0][columns] == state[2][columns] and state[0][columns] != "":
            return True
    
    if state[0][0] == state[1][1] and state[0][0] == state[2][2] and state[0][0] != "":
        return True
    
    if state[0][2] == state[1][1] and state[0][2] == state[2][0] and state[0][2] != "":
        return True
        
    return False

def Check_Draw(state):
    for rows in range(3):
        for columns in range(3):
            if state[rows][columns] == "":
                return False
    return True

def Create_File():
    print("Creating File ... ")
    state = [['','',''],['','',''],['','','']]
    states_done = []
    states_need_to_do = {"X":[[['','',''],['','',''],['','','']]], "O":[]}
    all_moves = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    done = False
    with open("TicTacToeQTable.csv", "w", newline="") as file:
        f = csv.writer(file)
        Turn = "X"
        while not(done):
            moves = Check_Moves(state)
            row = [state]
            for m in range(len(all_moves)):
                next_state = [x[:] for x in state]
                
                if all_moves[m] in moves:
                    row.append(all_moves[m])
                    
                if Turn == "X":
                    if all_moves[m] in moves:
                        next_state[all_moves[m][0]][all_moves[m][1]] = "X"
                        win = Check_Win(next_state)
                        draw = Check_Draw(next_state)
                    else:
                        win = False
                        draw = False
                        
                    if win:
                        row.append(0)
                    elif draw:
                        row.append(0)
                    elif all_moves[m] in moves:
                        row.append(0)
                        states_need_to_do["O"].append(next_state)
                          
                else:
                    if all_moves[m] in moves:
                        next_state[all_moves[m][0]][all_moves[m][1]] = "O"
                        win = Check_Win(next_state)
                        draw = Check_Draw(next_state)
                    else:
                        win = False
                        draw = False
                    
                    win = Check_Win(next_state)
                    draw = Check_Draw(next_state)
                    if win:
                        row.append(0)
                    elif draw:
                        row.append(0)
                    elif all_moves[m] in moves:
                        row.append(0)
                        states_need_to_do["X"].append(next_state)
                
            if Turn == "X":
                f.writerow(row)
            states_done.append(state)
            states_need_to_do[Turn].remove(state)
            if (len(states_need_to_do["X"]) == 0) and (len(states_need_to_do["O"]) == 0):
                done = True
            else:
                if len(states_need_to_do["X"]) >= len(states_need_to_do["O"]):
                    state = states_need_to_do["X"][0]
                    Turn = "X"
                else:
                    state = states_need_to_do["O"][0]
                    Turn = "O"
            
        print("File Created")

if __name__ == "__main__":
    #Create_File()
    for x in range(1000):
        print("Game:", x+1)
        Train()
    print("All Done!")










