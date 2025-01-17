from abc import ABC, abstractmethod


class States:
    ready = "ready"
    running = "running"
    waiting = "waiting"


class BaseTask(ABC):
    def __init__(self, task_id, execution_time, r1_need, r2_need, arrival_time):
        self.state = States.ready
        self.task_id = task_id
        self.r1_need = r1_need
        self.r2_need = r2_need
        self.execution_time = execution_time
        self.arrival_time = arrival_time

    @abstractmethod
    def execute(self):
        pass


class SubSystem1Task(BaseTask):
    def __init__(self, task_id, execution_time, r1_need, r2_need, arrival_time, core_number):
        self.core_number = core_number
        super().__init__(task_id, execution_time, r1_need, r2_need, arrival_time)

    def execute(self):
        pass
