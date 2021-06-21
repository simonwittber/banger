from clock import Clock
from midi_output import MidiOut
import scale
from midi_input import MidiIn
from ui import choice

import random
import uservalues
import banger
import mido
import pickle
import sequence


clock = Clock(bpm=120)
midi_out = MidiOut(clock)
midi_in = MidiIn(clock)
clock.run()

bangers = banger.Banger.instances



def save(b, name):
    with open(name, "wb") as f:
        if isinstance(b, banger.Banger):
            b.name = name
        pickle.dump(b, f)


def load(name):
    with open(name, "rb") as f:
        b = pickle.load(f)
        if isinstance(b, banger.Banger):
            banger.Banger.instances[b.name] = b
        return b


def clone(b):
    new_b = pickle.loads(pickle.dumps(b))
    if isinstance(new_b, Banger):
        banger.Banger.instances[id(new_b)] = new_b


def pause(*tasks):
    for b in tasks:
        if isinstance(b, banger.Banger):
            b.enabled = False
        else:
            midi_out.stop_task(b)


def resume(*tasks):
    for i in tasks:
        if isinstance(b, banger.Banger):
            b.enabled = True
        else:
            midi_out.resume_task(b)


def play_sequence(b):
    while True:
        cnvdp = next(b)
        if cnvdp is None:
            yield 1
        else:
            c, n, v, d, p = cnvdp
            if p:
                midi_out.note(c, n, velocity=v, duration=d)
            yield d


def play(b, when=0):
    if isinstance(b, banger.Banger):
        b.task = midi_out.schedule_task(when, play_sequence(b))
    else:
        return midi_out.schedule_task(when, b)


def Banger(*notes, channel=0):
    b = banger.Banger(*notes, channel=channel)
    play(b)
    return b


def rnd(start, stop, length=1):
    if length == 1:
        return random.randint(start, stop)
    else:
        return [random.randint(start, stop) for i in range(length)]


def open_input(p=None):
    ports = midi_in.list_ports()
    if p is None:
        p = choice("Choose an input port", ports)
        midi_in.open_port(p)
    else:
        print("Opening %s"%ports[p])
        midi_in.open_port(ports[p])


def open_output(p=None):
    ports = midi_out.list_ports()
    if p is None:
        p = choice("Choose an output port", ports)
        midi_out.open_port(p)
    else:
        print("Opening %s"%ports[p])
        midi_out.open_port(ports[p])

note = midi_out.note
cc = midi_out.cc
start_task = midi_out.schedule_task
stop_task = midi_out.stop_task
resume_task = midi_out.resume_task
shuffle = random.shuffle
ps = midi_out.ps
note_off = midi_out.note_off


