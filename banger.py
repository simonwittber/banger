import sequence
from patterns import Seq, Rnd


class Banger:
    instances = dict()

    __slots__ = "name","channel","_notes","_velocities","_durations","_pulses","enabled","scale","volume","watch"

    @classmethod
    @property
    def bangers(_class):
        return _class.instances

    def restart(self):
        self.notes.index = 0
        self.velocities.index = 0
        self.durations.index = 0
        self.pulses.index = 0

    def __init__(self, *notes, channel=0):
        self.name = "Banger %s"%id(self)
        self.channel = channel
        self.notes = Seq(*notes)
        self.velocities = Seq(120)
        self.durations = Seq(1)
        self.pulses = Seq(1)
        self.enabled = True
        self.scale = None
        self.volume = 1.0
        self.watch = False
        Banger.instances[id(self)] = self

    def __repr__(self):
        return  ("Channel:    %s\nVolume:     %s\nNotes:      %r\nVelocities: %s\nDurations:  %r\nPulses:     %r\nEnabled:    %r"%
                (self.channel, self.volume, self.notes, self.velocities, self.durations, self.pulses, self.enabled))

    @property
    def notes(self):
        return self._notes
    @notes.setter
    def notes(self, value):
        self.restart()
        self._notes = self.convert_value(value)


    @property
    def velocities(self):
        return self._velocities
    @velocities.setter
    def velocities(self, value):
        self.restart()
        self._velocities = self.convert_value(value)


    @property
    def durations(self):
        return self._durations
    @durations.setter
    def durations(self, value):
        self.restart()
        self._durations = self.convert_value(value)


    @property
    def pulses(self):
        return self._pulses
    @pulses.setter
    def pulses(self, value):
        self.restart()
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
            v = sequence.make_int(sequence.mul(v, self.volume))
            d = next(self.durations)
            p = next(self.pulses)
            values = self.channel, n, v, d, p
            if self.watch:
                print("Banger: %s -> %s"%(self.name, values))
            return values



