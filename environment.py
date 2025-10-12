from random import randint
from copy import deepcopy


class Game:
    def __init__(self):
        self.score = 0
        self.dices = [randint(1, 6) for _ in range(6)]
        self.user_decided_to_end = False
        self.failed = False

class Agent:
    def decide(self, score, dices, number_of_prev_fails=0):
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

    def play_one_turn(self, agent):
        game = Game()
        while True:
            response = agent.decide(game.score, deepcopy(game.dices))
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