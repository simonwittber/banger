import scale
import random
import banger
import mido
import pickle
import sequence
import os
import clock
import midi_in
import midi_out
import session

from ui import choice, confirm
from utils import CC



bangers = banger.Banger.instances

loaded_objects = {}

def record():
    midi_in.record = True
    midi_in.recordedMessages[:] = []
    input("Press enter to finish.")
    midi_in.record = False
    b = banger.bangify(midi_in.recordedMessages)
    return b


def save(b, name, msg=None):
    writeFile = True
    if os.path.isfile(name):
        writeFile = confirm(msg if msg is not None else "%s exists, overwrite"%name, False)
    if writeFile:
        with open(name, "wb") as f:
            if isinstance(b, banger.Banger):
                b.name = name
            pickle.dump(b, f)


def save_all():
    for k,v in loaded_objects.items():
        save(v, k)


def load(name, default=None):
    if os.path.isfile(name):
        with open(name, "rb") as f:
            try:
                b = pickle.load(f)
            except Exception:
                pass
            else:
                if isinstance(b, banger.Banger):
                    banger.Banger.instances[b.name] = b
                if hasattr(b, "_connect_midi_out"):
                    b._connect_midi_out()
                if hasattr(b, "_connect_midi_in"):
                    b._connect_midi_in()
                loaded_objects[name] = b
                return b

    if default is None:
        return None
    return default()


def clone(b):
    new_b = pickle.loads(pickle.dumps(b))
    if isinstance(new_b, banger.Banger):
        banger.Banger.instances[id(new_b)] = new_b


def pause(*tasks):
    for b in tasks:
        if isinstance(b, banger.Banger):
            b.enabled = False
        else:
            midi_out.stop_task(b)


def resume(*tasks):
    for b in tasks:
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
            #channel, note, velocity, duration, pulse
            c, n, v, d, p = cnvdp
            midi_out.note(c, n, velocity=v, duration=d, delay=p)
            yield midi_out.evaluate_parameter(p)


def play(b, when=0):
    if isinstance(b, banger.Banger):
        b.enabled = True
        return midi_out.schedule_task(when, play_sequence(b))
    else:
        return midi_out.schedule_task(when, b)


def Banger(*notes, channel=0):
    b = banger.Banger(*notes, channel=channel)
    return b


def rnd(start, stop, length=1):
    if length == 1:
        return random.randint(start, stop)
    else:
        return [random.randint(start, stop) for i in range(length)]


def open_input(*args):
    ports = midi_in.list_ports()
    if len(args) == 0:
        p = choice("Choose an input port", ports)
        midi_in.open_port(p)
    else:
        for i in args:
            print("Opening %s"%ports[i])
            midi_in.open_port(ports[i])


def open_output(*args):
    ports = midi_out.list_ports()
    if len(args) == 0:
        p = choice("Choose an output port", ports)
        midi_out.open_port(p)
    else:
        for i in args:
            print("Opening %s"%ports[i])
            midi_out.open_port(ports[i])


def learn_cc():
    c = CC()
    c.learn()
    return c



note = midi_out.note
cc = midi_out.cc
learn = midi_in.learn_cc
start_task = midi_out.schedule_task
stop_task = midi_out.stop_task
resume_task = midi_out.resume_task
shuffle = random.shuffle
ps = midi_out.ps
note_off = midi_out.note_off
Session = session.Expando


