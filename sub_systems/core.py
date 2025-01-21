import threading
from abc import abstractmethod
from threading import Thread

from sub_systems.sub_system_1.weighted_round_robin import WeightedRoundRobinScheduler
from task import BaseTask


class BaseCore(Thread):
    def __init__(self, queue_scheduler, core_id, ready_queue , waiting_queue):
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
        self.clock_event = threading.Event()
        self._lock = threading.Lock()
        super().__init__(queue_scheduler, core_id, ready_queue, waiting_queue)

    def run_task(self, task: BaseTask):
        task_status = task.execute()
        if task_status == 0:
            print(f"task {task.name} completed")
        elif task_status == -1:
            print(f"running task {task.name} failed because that task state is {task.state}")

    def add_queue(self , weight):
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
