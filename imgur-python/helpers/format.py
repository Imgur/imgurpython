import math


def center_pad(s, length):
    num_dashes = float(length - len(s) - 2) / 2
    num_dashes_left = int(math.floor(num_dashes))
    num_dashes_right = int(math.ceil(num_dashes))

    return ('=' * num_dashes_left) + ' ' + s + ' ' + ('=' * num_dashes_right)


def two_column_with_period(left, right, length):
    num_periods = int(length - (len(left) + len(right) + 2))
    return left + ' ' + ('.' * num_periods) + ' ' + right