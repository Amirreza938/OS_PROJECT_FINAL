import threading
from collections import deque
from threading import Thread

from resource_manager import ResourceManager
from sub_systems.core import BaseCore
from .shortest_remaining_job_first import ShortestRemainingJobFirstScheduler  # Relative import
from task import BaseTask

class SubSystem2Core(BaseCore):
    def __init__(self, scheduler: ShortestRemainingJobFirstScheduler, core_id):
        super().__init__(scheduler, core_id, scheduler.ready_queue, deque())
        self.lock = threading.Lock()
        self.scheduler = scheduler
        self.core_id = core_id
        self.clock_event = threading.Event()
        self.current_task = None  # Track the current task being executed

    def run_task(self, task: BaseTask):
        """Execute a task for one clock cycle."""
        task_status = task.execute()  # Execute the task for one clock cycle
        if task_status == 0:
            print(f"Task {task.name} completed on core {self.core_id}")
            self.scheduler.release_resource(task)  # Release resources after task completion
            self.current_task = None  # Clear the current task
        elif task_status == -1:
            print(f"Task {task.name} failed on core {self.core_id}")
            self.current_task = None  # Clear the current task
        else:
            # If the task is not completed, re-queue it without deducting resources
            self.scheduler.add_to_ready_queue(task, is_requeue=True)
            self.current_task = task  # Keep the task as current

    def run(self):
        """Main execution loop for the core."""
        while True:
            self.clock_event.wait()
            with self.lock:
                if not self.running:
                    break

                # Only fetch a task if the core is idle
                if self.current_task is None:
                    task = self.scheduler.get_next_task()
                    if task:
                        self.current_task = task  # Set the current task
                        self.run_task(task)

                # Increment the current time after each clock cycle
                self.scheduler.increment_time()
                self.clock_event.clear()

    def get_current_task(self):
        """Get the current task being processed by the core."""
        return self.current_task

    def toggle_clock(self):
        """Trigger the clock event for the core."""
        with self.lock:
            self.clock_event.set()

    def stop(self):
        """Stop the core."""
        with self.lock:
            self.running = False
            self.clock_event.set()

class SubSystem2(Thread):
    def __init__(self, resource_manager, r1_assigned, r2_assigned, tasks, finish_flag, subsystem_id):
        super().__init__()
        self._lock = threading.Lock()
        self.clock_event = threading.Event()

        self.num_cores = 2  # Number of cores in SubSystem2
        self.tasks = tasks

        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned

        # Create a single scheduler with a single ready queue
        self.scheduler = ShortestRemainingJobFirstScheduler(self.r1_assigned, self.r2_assigned)

        # Create cores and pass the single scheduler
        self.cores = [
            SubSystem2Core(self.scheduler, i + 1) for i in range(self.num_cores)
        ]
        self.resource_manager = resource_manager
        self.running = True
        self.finish_flag = finish_flag
        self.subsystem_id = subsystem_id  # Added subsystem_id for resource borrowing

        # Assign tasks to the single ready queue
        self.assign_tasks_to_queue()

    def assign_tasks_to_queue(self):
        """Assign tasks to the single ready queue."""
        for task in self.tasks:
            self.scheduler.add_to_ready_queue(task)

    def stop(self):
        """Stop the subsystem and all its cores."""
        with self._lock:
            self.running = False
            self.clock_event.set()

    def start_cores(self):
        """Start all cores."""
        for core in self.cores:
            core.start()

    def stop_cores(self):
        """Stop all cores."""
        for core in self.cores:
            core.stop()
            core.join()

    def toggle_clock(self):
        """Trigger the clock event for all cores."""
        self.clock_event.set()

    def check_finish_time(self):
        """Check if all tasks are completed."""
        # Check if all tasks have remaining_time == 0
        for task in self.tasks:
            if task.remaining_time > 0:
                return False  # At least one task is not completed
        return True  # All tasks are completed

    def run(self):
        """Main execution loop for the subsystem."""
        self.start_cores()
        while self.running:
            self.clock_event.wait()  # Wait for the clock event
            print('Clock in SubSystem2 triggered')

            with self._lock:
                for core in self.cores:
                    core.toggle_clock()

                # Check if all tasks are finished
                if self.check_finish_time():
                    print('All tasks finished in SubSystem2')
                    self.finish_flag = True
                    break

            self.clock_event.clear()  # Clear the clock event for the next iteration

        self.stop_cores()
        print('SubSystem2 stopped')