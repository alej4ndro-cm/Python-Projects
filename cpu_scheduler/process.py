# process.py
class Process:
    def __init__(self, pid, burst):
        self.pid = pid
        self.burst = burst
        self.cpu_burst = []
        self.io_burst = []
        self.io_wait = 0
        self.queue = 1

    def parse(self):
        for i in range(len(self.burst)):
            if i % 2 == 0:
                self.cpu_burst.append(self.burst[i])
            else:
                self.io_burst.append(self.burst[i])