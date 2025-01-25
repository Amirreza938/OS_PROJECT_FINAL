class WeightedRoundRobinScheduler:
    def __init__(self, waiting_queue, r1_assigned, r2_assigned):
        self.waiting_queue = waiting_queue
        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned
        self.queues = []
        self.weights = []
        self.current_queue_index = 0
        self.current_weight = 0
        self.current_time = 0
        self.starvation_threshold = 5

    def add_queue(self, queue, weight):
        self.queues.append(queue)
        self.weights.append(weight)

    def add_to_ready_queue(self, task):
        if self.r1_assigned > 0:
            self.queues[0].append(task)
            self.r1_assigned -= 1
        elif self.r2_assigned > 0:
            self.queues[1].append(task)
            self.r2_assigned -= 1
        else:
            self.waiting_queue.append(task)

    def get_next_task(self):
        if not self.queues:
            return None

        while True:
            queue = self.queues[self.current_queue_index]
            weight = self.weights[self.current_queue_index]

            ready_tasks = [task for task in queue if task.arrival_time <= self.current_time]

            if not ready_tasks:
                break
            if self.current_weight < weight:
                self.current_weight += 1
                return ready_tasks[0]
            else:
                self.current_weight = 0
                self.current_queue_index = (self.current_queue_index + 1) % len(self.queues)

                if self.current_time % self.starvation_threshold == 0:
                    self.promote_tasks_from_lower_queues()

    def promote_tasks_from_lower_queues(self):
        for i in range(len(self.queues) - 1, 0, -1):
            if self.queues[i]:
                task = self.queues[i].pop()
                self.queues[0].append(task)
                break

    def increment_time(self):
        self.current_time += 1
