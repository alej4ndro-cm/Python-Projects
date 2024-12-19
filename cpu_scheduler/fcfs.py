from scheduler import Scheduler
from collections import deque

class FCFS(Scheduler):
    def __init__(self):
        super().__init__()
        self.ready = deque()
        self.cpu_busy_time = 0  # Add this line to track CPU busy time

    def start(self):
        while self.ready:
            print(f"[Information] RQ: {self.rq_toString()}")
            print(f"[Information] DQ: {self.devicequeue_toString()}")
            process = self.ready.popleft()

            if self.pcb[process.pid - 1][0] == 0:
                self.pcb[process.pid - 1][2] = self.time_execution
                self.pcb[process.pid - 1][3] += self.time_execution
                self.pcb[process.pid - 1][0] = 1

            burst_time = process.cpu_burst[self.pcb[process.pid - 1][1]]
            self.time_execution += burst_time
            self.cpu_busy_time += burst_time  # Update CPU busy time
            print(f"[Te: {self.time_execution}] Process {process.pid} has ran")

            print(f"[Te: {self.time_execution}] Total execution finished: ", end="")
            try:
                process.io_wait = self.time_execution + process.io_burst[self.pcb[process.pid - 1][1]]
                self.device.append(process)
                print("No")
            except IndexError:
                self.terminated.append(process)
                self.pcb[process.pid - 1][4] = self.time_execution
                print("Yes")
            print()

            if not self.ready and self.device:
                p = min(self.device, key=lambda x: x.io_wait)

                if self.time_execution < p.io_wait:
                    print("[CPU] - Idling")
                    self.time_execution = p.io_wait

                self.pcb[p.pid - 1][1] += 1
                self.ready.append(p)
                self.device.remove(p)
                self.pcb[process.pid - 1][3] += self.time_execution - p.io_wait

        self.calculate_cpu_utilization()  # Calculate CPU utilization before printing
        self.print_analytics()

    def calculate_cpu_utilization(self):
        if self.time_execution > 0:
            self.cpu_util = (self.cpu_busy_time / self.time_execution) * 100
        else:
            self.cpu_util = 0