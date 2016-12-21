#!/usr/bin/env python

"""
Provide convenient way to select list elements with different probability.
"""

import random
import bisect
import collections
import logging


def set_log():
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    fm = logging.Formatter('%(filename)s [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')

    console = logging.StreamHandler()
    console.setLevel(LOG_LEVEL)
    console.setFormatter(fm)

    logger.addHandler(console)


def cdf(weights):
    total = sum(weights)
    result = []
    cum_sum = 0

    for w in weights:
        cum_sum += w
        result.append(cum_sum/total)

    return result


def get_by_distribution(collection, weights):
    assert len(collection) == len(weights)

    cdf_values = cdf(weights)
    x = random.random()
    idx = bisect.bisect(cdf_values, x)
    logging.debug("cdf_values: %s x: %d idx: %d", cdf_values, x, idx)

    return collection[idx]


if __name__ == '__main__':
    population = 'ABC'
    distribution = [0.3, 0.4, 0.3]

    LOG_LEVEL = 'INFO'   # 'DEBUG'
    set_log()

    counts = collections.defaultdict(int)
    for i in range(10000):
        counts[get_by_distribution(population, distribution)] += 1
    logging.info(counts)

    # % test.py
    # defaultdict(<type 'int'>, {'A': 3066, 'C': 2964, 'B': 3970})
