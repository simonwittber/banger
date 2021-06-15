import numbers
import random
import math
import collections
import operator


class UnaryOp:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, obj):
        return self.op(obj)

    def op(self, obj):
        if isinstance(obj, list):
            return self._op_list(obj)
        if isinstance(obj, tuple):
            return tuple(self._op_list(obj))
        if isinstance(obj, numbers.Number):
            return self._op_number(obj)

    def _op_list(self, items):
        return [self.op(i) for i in items]

    def _op_number(self, number):
        return self.fn(number)



class BinaryOp:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, obj1, obj2):
        return self.op(obj1, obj2)

    def op(self, obj1, obj2):
        if isinstance(obj1, list) and isinstance(obj2, list):
            return self._op_list_list(obj1, obj2)
        if isinstance(obj1, tuple) and isinstance(obj2, tuple):
            return tuple(self._op_list_list(obj1, obj2))
        if isinstance(obj1, list) and isinstance(obj2, numbers.Number):
            return self._op_list(obj1, obj2)
        if isinstance(obj1, tuple) and isinstance(obj2, numbers.Number):
            return tuple(self._op_list(obj1, obj2))
        if isinstance(obj1, numbers.Number) and isinstance(obj2, numbers.Number):
            return self._op_number(obj1, obj2)

    def _op_list(self, items, obj2):
        return [self.op(i, obj2) for i in items]

    def _op_number(self, number1, number2):
        return self.fn(number1, number2)

    def _op_list_list(self, items1, items2):
        return [self.op(a,b) for a,b in zip(items1, items2)]



add = BinaryOp(operator.add)
sub = BinaryOp(operator.sub)
truediv = BinaryOp(operator.truediv)
floordiv = BinaryOp(operator.floordiv)
mul = BinaryOp(operator.mul)
lerp = lambda a, b, x: add(a, mul(sub(b,a),x))
floor = UnaryOp(math.floor)
cos = UnaryOp(math.cos)
sin = UnaryOp(math.sin)
fabs = UnaryOp(math.fabs)
mutate = BinaryOp(lambda a, b: a + random.uniform(-b,b))
minimum = BinaryOp(lambda a, b: min(a,b))
maximum = BinaryOp(lambda a, b: max(a,b))
clamp = lambda a, mn, mx: maximum(minimum(a, mx), mn)
repeat = BinaryOp(lambda t, length: clamp(t - math.floor(t / length) * length, 0.0, length))
pingpong = BinaryOp(lambda t, length: length - abs(repeat(t, length * 2) - length))


__all__ = ["add","sub","truediv","floordiv","mul","lerp","floor","cos","sin","fabs","mutate",
           "minimum","maximum","clamp","repeat","pingpong"]
