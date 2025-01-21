import threading
from queue import Queue
from threading import Thread

from resource_manager import ResourceManager
from sub_systems.core import SubSystem1Core
from sub_systems.sub_system_1.weighted_round_robin import WeightedRoundRobinScheduler


class SubSystem1(Thread):
    def __init__(self, resource_requested, queue_weights, r1_assigned, r2_assigned, tasks, finish_flag):
        super().__init__()
        self._lock = threading.Lock()
        self.clock_event = threading.Event()

        self.num_cores = 3
        self.tasks = tasks
        self.ready_queues = [Queue() for _ in range(self.num_cores)]
        self.waiting_queue = Queue()

        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned

        self.cores = [
            SubSystem1Core(
                WeightedRoundRobinScheduler(self.waiting_queue, self.r1_assigned, self.r2_assigned),
                i + 1, self.ready_queues[i], self.waiting_queue) for i in range(self.num_cores)
        ]
        self.resource_manager = ResourceManager(resource_requested)
        self.running = True

        self.queue_weights: list = queue_weights
        self.finish_flag = finish_flag

        self.assign_tasks_to_queues()
        self.add_queues_to_schedulers()

    def assign_tasks_to_queues(self):
        scheduler = WeightedRoundRobinScheduler(self.waiting_queue, self.r1_assigned, self.r2_assigned)
        for core in self.cores:
            for queue, weight in zip(self.ready_queues, self.queue_weights):
                scheduler.add_queue(queue, weight)
        for task in self.tasks:
            scheduler.add_to_ready_queue(task)

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
            self.clock_event.set()

    def check_finish_time(self):
        print("lock finish times" , self._lock.locked())
        empty_flag = True
        for queue in self.ready_queues:
            empty_flag &= queue.empty()
        return self.waiting_queue.empty() and empty_flag

    def run(self):
        self.start_cores()
        while self.running:
            self.clock_event.wait()  # Wait for the clock event
            print('Clock in SubSystem1 triggered')

            print("lock before cores" , self._lock.locked())
            # Toggle cores' clocks
            with self._lock:
                for core in self.cores:
                    core.toggle_clock()
            print("lock after cores" , self._lock.locked())
            # Check if all tasks are finished
            if self.check_finish_time():
                print('All tasks finished in SubSystem1')
                break

            # Clear the clock event for the next iteration
            self.clock_event.clear()

        # Stop the cores and set the finish flag
        self.stop_cores()
        self.finish_flag = True
        print('SubSystem1 stopped')