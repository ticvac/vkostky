from environment import Environment, Agent
from random import randint

class Agent_1(Agent):

    def kolik_obsahuje_k(self,k,list_dices):
        count = 0
        while True:
            if k in list_dices:
                count += 1
                list_dices.remove(k)
            else:
                return count


    def decide(self, score, score_total, list_dices, fails):
        Next = False
        list_back = []
        if list_dices.sort() == [i for i in range(1, 7)]:
            print('a')
            list_back = list_dices
            Next = True
        if 1 in list_dices:
            list_back = [1]
            Next = True
        elif 5 in list_dices:
            list_back = [5]
            Next = True
        if score >= 350:
            return [False, list_back]

        return [Next, list_back]

agent = Agent_1()
env = Environment()

score = 0
for i in range(1000):
    score += env.play_one_turn(agent, 0, 0)
print(score/1000)