from threading import Thread, Lock, Event
from resource_manager import ResourceManager


class MainSystem(Thread):
    def __init__(self, sub_systems: list, total_r1: int, total_r2: int):
        super().__init__()
        self.sub_systems = sub_systems
        self.total_r1 = total_r1  # Total R1 resources in the system
        self.total_r2 = total_r2  # Total R2 resources in the system
        self.running = True
        self._lock = Lock()
        self.clock_event = Event()
        self.finish_flags = [False for _ in range(len(self.sub_systems))]

    def toggle_clock(self):
        """Trigger the clock event for the system."""
        self.clock_event.set()

    def toggle_sub_systems(self):
        """Trigger the clock event for all subsystems."""
        for sub_system in self.sub_systems:
            sub_system.toggle_clock()

    def stop(self):
        """Stop the main system and all subsystems."""
        with self._lock:
            self.running = False
            self.clock_event.set()

    def run_sub_systems(self):
        """Start all subsystems."""
        for sub_system in self.sub_systems:
            sub_system.start()

    def check_finish_time(self):
        """Check if all subsystems have completed their tasks."""
        finish_flag = True
        for flag in self.finish_flags:
            finish_flag &= flag
        return finish_flag

    def join_subsystems(self):
        """Wait for all subsystems to finish."""
        for sub_system in self.sub_systems:
            sub_system.join()

    def run(self):
        """Main execution loop for the system."""
        self.run_sub_systems()
        while True:
            self.clock_event.wait()
            with self._lock:
                if not self.running:
                    break
                self.toggle_sub_systems()
                if self.check_finish_time():
                    self.join_subsystems()
                    break
            self.clock_event.clear()