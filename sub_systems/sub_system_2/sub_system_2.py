import threading
from threading import Thread
import queue
from queue import Queue
from sub_systems.core import BaseCore
from shortest_remaining_job_first import ShortestRemainingJobFirstScheduler
from task import BaseTask

class SubSystem2Core(BaseCore):
    def __init__(self, scheduler:ShortestRemainingJobFirstScheduler, core_id):
        super().__init__(scheduler, core_id, Queue(), None)
        self.lock = threading.Lock()
        self.scheduler = scheduler
        self.core_id = core_id
        self.clock_event = threading.Event()
    def run_task(self, task:BaseTask):
        task_status = task.execute()
        if task_status == 0:
            print(f"Task {task.name} completed on core {self.core_id}")  
            self.scheduler.release_resource(task)
        elif task_status == -1:
            print(f"Task {task.name} failed on core {self.core_id}")
    def run(self):
        while True:
            self.clock_event.wait()
            with self.lock:
                if not self.running:
                    break
                task = self.scheduler.get_next_task()
                if task:
                    self.run_task(task)
                self.clock_event.clear()
    def toggle_clock(self):
        with self.lock:
            self.clock_event.set()
    def stop(self): 
        with self.lock:
            self.running = False
            self.clock_event.set()
class SubSystem2(Thread):
    def __init__(self,r1_assigned,r2_assigned): 
        super().__init__()
        self.number_of_cores = 2
        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned
        self.scheduler = ShortestRemainingJobFirstScheduler(r1_assigned,r2_assigned)
        self.cores = [SubSystem2Core(self.scheduler, i+1) for i in range(self.number_of_cores)]
        self.running = True
        self.lock = threading.Lock()
        self.clock_event = threading.Event()
    def start_cores(self):
        for core in self.cores:
            core.start()
    def stop_cores(self):   
        for core in self.cores:
            core.stop()
            core.join()
    def toggle_clock(self):
        with self.lock:
            self.clock_event.set()
    def run(self):
        self.start_cores()
        while True:
            self.clock_event.wait()
            with self.lock:
                if not self.running:
                    break
                for core in self.cores:
                    core.toggle_clock()
                self.clock_event.clear()
        self.stop_cores()
