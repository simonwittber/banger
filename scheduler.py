from heapq import heappush, heappop


class Task:
    __slots__ = "t","item"
    def __init__(self, t, item):
        self.t = t
        self.item = item

    def __lt__(self, other):
        return self.t < other.t


class Scheduler:
    def __init__(self):
        self.tick = 0
        self.tasks = []
        self._pending_tasks = []

    def add(self, task, t):
        self._pending_tasks.append(Task(self.tick+t,task))

    def ready_tasks(self):
        self.tick += 1
        for i in self._pending_tasks:
            heappush(self.tasks, i)
        self._pending_tasks[:] = []
        while True:
            if len(self.tasks) == 0: return
            if self.tasks[0].t > self.tick: return
            task  = heappop(self.tasks)
            yield task.item

    def clear(self):
        self.tasks[:] = []


import sys
sys.modules["scheduler"] = Scheduler()
