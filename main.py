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
import sequence

class Expando:
    def __init__(self):
        pass


header = "Welcome to Banger.\n\n"
footer = "Goodbye."

import commands

scope = {i:getattr(commands, i) for i in dir(commands) if not i.startswith("_")}
for i in sequence.__all__:
    scope[i] = getattr(sequence, i)


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
    print("Closing down.")
    commands.midi_in.stop()
    commands.midi_out.note_off()
print(footer)
