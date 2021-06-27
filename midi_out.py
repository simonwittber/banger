import mido
from heapq import heappush, heappop
import threading
import time
import random
import clock
import numbers



class MidiOut:
    def __init__(self):
        self.bpm = 99
        self.output = set()
        self.schedule = []
        self.stop_list = set()

        self.noteMessage = mido.Message("note_on", note=60, velocity=0)
        self.controlMessage = mido.Message("control_change")
        self.task_counter = 0
        clock.on_tick = self.execute_scheduled_tasks
        clock.on_bar = self.schedule_pending_tasks
        self.last_tick = 0
        self.playing_notes = {}
        self.tasks = {}
        self.pending_tasks = []
        self.outbox = {}
        self.debug = False
        self.lock = threading.Lock()
        self.tick_count = 0


    def send(self, msg):
        with self.lock:
            for i in self.output:
                i.send(msg)


    def flush_outbox(self):
        for key,value in self.outbox.items():
            c, n = key
            v, duration = value
            noteMessage = self.noteMessage.copy(channel=c, note=n, velocity=v)
            self.send(noteMessage)
            if v > 0:
                self.playing_notes[c, n] = duration * clock.beat_resolution
        self.outbox.clear()


    def ps(self):
        print("{0:>10} {1:>10} {2:>10} {3}".format("T", "LastT", "ID", "Task"))
        for i in self.schedule:
            t, last_t, task_id, task = i
            print("{0:>10} {1:>10} {2:>10} {3}".format(*i))


    def handle_note_off(self):
        for i in list(self.playing_notes):
            t = self.playing_notes[i] - 1
            if t <= 0:
                self.send(self.noteMessage.copy(channel=i[0],
                    note=i[1], velocity=0))
                del self.playing_notes[i]
            else:
                self.playing_notes[i] = t


    def schedule_pending_tasks(self, bar, now):
        if self.debug:
            print("Bar %s %s"%(bar, now))
        for t, task_id, fn in self.pending_tasks:
            heappush(self.schedule, (self.last_tick+t, 0, task_id, fn))
        self.pending_tasks[:] = []


    def execute_scheduled_tasks(self, tick, now):
        self.tick_count += 1
        self.handle_note_off()
        self.send(mido.Message(type='clock'))
        while len(self.schedule) > 0:
            t, last_t, task_id, next_task = heappop(self.schedule)
            isOneShot = callable(next_task)
            if t > tick:
                heappush(self.schedule, (t, last_t, task_id, next_task))
                break
            if(task_id in self.stop_list):
                if not isOneShot:
                    heappush(self.schedule, (tick+last_t, last_t, task_id, next_task))
                continue
            if isOneShot:
                try:
                    next_task()
                except Exception as e:
                    print("%s %s"%(next_task,e))
                continue
            try:
                beats = next(next_task, None)
            except Exception as e:
                print("%s %s"%(next_task,e))
            else:
                if beats is not None:
                    next_t = beats * clock.beat_resolution
                    heappush(self.schedule, (tick+next_t, next_t, task_id, next_task))
        self.last_tick = tick
        self.flush_outbox()


    def open_port(self, port):
        with self.lock:
            self.output.add(mido.open_output(port))


    def list_ports(self):
        return mido.get_output_names()


    def note(self, channel, note, velocity=100, duration=1, delay=None):
        if delay is None:
            self._note(channel, note, velocity, duration)
        else:
            ticks = delay * clock.beat_resolution
            heappush(self.schedule, (self.last_tick + ticks, 0, -1, lambda: self._note(channel, note, velocity, duration)))

    @staticmethod
    def evaluate_parameter(v):
        if isinstance(v, numbers.Number):
            return v
        if isinstance(v, list):
            return MidiOut.evaluate_parameter(random.choice(v))
        if callable(v):
            return MidiOut.evaluate_parameter(v())
        return None

    def _note(self, channel, note, velocity=100, duration=1):
        if self.output is not None:
            note = self.evaluate_parameter(note)
            if not isinstance(note, tuple):
                note = (note,)
            c = channel
            v = velocity
            for n in note:
                if n is not None and n >= 0:
                    self.outbox[channel, n] = velocity, duration


    def cc(self, channel, control, value):
        if self.output is not None:
            self.send(self.controlMessage.copy(channel=channel, control=control, value=value))


    def schedule_task(self, beats, fn):
        task_id = self.task_counter
        self.task_counter += 1
        ticks = beats * clock.beat_resolution
        self.pending_tasks.append((ticks, task_id, fn))
        return task_id


    def stop_task(self, task_id):
        self.stop_list.add(task_id)


    def resume_task(self, task_id):
        self.stop_list.remove(task_id)


    def panic(self):
        clock.stop()
        if self.output is None: return
        for i in range(0,16):
            for k in range(0,128):
                self.send(mido.Message('note_on', channel=i, note=k, velocity=0))
                self.send(mido.Message('note_off', channel=i, note=k, velocity=0))


    def note_off(self, channel=None):
        clock.stop()
        if self.output is None: return
        if channel is None:
            for i in range(0,16):
                for k in range(0,128):
                    self.send(mido.Message('note_on', channel=i, note=k, velocity=0))
                    time.sleep(0.0001)
                    self.send(mido.Message('note_off', channel=i, note=k, velocity=0))
        else:
            for k in range(0,128):
                self.send(mido.Message('note_on', channel=i, note=k, velocity=0))
                time.sleep(0.0001)
                self.send(mido.Message('note_off', channel=i, note=k, velocity=0))


import sys
sys.modules["midi_out"] = MidiOut()
