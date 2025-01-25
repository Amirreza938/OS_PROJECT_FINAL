from collections import deque
from threading import Thread, Event, Lock

from resource_manager import ResourceManager
from sub_systems.core import SubSystem1Core
from sub_systems.sub_system_1.weighted_round_robin import WeightedRoundRobinScheduler


class SubSystem1(Thread):
    def __init__(self, total_r1, total_r2, queue_weights, r1_assigned, r2_assigned, tasks, finish_flag, subsystem_id):
        super().__init__()
        self._lock = Lock()
        self.clock_event = Event()

        self.num_cores = 3
        self.tasks = tasks
        self.ready_queues = [deque() for _ in range(self.num_cores)]
        self.waiting_queue = deque()

        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned

        self.cores = [
            SubSystem1Core(
                WeightedRoundRobinScheduler(self.waiting_queue, self.r1_assigned, self.r2_assigned),
                i + 1, self.ready_queues[i], self.waiting_queue) for i in range(self.num_cores)
        ]
        # Initialize ResourceManager with total_r1 and total_r2
        self.resource_manager = ResourceManager(total_r1, total_r2)
        self.running = True

        self.queue_weights = queue_weights
        self.finish_flag = finish_flag
        self.subsystem_id = subsystem_id  # Added subsystem_id for resource borrowing

        self.assign_tasks_to_queues()
        self.add_queues_to_schedulers()

    def assign_tasks_to_queues(self):
        scheduler = WeightedRoundRobinScheduler(self.waiting_queue, self.r1_assigned, self.r2_assigned)
        for core in self.cores:
            for task in self.tasks:
                if task.core_number == core.core_id:
                    core.ready_queue.append(task)



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
        empty_flag = True
        for queue in self.ready_queues:
            empty_flag &= len(queue) == 0
        return len(self.waiting_queue) == 0 and empty_flag

    def run(self):
        self.start_cores()
        while self.running:
            self.clock_event.wait()  # Wait for the clock event
            print('Clock in SubSystem1 triggered')

            # Toggle cores' clocks
            with self._lock:
                for core in self.cores:
                    core.toggle_clock()

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