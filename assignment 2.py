class ResourceAllocationSystem:
    def __init__(self, resources, processes):
        self.resources = resources  # Dictionary of resources with total and available units
        self.processes = processes  # Dictionary of processes with max demand, allocation, and requests

    def request_resources(self, process_id, request):
        print(f"\nProcess {process_id} Requests Resources: {request}")
        can_allocate = True

        # Check if resources can be allocated
        for resource, units in request.items():
            if units > self.resources[resource]["available"]:
                can_allocate = False

        if can_allocate:
            for resource, units in request.items():
                self.resources[resource]["available"] -= units
                self.processes[process_id]["allocation"][resource] += units
                self.processes[process_id]["request"][resource] -= units
            print(f"Resources allocated to Process {process_id}")
        else:
            print(f"Process {process_id} must wait: Resources unavailable")

        self.print_state()

    def release_resources(self, process_id):
        print(f"\nProcess {process_id} Releases Resources")
        for resource, units in self.processes[process_id]["allocation"].items():
            self.resources[resource]["available"] += units
            self.processes[process_id]["allocation"][resource] = 0

        self.print_state()

    def detect_deadlock(self):
        print("\nDetecting Deadlock...")
        work = {res: self.resources[res]["available"] for res in self.resources}
        finish = {pid: False for pid in self.processes}

        while True:
            progress = False
            for pid, process in self.processes.items():
                if not finish[pid]:
                    if all(process["request"][res] <= work[res] for res in process["request"]):
                        for res in self.resources:
                            work[res] += process["allocation"][res]
                        finish[pid] = True
                        progress = True
                        print(f"Process {pid} can finish")
            if not progress:
                break

        if all(finish.values()):
            print("No Deadlock Detected")
        else:
            deadlocked = [pid for pid, done in finish.items() if not done]
            print(f"Deadlock Detected: Processes in deadlock: {deadlocked}")

    def print_state(self):
        print("\nCurrent State of Resources:")
        for res, info in self.resources.items():
            print(f"{res}: {info['available']} available")

        print("\nCurrent State of Processes:")
        for pid, process in self.processes.items():
            print(f"Process {pid}: Allocation {process['allocation']}, Request {process['request']}")


# Example System Setup
resources = {
    "R1": {"total": 3, "available": 3},
    "R2": {"total": 2, "available": 2},
    "R3": {"total": 2, "available": 2}
}

processes = {
    "P1": {
        "max_demand": {"R1": 0, "R2": 1, "R3": 1},
        "allocation": {"R1": 0, "R2": 0, "R3": 0},
        "request": {"R1": 0, "R2": 1, "R3": 1}
    },
    "P2": {
        "max_demand": {"R1": 0, "R2": 1, "R3": 1},
        "allocation": {"R1": 0, "R2": 0, "R3": 0},
        "request": {"R1": 0, "R2": 1, "R3": 1}
    },
    "P3": {
        "max_demand": {"R1": 1, "R2": 0, "R3": 1},
        "allocation": {"R1": 0, "R2": 0, "R3": 0},
        "request": {"R1": 1, "R2": 0, "R3": 1}
    }
}

# Create the system
system = ResourceAllocationSystem(resources, processes)

# Simulate Resource Requests
system.request_resources("P1", {"R1": 0, "R2": 1, "R3": 1})
system.request_resources("P2", {"R1": 0, "R2": 1, "R3": 1})
system.request_resources("P3", {"R1": 1, "R2": 0, "R3": 1})

# Check for Deadlock
system.detect_deadlock()
