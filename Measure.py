import time

class Counters:
    def __init__(self):
        self.num_sent_bytes = 0
        self.start_time = 0
        self.end_time = 0

    def start_test(self):
        self.start_time = time.process_time()

    def stop_test(self):
        self.end_time = time.process_time()

    def get_duration(self):
        return self.end_time - self.start_time

    def send_bytes(self, num_bytes: int):
        self.num_sent_bytes += num_bytes

    def get_send_bytes(self):
        return self.num_sent_bytes

    def print_results(self):    
        print("Total Performance:")
        print("Sent: " + str(self.get_send_bytes()) + " bytes over the network")
        print("Took: " + str(self.get_duration()) + " seconds")