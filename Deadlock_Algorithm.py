class Task:
    def __init__(self, task_id, arrival_time, execution_time, resource_requests):
        self.task_id = task_id  # Unique identifier for the task
        self.arrival_time = arrival_time  # Time when the task arrives
        self.execution_time = execution_time  # Total time required to complete the task
        self.remaining_time = execution_time  # Remaining time to complete the task
        self.resource_requests = resource_requests  # Resources needed by the task
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


class ResourceManager:
    def __init__(self, total_resources):
        self.total_resources = total_resources  # Total available resources
        self.allocated_resources = {resource: 0 for resource in total_resources}

    def can_allocate(self, resource_requests):
        """
        Check if the resources requested can be allocated.
        """
        for resource, amount in resource_requests.items():
            if self.allocated_resources[resource] + amount > self.total_resources[resource]:
                return False
        return True

    def allocate(self, resource_requests):
        """
        Allocate resources to a task.
        """
        for resource, amount in resource_requests.items():
            self.allocated_resources[resource] += amount

    def release(self, resource_requests):
        """
        Release resources held by a task.
        """
        for resource, amount in resource_requests.items():
            self.allocated_resources[resource] -= amount


def srtf_scheduler_with_deadlock_prevention(tasks, resource_manager):
    """
    Schedules tasks using the Shortest Remaining Time First (SRTF) algorithm
    with deadlock prevention via resource ordering.
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

            # Check if resources can be allocated to the task
            if resource_manager.can_allocate(shortest_task.resource_requests):
                resource_manager.allocate(shortest_task.resource_requests)
                shortest_task.execute(current_time)
                resource_manager.release(shortest_task.resource_requests)  # Release resources after execution
            else:
                print(f"Time {current_time}: Task {shortest_task.task_id} is waiting for resources.")
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


# Function to get resources and tasks from the user
def get_resources_and_tasks_from_user():
    # Get total resources
    total_resources = {}
    num_resources = int(input("Enter the number of resource types: "))
    for _ in range(num_resources):
        resource_name = input("Enter the resource name (e.g., R1, R2): ")
        resource_quantity = int(input(f"Enter the total quantity of {resource_name}: "))
        total_resources[resource_name] = resource_quantity

    # Get tasks
    tasks = []
    num_tasks = int(input("\nEnter the number of tasks: "))
    for i in range(num_tasks):
        task_id = i + 1
        arrival_time = int(input(f"\nEnter the arrival time for Task {task_id}: "))
        execution_time = int(input(f"Enter the execution time for Task {task_id}: "))

        # Get resource requests for the task
        resource_requests = {}
        for resource in total_resources.keys():
            requested_quantity = int(input(f"Enter the quantity of {resource} requested by Task {task_id}: "))
            resource_requests[resource] = requested_quantity

        tasks.append(Task(task_id, arrival_time, execution_time, resource_requests))

    return total_resources, tasks


# Main program
if __name__ == "__main__":
    # Get resources and tasks from the user
    total_resources, tasks = get_resources_and_tasks_from_user()

    # Initialize ResourceManager
    resource_manager = ResourceManager(total_resources)

    # Sort tasks by arrival time
    tasks.sort(key=lambda task: task.arrival_time)

    # Start SRTF scheduling with deadlock prevention
    print("\nStarting SRTF Scheduling with Deadlock Prevention...")
    srtf_scheduler_with_deadlock_prevention(tasks, resource_manager)
