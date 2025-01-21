import threading
from queue import PriorityQueue
from task import BaseTask  

class RateMonotonicScheduler:
    def __init__(self, r1_available, r2_available):
        self.ready_queue = PriorityQueue()  
        self.r1_available = r1_available
        self.r2_available = r2_available
        self._lock = threading.Lock()

    def add_task(self, task: BaseTask):
    
        with self._lock:
            self.ready_queue.put((task.period, task))

    def get_next_task(self):

        with self._lock:
            if not self.ready_queue.empty():
                _, task = self.ready_queue.get()
                if task.r1_need <= self.r1_available and task.r2_need <= self.r2_available:
                    self.r1_available -= task.r1_need
                    self.r2_available -= task.r2_need
                    return task
                else:
                    self.ready_queue.put((task.period, task))
            return None

    def release_resources(self, task: BaseTask):
        with self._lock:
            self.r1_available += task.r1_need
            self.r2_available += task.r2_need

    def change_resource_availability(self, r1_available, r2_available):
        with self._lock:
            self.r1_available = r1_available
            self.r2_available = r2_available