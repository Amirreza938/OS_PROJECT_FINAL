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

    def run_task(self, task: BaseTask):
        print(task.name)
        task_status = task.execute()  # Execute the task for one clock cycle
        if task_status == 0:
            print(f"Task {task.name} completed on core {self.core_id}")
            self.scheduler.release_resource(task)
        elif task_status == -1:
            print(f"Task {task.name} failed on core {self.core_id}")
        else:
            # If the task is not completed, re-queue it without deducting resources
            self.scheduler.add_to_ready_queue(task, is_requeue=True)

    def run(self):
        while True:
            self.clock_event.wait()
            
            with self.lock:
                if not self.running:
                    break
                task = self.scheduler.get_next_task()
                if task:
                    self.run_task(task)
                # Increment the current time after each clock cycle
                self.scheduler.increment_time()
                self.clock_event.clear()

    def toggle_clock(self):
        with self.lock:
            self.clock_event.set()

    def stop(self):
        with self.lock:
            self.running = False
            self.clock_event.set()

class SubSystem2(Thread):
    def __init__(self, resource_requested, r1_assigned, r2_assigned, tasks, finish_flag):
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
        self.resource_manager = ResourceManager(resource_requested)
        self.running = True
        self.finish_flag = finish_flag

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
        empty_ready_queue = len(self.scheduler.ready_queue) == 0
        
        print(f"Debug - Ready Queue: {len(self.scheduler.ready_queue)}")
        
        return empty_ready_queue 

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
                break

            self.clock_event.clear()  # Clear the clock event for the next iteration

        self.stop_cores()
        self.finish_flag = True
        print('SubSystem2 stopped')