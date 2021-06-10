
import IPython

from heapq import heappush, heappop
from devices import NovationCircuit
from clock import Clock
from midi_output import MidiOut
from midi_input import MidiIn
from banger import Banger
from ui import choice

import random
import uservalues


header = "Welcome to Banger.\n\n"
footer = "Goodbye."

clock = Clock(bpm=120)
midi = MidiOut(clock)
midi_in = MidiIn(clock)
circuit = NovationCircuit(midi, channels=(3,4,5))

clock.run()


def create_banger(beats):
    beater = Banger(beats)
    midi.schedule_task(beats, beater)
    return beater


def rand(start, stop, length=1):
    if length == 1:
        return random.randint(start, stop)
    else:
        return [random.randint(start, stop) for i in range(length)]


def open_input():
    ports = midi_in.list_ports()
    p = choice("Choose an input port", ports)
    if p is not None:
        midi_in.open_port(p)


def open_output():
    ports = midi.list_ports()
    p = choice("Choose an output port", ports)
    if p is not None:
        midi.open_port(p)



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
    create_banger = create_banger,
    banger = Banger,
    root = create_banger(0.125),
    Seq = uservalues.Seq,
    shuffle = random.shuffle,
    repeater = uservalues.repeater,
    pingponger = uservalues.pingponger,
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
    clock.stop()
    midi_in.stop()
print(footer)
