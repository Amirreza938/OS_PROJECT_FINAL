import threading
from queue import Queue

from task import SubSystem1Task


class WeightedRoundRobinScheduler:
    def __init__(self, waiting_queue , r1_available, r2_available):
        self.queues: list[Queue] = []
        self.weights: list[int] = []
        self.current_index = 0
        self.current_weight = 0
        self.waiting_queue: Queue = waiting_queue
        self.r1_available = r1_available
        self.r2_available = r2_available

        self._lock = threading.Lock()

    def add_queue(self, queue, weight):
        with self._lock:
            self.queues.append(queue)
            self.weights.append(weight)

    def change_resource_availablity(self,r1_available , r2_available):
        with self._lock:
            self.r1_available = r1_available
            self.r2_available = r2_available

    def get_next_task(self):
        with self._lock:
            if not self.queues:
                return None

            while True:
                self._set_current_index()
                # Check if the current queue has tasks and its weight allows processing
                if self.weights[self.current_index] >= self.current_weight:
                    queue = self.queues[self.current_index]
                    if not queue.empty():
                        task: SubSystem1Task = queue.get()
                        if self.add_to_waiting_queue(task):
                            continue
                        return task

    def _set_current_index(self):
        self.current_index = (self.current_index + 1) % len(self.queues)
        if self.current_index == 0:
            self.current_weight -= 1
            if self.current_weight <= 0:
                # Reset the weight to the maximum weight in the system
                self.current_weight = max(self.weights)

    def add_to_waiting_queue(self, task: SubSystem1Task):
        if task.r1_need > self.r1_available or task.r2_need > self.r2_available:
            self.waiting_queue.put(task)
            return True
        return False