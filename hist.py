""" Horizontal histogram plotting function. """

from __future__ import absolute_import
import matplotlib.pyplot as plt
import numpy as np


def horizontal_hist(items, title=None, axis_label=None, color=None, height=10, width=20, reverse=False):
    """
    Plots a histogram of values and frequencies.

    Arguments:
        items (iterable[any])     => Example, [1, 2, 3, 1, 2]
        title (Optional[str])     => Example, "Resulting histogram".
        axis_label (Optional[str]) => Example, "y-axis".
        color (Optional[str])     => Default: matplotlib's default plot color, a royal blue
        height (Optional[int])    => Default: 10
        width (Optional[int])     => Default: 20
        reverse (Optional[bool])  => From top to bottom in order of decreasing frequency or not.

    Returns:
        None, however a matplotlib figure should be produced.
    """

    unique_items, item_counts = np.unique(items, return_counts=True)
    item_counts, unique_items = zip(*sorted(zip(item_counts, unique_items), reverse=reverse))

    pos = np.arange(len(unique_items)) + 0.5
    plt.figure(figsize=(width, height))
    plt.barh(pos, item_counts, align='center', color=color)
    plt.yticks(pos, unique_items)
    plt.xlabel('Frequency')
    plt.ylabel(axis_label) if axis_label else None
    plt.title(title) if title else None

    plt.show()


if __name__ == '__main__':
    items = range(1, 10) * 100 + range(11, 20) * 50 + range(21, 30) * 25
    horizontal_hist(items, title="Resulting histogram")
