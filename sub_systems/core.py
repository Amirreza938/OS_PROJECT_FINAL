import threading
from abc import abstractmethod
from sub_systems.sub_system_1.weighted_round_robin import WeightedRoundRobinScheduler
from threading import Thread, Event, Lock

class BaseCore(Thread):
    def __init__(self, queue_scheduler, core_id, ready_queue, waiting_queue):
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


class SubSystem1Core(Thread):
    def __init__(self, queue_scheduler: WeightedRoundRobinScheduler, core_id, ready_queue, waiting_queue):
        super().__init__()
        self.queue_scheduler = queue_scheduler
        self.core_id = core_id
        self.ready_queue = ready_queue
        self.waiting_queue = waiting_queue
        self.clock_event = Event()
        self._lock = Lock()
        self.running = True

    def get_current_task(self):
        """Get the next task to process from the scheduler."""
        return self.queue_scheduler.get_next_task()

    def add_task(self, task):
        """Add a task to the ready queue."""
        self.ready_queue.append(task)

    def add_queue(self, weight):
        """Add a queue with its weight to the scheduler."""
        self.queue_scheduler.add_queue(self.ready_queue, weight)

    def run(self):
        """Core execution loop: process tasks on each clock tick."""
        while self.running:
            self.clock_event.wait()  # Wait for the clock tick
            with self._lock:
                if not self.running:
                    break

                task = self.get_current_task()
                if task:
                    result = task.execute()
                    if not result:
                        self.ready_queue.popleft()
                else:
                    print(f"Core {self.core_id} has no tasks to process")

            self.clock_event.clear()  # Reset the clock event for the next tick

    def toggle_clock(self):
        """Trigger the clock event to process the next task."""
        self.clock_event.set()

    def stop(self):
        """Stop the core's execution."""
        with self._lock:
            self.running = False
            self.clock_event.set()