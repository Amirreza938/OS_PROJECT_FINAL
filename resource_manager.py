class ResourceManager:
    def __init__(self, total_resources):
        self.total_resources = total_resources  # Total available resources
        self.allocated_resources = {resource: 0 for resource in total_resources}

    def can_allocate(self, resource_requests):
        """
        Check if the resources requested can be allocated.
        """
        for resource, amount in resource_requests.items():
            if self.allocated_resources[resource] + amount > self.total_resources[resource]:
                return False
        return True

    def allocate(self, resource_requests):
        """
        Allocate resources to a task.
        """
        if self.can_allocate(resource_requests):
            for resource, amount in resource_requests.items():
                self.allocated_resources[resource] += amount
            return True
        else: return False

    def release(self, resource_requests):
        """
        Release resources held by a task.
        """
        for resource, amount in resource_requests.items():
            self.allocated_resources[resource] -= amount