import IPython

from heapq import heappush, heappop
from devices import NovationCircuit
from ui import choice
from traitlets.config import Config

import random
import banger
import mido
import pickle
import sequence
import os
import session
import commands
import clock
import midi_in
import midi_out


header = "Welcome to Banger.\n\n"
footer = "Goodbye."

scope = {i:getattr(commands, i) for i in dir(commands) if not i.startswith("_")}
for i in sequence.__all__:
    scope[i] = getattr(sequence, i)

s = commands.load("session", session.Expando)
scope["s"] = s
circuit = scope["circuit"] = NovationCircuit()
scope["k"] =  lambda a,b: lambda: circuit.drum[a].patch(b).trigger()

c = Config()
c.InteractiveShell.autocall = 2
c.TerminalInteractiveShell.confirm_exit = False

print(header)
print("\n")
print("Banger commands:\n")
print(", ".join(scope))
print("\nType help(command) for more information.\n")
try:
    IPython.start_ipython(user_ns=scope, config=c)
finally:
    print("Closing down.")
    commands.save(s, "session", "Would you like to save the global session")
    commands.midi_in.stop()
    commands.midi_out.stop()
    clock.stop()
print(footer)
