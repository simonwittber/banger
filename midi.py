import mido
from heapq import heappush, heappop
from uservalues import _ev


class Midi:
    bpm = 99
    def __init__(self, clock):
        self.output = None
        self.schedule = []
        self.stop_list = set()

        self.noteMessage = mido.Message("note_on", note=60, velocity=0)
        self.controlMessage = mido.Message("control_change")
        self.task_counter = 0
        self.clock = clock
        self.clock.on_tick = self.execute_scheduled_tasks
        self.last_tick = 0
        self.playing_notes = {}

    def handle_note_off(self):
        for i in list(self.playing_notes):
            t = self.playing_notes[i] - 1
            if t <= 0:
                self.output.send(self.noteMessage.copy(channel=i[0],
                    note=i[1], velocity=0))
                del self.playing_notes[i]
            else:
                self.playing_notes[i] = t


    def execute_scheduled_tasks(self, tick):
        self.handle_note_off()
        while len(self.schedule) > 0:
            t, last_t, task_id, next_task = heappop(self.schedule)
            if t > tick:
                heappush(self.schedule, (t, last_t, task_id, next_task))
                break
            if(task_id in self.stop_list):
                heappush(self.schedule, (tick+last_t, last_t, task_id, next_task))
                continue
            if callable(next_task):
                next_task()
                continue
            beats = next(next_task, None)
            if beats is not None:
                beats = _ev(beats)
                next_t = beats * self.clock.beat_resolution
                heappush(self.schedule, (tick+next_t, next_t, task_id, next_task))
        self.last_tick = tick

    def open_port(self, port):
        self.output = mido.open_output(port)

    def list_ports(self):
        return mido.get_output_names()

    def note(self, channel, note, velocity=100, duration=1):
        if self.output is not None:
            n = int(_ev(note, 128))
            if n is not None:
                c = int(_ev(channel, 16))
                v =  int(_ev(velocity, 128))
                noteMessage = self.noteMessage.copy(channel=c,note=n,
                        velocity=v)
                self.output.send(noteMessage)
                if velocity > 0:
                    d = _ev(duration)
                    self.playing_notes[(noteMessage.channel, noteMessage.note)] = \
                    d * self.clock.beat_resolution


    def cc(self, channel, control, value):
        if self.output is not None:
            self.output.send(self.controlMessage.copy(channel=_ev(channel, 16),
                control=_ev(control, 128), value=_ev(value, 128)))

    def schedule_task(self, beats, fn):
        task_id = self.task_counter
        self.task_counter += 1
        ticks = beats * self.clock.beat_resolution
        heappush(self.schedule, (self.last_tick + ticks, 0, task_id, fn))
        return task_id

    def stop_task(self, task_id):
        self.stop_list.add(task_id)

    def resume_task(self, task_id):
        self.stop_list.remove(task_id)

    def panic(self):
        if self.output is None: return
        for i in range(0,16):
            for k in range(0,128):
                self.output.send(self.noteMessage.copy(channel=i, note=k,
                    velocity=0))


