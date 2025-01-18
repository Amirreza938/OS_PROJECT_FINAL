import threading
from queue import Queue
from threading import Thread

from resource_manager import ResourceManager
from sub_systems.core import SubSystem1Core
from sub_systems.weighted_round_robin import WeightedRoundRobinScheduler


class SubSystem1(Thread):
    def __init__(self, resource_requested, queue_weights, r1_assigned, r2_assigned):
        super().__init__()
        self.num_cores = 3
        self.is_clock_time = False
        self.ready_queues = [Queue() for _ in range(self.num_cores)]
        self.waiting_queue = Queue()
        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned
        self.cores = [
            SubSystem1Core(WeightedRoundRobinScheduler(self.waiting_queue, self.r1_assigned, self.r2_assigned), i + 1,
                           self.ready_queues[i], self.waiting_queue) for i in range(self.num_cores)
        ]
        self.resource_manager = ResourceManager(resource_requested)
        self.running = True

        self.queue_weights: list = queue_weights

        self._lock = threading.Lock()
        self.clock_event = threading.Event()

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

        self.stop_cores()
