import midi_in
import midi_out


class CC:
    __slots__ = ["channel", "control", "_value", "_send", "_fn"]
    def __init__(self):
        self.channel = None
        self.control = None
        self._value = None
        self._send = False
        self._fn = None

    def _setter(self, channel, control, _value):
        self.channel = channel
        self.control = control
        self._value = _value

    def _connect_midi_in(self):
        if self.channel is not None and self.control is not None:
            midi_in.connect_cc(self.channel, self.control, self._setter)

    def learn(self):
        midi_in.learn_cc(self._setter)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        midi_out.cc(self.channel, self.control, v)

    def _sender(self):
        self.value = self._fn()
        if self._send:
            midi_out.schedule(self._sender)

    def send(self, fn):
        self._send = True
        self._fn = fn
        self._sender()


    def stop(self):
        self._send = False


    def __repr__(self):
        return repr(self._value)


