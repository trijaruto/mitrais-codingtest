import random

class TokenRandom(object):
    @staticmethod
    def get_token_random_range(v_digit):
        return random.sample(range(0,9),v_digit)
