from scheduler import Scheduler

class SJF(Scheduler):
    def start(self):
        while self.ready:
            self.ready.sort(key=lambda p: p.cpu_burst[self.pcb[p.pid - 1][1]])

            print(f"[Information] RQ: {self.rq_toString()}")
            print(f"[Information] DQ: {self.devicequeue_toString()}")
            process = self.ready[0]
            for p in self.ready:
                if p.cpu_burst[self.pcb[p.pid - 1][1]] == process.cpu_burst[self.pcb[process.pid - 1][1]] and p.pid != process.pid:
                    print(f"Process {p.pid} has the same CPU burst ({p.cpu_burst[self.pcb[p.pid - 1][1]]}) as Process {process.pid}")
                    if p.io_wait < process.io_wait:
                        arrival_time = process.io_wait
                        process = p
                        print(f"Running Process {process.pid} because {process.io_wait} < {arrival_time}")

            if self.pcb[process.pid - 1][0] == 0:
                self.pcb[process.pid - 1][2] = self.time_execution
                self.pcb[process.pid - 1][0] = 1

            wait_time = self.time_execution - process.io_wait
            self.pcb[process.pid - 1][3] += wait_time

            burst_time = process.cpu_burst[self.pcb[process.pid - 1][1]]
            self.time_execution += burst_time
            self.cpu_busy_time += burst_time  # Update CPU busy time
            print(f"[Te: {self.time_execution}] - Process {process.pid} has ran")

            print("Total execution has finished: ", end="")
            try:
                process.io_wait = self.time_execution + process.io_burst[self.pcb[process.pid - 1][1]]
                self.device.append(process)
                print("No")
            except IndexError:
                self.pcb[process.pid - 1][4] = self.time_execution
                self.terminated.append(process)
                print("Yes")

            self.ready.remove(process)

            if self.device:
                tmp = []
                for p in self.device:
                    if p.io_wait <= self.time_execution:
                        tmp.append(p)
                        self.ready.append(p)

                for p in tmp:
                    self.pcb[p.pid - 1][1] += 1
                    self.device.remove(p)

            if not self.ready and self.device:
                temp_p = min(self.device, key=lambda p: p.io_wait)
                idle_time = temp_p.io_wait - self.time_execution
                self.time_execution = temp_p.io_wait
                # We don't update cpu_busy_time here because the CPU is idle

                self.ready.append(temp_p)
                self.pcb[temp_p.pid - 1][1] += 1
                self.device.remove(temp_p)

            print()

        self.print_analytics()