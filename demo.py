from random import randint
from copy import deepcopy


class Agent:
    def decide(self, score, dices):
        """
        Returns [bool next, [keep]]
        """
        raise NotImplementedError("Subclasses must implement this method.")


class OneFiveEnjoyer(Agent):
    def decide(self, score, dices):
        keep = []
        for d in dices:
            if d == 1 or d == 5:
                keep.append(d)
        if (Environment.calculate_score(keep) + score) < 350:
            return [True, keep]
        return [False, keep]

class TakesAllRiskManaged(Agent):
    def __init__(self, aggression_level):
        super().__init__()
        # should be between 1 and 5
        self.aggression_level = aggression_level

    def decide(self, score, dices):
        keep = []
        for i in range(1, 7):
            if dices.count(i) >= 3:
                keep.extend([i] * dices.count(i))
        if dices.count(1) < 3:
            keep.extend([1] * dices.count(1))
        if dices.count(5) < 3:
            keep.extend([5] * dices.count(5))
        if (Environment.calculate_score(keep) + score) < 350:
            return [True, keep]
        # calculate remaining dices
        remaining_dices = len(dices) - len(keep)
        if remaining_dices == 0:
            remaining_dices = 6
        should_continue = True if remaining_dices >= self.aggression_level else False
        return [should_continue, keep]

class Game:
    def __init__(self):
        self.score = 0
        self.dices = [randint(1, 6) for _ in range(6)]
        self.user_decided_to_end = False
        self.failed = False


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
        return False
    
    @staticmethod
    def calculate_score(keep):
        score = 0
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

    @staticmethod
    def check_if_can_keep(dices, keep):
        for d in keep:
            if keep.count(d) > dices.count(d):
                return False
        return True

    def play_one_game(self, agent):
        game = Game()
        while True:
            response = agent.decide(game.score, deepcopy(game.dices))
            # check user response
            if Environment.check_if_can_keep(game.dices, response[1]) == False:
                raise ValueError("Agent tried to keep dices that are not in the current hand.")
            game.score += Environment.calculate_score(response[1])
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
        return game.score


class Tests:
    def test_check_if_playable(self):
        env = Environment()
        assert env.check_if_playable([1, 2, 3, 4, 5, 6]) == True
        assert env.check_if_playable([]) == False
        assert env.check_if_playable([2, 3, 4, 6]) == False
        assert env.check_if_playable([2, 2, 2, 2, 4, 4]) == True
        assert env.check_if_playable([2, 5, 6]) == True
        print("test_check_if_playable passed.")

    def test_keep_calculation(self):
        env = Environment()
        assert env.calculate_score([1, 1, 1, 5, 5]) == 1100
        assert env.calculate_score([2, 2, 2, 5, 5]) == 300
        assert env.calculate_score([3, 3, 3, 1, 1]) == 500
        assert env.calculate_score([4, 4, 4, 4, 5]) == 850
        assert env.calculate_score([1, 1, 1, 1, 1]) == 4000
        assert env.calculate_score([6, 6, 6, 6, 6, 6]) == 4800
        print("test_keep_calculation passed.")

    def test_play_one_game(self):
        print(" - test_play_one_game to be implemented.")

    def test_check_if_can_keep(self):
        env = Environment()
        assert env.check_if_can_keep([1, 2, 3, 4, 5, 6], [1, 2]) == True
        assert env.check_if_can_keep([1, 2, 3, 4, 5, 6], [1, 7]) == False
        assert env.check_if_can_keep([1, 2, 3, 4, 5, 6], [7]) == False
        assert env.check_if_can_keep([1, 2, 3, 4, 5, 6], []) == True
        assert env.check_if_can_keep([1], [1, 1, 1]) == False
        print("test_check_if_can_keep passed.")

    def __init__(self):
        self.test_check_if_playable()
        self.test_keep_calculation()
        self.test_play_one_game()
        self.test_check_if_can_keep()
        print("All tests passed.")


def avg_of_n_games(agent, n):
    env = Environment()
    total_score = 0
    for _ in range(n):
        total_score += env.play_one_game(agent)
    return total_score / n

if __name__ == "__main__":
    Tests()
    env = Environment()
    agent = OneFiveEnjoyer()
    takes_all_0 = TakesAllRiskManaged(aggression_level=0)
    takes_all_1 = TakesAllRiskManaged(aggression_level=1)
    takes_all_2 = TakesAllRiskManaged(aggression_level=2)
    takes_all_3 = TakesAllRiskManaged(aggression_level=3)
    takes_all_4 = TakesAllRiskManaged(aggression_level=4)
    takes_all_5 = TakesAllRiskManaged(aggression_level=5)
    takes_all_6 = TakesAllRiskManaged(aggression_level=6)
    takes_all_7 = TakesAllRiskManaged(aggression_level=7)

    print(f"Average score of TakesAllRiskManaged (0) over 100000 games: {avg_of_n_games(takes_all_0, 100000)}")
    print(f"Average score of TakesAllRiskManaged (1) over 100000 games: {avg_of_n_games(takes_all_1, 100000)}")
    print(f"Average score of TakesAllRiskManaged (2) over 100000 games: {avg_of_n_games(takes_all_2, 100000)}")
    print(f"Average score of TakesAllRiskManaged (3) over 100000 games: {avg_of_n_games(takes_all_3, 100000)}")
    print(f"Average score of TakesAllRiskManaged (4) over 100000 games: {avg_of_n_games(takes_all_4, 100000)}")
    print(f"Average score of TakesAllRiskManaged (5) over 100000 games: {avg_of_n_games(takes_all_5, 100000)}")
    print(f"Average score of TakesAllRiskManaged (6) over 100000 games: {avg_of_n_games(takes_all_6, 100000)}")
    print(f"Average score of TakesAllRiskManaged (7) over 100000 games: {avg_of_n_games(takes_all_7, 100000)}")

    # print(f"Average score of OneFiveEnjoyer over 100000 games: {avg_of_n_games(agent, 100000)}")
