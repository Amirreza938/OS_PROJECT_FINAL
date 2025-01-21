import threading
from queue import Queue
from threading import Thread

from resource_manager import ResourceManager
from sub_systems.core import SubSystem1Core
from sub_systems.sub_system_1.weighted_round_robin import WeightedRoundRobinScheduler


class SubSystem1(Thread):
    def __init__(self, resource_requested, queue_weights, r1_assigned, r2_assigned, finish_flag):
        super().__init__()
        self._lock = threading.Lock()
        self.clock_event = threading.Event()

        self.num_cores = 3

        self.ready_queues = [Queue() for _ in range(self.num_cores)]
        self.waiting_queue = Queue()

        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned

        self.cores = [
            SubSystem1Core(
                WeightedRoundRobinScheduler(self.waiting_queue, self.r1_assigned, self.r2_assigned, lock=self._lock),
                i + 1, self.ready_queues[i], self.waiting_queue) for i in range(self.num_cores)
        ]
        self.resource_manager = ResourceManager(resource_requested)
        self.running = True

        self.queue_weights: list = queue_weights

        self.finish_flag = finish_flag

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

    def toggle_clock(self):
        with self._lock:
            self.clock_event.set()

    def check_finish_time(self):
        empty_flag = True
        for queue in self.ready_queues:
            empty_flag &= queue.empty()
        return self.waiting_queue.empty() and empty_flag

    def run(self):
        self.start_cores()
        while True:
            self.clock_event.wait()
            with self._lock:
                if not self.running:
                    break
                for core in self.cores:
                    core.toggle_clock()

                if self.check_finish_time():
                    break

                self.clock_event.clear()
        self.stop_cores()
        self.finish_flag = True