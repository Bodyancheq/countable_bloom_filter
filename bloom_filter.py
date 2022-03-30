import math
import re
import random

from text import text


class CBF:
    def __init__(self, m: int, n=None, k=None):
        """
        :param m: Length of dictionary (len(set(words_list)))
        :param n: Length of CBF
        :param k: Number of hash functions
        """
        self._memomask = {}
        self.m = m
        self.n = self.m * 5 if n is None else n
        self.k = int(self.n / self.m * math.log(2)) if k is None else k
        self.hashes = [self.hash_function(i) for i in range(self.k)]
        self.cbf = [0 for _ in range(self.n)]
        self.fp_rate = round(pow(1 - math.exp(-self.k * self.m / self.n), self.k), 2)

    def hash_function(self, n_):
        mask = self._memomask.get(n_)
        if mask is None:
            random.seed(n_)
            mask = self._memomask[n_] = random.getrandbits(32)

        def myhash(x):
            return hash(x) ^ mask

        return myhash

    def add_word(self, word):
        indexes = [self.hashes[i](word) % self.n for i in range(self.k)]
        for i in indexes:
            self.cbf[i] += 1

    def check_word(self, word):
        check_indexes = [self.hashes[i](word) % self.n for i in range(self.k)]
        if all([self.cbf[i] for i in check_indexes]):
            print(f"Word [{word}] may be in text with probability of {1 - self.fp_rate}")
        else:
            print(f"No such word [{word}] in text")


if __name__ == '__main__':
    re_pattern = re.compile(r"[\w’]+")
    words = re_pattern.findall(text)
    dictionary = set(words)

    my_cbf = CBF(m=len(dictionary))
    for word in words:
        my_cbf.add_word(word)

    my_cbf.check_word("aboba")
    my_cbf.add_word("aboba")
    my_cbf.check_word("aboba")
