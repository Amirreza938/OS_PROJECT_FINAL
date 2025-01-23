import threading
from abc import abstractmethod
from threading import Thread

from sub_systems.sub_system_1.weighted_round_robin import WeightedRoundRobinScheduler
from task import SubSystem1Task, States


class BaseCore(Thread):
    def __init__(self, queue_scheduler, core_id, ready_queue, waiting_queue):
        super().__init__()
        self.running = True
        self.queue_scheduler = queue_scheduler
        self.core_id = core_id
        self.ready_queue = ready_queue
        self.waiting_queue = waiting_queue

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def run_task(self, task):
        pass


class SubSystem1Core(BaseCore):
    def __init__(self, queue_scheduler: WeightedRoundRobinScheduler, core_id, ready_queue, waiting_queue):
        super().__init__(queue_scheduler, core_id, ready_queue, waiting_queue)
        self.clock_event = threading.Event()
        self._lock = threading.Lock()

    def get_current_task(self):
        pass

    def add_task(self, task):
        self.ready_queue.put(task)
    
    def add_queue(self, weight):
        self.queue_scheduler.add_queue(self.ready_queue, weight)

    def run(self):
        while True:
            self.clock_event.wait()
            with self._lock:
                if not self.running:
                    break

            self.clock_event.clear()

    def toggle_clock(self):
        self.clock_event.set()

    def stop(self):
        with self._lock:
            self.running = False
            self.clock_event.set()
