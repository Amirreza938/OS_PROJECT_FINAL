class Task:
    def __init__(self, task_id, arrival_time, execution_time):
        self.task_id = task_id  # Unique identifier for the task
        self.arrival_time = arrival_time  # Time when the task arrives
        self.execution_time = execution_time  # Total time required to complete the task
        self.remaining_time = execution_time  # Remaining time to complete the task
        self.start_time = None  # Time when the task starts execution
        self.end_time = None  # Time when the task completes execution

    def execute(self, current_time):
        """
        Execute the task for one unit of time.
        """
        if self.remaining_time > 0:
            if self.start_time is None:
                self.start_time = current_time  # Set start time when task first executes
            self.remaining_time -= 1
            print(f"Time {current_time}: Task {self.task_id} is executing. Remaining time: {self.remaining_time}")
            if self.remaining_time == 0:
                self.end_time = current_time + 1  # Set end time when task completes
                print(f"Time {current_time + 1}: Task {self.task_id} completed.")

    def is_completed(self):
        """
        Check if the task is completed.
        """
        return self.remaining_time == 0


def srtf_scheduler(tasks):
    """
    Schedules tasks using the Shortest Remaining Time First (SRTF) algorithm.
    """
    current_time = 0
    completed_tasks = 0
    total_tasks = len(tasks)

    while completed_tasks < total_tasks:
        # Find all tasks that have arrived and are not completed
        ready_tasks = [task for task in tasks if task.arrival_time <= current_time and not task.is_completed()]

        if ready_tasks:
            # Select the task with the shortest remaining time
            shortest_task = min(ready_tasks, key=lambda task: task.remaining_time)
            shortest_task.execute(current_time)
        else:
            print(f"Time {current_time}: No tasks to execute.")

        current_time += 1

        # Check if any tasks have completed
        for task in tasks:
            if task.is_completed() and task.end_time == current_time:
                completed_tasks += 1

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

    # Sort tasks by arrival time (in case they are not entered in order)
    tasks.sort(key=lambda task: task.arrival_time)

    # Start SRTF scheduling
    print("\nStarting Shortest Remaining Time First (SRTF) Scheduling...")
    srtf_scheduler(tasks)