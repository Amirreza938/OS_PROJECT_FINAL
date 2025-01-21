from threading import Thread, Lock, Event


class MainSystem(Thread):
    def __init__(self, sub_systems: list):
        super().__init__()
        self.sub_systems = sub_systems
        self.running = True
        self._lock = Lock()
        self.clock_event = Event()

    def toggle_clock(self):
        self.clock_event.set()

    def toggle_sub_systems(self):
        for sub_system in self.sub_systems:
            sub_system.toggle_clock()

    def stop(self):
        with self._lock:
            self.running = False
            self.clock_event.set()

    def run(self):
        while True:
            self.clock_event.wait()
            with self._lock:
                if not self.running:
                    break
                self.toggle_sub_systems()
                self.clock_event.clear()
