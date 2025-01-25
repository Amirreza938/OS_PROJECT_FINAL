from collections import deque
from threading import Thread, Event, Lock

from resource_manager import ResourceManager
from sub_systems.core import SubSystem1Core
from sub_systems.sub_system_1.weighted_round_robin import WeightedRoundRobinScheduler


class SubSystem1(Thread):
    def __init__(self, resource_requested, queue_weights, r1_assigned, r2_assigned, tasks, finish_flag):
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
                i , self.ready_queues[i], self.waiting_queue) for i in range(self.num_cores)
        ]
        self.resource_manager = ResourceManager(resource_requested)
        self.running = True

        self.queue_weights = queue_weights
        self.finish_flag = finish_flag

        self.assign_tasks_to_queues()
        self.add_queues_to_schedulers()

    def assign_tasks_to_queues(self):
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
            self.clock_event.wait()
            print('Clock in SubSystem1 triggered')


            with self._lock:
                for core in self.cores:
                    core.toggle_clock()


            if self.check_finish_time():
                print('All tasks finished in SubSystem1')
                break

            self.clock_event.clear()

        self.stop_cores()
        self.finish_flag = True
        print('SubSystem1 stopped')