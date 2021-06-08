import mido

class NovationCircuit:
    def __init__(self, midi, channels=(1,2,10)):
        self.midi = midi
        self.synth1_channel = channels[0]
        self.synth2_channel = channels[1]
        self.drum_channel = channels[2]
        self.drum = (
            NovationDrum(midi, channels[2], 0),
            NovationDrum(midi, channels[2], 1),
            NovationDrum(midi, channels[2], 2),
            NovationDrum(midi, channels[2], 3)
        )


def smoothdamp(c, t, currentVelocity, smoothTime, maxSpeed, deltaTime):
    smoothTime = max(0.0001, smoothTime)
    num  = 2 / smoothTime
    num2 = num * deltaTime
    num3 = 1 / (1 + num2 + 0.48 * num2 * num2 + 0.235 * num2 * num2 * num2)
    num4 = c - t
    num5 = t
    num6 = maxSpeed * smoothTime
    num4 = min(max(num4, -num6), num6)
    target = c - num4
    num7 = (currentVelocity + num * num4) * deltaTime
    currentVelocity = (currentVelocity - num * num7) * num3
    num8 = target + (num4 + num7) * num3
    if (num5 - c > 0) == (num8 > num5):
        num8 = num5
        currentVelocity = (num8 - num5) / deltaTime
    return num8, currentVelocity


class Knobs:
    def __init__(self):
        self.values = {}

    def get(self, name, defaultValue=0, defaultSmoothTime=0.1):
        if name in self.values:
            return self.values[name][0]
        else:
            self.values[name] = (defaultValue, defaultSmoothTime, defaultValue, 0)
            return defaultValue

    def update(self, deltaTime):
        for i in self.values:
            value, smoothTime, target, velocity = self.values[i]
            newValue, newVelocity = smoothdamp(value, target, velocity, smoothTime, 1, deltaTime)
            self.values[i] = newValue, smoothTime, target, newVelocity


class NovationDrum:
    drum_controls = (
        dict(
            patchselect = 8,
            level = 12,
            pitch = 14,
            decay = 15,
            distortion = 16,
            eq = 17,
            pan = 77
        ),
        dict(
            patchselect = 18,
            level = 23,
            pitch = 34,
            decay = 40,
            distortion = 42,
            eq = 43,
            pan = 78
        ),
        dict(
            patchselect = 44,
            level = 45,
            pitch = 46,
            decay = 47,
            distortion = 48,
            eq = 49,
            pan = 79
        ),
        dict(
            patchselect = 50,
            level = 53,
            pitch = 55,
            decay = 57,
            distortion = 61,
            eq = 76,
            pan = 80
        ))
    note_on = {0:60, 1:62, 2:64, 3:65}
    def __init__(self, midi, channel, index):
        self.midi = midi
        self.channel = channel
        self.index = index
        self.note_on_number = self.note_on[index]
        self.knobs = Knobs()

    def update(self, deltaTime):
        self.knobs.update(deltaTime)
            
    def cc(self, control_name, value):
        control = self.drum_controls[self.index][control_name]
        self.midi.cc(self.channel, control, value)
        return self

    def trigger(self, velocity=100):
        self.midi.note(self.channel, self.note_on_number, velocity)
        return self
    
    def patch(self, index):
        self.cc('patchselect', index)
        return self
    
    def level(self, value):
        self.cc('level', value)
        return self
    
    def pitch(self, value):
        self.cc('pitch', value)
        return self
    
    def decay(self, value):
        self.cc('decay', value)
        return self

    def distortion(self, value):
        self.cc('distortion', value)
        return self

    def eq(self, value):
        self.cc('eq', value)
        return self

    def pan(self, value):
        self.cc('pan', value)
        return self
        


