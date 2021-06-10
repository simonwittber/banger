import time
import threading
from posix.time cimport clock_gettime, timespec, CLOCK_REALTIME


cdef float get_time() nogil:
    cdef timespec ts
    cdef float current
    clock_gettime(CLOCK_REALTIME, &ts)
    current = ts.tv_sec + (ts.tv_nsec / 1000000000.)
    return current


class Clock:
    def __init__(self, bpm=120):
        self.bpm = bpm
        self.execute = True
        self.on_tick = lambda tick: None
        self.on_beat = lambda beat: None
        self.beat_resolution = 24


    def loop(self):
        cdef int beat_counter = 0
        cdef int tick_counter = 0
        cdef float tick_duration = 60 / (self.beat_resolution * self.bpm)
        cdef float next_tick = time.process_time() + tick_duration
        cdef float now = get_time()
        while(self.execute):
            #spin lock wait till next tick time is reached.
            with nogil:
                while(now < next_tick):
                    now = get_time()

            self.on_tick(tick_counter)
            tick_counter += 1
            if tick_counter % self.beat_resolution == 0:
                beat_counter += 1
                self.on_beat(beat_counter)

            now = get_time()
            duration = now - next_tick

            wait = tick_duration - duration

            next_tick += tick_duration

            if(wait < 0):
                #clock will be out of sync, so move it forward a bit
                next_tick += wait * -1
            else:
                #soft wait for for half of total wait period till next tick
                time.sleep(wait*0.9)
            tick_duration = 60 / (self.beat_resolution * self.bpm)

    def run(self):
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def stop(self):
        self.execute = False
        self.thread.join(2000)

