import IPython
import mido

from collections import deque
from heapq import heappush, heappop
import random

from devices import NovationCircuit
from clock import Clock
from midi import Midi
from banger import Banger
from uservalues import Seq, PingPong


header = "Welcome to Banger.\n\n"
footer = "Goodbye."

clock = Clock(bpm=120)
midi = Midi(clock)
circuit = NovationCircuit(midi, channels=(3,4,5))

clock.run()

def create_beater(beats):
    beater = Banger(beats)
    midi.schedule_task(beats, beater)
    return beater

scope = dict(
    note = midi.note,
    cc = midi.cc,
    circuit = circuit,
    start = midi.schedule_task,
    stop = midi.stop_task,
    resume = midi.resume_task,
    rand = random.randint,
    clock = clock,
    midi = midi,
    create_beater = create_beater,
    banger = Banger,
    root = create_beater(0.125),
    open_port = midi.open_port,
    list_ports = midi.list_ports,
    seq = Seq,
    pingpong = PingPong
)


print(header)
try:
    IPython.start_ipython(user_ns=scope)
finally:
    clock.stop()
print(footer)
