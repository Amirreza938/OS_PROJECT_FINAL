class ResourceManager:
    def __init__(self, total_r1, total_r2):
        self.total_r1 = total_r1  # Total R1 resources in the system
        self.total_r2 = total_r2  # Total R2 resources in the system
        self.allocated_r1 = {}    # Track allocated R1 resources by subsystem
        self.allocated_r2 = {}    # Track allocated R2 resources by subsystem

    def allocate_resources(self, subsystem_id, r1_needed, r2_needed):
        """Allocate resources to a subsystem if available."""
        if r1_needed <= self.total_r1 and r2_needed <= self.total_r2:
            self.total_r1 -= r1_needed
            self.total_r2 -= r2_needed
            self.allocated_r1[subsystem_id] = r1_needed
            self.allocated_r2[subsystem_id] = r2_needed
            return True
        return False

    def release_resources(self, subsystem_id):
        """Release resources from a subsystem."""
        if subsystem_id in self.allocated_r1:
            self.total_r1 += self.allocated_r1[subsystem_id]
            self.total_r2 += self.allocated_r2[subsystem_id]
            del self.allocated_r1[subsystem_id]
            del self.allocated_r2[subsystem_id]

    def borrow_resources(self, borrower_id, lender_id, r1_needed, r2_needed):
        """Borrow resources from another subsystem."""
        if lender_id in self.allocated_r1 and self.allocated_r1[lender_id] >= r1_needed and self.allocated_r2[lender_id] >= r2_needed:
            self.allocated_r1[lender_id] -= r1_needed
            self.allocated_r2[lender_id] -= r2_needed
            self.allocated_r1[borrower_id] = r1_needed
            self.allocated_r2[borrower_id] = r2_needed
            return True
        return False