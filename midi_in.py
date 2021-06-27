import mido
import threading
import time
import clock
import midi_out



class MidiIn:
    def __init__(self):
        self.inputs = set()
        self.cc = {}
        self.note = {}
        self.run()
        self.learn = None
        self.watch = False
        self.recordedMessages = []
        self.record = False

    def open_port(self, name):
        self.inputs.add(mido.open_input(name))


    def list_ports(self):
        return mido.get_input_names()

    def loop(self):
        while self.execute:
            for inp in self.inputs:
                for msg in inp.iter_pending():
                    if msg.type != 'clock':
                        if self.watch:
                            print("Midi In: %r"%msg)
                        if self.record:
                            self.recordedMessages.append(msg.copy(time=midi_out.tick_count))
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
                self.connect_cc(msg.channel, msg.control, self.learn)
                print("Connected %s to %s"%(self.learn, msg.control))
                self.learn = None
            key = msg.channel, msg.control
            if key in self.cc:
                self.cc[key](msg.channel, msg.control, msg.value)
        elif msg.type == 'aftertouch':
            pass
        else:
            print(msg)

    def connect_cc(self, channel, control, fn):
        self.cc[channel,control] = fn

    def disconnect_cc(self, channel, control):
        del self.cc[channel,control]

    def connect_note(self, note, fn):
        self.note[note] = fn

    def learn_cc(self, fn):
        print("Please move a control to perform a midi learn:")
        self.learn = fn

import sys
sys.modules["midi_in"] = MidiIn()



