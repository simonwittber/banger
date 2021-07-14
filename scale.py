from sequence import repeat, pingpong

class Scale:
    def __init__(self, tonic, scale):
        self.tonic = tonic
        new_scale = [0]
        for i in scale.split(' '):
            if i == 'T': new_scale.append(new_scale[-1] + 2)
            if i == 'S': new_scale.append(new_scale[-1] + 1)
            if i == 'T+S': new_scale.append(new_scale[-1] + 3)
        self.scale = tuple(new_scale)
        self.stretch()

    def bounce(self):
        self.quantize = self.quantize_bounce

    def linear(self):
        self.quantize = self.quantize_linear

    def stretch(self):
        self.quantize = self.quantize_stretch

    def loop(self):
        self.quantize = self.quantize_loop

    def off(self):
        self.quantize = lambda x: x

    def __repr__(self):
        return "%r %r"%(self.tonic, self.scale)

    def quantize_linear(self, note):
        c = len(self.scale)
        octave = int(note / c)
        note_number = note % c
        actual_note = self.scale[note_number]
        quantized_note = octave * 12 + actual_note + self.tonic
        return quantized_note

    def quantize_stretch(self, note):
        octave = int(note / 12)
        note_number = note % 12
        index = int((1 / 12) * note_number * len(self.scale))
        actual_note = self.scale[index]
        quantized_note = octave * 12 + actual_note + self.tonic
        return quantized_note

    def quantize_loop(self, note):
        octave = int(note / 12)
        note_number = note % 12
        index = repeat(note_number, len(self.scale))
        actual_note = self.scale[index]
        quantized_note = octave * 12 + actual_note + self.tonic
        return quantized_note

    def quantize_bounce(self, note):
        octave = int(note / 12)
        note_number = note % 12
        index = pingpong(note_number, len(self.scale)-1)
        actual_note = self.scale[index]
        quantized_note = octave * 12 + actual_note + self.tonic
        return quantized_note

    def __call__(self, note):
        if isinstance(note, tuple):
            return tuple(self(i) for i in note)
        if isinstance(note, list):
            return list(self(i) for i in note)
        if note < 0: return note
        return self.quantize(note)


Major = Scale(0, 'T T S T T T S')
Minor = Scale(0, 'T S T T S T T')
Ionian = Scale(0, 'T T S T T T S')
Dorian = Scale(0, 'T S T T T S T')
Phrygian = Scale(0, 'S T T T S T T')
Lydian = Scale(0,  'T T T S T T S')
Mixolydian = Scale(0, 'T T S T T S T')
Aeolian = Scale(0, 'T S T T S T T')
Locrian = Scale(0, 'S T T S T T T')
MinorPentatonic = Scale(0, 'T+S T T T+S T')
MajorPentatonic = Scale(0, 'T T T+S T T+S')
Blues = Scale(0, 'T+S T S S T+S T')
SpanishPhrygian = Scale(0, 'S T+S S T S T T')
