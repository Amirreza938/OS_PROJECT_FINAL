from collections import deque
import threading

class RateMonotonicScheduler:
    def __init__(self, r1_assigned, r2_assigned):
        self.r1_assigned = r1_assigned  # Available R1 resources
        self.r2_assigned = r2_assigned  # Available R2 resources
        self.ready_queue = deque()  # Ready queue for tasks
        self.current_time = 0  # Current simulation time
        self._lock = threading.Lock()  # Lock for thread safety

    def add_task(self, task):
        with self._lock:
            if task.r1_need <= self.r1_assigned and task.r2_need <= self.r2_assigned:
                self.ready_queue.append(task)
                self.r1_assigned -= task.r1_need
                self.r2_assigned -= task.r2_need
                print(f"Task {task.name} added to ready queue. Resources: R1={self.r1_assigned}, R2={self.r2_assigned}")
                return True  # Task added successfully
            else:
                print(f"Task {task.name} cannot be added due to insufficient resources. Resources: R1={self.r1_assigned}, R2={self.r2_assigned}")
                return False  # Task not added

    def get_next_task(self):
        with self._lock:
            if not self.ready_queue:
                return None  # No tasks in the queue

            # Filter tasks that have arrived (arrival_time <= current_time)
            ready_tasks = [task for task in self.ready_queue if task.arrival_time <= self.current_time]

            if not ready_tasks:
                return None  # No tasks have arrived yet

            # Find the task with the shortest period among ready tasks
            shortest_period_task = min(ready_tasks, key=lambda t: t.period)
            self.ready_queue.remove(shortest_period_task)
            return shortest_period_task

    def release_resources(self, task):
        with self._lock:
            self.r1_assigned += task.r1_need
            self.r2_assigned += task.r2_need
            print(f"Resources released: R1={self.r1_assigned}, R2={self.r2_assigned}")

    def increment_time(self):
        with self._lock:
            self.current_time += 1
            print(f"Current time: {self.current_time}")