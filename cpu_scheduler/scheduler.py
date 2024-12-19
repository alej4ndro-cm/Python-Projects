from abc import ABC, abstractmethod

class Scheduler(ABC):
    def __init__(self):
        self.ready = []
        self.device = []
        self.terminated = []
        self.time_execution = 0
        self.cpu_busy_time = 0  # New: Track CPU busy time
        self.avg_response_time = 0
        self.avg_wait_time = 0
        self.avg_turnaround_time = 0
        self.cpu_util = 0
        self.pcb = [[0] * 5 for _ in range(8)]

    def add(self, p):
        self.ready.append(p)

    def rq_toString(self):
        if not self.ready:
            return "Empty"
        return " ".join(f"P{p.pid}({p.cpu_burst[self.pcb[p.pid - 1][1]]})" for p in self.ready)

    def devicequeue_toString(self):
        if not self.device:
            return "Empty"
        return " ".join(f"P{p.pid}({p.io_wait - self.time_execution})" for p in self.device)

    def calculate_cpu_utilization(self):
        if self.time_execution > 0:
            self.cpu_util = (self.cpu_busy_time / self.time_execution) * 100
        else:
            self.cpu_util = 0

    def print_analytics(self):
        self.calculate_cpu_utilization()  # Calculate CPU utilization before printing
        print(f"\nTime needed to complete all processes: {self.time_execution}")
        print(f"CPU Utilization: {self.cpu_util:.2f}%")
        
        if self.terminated:
            print("\nTurnaround Times:")
            for p in self.terminated:
                print(f"P{p.pid}: {self.pcb[p.pid - 1][4]}")
            print(f"Average: {sum(self.pcb[p.pid - 1][4] for p in self.terminated) / len(self.terminated):.2f}")
            
            print("\nResponse Times:")
            for p in self.terminated:
                print(f"P{p.pid}: {self.pcb[p.pid - 1][2]}")
            print(f"Average: {sum(self.pcb[p.pid - 1][2] for p in self.terminated) / len(self.terminated):.2f}")
            
            print("\nWait Times:")
            for p in self.terminated:
                print(f"P{p.pid}: {self.pcb[p.pid - 1][3]}")
            print(f"Average: {sum(self.pcb[p.pid - 1][3] for p in self.terminated) / len(self.terminated):.2f}")
        else:
            print("No processes were terminated. Unable to calculate averages.")

    @abstractmethod
    def start(self):
        pass