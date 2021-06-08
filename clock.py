import time
import threading

class Clock:
    def __init__(self, bpm=120):
        self.bpm = bpm
        self.execute = True
        self.on_tick = lambda tick: None
        self.on_beat = lambda beat: None
        self.beat_resolution = 24

            
    def loop(self):
        beat_counter = 0
        tick_counter = 0
        tick_duration = 60 / (self.beat_resolution * self.bpm)
        next_tick = time.process_time() + tick_duration
        get_time = time.perf_counter
        now = get_time()
        while(self.execute):
            #spin lock wait till next tick time is reached.
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
                time.sleep(wait*0.5)
            self.stats = tick_duration, duration, wait
            tick_duration = 60 / (self.beat_resolution * self.bpm)
    
    def run(self):
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()
    
    def stop(self):
        self.execute = False
        self.thread.join(2000)

