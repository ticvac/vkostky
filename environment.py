from random import randint
from copy import deepcopy


class Game:
    def __init__(self):
        self.score = 0
        self.global_score = 0
        self.dices = [randint(1, 6) for _ in range(6)]
        self.user_decided_to_end = False
        self.failed = False

class Agent:
    def avg_score(self,dice_count):
        table = [24.939,50.199,86.979,143.318,227.0865,357.362]
        return table[dice_count-1]

    def null_prob(self,dice_count):
        table = [0.66815,0.44386,0.27648,0.15734,0.07646,0.03114]
        return table[dice_count-1]

    def histogram(self,dice_count,score):
        histogram = [
            {0: 0.66759, 50: 0.16482, 100: 0.16759},

            {0: 0.44325, 50: 0.22263, 100: 0.2504, 150: 0.05513, 200: 0.02859},

            {0: 0.27666, 50: 0.22146, 100: 0.27768, 150: 0.11255, 200: 0.07382, 250: 0.01396, 300: 0.00467, 400: 0.00481, 500: 0.00476, 600: 0.0047, 1000: 0.00493},

            {0: 0.15685, 50: 0.18313, 100: 0.26041, 150: 0.14888, 200: 0.11992, 250: 0.04065, 300: 0.01727, 350: 0.00312, 400: 0.01297, 450: 0.00287, 500: 0.01585, 600: 0.0138, 650: 0.00322, 700: 0.00321, 800: 0.00084, 1000: 0.01243, 1050: 0.00307, 1200: 0.00077, 2000: 0.00074},

            {0: 0.07736, 50: 0.13277, 100: 0.20774, 150: 0.1555, 200: 0.14903, 250: 0.0691, 300: 0.03667, 350: 0.00985, 400: 0.02348, 
            450: 0.01048, 500: 0.03219, 550: 0.00295, 600: 0.02438, 650: 0.00855, 700: 0.01105, 750: 0.00258, 800: 0.00333, 850: 0.00055, 900: 0.00073, 1000: 0.02343, 1050: 0.00951, 1100: 0.00212, 1200: 0.00178, 1250: 0.00055, 1300: 0.00054, 1600: 0.00011, 2000: 0.00276, 2050: 0.00071, 2400: 0.00011, 4000: 9e-05}
        ]

        prob = 0
        #key_sum

        for key,value in histogram[dice_count-1].items():
            if key >= score:
                prob += value #*key
                #key_sum += key
        #prob /= key_sum
        return prob

    def decide(self, score, total_score, dices, number_of_prev_fails):
        """
        Returns [bool next, [keep]]
        """
        raise NotImplementedError("Subclasses must implement this method.")


class Environment:
    def __init__(self):
        ...

    @staticmethod
    def check_if_playable(dices):
        if 1 in dices:
            return True
        if 5 in dices:
            return True
        for i in range(1, 7):
            if dices.count(i) >= 3:
                return True
        # postupka
        if sorted(dices) == [1, 2, 3, 4, 5, 6]:
            return True
        return False
    
    """Assumes maximum of 6 dices!"""
    @staticmethod
    def calculate_score(keep):
        score = 0
        # postupka
        if sorted(keep) == [1, 2, 3, 4, 5, 6]:
            score += 1500
            return score
        # rest
        if keep.count(1) >= 3:
            score += 1000 * (2 ** (keep.count(1) - 3))
        for i in [2, 3, 4, 5, 6]:
            if keep.count(i) >= 3:
                score += i * 100 * (2 ** (keep.count(i) - 3))
        if keep.count(1) < 3:
            score += keep.count(1) * 100
        if keep.count(5) < 3:
            score += keep.count(5) * 50
        return score

    """Assumes maximum of 6 dices!"""
    @staticmethod
    def check_if_can_keep(dices, keep):
        if len(keep) > 6 or keep == []:
            return False
        # postupka
        if sorted(keep) == [1, 2, 3, 4, 5, 6] and sorted(dices) == [1, 2, 3, 4, 5, 6]:
            return True
        # trojice a zbytek...
        for i in [2, 3, 4, 6]:
            # chce si nechat malo
            if 0 < keep.count(i) < 3:
                return False
            # chce si nechat vic nez ma
            if keep.count(i) > dices.count(i):
                return False
            # odstranime...
            keep = [x for x in keep if x != i]
        if keep.count(1) > dices.count(1):
            return False
        if keep.count(5) > dices.count(5):
            return False
        # odstranime jednicky...
        keep = [x for x in keep if x != 1 and x != 5]
        return len(keep) == 0

    def play_one_turn(self, agent, total_score, number_of_prev_fails):
        game = Game()
        while True:
            response = agent.decide(game.score, total_score, deepcopy(game.dices), number_of_prev_fails)
            # check user response
            if self.check_if_can_keep(game.dices, response[1]) == False and len(response[1]) > 0:
                raise ValueError(f"Agent tried to keep dices that are not in the current hand or not valid keep.\nresponse: {response[1]}\ngame.dices: {game.dices}")
            game.score += self.calculate_score(response[1])
            # new dices
            game.dices = [randint(1, 6) for _ in range(len(game.dices) - len(response[1]))]
            # new hand if played all
            if len(game.dices) == 0:
                game.dices = [randint(1, 6) for _ in range(6)]
            # user failed
            if len(response[1]) == 0:
                game.failed = True
                game.score = 0
                break
            # user decided to end
            if response[0] == False:
                game.user_decided_to_end = True
                break
        if game.score < 350:
            game.score = 0
        return game.score
    
    def play_one_game(self,agent,target_score):
        game = Game()
        turns = 0

        null_counter = 0
        dif = 0
        list_score = []

        while game.global_score <= target_score:
            #while turns <= 500:
            dif = self.play_one_turn(agent, game.global_score, 0)
            game.global_score += dif

            if dif == 0:
                null_counter += 1
            else:
                null_counter = 0
            
            if null_counter >= 3:
                game.global_score = 0
                null_counter = 0

            list_score.append(game.global_score)

            
            turns += 1
    
        return list_score
