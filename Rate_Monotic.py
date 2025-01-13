class Task:
    def __init__(self, task_id, execution_time, period, deadline):
        self.task_id = task_id  # Unique identifier for the task
        self.execution_time = execution_time  # Time required to execute the task
        self.period = period  # Time period of the task
        self.deadline = deadline  # Deadline for the task
        self.remaining_time = execution_time  # Remaining execution time
        self.next_arrival_time = 0  # Next time the task is ready to execute
        self.completed_instances = 0  # Count of completed instances

    def is_ready(self, current_time):
        """
        Check if the task is ready to execute at the current time.
        """
        return current_time >= self.next_arrival_time and self.remaining_time > 0

    def execute(self, current_time):
        """
        Execute the task for one unit of time.
        """
        if self.remaining_time > 0:
            self.remaining_time -= 1
            print(f"Time {current_time}: Task {self.task_id} is executing. Remaining time: {self.remaining_time}")
            if self.remaining_time == 0:
                print(f"Time {current_time}: Task {self.task_id} instance completed.")
                self.completed_instances += 1

    def reset_for_next_period(self):
        """
        Reset the task for the next period.
        """
        self.remaining_time = self.execution_time
        self.next_arrival_time += self.period


def rate_monotonic_scheduler(tasks, simulation_time):
    """
    Schedules tasks using the Rate Monotonic Scheduling (RMS) algorithm.
    """
    # Sort tasks by their period (shorter period = higher priority)
    tasks.sort(key=lambda task: task.period)

    # Current time in the simulation
    current_time = 0

    while current_time < simulation_time:
        # Find the highest-priority ready task
        ready_tasks = [task for task in tasks if task.is_ready(current_time)]

        if ready_tasks:
            # Select the task with the highest priority (shortest period)
            highest_priority_task = ready_tasks[0]
            highest_priority_task.execute(current_time)
        else:
            print(f"Time {current_time}: No tasks to execute.")

        # Check for missed deadlines
        for task in tasks:
            if current_time == task.deadline + (task.completed_instances * task.period) and task.remaining_time > 0:
                print(f"Time {current_time}: Task {task.task_id} missed its deadline!")

        # Reset tasks for the next period if necessary
        for task in tasks:
            if current_time == task.next_arrival_time and task.remaining_time == 0:
                task.reset_for_next_period()

        # Increment current time
        current_time += 1

    # Print task completion details
    print("\nTask Completion Details:")
    for task in tasks:
        print(f"Task {task.task_id}: Completed Instances = {task.completed_instances}")


# Function to get tasks from the user
def get_tasks_from_user():
    tasks = []
    num_tasks = int(input("Enter the number of tasks: "))
    for i in range(num_tasks):
        task_id = i + 1
        execution_time = int(input(f"Enter the execution time for Task {task_id}: "))
        period = int(input(f"Enter the period for Task {task_id}: "))
        deadline = int(input(f"Enter the deadline for Task {task_id}: "))
        tasks.append(Task(task_id, execution_time, period, deadline))
    return tasks


# Main program
if __name__ == "__main__":
    # Get tasks from the user
    tasks = get_tasks_from_user()

    # Get simulation time
    simulation_time = int(input("\nEnter the total simulation time: "))

    # Start RMS scheduling
    print("\nStarting Rate Monotonic Scheduling (RMS)...")
    rate_monotonic_scheduler(tasks, simulation_time)
