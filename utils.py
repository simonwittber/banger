import midi_in


class CC:
    __slots__ = ["control", "value"]
    def __init__(self):
        self.control = None
        self.value = None

    def _setter(self, control, value):
        self.control = control
        self.value = value

    def _connect_midi_in(self):
        if self.control is not None:
            midi_in.connect_cc(self.control, self._setter)

    def learn(self):
        midi_in.learn_cc(self._setter)


