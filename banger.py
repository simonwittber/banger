import numbers
from uservalues import _ev, Seq, Rnd


class Banger:
    instances = dict()

    @classmethod
    @property
    def bangers(_class):
        return _class.instances

    def __init__(self, *notes, channel=0):
        self.channel = channel
        self.notes = Seq(*notes)
        self.velocities = Seq(120)
        self.durations = Seq(1)
        self.pulses = Seq(1)
        self.enabled = True
        self.scale = None
        Banger.instances[id(self)] = self

    def __repr__(self):
        return  ("Channel:    %s\nNotes:      %r\nVelocities: %s\nDurations:  %r\nPulses:     %r"%
                (self.channel, self.notes, self.velocities, self.durations, self.pulses))

    def __setattr__(self, key, value):
        if isinstance(value, list):
            self.__dict__[key] = Rnd(*value)
        elif isinstance(value, tuple):
            self.__dict__[key] = Seq(*value)
        else:
            self.__dict__[key] = value

    def __next__(self):
        if self.enabled:
            n = next(self.notes)
            if self.scale is not None:
                n = self.scale[n]
            v = next(self.velocities)
            d = next(self.durations)
            p = next(self.pulses)
            return self.channel, n, v, d, p



