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
        if k in list_dices:
            return True
        else:
            return False

    def decide(self, score_total, score, list_dices, fails):
        Next = None
        list_back = []
        if list_dices.sort() == [i for i in range(1, 7)]:
            list_back = list_dices
            Next = True
        elif self.k_v_listu(len(list_dices), list_dices) != None:
            list_back = list_dices
            Next = True
        else:
            Next = False

        return Next, list_back