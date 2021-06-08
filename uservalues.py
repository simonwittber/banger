import numbers
import random

class UserList:
    def __init__(self, *args):
        self.items = list(args)
        self.index = 0
        self.direction = 1

    def __add__(self, value):
        return self.__class__(*[i + value for i in self.items])

    def __sub__(self, value):
        return self.__class__(*[i - value for i in self.items])

    def __mul__(self, value):
        return self.__class__(*[i * value for i in self.items])

    def __div__(self, value):
        return self.__class__(*[i / value for i in self.items])

    def __repr__(self):
        return repr(self.items)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(*self.items[i])
        return self.items[i]



class Seq(UserList):
    def __next__(self):
        if self.index >= len(self.items):
            self.index = 0
        v = self.items[self.index]
        self.index += self.direction
        return v


class PingPong(UserList):

    def __next__(self):
        if self.index >= len(self.items):
            self.index = len(self.items) - 2
            self.direction = -1
        if self.index < 0:
            self.index = 1
            self.direction = 1
        v = self.items[self.index]
        self.index += self.direction
        return v


tuples = {}

def _ev(o, maximum=None):
    if isinstance(o, tuple):
        return _ev(random.choice(o), maximum)
    if isinstance(o, list):
        return _ev(random.choice(o), maximum)
    if isinstance(o, PingPong):
        return _ev(next(o), maximum)
    if isinstance(o, Seq):
        return _ev(next(o), maximum)
    if isinstance(o, numbers.Number) and maximum is not None:
        return o % maximum
    return o
