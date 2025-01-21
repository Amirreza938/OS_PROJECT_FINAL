import threading
from queue import Queue
from threading import Thread
from core import BaseCore
from rate_monotonic import RateMonotonicScheduler
from task import BaseTask
from resource_manager import ResourceManager

class SubSystem3Core(BaseCore):
    def __init__(self, scheduler: RateMonotonicScheduler, core_id, ready_queue, waiting_queue):
        self.clock_event = threading.Event()
        self._lock = threading.Lock()
        super().__init__(scheduler, core_id, ready_queue, waiting_queue)

    def run_task(self, task: BaseTask):
        task_status = task.execute()
        if task_status == 0:
            print(f"Task {task.name} completed on core {self.core_id}")
            self.queue_scheduler.release_resources(task)
        elif task_status == -1:
            print(f"Task {task.name} failed on core {self.core_id}")

    def add_queue(self, weight):
        self.queue_scheduler.add_queue(self.ready_queue, weight)

    def run(self):
        while True:
            self.clock_event.wait()
            with self._lock:
                if not self.running:
                    break
                task = self.queue_scheduler.get_next_task()
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
    def __init__(self, resource_requested, queue_weights, r1_assigned, r2_assigned):
        super().__init__()
        self._lock = threading.Lock()
        self.clock_event = threading.Event()

        self.num_cores = 1

        self.ready_queues = [Queue() for _ in range(self.num_cores)]
        self.waiting_queue = Queue()

        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned

        self.cores = [
            SubSystem3Core(
                RateMonotonicScheduler(self.waiting_queue, self.r1_assigned, self.r2_assigned, lock=self._lock),
                i + 1, self.ready_queues[i], self.waiting_queue) for i in range(self.num_cores)
        ]
        self.resource_manager = ResourceManager(resource_requested)
        self.running = True

        self.queue_weights: list = queue_weights

        self.add_queues_to_schedulers()

    def add_queues_to_schedulers(self):
        for core in self.cores:
            for queue, weight in zip(self.ready_queues, self.queue_weights):
                core.add_queue(weight)

    def stop(self):
        with self._lock:
            self.running = False
            self.clock_event.set()

    def start_cores(self):
        for core in self.cores:
            core.start()

    def stop_cores(self):
        for core in self.cores:
            core.stop()
            core.join()

    def set_clock_event(self):
        with self._lock:
            self.clock_event.set()

    def run(self):
        self.start_cores()
        while True:
            self.clock_event.wait()
            with self._lock:
                if not self.running:
                    break
                for core in self.cores:
                    core.set_clock_event()
                self.clock_event.clear()
        self.stop_cores()