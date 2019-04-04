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

    def feed(self, data, start=0, end=None):
        """
        Make this object point to some next position in the source code

        Assuming `data` is the source code and the current position points to data[start],
        the resulting position will point to data[end]

        This interface may seem inconvenient, but it also allows to be used in quite different way.
        Consider the following code:

            class MyStringProcessor:
                def __init__(self, string):
                    self.string = string
                    self.posinfo = Posinfo(1, 1)
                    self.offset = 0

                def process_part(self, length):
                    # Process part of the string starting from the current position and with specified length
                    part = self.string[self.offset : self.offset + length]

                    # ... Do something with the string ...

                    # Update Posinfo and offset
                    # equivalent to: self.posinfo.feed(self.string, self.offset, self.offset + length)
                    self.posinfo.feed(part)

                    self.offset += length

        In it we pass only the current part of the string to Posinfo.feed(), which is possible too (and may be
        the preferred way of using this method)

        Unlike from_data() function, this method is usually safe to use from the perspective of the
        performance because if used properly, all invocations of this method will make O(n) operations
        in total, where n is the total number of characters processed

        Arguments:
            data  - source code
            start - current position
            end   - next position. None means len(data)

        Returns:
            None

        Raises:
            IndexError if end < start or start < 0 or end > len(data)

        Complexity:
            O(end - start)
        """
        if end is None:
            end = len(data)
        if end < start or start < 0 or end > len(data):
            raise IndexError((start, end))

        for i in range(start, end):
            if data[i] == '\n':
                self.row += 1
                self.col = 1
            else:
                self.col += 1
        

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
