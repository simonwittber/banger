import midi_in


class CC:
    __slots__ = ["channel", "control", "value"]
    def __init__(self):
        self.channel = None
        self.control = None
        self.value = None

    def _setter(self, channel, control, value):
        self.channel = channel
        self.control = control
        self.value = value

    def _connect_midi_in(self):
        if self.channel is not None and self.control is not None:
            midi_in.connect_cc(self.channel, self.control, self._setter)

    def learn(self):
        midi_in.learn_cc(self._setter)

    def __repr__(self):
        return repr(self.value)


