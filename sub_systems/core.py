from threading import Thread
from sub_systems.weighted_round_robin import  WeightedRoundRobinScheduler


class Core(Thread):
    def __init__(self, core_id, ready_queue):
        super().__init__()
        self.core_id = core_id
        self.ready_queue = ready_queue
        self.running = True
        self.scheduler = WeightedRoundRobinScheduler()  # WRR scheduler

    def add_queue(self, queue, weight):
        """
        Add a queue with a specific weight to the scheduler.
        """
        self.scheduler.add_queue(queue, weight)

    def process_task(self, task):
        """
        Process a task (placeholder for task execution logic).
        """
        print(f"Core {self.core_id} processing task: {task}")

    def run(self):
        """
        Run the core to process tasks using WRR scheduling.
        """
        while self.running:
            task = self.scheduler.get_next_task()
            if task:
                self.process_task(task)
            else:
                # No task available, avoid busy-waiting
                time.sleep(0.01)