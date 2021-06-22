import numbers
from patterns import Seq, Rnd


class Banger:
    instances = dict()

    __slots__ = "channel","_notes","_velocities","_durations","_pulses","enabled","scale"

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

    @property
    def notes(self):
        return self._notes
    @notes.setter
    def notes(self, value):
        self._notes = self.convert_value(value)


    @property
    def velocities(self):
        return self._velocities
    @velocities.setter
    def velocities(self, value):
        self._velocities = self.convert_value(value)


    @property
    def durations(self):
        return self._durations
    @durations.setter
    def durations(self, value):
        self._durations = self.convert_value(value)


    @property
    def pulses(self):
        return self._pulses
    @pulses.setter
    def pulses(self, value):
        self._pulses = self.convert_value(value)


    def convert_value(self, value):
        if isinstance(value, list):
            return Rnd(*value)
        elif isinstance(value, tuple):
            return Seq(*value)
        else:
            return value

    def __next__(self):
        if self.enabled:
            if len(self.notes) == 0: return None
            if len(self.velocities) == 0: return None
            if len(self.durations) == 0: return None
            if len(self.pulses) == 0: return None

            n = next(self.notes)
            if self.scale is not None:
                n = self.scale(n)
            v = next(self.velocities)
            d = next(self.durations)
            p = next(self.pulses)
            return self.channel, n, v, d, p



