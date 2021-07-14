import math
import time

import clock


def sine(t, frequency):
    return math.sin(2.0 * math.pi * t * frequency)

def square(t, frequency):
    return -1 if sine(t, frequency) < 0 else 1

def triangle(t, frequency):
    t = t * frequency
    return 1.0 - 4.0 * abs(round(t - 0.25) - (t - 0.25))

def sawtooth(t, frequency):
    t = t * frequency
    return 2.0 * (t - math.floor(t + 0.5))

def lerp(a, b, t):
    return (1.0 - t) * a + b * t

def inverse_lerp(a, b, v):
    return (v - a) / (b - a)


class LFO:
    def __init__(self):
        self.frequency = 0.1
        self.type = 0

    def value(self):
        t = clock.time
        f = self.frequency
        values = sine(t, f), triangle(t, f), square(t, f), sawtooth(t, f)
        count = len(values) - 1
        pos = self.type * count #1.2
        indexA = int(math.floor(pos))
        indexB = int((indexA + 1) % count)
        fract = pos - indexA #0.2
        partA = values[indexA]
        partB = values[indexB]
        return lerp(partA, partB, fract)




