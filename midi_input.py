import mido
import threading
import time



class MidiIn:
    def __init__(self, clock):
        self.clock = clock
        self.input = None
        self.run()

    def open_port(self, name):
        self.input = mido.open_input(name)

    def list_ports(self):
        return mido.get_input_names()

    def loop(self):
        while self.execute:
            if self.input is None: continue
            for msg in self.input.iter_pending():
                self.dispatch(msg)
            time.sleep(0)

    def run(self):
        self.execute = True
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def stop(self):
        self.execute = False
        if self.thread is not None:
            self.thread.join(2000)

    def dispatch(self, msg):
        if msg.type == 'clock': return
        print(msg)

