from environment import Environment, Agent
from random import randint

class Agent_1(Agent):
    def k_v_listu(self, k, list_dices):
        m = [0 for i in range(6)]
        for i in range(1, 7):
            while True:
                if i in list_dices:
                    m[i - 1] += 1
                    list_dices.remove(j)
                else:
                    break
            if max(m) >= k:
                return m.index(max(m)) + 1, max(m)
            else:
                return None, None

    def obsahuje_k(self,k,list_dices):
        for x in list_dices:
            if k == x:
                return True
        return False

    def decide(self, score, score_total, list_dices, fails):
        Next = False
        list_back = []
        """if list_dices.sort() == [i for i in range(1, 7)]:
            print('a')
            list_back = list_dices
            Next = True"""
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