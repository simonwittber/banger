import random
import numbers

import sequence
from patterns import Pattern
import clock
import midi_out


class Banger:
    note = Pattern()
    velocity = Pattern()
    duration = Pattern()
    pulse = Pattern()
    probability = Pattern()
    transpose = Pattern()

    def restart(self):
        if self.enabled:
            self.note.index = 0
            self.velocity.index = 0
            self.durations.index = 0
            self.pulse.index = 0
            self.transpose.index = 0
            self.probability.index = 0

    def __init__(self, *notes, channel=0):
        self.enabled = None
        self.name = "Banger %s"%id(self)
        self.channel = channel
        self.note = notes
        self.velocity = 120,
        self.duration = 1,
        self.pulse = 1,
        self.transpose = 0,
        self.probability = 1,
        self.scale = None
        self.volume = 1.0
        self.watch = False

    def __repr__(self):
        r = []
        for name in "channel","note", "velocity", "pulse", "duration", "transpose", "probability", "volume","scale":
            r.append(name.ljust(17) + ": " + str(getattr(self, name)))
        return "\r\n".join(r)

    def _play(self, beats=16):
        max_notes = 10000
        time = 0
        if self.enabled:
            while max_notes > 0 and time < beats:
                max_notes -= 1
                channel, note, velocity, duration, p, chance = next(self)
                beat = midi_out.ev(p)
                if chance:
                    midi_out.note(channel, note, velocity=velocity, duration=duration, beat=time+beat)
                time += beat
        return time


    def play(self):
        if self.enabled is None:
            self.enabled = True
        if self.enabled:
            t = self._play(4)
            midi_out.schedule(self.play, t-1)


    def stop(self):
        self.enabled = False


    def __next__(self):
        if self.enabled:
            if len(self.note) == 0: return None
            if len(self.velocity) == 0: return None
            if len(self.duration) == 0: return None
            if len(self.pulse) == 0: return None

            n = next(self.note)
            t = next(self.transpose)
            n += t
            if self.scale is not None:
                n = self.scale(n)
            v = next(self.velocity)
            v = sequence.make_int(sequence.mul(v, self.volume))
            d = next(self.duration)
            p = next(self.pulse)
            chance = random.random() < next(self.probability)
            values = self.channel, n, v, d, p, chance
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






