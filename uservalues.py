import numbers
import random
import math
import collections


class Seq:
    def __init__(self, *args):
        self.items = list(args)
        self.index = 0

    def __len__(self): return len(self.items)

    def __add__(self, value):
        if isinstance(value, collections.Iterator) or isinstance(value, Seq):
            return self.__class__(*(self.items + list(value)))
        else:
            return self.__class__(*[i + value for i in self.items])

    def __sub__(self, value):
        return self.__class__(*[i - value for i in self.items])

    def __mul__(self, value):
        return self.__class__(*[i * value for i in self.items])

    def __truediv__(self, value):
        return self.__class__(*[i / value for i in self.items])

    def __floordiv__(self, value):
        return self.__class__(*[i // value for i in self.items])

    def __repr__(self):
        return "%s%s"%(self.__class__.__name__, repr(self.items))

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(*self.items[i])
        return self.items[i]

    def __setitem__(self, i, v):
        self.items[i] = v

    def __next__(self):
        if self.index >= len(self.items):
            self.index = 0
        v = self.items[self.index]
        self.index += 1
        return v


class Rnd(Seq):
    def __next__(self):
        return random.choice(self.items)


def clamp(t, a, b):
    if t < a: return a
    if t > b: return b
    return t


def repeat(t, length):
    return clamp(t - math.floor(t / length) * length, 0.0, length)


def pingpong(t, length):
    t = repeat(t, length * 2);
    return length - abs(t - length);


def _ev(o, clamp=None):
    if isinstance(o, tuple) or isinstance(o, list):
        return _ev(random.choice(o), clamp)
    if isinstance(o, collections.Iterator):
        return _ev(next(o), clamp)
    if clamp is not None:
        if isinstance(o, int):
            return o % clamp
        if isinstance(o, float):
            return int((o * clamp) % clamp)
    return o
