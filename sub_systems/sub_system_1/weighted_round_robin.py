from collections import deque


class WeightedRoundRobinScheduler:
    def __init__(self, waiting_queue, r1_available, r2_available):
        self.queues = []
        self.weights = []
        self.current_index = 0
        self.current_weight = 0
        self.waiting_queue = waiting_queue
        self.r1_available = r1_available
        self.r2_available = r2_available

    def add_queue(self, queue, weight):
        self.queues.append(queue)
        self.weights.append(weight)

    def change_resource_availablity(self, r1_available, r2_available):
        self.r1_available = r1_available
        self.r2_available = r2_available

    def get_next_task(self):
        if not self.queues:
            return None

        self._check_waiting_queue()

        while True:
            self._set_current_index()
            queue = self.queues[self.current_index]

            if self.weights[self.current_index] >= self.current_weight and queue:
                task = queue.popleft()

                if self.add_to_waiting_queue(task):
                    continue

                return task

            if self.current_index == 0 and self.current_weight <= 0:
                break

        return None

    def _check_waiting_queue(self):
        still_waiting = deque()

        while self.waiting_queue:
            task = self.waiting_queue.popleft()
            if task.r1_need <= self.r1_available and task.r2_need <= self.r2_available:
                self.add_to_ready_queue(task)
            else:
                still_waiting.append(task)

        for task in still_waiting:
            self.waiting_queue.append(task)

    def add_to_ready_queue(self, task):
        min_queue_len = len(self.queues[0])
        min_sized_queue = self.queues[0]
        for queue in self.queues:
            if len(queue) < min_queue_len:
                min_sized_queue = queue
                min_queue_len = len(queue)
        min_sized_queue.append(task)

    def _set_current_index(self):
        self.current_index = (self.current_index + 1) % len(self.queues)
        if self.current_index == 0:
            self.current_weight -= 1
            if self.current_weight <= 0:
                self.current_weight = max(self.weights)

    def add_to_waiting_queue(self, task):
        if task.r1_need > self.r1_available or task.r2_need > self.r2_available:
            self.waiting_queue.append(task)
            return True
        return False