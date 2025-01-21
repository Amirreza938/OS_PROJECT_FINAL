import threading
from threading import Thread
from queue import Queue
from core import BaseCore
from shortest_remaining_job_first import ShortestRemainingJobFirstScheduler
from task import BaseTask
from resource_manager import ResourceManager

class SubSystem2Core(BaseCore):
    def __init__(self, scheduler: ShortestRemainingJobFirstScheduler, core_id, ready_queue):
        super().__init__(scheduler, core_id, ready_queue, None)
        self.lock = threading.Lock()
        self.scheduler = scheduler
        self.core_id = core_id
        self.clock_event = threading.Event()

    def run_task(self, task: BaseTask):
        task_status = task.execute()
        if task_status == 0:
            print(f"Task {task.name} completed on core {self.core_id}")
            self.scheduler.release_resource(task)
        elif task_status == -1:
            print(f"Task {task.name} failed on core {self.core_id}")

    def run(self):
        while True:
            self.clock_event.wait()
            with self.lock:
                if not self.running:
                    break
                task = self.scheduler.get_next_task()
                if task:
                    self.run_task(task)
                self.clock_event.clear()

    def set_clock_event(self):
        with self.lock:
            self.clock_event.set()

    def stop(self):
        with self.lock:
            self.running = False
            self.clock_event.set()

class SubSystem2(Thread):
    def __init__(self, resource_requested, queue_weights, r1_assigned, r2_assigned):
        super().__init__()
        self.number_of_cores = 2
        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned
        self.scheduler = ShortestRemainingJobFirstScheduler(r1_assigned, r2_assigned)
        self.cores = [SubSystem2Core(self.scheduler, i + 1, Queue()) for i in range(self.number_of_cores)]
        self.running = True
        self.lock = threading.Lock()
        self.clock_event = threading.Event()
        self.resource_manager = ResourceManager(resource_requested)
        self.queue_weights = queue_weights

        self.add_queues_to_schedulers()

    def add_queues_to_schedulers(self):
        for core in self.cores:
            for queue, weight in zip(self.ready_queues, self.queue_weights):
                core.add_queue(weight)

    def start_cores(self):
        for core in self.cores:
            core.start()

    def stop_cores(self):
        for core in self.cores:
            core.stop()
            core.join()

    def set_clock_event(self):
        with self.lock:
            self.clock_event.set()

    def run(self):
        self.start_cores()
        while True:
            self.clock_event.wait()
            with self.lock:
                if not self.running:
                    break
                for core in self.cores:
                    core.set_clock_event()
                self.clock_event.clear()
        self.stop_cores()

    def stop(self):
        with self.lock:
            self.running = False
            self.clock_event.set()