from threading import Thread, Lock, Event

class MainSystem(Thread):
    def __init__(self, sub_systems: list):
        super().__init__()
        self.sub_systems = sub_systems
        self.running = True
        self._lock = Lock()
        self.clock_event = Event()
        self.finish_flags = [False for _ in range(len(self.sub_systems))]

    def toggle_clock(self):
        self.clock_event.set()

    def toggle_sub_systems(self):
        for sub_system in self.sub_systems:
            sub_system.toggle_clock()

    def stop(self):
        with self._lock:
            self.running = False
            self.clock_event.set()

    def run_sub_systems(self):
        for sub_system in self.sub_systems:
            sub_system.start()

    def check_finish_time(self):
        finish_flag = True
        for flag in self.finish_flags:
            finish_flag &= flag
        return finish_flag

    def join_subsystems(self):
        for sub_system in self.sub_systems:
            sub_system.join()
            sub_system.finish()


    def run(self):
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
