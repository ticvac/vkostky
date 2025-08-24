from random import randint


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
        # TODO - now only counts ones and fives.
        score = 0
        score += keep.count(1) * 100
        score += keep.count(5) * 50
        return score

    def play_one_game(self, agent):
        game = Game()
        while True:
            response = agent.decide(game.score, game.dices) # TODO send deep copy
            # TODO check if he keeps relevant dices
            game.score += self.calculate_score(response[1])
            game.dices = [randint(1, 6) for _ in range(len(game.dices) - len(response[1]))]
            # new hand...
            if len(game.dices) == 0:
                game.dices = [randint(1, 6) for _ in range(6)]
            if len(response[1]) == 0:
                game.failed = True
                game.score = 0
                break
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
        print(" - test_keep_calculation to be implemented.")

    def __init__(self):
        self.test_check_if_playable()
        self.test_keep_calculation()
        print("All tests passed.")


if __name__ == "__main__":
    Tests()
    env = Environment()
    agent = OneFiveEnjoyer()
    env.play_one_game(agent)

    sum_score = 0
    for i in range(200000):
        sum_score += env.play_one_game(agent)
    print(f"Average score over 200000 games: {sum_score / 200000}")
