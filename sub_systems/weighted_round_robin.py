class WeightedRoundRobinScheduler:
    def __init__(self):
        self.queues = []
        self.weights = []
        self.current_index = 0
        self.current_weight = 0

    def add_queue(self, queue, weight):
        """
        Add a queue to the scheduler with its corresponding weight.
        """
        self.queues.append(queue)
        self.weights.append(weight)

    def get_next_task(self):
        """
        Get the next task from the queues based on WRR scheduling.
        """
        if not self.queues:
            return None

        while True:
            # Loop through the queues
            self.current_index = (self.current_index + 1) % len(self.queues)
            if self.current_index == 0:
                self.current_weight -= 1
                if self.current_weight <= 0:
                    # Reset the weight to the maximum weight in the system
                    self.current_weight = max(self.weights)

            # Check if the current queue has tasks and its weight allows processing
            if self.weights[self.current_index] >= self.current_weight:
                queue = self.queues[self.current_index]
                if not queue.empty():
                    return queue.get()
