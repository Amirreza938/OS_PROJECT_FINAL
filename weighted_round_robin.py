class Task:
    def __init__(self, task_id, execution_time):
        self.task_id = task_id  # Unique identifier for the task
        self.execution_time = execution_time  # Total time required to complete the task
        self.remaining_time = execution_time  # Remaining time to complete the task
        self.weight = 0  # Weight of the task (calculated based on length)

    def execute(self, time_slice):
        """
        Execute the task for a given time slice.
        """
        if self.remaining_time > 0:
            if self.remaining_time > time_slice:
                self.remaining_time -= time_slice
                print(f"Task {self.task_id} executed for {time_slice} units. Remaining time: {self.remaining_time}")
            else:
                print(f"Task {self.task_id} executed for {self.remaining_time} units and completed.")
                self.remaining_time = 0
        else:
            print(f"Task {self.task_id} has already been completed.")

    def is_completed(self):
        """
        Check if the task is completed.
        """
        return self.remaining_time == 0


class WeightedRoundRobinScheduler:
    def __init__(self, tasks):
        self.tasks = tasks  # List of tasks to be scheduled
        self.current_task_index = 0  # Index of the current task being executed
        self.calculate_weights()  # Calculate weights for tasks based on their lengths

    def calculate_weights(self):
        """
        Calculate weights for tasks based on their lengths.
        The shortest task gets a weight of 1, and others get proportional weights.
        """
        # Find the shortest task
        shortest_task = min(self.tasks, key=lambda task: task.execution_time)
        shortest_length = shortest_task.execution_time

        # Calculate weights for all tasks
        for task in self.tasks:
            task.weight = task.execution_time // shortest_length

    def get_time_slice(self, task):
        """
        Calculate the time slice for a task based on its weight.
        The shortest task gets 1 quantum, and others get proportional quanta.
        """
        return task.weight

    def schedule(self):
        """
        Execute tasks using the Weighted Round Robin algorithm.
        """
        while True:
            # Get the current task
            current_task = self.tasks[self.current_task_index]

            # Skip completed tasks
            if current_task.is_completed():
                self.current_task_index = (self.current_task_index + 1) % len(self.tasks)
                continue

            # Get the time slice for the current task
            time_slice = self.get_time_slice(current_task)

            # Execute the task for the calculated time slice
            current_task.execute(time_slice)

            # Move to the next task
            self.current_task_index = (self.current_task_index + 1) % len(self.tasks)

            # Check if all tasks are completed
            if all(task.is_completed() for task in self.tasks):
                print("All tasks completed.")
                break


# Function to get tasks from the user
def get_tasks_from_user():
    tasks = []
    num_tasks = int(input("Enter the number of tasks: "))
    for i in range(num_tasks):
        task_id = i + 1
        execution_time = int(input(f"Enter the execution time for Task {task_id}: "))
        tasks.append(Task(task_id, execution_time))
    return tasks


# Main program
if __name__ == "__main__":
    # Get tasks from the user
    tasks = get_tasks_from_user()

    # Create a Weighted Round Robin scheduler
    scheduler = WeightedRoundRobinScheduler(tasks)

    # Start scheduling
    print("\nStarting Weighted Round Robin Scheduling...")
    scheduler.schedule()