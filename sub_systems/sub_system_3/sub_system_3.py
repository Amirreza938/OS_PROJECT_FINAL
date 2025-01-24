import threading
from queue import Queue
from threading import Thread
from resource_manager import ResourceManager
from sub_systems.core import BaseCore
from .rate_monotonic import RateMonotonicScheduler
from task import BaseTask

class SubSystem3Core(BaseCore):
    def __init__(self, scheduler: RateMonotonicScheduler, core_id):
        super().__init__(scheduler, core_id, Queue(), None)
        self.scheduler = scheduler
        self.core_id = core_id
        self._lock = threading.Lock()
        self.clock_event = threading.Event()
        self.current_task = None  # Track the current task being executed

    def run_task(self, task: BaseTask):
        """Execute a task for one clock cycle."""
        task_status = task.execute()  # Execute the task for one clock cycle
        if task_status == 0:
            print(f"Task {task.name} completed on Core {self.core_id}")
            self.scheduler.release_resources(task)  # Release resources after task completion
            self.current_task = None  # Clear the current task
        elif task_status == -1:
            print(f"Task {task.name} failed on Core {self.core_id}")
            self.current_task = None  # Clear the current task
        else:
            # Release resources before re-queueing the task
            self.scheduler.release_resources(task)
            # Re-queue the task if resources are available
            if self.scheduler.add_task(task):
                print(f"Task {task.name} re-queued with remaining time: {task.remaining_time}")
            else:
                print(f"Task {task.name} cannot be re-queued due to insufficient resources.")
            self.current_task = task  # Keep the task as current

    def run(self):
        """Main execution loop for the core."""
        while True:
            self.clock_event.wait()
            with self._lock:
                if not self.running:
                    break
                task = self.scheduler.get_next_task()
                if task:
                    self.current_task = task  # Set the current task
                    self.run_task(task)
                self.scheduler.increment_time()  # Increment time after each clock cycle
                self.clock_event.clear()

    def get_current_task(self):
        """Get the current task being processed by the core."""
        return self.current_task

    def toggle_clock(self):
        """Trigger the clock event for the core."""
        with self._lock:
            self.clock_event.set()

    def stop(self):
        """Stop the core."""
        with self._lock:
            self.running = False
            self.clock_event.set()

class SubSystem3(Thread):
    def __init__(self, resource_requested, r1_assigned, r2_assigned, tasks, finish_flag):
        super().__init__()
        self.num_cores = 1  # SubSystem3 has only one core
        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned
        self.tasks = tasks  # List of tasks to be assigned
        self.finish_flag = finish_flag  # Flag to indicate if all tasks are completed
        self.scheduler = RateMonotonicScheduler(r1_assigned, r2_assigned)
        self.core = SubSystem3Core(self.scheduler, 1)  # Create the single core
        self.running = True
        self._lock = threading.Lock()
        self.clock_event = threading.Event()
        self.resource_manager = ResourceManager(resource_requested)
        # Assign tasks to the scheduler
        self.assign_tasks_to_scheduler()
    def print_state(self):
        """Print the state of SubSystem3."""
        print(f"Sub3:")
        print(f"Resources: R1: {self.r1_assigned} R2: {self.r2_assigned}")
        print(f"Waiting Queue {list(self.scheduler.ready_queue)}")
        print(f"Ready Queue: {list(self.scheduler.ready_queue)}")
        print(f"Core1:")
        task = self.core.get_current_task()
        if task:
            print(f"Running Task: {task.name}")
        else:
            print("Running Task: idle")
        print()
    def assign_tasks_to_scheduler(self):
        """Assign tasks to the Rate Monotonic Scheduler."""
        for task in self.tasks:
            self.scheduler.add_task(task)
            print(f"Task {task.name} added to SubSystem3 with period={task.period}")

    def start_core(self):
        """Start the core."""
        self.core.start()

    def stop_core(self):
        """Stop the core."""
        self.core.stop()
        self.core.join()

    def toggle_clock(self):
        """Trigger the clock event for the core."""
        with self._lock:
            self.clock_event.set()

    def check_finish_time(self):
        """Check if all tasks are completed."""
        # Check if all tasks have remaining_time == 0
        for task in self.tasks:
            if task.remaining_time > 0:
                return False  # At least one task is not completed
        return True  # All tasks are completed

    def run(self):
        """Main execution loop for SubSystem3."""
        self.start_core()
        while self.running:
            self.clock_event.wait()
            with self._lock:
                if not self.running:
                    break
                self.core.toggle_clock()

                # Check if all tasks are finished
                if self.check_finish_time():
                    print("All tasks finished in SubSystem3")
                    self.finish_flag = True
                    break

                self.clock_event.clear()
        self.stop_core()