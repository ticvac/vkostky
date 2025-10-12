from environment import Environment

class Tests:
    def test_check_if_playable(self):
        env = Environment()
        assert env.check_if_playable([1, 2, 3, 4, 5, 6]) == True
        assert env.check_if_playable([]) == False
        assert env.check_if_playable([2, 3, 4, 6]) == False
        assert env.check_if_playable([2, 2, 2, 2, 4, 4]) == True
        assert env.check_if_playable([2, 5, 6]) == True
        assert env.check_if_playable([1, 2, 3, 4, 5, 6]) == True
        assert env.check_if_playable([3, 1, 2, 3, 4, 5]) == True
        assert env.check_if_playable([2, 3, 4, 4, 6, 6]) == False
        print("test_check_if_playable passed.")

    def test_keep_calculation(self):
        env = Environment()
        assert env.calculate_score([1, 1, 1, 5, 5]) == 1100
        assert env.calculate_score([2, 2, 2, 5, 5]) == 300
        assert env.calculate_score([3, 3, 3, 1, 1]) == 500
        assert env.calculate_score([4, 4, 4, 4, 5]) == 850
        assert env.calculate_score([1, 1, 1, 1, 1]) == 4000
        assert env.calculate_score([6, 6, 6, 6, 6, 6]) == 4800
        assert env.calculate_score([1, 2, 3, 4, 5, 6]) == 1500
        assert env.calculate_score([2, 3, 4, 5, 6]) == 50
        assert env.calculate_score([2, 3, 4, 1, 5]) == 150
        assert env.calculate_score([2, 3, 4, 1, 5, 1]) == 250
        assert env.calculate_score([5, 1, 2, 3, 4, 6]) == 1500
        print("test_keep_calculation passed.")

t = Tests()
t.test_check_if_playable()
t.test_keep_calculation()