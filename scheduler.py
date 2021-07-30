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
        self.task_count = 0
        self.tasks = []
        self._pending_tasks = []

    def add(self, task, t):
        self.task_count += 1
        schedule_time = self.tick + t, self.task_count
        self._pending_tasks.append(Task(schedule_time, task))

    def ready_tasks(self):
        self.tick += 1
        for i in self._pending_tasks:
            heappush(self.tasks, i)
        self._pending_tasks[:] = []
        while True:
            if len(self.tasks) == 0: return
            if self.tasks[0].t[0] > self.tick: return
            task  = heappop(self.tasks)
            yield task.item

    def clear(self):
        self.tasks[:] = []


import sys
sys.modules["scheduler"] = Scheduler()
