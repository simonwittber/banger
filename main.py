import IPython
import mido

from collections import deque
from heapq import heappush, heappop
import random

from devices import NovationCircuit
from clock import Clock
from midi import Midi
from banger import Banger
import uservalues


header = "Welcome to Banger.\n\n"
footer = "Goodbye."

clock = Clock(bpm=120)
midi = Midi(clock)
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

scope = dict(
    note = midi.note,
    cc = midi.cc,
    circuit = circuit,
    start = midi.schedule_task,
    stop = midi.stop_task,
    resume = midi.resume_task,
    rand = rand,
    clock = clock,
    midi = midi,
    create_banger = create_banger,
    banger = Banger,
    root = create_banger(0.125),
    open_port = midi.open_port,
    list_ports = midi.list_ports,
    Seq = uservalues.Seq,
    shuffle = random.shuffle,
    repeater = uservalues.repeater,
    pingponger = uservalues.pingponger
)


print(header)
try:
    IPython.start_ipython(user_ns=scope)
finally:
    clock.stop()
print(footer)
