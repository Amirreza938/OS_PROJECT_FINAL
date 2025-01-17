from abc import ABC, abstractmethod
from threading import Thread


class BaseCore(Thread):
    def __init__(self, scheduler, core_id):
        super().__init__()
        self.running = True
        self.scheduler = scheduler
        self.core_id = core_id

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def start(self):
        pass

    def run_task(self, task):
        pass
