from abc import ABC, abstractmethod


class States:
    ready = "ready"
    running = "running"
    waiting = "waiting"


class BaseTask(ABC):
    def __init__(self, name, execution_time, r1_need, r2_need, arrival_time):
        self.state = States.ready
        self.name = name
        self.r1_need = r1_need
        self.r2_need = r2_need
        self.execution_time = execution_time
        self.arrival_time = arrival_time

    @abstractmethod
    def execute(self):
        pass


class SubSystem1Task(BaseTask):
    def __init__(self, name, execution_time, r1_need, r2_need, arrival_time, core_number):
        self.core_number = core_number
        self.remaining_time = execution_time
        super().__init__(name, execution_time, r1_need, r2_need, arrival_time)

    def execute(self):
        if self.state == States.running:
            if self.remaining_time > 0:
                self.remaining_time -= 1
            return self.remaining_time
        return -1
