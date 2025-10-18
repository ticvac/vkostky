from environment import Environment, Agent
from random import randint
from itertools import combinations
import matplotlib.pyplot as plt


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

        for x in [2, 3, 4, 6]:
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
            return [next_turn, list_back]

        list_back = [1 for i in range(list_dices.count(1))]
        list_back += [5 for i in range(list_dices.count(5))]

        for x in [2, 3, 4, 6]:
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

        if (score + env.calculate_score(list_back)) < 350:
            next_turn = True

        # print(next_turn, list_back, list_dices)
        return [next_turn, list_back]


class Agent_4(Agent):
    def decide(self, score, score_total, list_dices, fails, agresivita=100):
        list_back = []
        next_turn = False

        if sorted(list_dices) == [i for i in range(1, 7)]:
            list_back = list_dices
            next_turn = True

        list_back = [1 for i in range(list_dices.count(1))]
        list_back += [5 for i in range(list_dices.count(5))]

        for x in [2, 3, 4, 6]:
            if list_dices.count(x) >= 3:
                list_back += [x for i in range(list_dices.count(x))]

        prob = 1
        maximum = 1
        for i in range(1, len(list_back) + 1):
            for subset in combinations(list_back, i):
                if not env.check_if_can_keep(list_dices, list(subset)):
                    continue

                prob = self.histogram(6 - len(subset), 350 - (score + env.calculate_score(list(subset))))

                if prob < maximum:
                    maximum = prob
                    list_back = list(subset)

        # print(prob, maximum, list_dices, list_back)
        if (score + env.calculate_score(list_back)) < 350:
            next_turn = True

        return [next_turn, list_back]

class Agent_5(Agent):
    def decide(self, score, score_total, list_dices, fails):
        list_back = []
        next_turn = False

        if sorted(list_dices) == [i for i in range(1, 7)]:
            list_back = list_dices
            next_turn = True
            return [next_turn, list_back]

        list_back = [1 for i in range(list_dices.count(1))]
        list_back += [5 for i in range(list_dices.count(5))]

        for x in [2, 3, 4, 6]:
            if list_dices.count(x) >= 3:
                list_back += [x for i in range(list_dices.count(x))]

        if list_dices.count(1) >= 1 and env.calculate_score(list_back) < 100 + self.avg_score(len(list_dices) - 1):
            list_back = [1]
            next_turn = True
        elif list_dices.count(5) >= 1 and env.calculate_score(list_back) < 50 + self.avg_score(len(list_dices) - 1):
            list_back = [5]
            next_turn = True

        if (score + env.calculate_score(list_back)) < 350 or len(list_dices) - len(list_back) >= 5:
            next_turn = True
        else:
            next_turn = False
        if len(list_dices) - len(list_back) == 0:
            next_turn = True

        # print(next_turn, list_back, list_dices)
        return [next_turn, list_back]


def plot_graphs():
    p = [agent_5]
    names = ['agent_5']

    list_of_scores = [env.play_one_game(p[x], 10000) for x in range(len(p))]

    for i in range(len(list_of_scores)):
        plt.plot(list_of_scores[i])
        plt.savefig(names[i])
        plt.close()

def avg_game(iterace = 1000, agent = Agent_5):
    soucet = 0
    for j in range(iterace):
        soucet += len(env.play_one_game(agent, 10000))
        #print(j)
    print("Soucet agent" , agent , "  " , soucet/iterace)

def avg_turn(iterace = 10000, agent = Agent_5):
    score = 0
    nuly = 0

    for i in range(iterace):
        diff = env.play_one_turn(agent_5, 0, 0)
        score += diff

        if diff == 0:
            nuly += 1
    print(score/iterace)
    print(nuly/iterace)

def play_against_human(agent = Agent_5):
    agent_score = 0
    player_score = 0

    while True:
        dif = env.play_one_turn(agent_5, agent_score, 0)
        agent_score += dif

        if agent_score >= 10000:
            print("Agent won!")
            break

        print("Agent score: ", agent_score, "    Agent diff: ", dif, "      Player score: ", player_score)
        
        player_dif = input("Enter your score: ")
        player_null_counter = 0

        if player_dif == "":
            player_dif = "0"
        if player_dif == "X":
            break
        elif player_dif.isdigit():
            player_score += int(player_dif)
        else:
            print("Invaid input, terminated game.")
            break
        
        if player_score >= 10000:
            print("Player won!")
            break
        
        if int(player_dif) == 0:
            player_null_counter += 1
            print(player_null_counter)
            if player_null_counter >= 3:
                player_score = 0
                print("Player score reset to 0 due to 3 consecutive fails.")
        else:
            player_null_counter = 0

         
env = Environment()
agent_0 = Agent_0()
agent_1 = Agent_1()
agent_2 = Agent_2()
agent_3 = Agent_3()
agent_4 = Agent_4()
agent_5 = Agent_5()


avg_game(iterace = 100)

