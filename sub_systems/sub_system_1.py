from queue import Queue
from threading import Thread

from resource_manager import ResourceManager
from sub_systems.core import Core


class SubSystem1(Thread):
    def __init__(self, resource_requested, queue_weights):
        super().__init__()
        self.num_cores = 3
        self.ready_queues = [Queue() for _ in range(self.num_cores)]
        self.waiting_queue = Queue()
        self.cores = [Core(i, self.ready_queues[i]) for i in range(self.num_cores)]
        self.resource_manager = ResourceManager(resource_requested)
        self.running = True

        # Assign weights to queues (example weights)
        self.queue_weights: list = queue_weights

        # Add queues and weights to each core's scheduler
        for core in self.cores:
            for queue, weight in zip(self.ready_queues, self.queue_weights):
                core.add_queue(queue, weight)

    def start_cores(self):
        for core in self.cores:
            core.start()

    def stop_cores(self):
        for core in self.cores:
            core.running = False
            core.join()

    def add_task(self, task, core_id=None):



    def run(self):
        """
        Main loop to start cores and manage the waiting queue.
        """
        self.start_cores()
        while self.running:
            self.redistribute_waiting_tasks()
        self.stop_cores()
