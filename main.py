
import IPython

from heapq import heappush, heappop
from devices import NovationCircuit
from clock import Clock
from midi_output import MidiOut
from midi_input import MidiIn
from ui import choice

import random
import uservalues
import banger
import mido
import pickle


header = "Welcome to Banger.\n\n"
footer = "Goodbye."

clock = Clock(bpm=120)
midi = MidiOut(clock)
midi_in = MidiIn(clock)
circuit = NovationCircuit(midi, channels=(3,4,5))

clock.run()


def save(b, name):
    with open(name, "wb") as f:
        pickle.dump(b, f)


def load(name):
    with open(name, "rb") as f:
        return pickle.load(f)


def _play(b):
    while True:
        cnvdp = next(b)
        if cnvdp is None:
            yield 1
        else:
            c, n, v, d, p = cnvdp
            if p:
                midi.note(c, n, velocity=v, duration=d)
            yield d


def play(b):
    b.task = midi.schedule_task(0, _play(b))


def Banger(*notes, channel=0):
    b = banger.Banger(*notes, channel=channel)
    play(b)
    return b


def rand(start, stop, length=1):
    if length == 1:
        return random.randint(start, stop)
    else:
        return [random.randint(start, stop) for i in range(length)]


def open_input(p = None):
    ports = midi_in.list_ports()
    if p is None:
        p = choice("Choose an input port", ports)
        midi_in.open_port(p)
    else:
        midi_in.open_port(ports[p])


def open_output(p = None):
    ports = midi.list_ports()
    if p is None:
        p = choice("Choose an output port", ports)
        midi.open_port(p)
    else:
        midi.open_port(ports[p])


scope = dict(
    open_input=open_input,
    open_output=open_output,
    note = midi.note,
    cc = midi.cc,
    circuit = circuit,
    start = midi.schedule_task,
    stop = midi.stop_task,
    resume = midi.resume_task,
    rand = rand,
    clock = clock,
    midi = midi,
    midi_in = midi_in,
    Banger = Banger,
    banger = Banger,
    Seq = uservalues.Seq,
    Rnd = uservalues.Rnd,
    shuffle = random.shuffle,
    play = play, load = load, save = save,
    ps = midi.ps
)


from traitlets.config import Config
c = Config()
c.InteractiveShell.autocall = 2

print(header)
print("\n")
print("Banger commands:\n")
print(", ".join(scope))
print("\nType help(command) for more information.\n")
try:
    IPython.start_ipython(user_ns=scope, config=c)
finally:
    midi_in.stop()
    midi.panic()
print(footer)
