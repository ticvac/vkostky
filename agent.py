from environment import Environment, Agent
from random import randint

class Agent_0(Agent):
    def decide(self, score, score_total, list_dices, fails):
        next_turn = False
        list_back = []
        if sorted(list_dices) == [i for i in range(1, 7)]:
            list_back = list_dices
        
        return [next_turn, list_back]

class Agent_1(Agent):
    def decide(self, score, score_total, list_dices, fails):
        next_turn = False
        list_back = []
        if sorted(list_dices) == [i for i in range(1, 7)]:
            list_back = list_dices
            next_turn = True
        elif 1 in list_dices:
            list_back = [1]
            next_turn = True
        elif 5 in list_dices:
            list_back = [5]
            next_turn = True
        if score >= 350:
            return [False, list_back]

        return [next_turn, list_back]

class Agent_2(Agent):
    def decide(self, score, score_total, list_dices, fails):
        list_back = []
        next_turn = False

        if sorted(list_dices) == [i for i in range(1, 7)]:
            list_back = list_dices
            next_turn = True
        
        list_back = [1 for i in range(list_dices.count(1))]
        list_back += [5 for i in range(list_dices.count(5))]

        for x in [2,3,4,6]:
            if list_dices.count(x) >= 3:
                list_back += [x for i in range(list_dices.count(x))]
        
        if env.calculate_score(list_back) < 350:
            next_turn = True

        return [next_turn, list_back]

class Agent_3(Agent):
    def decide(self, score, score_total, list_dices, fails):
        list_back = []
        next_turn = False

        if sorted(list_dices) == [i for i in range(1, 7)]:
            list_back = list_dices
            next_turn = True
        
        list_back = [1 for i in range(list_dices.count(1))]
        list_back += [5 for i in range(list_dices.count(5))]

        for x in [2,3,4,6]:
            if list_dices.count(x) >= 3:
                list_back += [x for i in range(list_dices.count(x))]
        
        if env.calculate_score(list_back) < self.avg_score(len(list_dices)):
            if list_dices.count(1) >= 1:
                list_back = [1]
                next_turn = True
            elif list_dices.count(5) >= 1:
                list_back = [5]
                next_turn = True
            else:
                next_turn = True

        if env.calculate_score(list_back) < 350:
            next_turn = True

        return [next_turn, list_back]

class Agent_3_1(Agent):
    def decide(self, score, score_total, list_dices, fails):
        list_back = []
        next_turn = False

        if sorted(list_dices) == [i for i in range(1, 7)]:
            list_back = list_dices
            next_turn = True
        
        list_back = [1 for i in range(list_dices.count(1))]
        list_back += [5 for i in range(list_dices.count(5))]

        for x in [2,3,4,6]:
            if list_dices.count(x) >= 3:
                list_back += [x for i in range(list_dices.count(x))]
        
        if env.calculate_score(list_back) < self.avg_score(len(list_dices)):
            if list_dices.count(1) >= 1:
                if len(list_dices) == 6:
                    list_back = [1 for i in range(list_dices.count(1))]
                else:
                    list_back = [1]
                next_turn = True
            elif list_dices.count(5) >= 1:
                list_back = [5]
                next_turn = True
            else:
                next_turn = True

        if env.calculate_score(list_back) < 350:
            next_turn = True

        return [next_turn, list_back]

env = Environment()
agent = Agent_3_1()

score = 0
nuly = 0

opakovani = 10000

for i in range(opakovani):
    score += env.play_one_turn(agent, 0, 0)
    if env.play_one_turn(agent, 0, 0) == 0:
        nuly += 1
print(score/opakovani)
print(nuly/opakovani)