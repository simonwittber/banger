import numbers
import random
import math
import collections
import sequence
import midi_out


class Seq:
    def __init__(self, *args):
        self.items = list(args)
        self.index = 0
        self.divider = 1
        self.counter = 0

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
        return "%s/%s:%s"%(self.__class__.__name__, self.divider, repr(self.items))

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
        self.counter += 1
        if self.counter % self.divider == 0:
            self.index += 1
        return v

    def quantize(self, v):
        return self.__class__(*sequence.quant(self.items, v))



class Rnd(Seq):
    def __next__(self):
        v = self.items[self.index]
        self.counter += 1
        if self.counter % self.divider == 0:
            self.index = random.randint(0, len(self.items)-1)
        return v


class Pattern:

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, instance, instance_type):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        typed_value = self.convert_value(value)
        if typed_value is not None:
            setattr(instance, self.private_name, typed_value)

    def convert_value(self, value):
        if isinstance(value, list):
            return Rnd(*value)
        elif isinstance(value, tuple):
            return Seq(*value)
        elif isinstance(value, Rnd):
            return value
        elif isinstance(value, Seq):
            return value
        elif isinstance(value, numbers.Number):
            return Seq(value)
        print("Cannot assign type %s."%type(value))
        return None
