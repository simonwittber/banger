import time
import threading
from posix.time cimport clock_gettime, timespec, CLOCK_REALTIME
from posix.time cimport nanosleep


cdef double get_time() nogil:
    cdef timespec ts
    cdef double current
    clock_gettime(CLOCK_REALTIME, &ts)
    current = ts.tv_sec + (ts.tv_nsec / 1000000000.)
    return current


cdef void zzz(double msec) nogil:
    cdef double current
    cdef long a = <long>msec / 1000
    cdef long b = (<long>msec % 1000) * 1000000
    cdef timespec ts
    ts.tv_sec = a
    ts.tv_nsec = b
    nanosleep(&ts, &ts)


class Clock:
    def __init__(self, bpm=120):
        self.bpm = bpm
        self.time_signature = [4,4]
        self.execute = True
        self.on_tick = lambda tick: None
        self.on_beat = lambda beat: None
        self.on_bar = lambda bar: None
        self.beat_resolution = 24


    def loop(self):
        cdef int bar_counter = 0
        cdef int beat_counter = 0
        cdef int tick_counter = 0
        cdef double tick_duration = 60 / (self.beat_resolution * self.bpm)
        cdef double next_tick = get_time() + tick_duration
        cdef double now = get_time()
        cdef double last_tick = now
        cdef double last_bar = now
        while(self.execute):
            #spin lock wait till next tick time is reached.
            with nogil:
                while(now < next_tick):
                    now = get_time()

            self.on_tick(tick_counter, now-last_tick)
            last_tick = now
            tick_counter += 1
            if tick_counter % self.beat_resolution == 0:
                beat_counter += 1
                self.on_beat(beat_counter)
                if beat_counter % self.time_signature[0] == 0:
                    bar_counter += 1
                    self.on_bar(bar_counter, now-last_bar)
                    last_bar = now
            
            tick_duration = 60 / (self.beat_resolution * self.bpm)
            with nogil:
                now = get_time()
                duration = now - next_tick

                wait = tick_duration - duration

                next_tick += tick_duration

                if(wait < 0):
                    #clock will be out of sync, so move it forward a bit
                    next_tick += wait * -1
                else:
                    #soft wait for for part of total wait period till next tick
                    zzz(wait*0.9*1000)

    def run(self):
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def stop(self):
        self.execute = False
        self.thread.join(2000)

