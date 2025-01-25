from collections import deque
class ShortestRemainingJobFirstScheduler:
    def __init__(self, r1_assigned, r2_assigned):
        self.r1_assigned = r1_assigned  # Available R1 resources
        self.r2_assigned = r2_assigned  # Available R2 resources
        self.ready_queue = deque()  # Single ready queue for all tasks
        self.current_time = 0  # Current simulation time

    def add_to_ready_queue(self, task, is_requeue=False):
        """Add a task to the ready queue if all required resources are available."""
        if task.r1_need <= self.r1_assigned and task.r2_need <= self.r2_assigned:
            self.ready_queue.append(task)
            if not is_requeue:
                # Deduct resources only if this is not a re-queue
                self.r1_assigned -= task.r1_need
                self.r2_assigned -= task.r2_need
            print(f"Task {task.name} added to ready queue. Resources: R1={self.r1_assigned}, R2={self.r2_assigned}")
        else:
            print(f"Task {task.name} cannot be added due to insufficient resources. Resources: R1={self.r1_assigned}, R2={self.r2_assigned}")

    def get_next_task(self):
        """Get the next task to process based on shortest remaining time first scheduling."""
        if not self.ready_queue:
            return None  # No tasks in the queue

        # Filter tasks that have arrived (arrival_time <= current_time)
        ready_tasks = [task for task in self.ready_queue if task.arrival_time <= self.current_time]

        if not ready_tasks:
            return None  # No tasks have arrived yet

        # Find the task with the shortest remaining time among ready tasks
        shortest_task = min(ready_tasks, key=lambda t: t.remaining_time)
        self.ready_queue.remove(shortest_task)
        return shortest_task

    def release_resource(self, task):
        """Release resources when a task is completed."""
        self.r1_assigned += task.r1_need
        self.r2_assigned += task.r2_need
        print(f"Resources released: R1={self.r1_assigned}, R2={self.r2_assigned}")

    def increment_time(self):
        """Increment the current simulation time."""
        self.current_time += 1
        print(f"Current time: {self.current_time}")