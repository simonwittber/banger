import mido
import threading
import time



class MidiIn:
    def __init__(self, clock):
        self.clock = clock
        self.input = None
        self.run()
        self.cc = {}
        self.note = {}

    def open_port(self, name):
        self.input = mido.open_input(name)

    def list_ports(self):
        return mido.get_input_names()

    def loop(self):
        while self.execute:
            if self.input is not None:
                for msg in self.input.iter_pending():
                    self.dispatch(msg)
            time.sleep(0.1)

    def run(self):
        self.execute = True
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def stop(self):
        self.execute = False
        if self.thread is not None:
            self.thread.join(2000)

    def dispatch(self, msg):
        if msg.type == 'clock': return
        if msg.type == 'note_on':
            if msg.note in self.note:
                self.note[msg.note](msg.velocity)
        elif msg.type == 'note_off':
            if msg.note in self.note:
                self.note[msg.note](0)
        elif msg.type == "control_change":
            if msg.control in self.cc:
                self.cc[msg.control](msg.value)
        else:
            print(msg)

    def connect_cc(self, control, fn):
        self.cc[control] = fn

    def connect_note(self, note, fn):
        self.note[note] = fn



