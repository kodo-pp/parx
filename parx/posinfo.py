# (c) 2019 Alexander Korzun
# This file is licensed under the MIT license. See LICENSE file


class Posinfo(object):
    """
    Represents a position in the source code (column and row)
    """

    def __init__(self, row, col):
        """
        Constructor

        Arguments:
            row - row, indexed from 1
            col - column, indexed from 1

        Raises:
            None
        """
        self.row = row
        self.col = col

    def __str__(self):
        return '{}:{}'.format(self.row, self.col)

    def __repr__(self):
        return 'Posinfo({})'.format(str(self))

    def __eq__(self, other):
        return (self.row, self.col) == (other.row, other.col)

    def __ne__(self, other):
        return not (self == other)


def from_data(data, offset):
    """
    Construct a Posinfo object given the input string and offset in it

    Warning: this function is quite slow, as it has to iterate over all
    characters in data[:offset] (see Complexity section). If misused,
    it may make tokenization run in O(n²), where n is the length of input

    Arguments:
        data - input string
        offset - offset in `data`, indexed from 0

    Returns:
        Posinfo object with row and column information

    Raises:
        IndexError if offset is out of range [0; length), where length = len(data)

    Complexity:
        O(offset)
    """
    if offset < 0 or offset >= len(data):
        raise IndexError(offset)

    row, col = 1, 1
    for index in range(offset):
        if data[index] == '\n':
            row += 1
            col = 1
        else:
            col += 1
    return Posinfo(row, col)
