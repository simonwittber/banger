import mido
import threading
import time
import clock



class MidiIn:
    def __init__(self):
        self.input = None
        self.cc = {}
        self.note = {}
        self.run()
        self.learn = None

    def open_port(self, name):
        self.input = mido.open_input(name)

    def list_ports(self):
        return mido.get_input_names()

    def loop(self):
        while self.execute:
            if self.input is not None:
                for msg in self.input.iter_pending():
                    self.dispatch(msg)
            time.sleep(0.01)

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
            if self.learn is not None:
                self.connect_cc(msg.control, self.learn)
                print("Connected %s to %s"%(self.learn, msg.control))
                self.learn = None
            if msg.control in self.cc:
                self.cc[msg.control](msg.control, msg.value)
        else:
            print(msg)

    def connect_cc(self, control, fn):
        self.cc[control] = fn

    def disconnect_cc(self, control):
        del self.cc[control]

    def connect_note(self, note, fn):
        self.note[note] = fn

    def learn_cc(self, fn):
        print("Please move a control to perform a midi learn:")
        self.learn = fn

import sys
sys.modules["midi_in"] = MidiIn()



