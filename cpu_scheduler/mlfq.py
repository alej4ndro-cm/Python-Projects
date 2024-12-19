from collections import deque
from scheduler import Scheduler

class MLFQ(Scheduler):
    def __init__(self):
        super().__init__()
        self.RR_TQ_QUEUE_1 = 5
        self.RR_TQ_QUEUE_2 = 10
        self.queue_1 = deque()
        self.queue_2 = deque()
        self.queue_3 = deque()
        self.cpu_busy_time = 0  # Add this line to track CPU busy time

    def start(self):
        for p in self.ready:
            self.queue_1.append(p)
        self.ready.clear()

        while self.queue_1 or self.queue_2 or self.queue_3 or self.device:
            while self.queue_1:
                print("\n\nQ1:", self.q1_toString())
                print("Q2:", self.q2_toString())
                print("Q3:", self.q3_toString())
                print("DQ:", self.devicequeue_toString())

                p = self.queue_1.popleft()
                if self.pcb[p.pid - 1][0] == 0:
                    self.pcb[p.pid - 1][0] = 1
                    self.pcb[p.pid - 1][2] = self.time_execution

                if p.cpu_burst[self.pcb[p.pid - 1][1]] <= self.RR_TQ_QUEUE_1:
                    burst_time = p.cpu_burst[self.pcb[p.pid - 1][1]]
                    self.time_execution += burst_time
                    self.cpu_busy_time += burst_time  # Update CPU busy time
                    print(f"[Te: {self.time_execution}] - Process {p.pid} ran")
                    print(f"[Te: {self.time_execution}] Total execution has finished: ", end="")
                    try:
                        self.pcb[p.pid - 1][3] += (self.time_execution - burst_time) - p.io_wait
                        p.io_wait = self.time_execution + p.io_burst[self.pcb[p.pid - 1][1]]
                        self.device.append(p)
                        print("No")
                    except IndexError:
                        self.terminated.append(p)
                        print("Yes")
                        self.pcb[p.pid - 1][4] = self.time_execution
                else:
                    self.time_execution += self.RR_TQ_QUEUE_1
                    self.cpu_busy_time += self.RR_TQ_QUEUE_1  # Update CPU busy time
                    print(f"[Te: {self.time_execution}] - Process {p.pid} ran")
                    p.cpu_burst[self.pcb[p.pid - 1][1]] -= self.RR_TQ_QUEUE_1
                    self.queue_2.append(p)
                    p.queue = 2
                    print(f"[Te: {self.time_execution}] Total execution has finished: No")

                self.check_io()

            while self.queue_2 and not self.queue_1:
                print("\n\nQ1:", self.q1_toString())
                print("Q2:", self.q2_toString())
                print("Q3:", self.q3_toString())
                print("DQ:", self.devicequeue_toString())

                p = self.queue_2.popleft()
                if p.cpu_burst[self.pcb[p.pid - 1][1]] <= self.RR_TQ_QUEUE_2:
                    burst_time = p.cpu_burst[self.pcb[p.pid - 1][1]]
                    self.time_execution += burst_time
                    self.cpu_busy_time += burst_time  # Update CPU busy time
                    print(f"[Te: {self.time_execution}] - Process {p.pid} ran")
                    print(f"[Te: {self.time_execution}] Total execution has finished: ", end="")
                    try:
                        self.pcb[p.pid - 1][3] += (self.time_execution - burst_time) - p.io_wait
                        p.io_wait = self.time_execution + p.io_burst[self.pcb[p.pid - 1][1]]
                        self.device.append(p)
                        print("No")
                    except IndexError:
                        self.terminated.append(p)
                        self.pcb[p.pid - 1][4] = self.time_execution
                        print("Yes")
                else:
                    self.time_execution += self.RR_TQ_QUEUE_2
                    self.cpu_busy_time += self.RR_TQ_QUEUE_2  # Update CPU busy time
                    print(f"[Te: {self.time_execution}] - Process {p.pid} ran")
                    print(f"[Te: {self.time_execution}] Total execution has finished: No")
                    p.cpu_burst[self.pcb[p.pid - 1][1]] -= self.RR_TQ_QUEUE_2
                    self.queue_3.append(p)
                    p.queue = 3
                self.check_io()

            while self.queue_3 and not self.queue_1 and not self.queue_2:
                print("\n\nQ1:", self.q1_toString())
                print("Q2:", self.q2_toString())
                print("Q3:", self.q3_toString())
                print("DQ:", self.devicequeue_toString())

                p = self.queue_3.popleft()
                burst_time = p.cpu_burst[self.pcb[p.pid - 1][1]]
                self.time_execution += burst_time
                self.cpu_busy_time += burst_time  # Update CPU busy time
                print(f"[Te: {self.time_execution}] - Process {p.pid} ran")
                print(f"[Te: {self.time_execution}] Total execution has finished: ", end="")
                try:
                    self.pcb[p.pid - 1][3] += (self.time_execution - burst_time) - p.io_wait
                    p.io_wait = self.time_execution + p.io_burst[self.pcb[p.pid - 1][1]]
                    self.device.append(p)
                    print("No")
                except IndexError:
                    self.terminated.append(p)
                    self.pcb[p.pid - 1][4] = self.time_execution
                    print("Yes")

                self.check_io()

        self.calculate_cpu_utilization()  # Calculate CPU utilization
        self.print_analytics()

    def check_io(self):
        if self.device:
            p = min(self.device, key=lambda x: x.io_wait)
            if p.io_wait <= self.time_execution:
                self.device.remove(p)
                self.pcb[p.pid - 1][1] += 1
                if p.queue == 1:
                    self.queue_1.append(p)
                elif p.queue == 2:
                    self.queue_2.append(p)
                else:
                    self.queue_3.append(p)

        if self.device and not self.queue_1 and not self.queue_2 and not self.queue_3:
            p = min(self.device, key=lambda x: x.io_wait)
            idle_time = p.io_wait - self.time_execution
            if idle_time > 0:
                self.time_execution = p.io_wait
            self.device.remove(p)
            self.pcb[p.pid - 1][1] += 1
            if p.queue == 1:
                self.queue_1.append(p)
            elif p.queue == 2:
                self.queue_2.append(p)
            else:
                self.queue_3.append(p)

    def calculate_cpu_utilization(self):
        if self.time_execution > 0:
            self.cpu_util = (self.cpu_busy_time / self.time_execution) * 100
        else:
            self.cpu_util = 0

    def q1_toString(self):
        return " ".join(f"P{p.pid}({p.cpu_burst[self.pcb[p.pid - 1][1]]})" for p in self.queue_1) or "Empty"

    def q2_toString(self):
        return " ".join(f"P{p.pid}({p.cpu_burst[self.pcb[p.pid - 1][1]]})" for p in self.queue_2) or "Empty"

    def q3_toString(self):
        return " ".join(f"P{p.pid}({p.cpu_burst[self.pcb[p.pid - 1][1]]})" for p in self.queue_3) or "Empty"