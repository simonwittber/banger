import mido
import threading
import time
import random
import numbers

import clock
import scheduler


class MidiOut:
    def __init__(self):
        self.outputs = set()
        clock.on_tick = self._execute_scheduled_tasks
        clock.on_bar = self._schedule_pending_tasks
        self.lock = threading.Lock()
        self._pending_tasks = []
        self._active_notes = set()
        self.enable_clock = False
        self.watch = False
        self.tick = 0


    def note(self, channel, note, velocity=100, gate=1, beat=0):
        c = self.ev(channel)
        n = self.ev(note)
        v = self.ev(velocity)
        g = self.ev(gate, to_int=False)
        b = self.ev(beat, clamp=False, to_int=False)
        msg = mido.Message("note_on", channel=c, note=n, velocity=v)
        self.schedule(msg, b)
        self.schedule(msg.copy(velocity=0), b+g)


    def cc(self, channel, control, value, beat=0):
        c = self.ev(channel)
        cc = self.ev(control)
        v = self.ev(value)
        self.send(mido.Message("control_change", channel=c, control=cc, value=v))


    def pitchwheel(self, channel, value, beat=0):
        c = self.ev(channel)
        v = self.ev(value)
        self.schedule(mido.Message("pitchwheel", channel=c, value=v), beat)


    def aftertouch(self, channel, value, beat=0):
        c = self.ev(channel)
        v = self.ev(value)
        self.schedule(mido.Message("aftertouch", channel=c, value=v), beat)


    def polytouch(self, channel, note, value, beat=0):
        c = self.ev(channel)
        n = self.ev(note)
        v = self.ev(value)
        self.schedule(mido.Message("polytouch", channel=c, note=n, value=v), beat)


    def schedule(self, task, beat=None):
        if beat is not None:
            t = beat * clock.beat_resolution
            self._pending_tasks.append((task, t))
        else:
            scheduler.add(task, 0)


    def send(self, msg):
        if msg.type == "note_on":
            if msg.velocity > 0:
                self._active_notes.add((msg.channel, msg.note))
            else:
                self._active_notes.discard((msg.channel, msg.note))
        elif msg.type == "note_off":
            self._active_notes.discard((msg.channel, msg.note))
        with self.lock:
            msg.time = self.tick / 24
            if self.watch: print("Midi Out -> %s"%msg)
            for i in self.outputs:
                i.send(msg)


    def stop(self):
        with self.lock:
            for channel,note in self._active_notes:
                msg = mido.Message("note_on", velocity=0, note=note, channel=channel)
                for i in self.outputs:
                    i.send(msg)
            self._active_notes.clear()
            scheduler.clear()


    def _schedule_pending_tasks(self, bar, now):
        for task, t in self._pending_tasks:
            scheduler.add(task, t)
        self._pending_tasks[:] = []


    def _execute_scheduled_tasks(self, tick, now):
        self.tick += 1
        for task in scheduler.ready_tasks():
            if isinstance(task, mido.Message):
                self.send(task)
                continue
            if callable(task):
                task()
                continue
        if self.enable_clock:
            self.send(mido.Message(type='clock'))


    def open_port(self, port):
        with self.lock:
            self.outputs.add(mido.open_output(port))


    def list_ports(self):
        return mido.get_output_names()


    @staticmethod
    def ev(v, clamp=True, to_int=True):
        if isinstance(v, numbers.Number):
            if to_int:
                n = int(v)
            else:
                n = float(v)
            if clamp:
                n = min(max(n, 0), 127)
            return n
        if isinstance(v, list):
            return MidiOut.ev(random.choice(v))
        if isinstance(v, tuple):
            return v
        if callable(v):
            return v
        return None




import sys
sys.modules["midi_out"] = MidiOut()
