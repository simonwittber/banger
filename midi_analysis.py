from mido import MidiFile
from heapq import heappush, heappop

import random


class Chain:
    def __init__(self, order, items, fn):
        self.states = {}
        key = []
        self.last_value = None
        for i in items:
            key.append(fn(i))
            if len(key) == order+1:
                state = tuple(key[0:order])
                next_state = key[-1]
                if state in self.states:
                    transitions = self.states[state]
                else:
                    transitions = self.states[state] = []
                transitions.append(next_state)
                key.pop(0)

    def __next__(self):
        if self.last_value is None:
            last_value = list(random.choice(list(self.states)))
        choice = random.choice(self.states[tuple(last_value)])
        last_value.append(choice)
        last_value.pop(0)
        return choice



class TrackAnalyzer:
    def __init__(self, track, order):
        self.track = track
        self.notes = Chain(order, [i for i in track if i.type == 'note_on' and i.velocity > 0], lambda x: x.note)
        self.velocities = Chain(order, [i for i in track if i.type == 'note_on' and i.velocity > 0], lambda x: x.velocity)
        self.durations = self._calculate_duration_chain(track, order)

    def _calculate_duration_chain(self, track, order):
        durations = []
        playing = {}

        tick = 0
        for i in list(track):
            tick = tick + i.time
            if i.type == 'note_on' and i.velocity > 0:
                note = i.note
                if note in playing:
                    duration = tick - playing[note]
                    durations.append(duration)
                playing[note] = tick
            if i.type == 'note_on' and i.velocity == 0 or i.type == 'note_off':
                note = i.note
                if note in playing:
                    duration = tick - playing[note]
                    durations.append(duration)
                    playing.pop(note)

        return Chain(order, durations, lambda x: x)



class Analyzer:

    def __init__(self, filename):
        self.midi_file = MidiFile(filename)
        self.tracks = {}
        for i in self.midi_file.tracks:
            print("Loading Track %s"%i.name)
            for order in [1,2,3]:
                self.tracks[i.name, order] = TrackAnalyzer(i,order)


