import numbers
import random
import math
import collections
import sequence


class Seq:
    def __init__(self, *args):
        self.items = list(args)
        self.index = 0

    def append(self, v):
        self.items.append(v)

    def __len__(self): return len(self.items)

    def __add__(self, value):
        return self.__class__(*sequence.add(self.items, value))

    def __sub__(self, value):
        return self.__class__(*sequence.sub(self.items, value))

    def __mul__(self, value):
        return self.__class__(*sequence.mul(self.items, value))

    def __truediv__(self, value):
        return self.__class__(*sequence.truediv(self.items, value))

    def __floordiv__(self, value):
        return self.__class__(*sequence.floordiv(self.items, value))

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

    def quantize(self, v):
        return self.__class__(*sequence.quant(self.items, v))


class Rnd(Seq):
    def __next__(self):
        return random.choice(self.items)

