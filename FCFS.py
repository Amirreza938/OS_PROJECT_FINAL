class Task:
    def __init__(self, task_id, arrival_time, execution_time):
        self.task_id = task_id  # Unique identifier for the task
        self.arrival_time = arrival_time  # Time when the task arrives
        self.execution_time = execution_time  # Total time required to complete the task
        self.start_time = None  # Time when the task starts execution
        self.end_time = None  # Time when the task completes execution

    def execute(self, current_time):
        """
        Execute the task and set its start and end times.
        """
        if self.start_time is None:
            self.start_time = current_time
        self.end_time = current_time + self.execution_time
        print(f"Time {current_time}: Task {self.task_id} started execution. "
              f"Will complete at time {self.end_time}.")
        return self.execution_time


def fcfs_scheduler(tasks):
    """
    Schedules tasks using the First-Come, First-Served (FCFS) algorithm.
    """
    # Sort tasks by their arrival time
    tasks.sort(key=lambda task: task.arrival_time)

    current_time = 0
    print("\nStarting First-Come, First-Served (FCFS) Scheduling...")

    for task in tasks:
        # Wait for the task to arrive if necessary
        if current_time < task.arrival_time:
            print(f"Time {current_time}: No tasks to execute. Waiting for Task {task.task_id} to arrive.")
            current_time = task.arrival_time

        # Execute the task
        time_taken = task.execute(current_time)
        current_time += time_taken

    # Print task completion details
    print("\nTask Completion Details:")
    for task in tasks:
        print(f"Task {task.task_id}: Arrival Time = {task.arrival_time}, Start Time = {task.start_time}, "
              f"End Time = {task.end_time}")


# Function to get tasks from the user
def get_tasks_from_user():
    tasks = []
    num_tasks = int(input("Enter the number of tasks: "))
    for i in range(num_tasks):
        task_id = i + 1
        arrival_time = int(input(f"Enter the arrival time for Task {task_id}: "))
        execution_time = int(input(f"Enter the execution time for Task {task_id}: "))
        tasks.append(Task(task_id, arrival_time, execution_time))
    return tasks


# Main program
if __name__ == "__main__":
    # Get tasks from the user
    tasks = get_tasks_from_user()

    # Start FCFS scheduling
    fcfs_scheduler(tasks)
