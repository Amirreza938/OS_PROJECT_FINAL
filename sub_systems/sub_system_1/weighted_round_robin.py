class WeightedRoundRobinScheduler:
    def __init__(self, waiting_queue, r1_assigned, r2_assigned):
        self.waiting_queue = waiting_queue
        self.r1_assigned = r1_assigned
        self.r2_assigned = r2_assigned
        self.queues = []  # List of ready queues
        self.weights = []  # List of weights for each queue
        self.current_queue_index = 0  # Current queue being processed
        self.current_weight = 0  # Current weight counter

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
        """Get the next task to process based on weighted round-robin scheduling."""
        if not self.queues:
            return None

        while True:
            queue = self.queues[self.current_queue_index]
            weight = self.weights[self.current_queue_index]

            if queue and self.current_weight < weight:
                self.current_weight += 1
                return queue[0]  # Return the task at the front of the queue
            else:
                self.current_weight = 0
                self.current_queue_index = (self.current_queue_index + 1) % len(self.queues)
