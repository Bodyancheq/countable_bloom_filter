import math
import re
import random

from text import text

_memomask = {}


def hash_function(n_):
    mask = _memomask.get(n_)
    if mask is None:
        random.seed(n_)
        mask = _memomask[n_] = random.getrandbits(32)

    def myhash(x):
        return hash(x) ^ mask

    return myhash


re_pattern = re.compile(r"[\w’]+")
words = re_pattern.findall(text)
dictionary = set(words)

n = len(dictionary)
print(f"m = {n}\nn = 5 * m")
k = int((n * 5) / n * math.log(2))
print(f"k = {k}")
hashes = [hash_function(i) for i in range(k)]
cbf = [0 for i in range(n * 5)]
fp_rate = round(pow(1 - math.exp(-k * n / (5 * n)), k), 2)
print(f"False positive rate is {fp_rate}")

for word in dictionary:
    indexes = [hashes[i](word) % len(cbf) for i in range(k)]
    for i in indexes:
        cbf[i] += 1


def check_word(to_check):
    check_indexes = [hashes[i](to_check) % len(cbf) for i in range(k)]
    if all([cbf[i] for i in check_indexes]):
        print(f"Word [{to_check}] may be in text")
    else:
        print(f"No such word [{to_check}] 100%")


def add_word(new_word):
    add_indexes = [hashes[i](new_word) % len(cbf) for i in range(k)]
    for i in add_indexes:
        cbf[i] += 1
    print(f"Added word [{new_word}]")


check_word("abobus")
add_word("abobus")
check_word("abobus")
