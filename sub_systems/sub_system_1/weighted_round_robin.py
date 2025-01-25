class WeightedRoundRobinScheduler:
    def __init__(self, waiting_queue, r1_assigned, r2_assigned):
        self.waiting_queue = waiting_queue
        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned
        self.queues = []  # List of ready queues
        self.weights = []  # List of weights for each queue
        self.current_queue_index = 0  # Current queue being processed
        self.current_weight = 0  # Current weight counter
        self.current_time = 0  # Current simulation time
        self.starvation_threshold = 5

    def add_queue(self, queue, weight):
        """Add a queue with its associated weight."""
        self.queues.append(queue)
        self.weights.append(weight)

    def add_to_ready_queue(self, task):
        """Add a task to the appropriate queue based on resource availability."""
        if self.r1_assigned > 0:
            self.queues[0].append(task)
            self.r1_assigned -= 1
        elif self.r2_assigned > 0:
            self.queues[1].append(task)
            self.r2_assigned -= 1
        else:
            self.waiting_queue.append(task)

    def get_next_task(self):
        """Get the next task to process based on weighted round-robin scheduling, considering arrival time."""
        if not self.queues:
            return None

        while True:
            queue = self.queues[self.current_queue_index]
            weight = self.weights[self.current_queue_index]

            # Filter tasks that have arrived
            ready_tasks = [task for task in queue if task.arrival_time <= self.current_time]

            if not ready_tasks:
                break
            if self.current_weight < weight:
                self.current_weight += 1
                return ready_tasks[0]  # Return the first ready task in the queue
            else:
                self.current_weight = 0
                self.current_queue_index = (self.current_queue_index + 1) % len(self.queues)

                if self.current_time % self.starvation_threshold == 0:
                    self.promote_tasks_from_lower_queues()

    def promote_tasks_from_lower_queues(self):
        """Promote tasks from lower-priority queues to prevent starvation."""
        for i in range(len(self.queues) - 1, 0, -1):  # Start from the lowest priority queue
            if self.queues[i]:
                task = self.queues[i].pop(0)
                self.queues[0].append(task)  # Promote to the highest priority queue
                break

    def increment_time(self):
        """Increment the current simulation time and handle resource allocation."""
        self.current_time += 1
