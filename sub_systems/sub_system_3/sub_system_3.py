import threading
from queue import Queue
from threading import Thread

from core import BaseCore  
from rate_monotonic import RateMonotonicScheduler
from task import BaseTask  

class SubSystem3Core(BaseCore):
    def __init__(self, scheduler: RateMonotonicScheduler, core_id):
        super().__init__(scheduler, core_id, Queue(), None)  
        self.scheduler = scheduler
        self.core_id = core_id
        self._lock = threading.Lock()
        self.clock_event = threading.Event()

    def run_task(self, task: BaseTask):
        task_status = task.execute()
        if task_status == 0:
            print(f"Task {task.name} completed on Core {self.core_id}")
            self.scheduler.release_resources(task) 
        elif task_status == -1:
            print(f"Task {task.name} failed on Core {self.core_id}")

    def run(self):
        while True:
            self.clock_event.wait()
            with self._lock:
                if not self.running:
                    break
                task = self.scheduler.get_next_task()
                if task:
                    self.run_task(task)
                self.clock_event.clear()

    def set_clock_event(self):
        with self._lock:
            self.clock_event.set()

    def stop(self):
        with self._lock:
            self.running = False
            self.clock_event.set()

class SubSystem3(Thread):
    def __init__(self, r1_assigned, r2_assigned):
        super().__init__()
        self.num_cores = 1 
        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned
        self.scheduler = RateMonotonicScheduler(r1_assigned, r2_assigned)
        self.core = SubSystem3Core(self.scheduler, 1)
        self.running = True
        self._lock = threading.Lock()
        self.clock_event = threading.Event()

    def start_core(self):
        self.core.start()

    def stop_core(self):
        self.core.stop()
        self.core.join()

    def set_clock_event(self):
        with self._lock:
            self.clock_event.set()

    def run(self):
        self.start_core()
        while True:
            self.clock_event.wait()
            with self._lock:
                if not self.running:
                    break
                self.core.set_clock_event()
                self.clock_event.clear()
        self.stop_core()