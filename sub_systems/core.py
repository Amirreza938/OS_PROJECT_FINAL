from abc import ABC, abstractmethod
from sched import scheduler
from threading import Thread

from sub_systems.weighted_round_robin import WeightedRoundRobinScheduler
from task import BaseTask, SubSystem1Task


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
        self.is_clock_time = False

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
        while self.running:
            while not self.is_clock_time: pass
            task :SubSystem1Task= self.queue_scheduler.get_next_task()
            if task:
                self.run_task(task)
            self.is_clock_time = False
