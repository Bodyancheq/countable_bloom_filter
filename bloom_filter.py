import math
import re
import random

from text import text

_memomask = {}


def hash_function(n):
    mask = _memomask.get(n)
    if mask is None:
        random.seed(n)
        mask = _memomask[n] = random.getrandbits(32)

    def myhash(x):
        return hash(x) ^ mask

    return myhash


re_pattern = re.compile(r"[\w’]+")
words = re_pattern.findall(text)
dictionary = set(words)

n = len(dictionary)
k = int((n * 5) / n * math.log(2))
hashes = [hash_function(i) for i in range(k)]
cbf = [0 for i in range(n * 5)]
fp_rate = round(pow(1 - math.exp(-k * n / (5 * n)), k), 2)
print(f"False positive rate is {fp_rate}")

for word in dictionary:
    indexes = [hashes[i](word) % len(cbf) for i in range(k)]
    for i in indexes:
        cbf[i] += 1


def check_word(check_word):
    check_indexes = [hashes[i](check_word) % len(cbf) for i in range(k)]
    if all([cbf[i] for i in check_indexes]):
        print(f"Word [{check_word}] may be in text")
    else:
        print(f"No such word [{check_word}] 100%")


def add_word(new_word):
    add_indexes = [hashes[i](new_word) % len(cbf) for i in range(k)]
    for i in add_indexes:
        cbf[i] += 1
    print(f"Added word [{new_word}]")


check_word("abobus")
add_word("abobus")
check_word("abobus")
