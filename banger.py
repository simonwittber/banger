import random
import numbers

import sequence
from patterns import Pattern
import clock
import midi_out


class Banger:
    pitch = Pattern()
    velocity = Pattern()
    duration = Pattern()
    gate = Pattern()
    pulse = Pattern()
    probability = Pattern()
    transpose = Pattern()

    def restart(self):
        if self.enabled:
            self.pitch.index = 0
            self.velocity.index = 0
            self.durations.index = 0
            self.gate.index = 0
            self.pulse.index = 0
            self.transpose.index = 0
            self.probability.index = 0

    def __init__(self, *pitchs, channel=0):
        self.enabled = None
        self.name = "Banger %s"%id(self)
        self.channel = channel
        self.pitch = pitchs
        self.velocity = 120,
        self.duration = 1,
        self.gate = 1/4,
        self.pulse = True,
        self.transpose = 0,
        self.probability = 1,
        self.scale = None
        self.volume = 1.0
        self.watch = False

    def __repr__(self):
        r = []
        for name in "channel","pitch", "velocity", "pulse", "duration", "gate", "transpose", "probability", "volume","scale":
            r.append(name.ljust(17) + ": " + str(getattr(self, name)))
        return "\r\n".join(r)

    def _play(self, beats=16):
        max_pitchs = 10000
        time = 0
        if self.enabled:
            while max_pitchs > 0 and time < beats:
                max_pitchs -= 1
                channel, pitch, velocity, duration, gate, pulse, chance = next(self)
                if chance and pulse:
                    midi_out.note(channel, pitch, velocity=velocity, gate=gate, beat=time)
                time += duration
        return time


    def play(self):
        if self.enabled is None:
            self.enabled = True
        if self.enabled:
            t = self._play(4)
            midi_out.schedule(self.play, t-1)
        else:
            self.enabled = None


    def stop(self):
        self.enabled = False


    def __next__(self):
        if self.enabled:
            if len(self.pitch) == 0: return None
            if len(self.velocity) == 0: return None
            if len(self.duration) == 0: return None
            if len(self.gate) == 0: return None
            if len(self.pulse) == 0: return None

            n = next(self.pitch)
            t = next(self.transpose)
            n += t
            if self.scale is not None:
                n = self.scale(n)
            v = next(self.velocity)
            v = sequence.make_int(sequence.mul(v, self.volume))
            d = next(self.duration)
            p = next(self.pulse)
            g = next(self.gate)
            chance = random.random() < next(self.probability)
            values = self.channel, n, v, d, g, p, chance
            if self.watch:
                print("Banger: %s -> %s"%(self.name, values))
            return values



def bangify(track):
    class Ev:
        def __init__(self, tick, pitch, velocity):
            self.tick = tick
            self.pitch = pitch
            self.velocity = velocity
            self.duration = 0

    events = []
    playing = {}

    for i in list(track):
        tick = i.time
        if i.type == 'pitch_on' and i.velocity > 0:
            pitch = i.pitch
            if pitch in playing:
                #turn last playing pitch off.
                ev = playing[pitch]
                ev.duration = tick -  ev.tick
            #create new playing pitch
            ev = playing[pitch] = Ev(tick, pitch, i.velocity)
            events.append(ev)
        if i.type == 'pitch_on' and i.velocity == 0 or i.type == 'pitch_off':
            pitch = i.pitch
            if pitch in playing:
                ev = playing[pitch]
                ev.duration = tick -  ev.tick
                playing.pop(pitch)

    b = Banger()
    b.pitchs = tuple(i.pitch for i in events)
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
    b.pitchs.append(-1)
    b.durations.append(1)
    b.pulses.append(1)
    b.velocities.append(0)
    return b






