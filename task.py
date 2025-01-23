import logging
from abc import ABC, abstractmethod


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


class States:
    ready = "ready"
    running = "running"
    waiting = "waiting"
    finished = "finished"


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
        self.state = States.running
        logger.info(f"Task '{self.name}' created with state={self.state}, execution_time={self.execution_time}, "
                    f"r1_need={self.r1_need}, r2_need={self.r2_need}, arrival_time={self.arrival_time}")

        logger.info(f"SubSystem1Task '{self.name}' assigned to core {self.core_number}")

    def execute(self):
        if self.state == States.running:
            if self.remaining_time > 0:
                self.remaining_time -= 1
                logger.info(f"Task '{self.name}' executed on core {self.core_number}. Remaining time: {self.remaining_time}")
                return self.remaining_time
            else:
                logger.info(f"Task '{self.name}' completed on core {self.core_number}")
                return 0
        else:
            logger.warning(f"Task '{self.name}' is not in 'running' state. Current state: {self.state}")
            return -1

    def set_state(self, new_state):
        logger.info(f"Task '{self.name}' state changed from {self.state} to {new_state}")
        self.state = new_state
