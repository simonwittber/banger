import midi_in
import midi_out


class Expando:
    def __init__(self):
        pass

    def __repr__(self):
        return repr(list(i for i in dir(self) if not i.startswith('_')))

    def __setattr__(self, key, value):
        if hasattr(self, key):
            current_type = type(self.__dict__[key])
            if type(value) != current_type:
                print("Error: Cannot assign a different type to an existing name.")
                return;
        else:
            self.__dict__[key] = value

    def _connect_midi_in(self):
        for i in dir(self):
            if i.startswith("_"): continue
            o = getattr(self, i)
            if hasattr(o, "_connect_midi_in"):
                o._connect_midi_in()

    def _connect_midi_out(self):
        for i in dir(self):
            if i.startswith("_"): continue
            o = getattr(self, i)
            if hasattr(o, "_connect_midi_out"):
                o._connect_midi_out()


