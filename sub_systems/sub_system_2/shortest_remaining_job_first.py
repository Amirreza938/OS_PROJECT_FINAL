import threading
from queue import Queue, PriorityQueue
from task import BaseTask
class ShortestRemainingJobFirstScheduler:
    def __init(self, r1_available, r2_available):
        self.r1_available = r1_available
        self.r2_available = r2_available
        self.queue = PriorityQueue()
        self.lock = threading.Lock()
    def add_task(self, task):
        with self._lock:
            self.ready_queue.put((task.remaining_time, task))
    def get_next_task(self):
        with self._lock:
            if not self.ready_queue.empty():
                _, task = self.ready_queue.get()
                if task.r1_need <= self.r1_available and task.r2_need <= self.r2_available:
                    self.r1_available -= task.r1_need
                    self.r2_available -= task.r2_need
                    return task
                else:
                    self.ready_queue.put((task.remaining_time, task))
            return None
    def release_resource(self, task:BaseTask):
        with self._lock:
            self.r1_available += task.r1_need
            self.r2_available += task.r2_need
    def change_resource_availability(self,r1_available,r2_available):
        with self._lock:
            self.r1_available = r1_available    
            self.r2_available = r2_available