import sequence
from patterns import Seq, Rnd
import clock


class Banger:
    instances = dict()

    __slots__ = "name","channel","_notes","_velocities","_durations","_pulses","enabled","scale","volume","watch"

    @classmethod
    @property
    def bangers(_class):
        return _class.instances

    def restart(self):
        if self.enabled:
            self.notes.index = 0
            self.velocities.index = 0
            self.durations.index = 0
            self.pulses.index = 0

    def __init__(self, *notes, channel=0):
        self.enabled = False
        self.name = "Banger %s"%id(self)
        self.channel = channel
        self.notes = Seq(*notes)
        self.velocities = Seq(120)
        self.durations = Seq(1)
        self.pulses = Seq(1)
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
        self._notes = self.convert_value(value)
        self.restart()

    @property
    def velocities(self):
        return self._velocities
    @velocities.setter
    def velocities(self, value):
        self._velocities = self.convert_value(value)
        self.restart()

    @property
    def durations(self):
        return self._durations
    @durations.setter
    def durations(self, value):
        self._durations = self.convert_value(value)
        self.restart()

    @property
    def pulses(self):
        return self._pulses
    @pulses.setter
    def pulses(self, value):
        self._pulses = self.convert_value(value)
        self.restart()

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



def bangify(track):
    class Ev:
        def __init__(self, tick, note, velocity):
            self.tick = tick
            self.note = note
            self.velocity = velocity
            self.duration = 0

    events = []
    playing = {}

    for i in list(track):
        tick = i.time
        if i.type == 'note_on' and i.velocity > 0:
            note = i.note
            if note in playing:
                #turn last playing note off.
                ev = playing[note]
                ev.duration = tick -  ev.tick
            #create new playing note
            ev = playing[note] = Ev(tick, note, i.velocity)
            events.append(ev)
        if i.type == 'note_on' and i.velocity == 0 or i.type == 'note_off':
            note = i.note
            if note in playing:
                ev = playing[note]
                ev.duration = tick -  ev.tick
                playing.pop(note)

    b = Banger()
    b.notes = tuple(i.note for i in events)
    b.velocities = tuple(i.velocity for i in events)
    b.durations = tuple(i.duration for i in events)
    pulses = []
    last_p = None
    first = 0
    for i,v in enumerate(events):
        if i == 0:
            pulses.append(0)
        else:
            pulses.append(v.tick - events[i-1].tick)
    b.pulses = tuple(pulses)
    qbeat = clock.beat_resolution / 4
    b.durations = b.durations.quantize(qbeat) / clock.beat_resolution
    b.pulses = b.pulses.quantize(qbeat) / clock.beat_resolution
    b.notes.append(-1)
    b.durations.append(1)
    b.pulses.append(1)
    b.velocities.append(0)
    return b






