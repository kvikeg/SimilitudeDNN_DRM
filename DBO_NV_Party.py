from Measure import Counters
import threading
import sys
import time

class PartySync:
    def __init__(self, parties: int):
        self.parties = parties
        self.secret_sharing_sync = threading.Event()
        self.online_start_sync = threading.Event()
        self.online_phase_2_sync = threading.Event()
        self.barrier = threading.Barrier(parties, self.stage_finished) 
        self.stage_done = threading.Event()

    def stage_finished(self):
        self.stage_done.set()
        self.barrier.reset()

    def wait_stage_done(self):
        self.stage_done.wait()
        self.stage_done.clear()

    def wait_secret_sharing(self):
        self.secret_sharing_sync.wait()

    def start_secret_sharing(self):
        self.secret_sharing_sync.set()

    def done_secret_sharing(self):
        self.barrier.wait()

    def wait_online(self):
        self.online_start_sync.wait()

    def start_online(self):
        self.online_start_sync.set()

    def done_online(self):
        self.barrier.wait()

    def wait_phase_2(self):
        self.online_phase_2_sync.wait()

    def start_online_phase_2(self):
        self.online_phase_2_sync.set()

    def done_phase_2(self):
        self.barrier.wait()

class PartyData:
    def __init__(self, sync: PartySync, poly_degree: int):
        self.share = None
        self.sync = sync
        self.poly_degree = poly_degree

    def set_threadid(self, threadID):
        self.threadID = threadID

    def set_share(self, share):
        self.share = share

class PartyThread (threading.Thread):
    def __init__(self, threadID, name, data):
        super(PartyThread, self).__init__()
        self.name = name
        self.data = data
        self.data.set_threadid(threadID)

    def run(self):
        print(self.name +  " ID:" + str(self.data.threadID) + " is ready")

        # wait for the initialization of shares 
        self.data.sync.wait_secret_sharing()

        # TODO: mult-split and distribute shares

        self.data.sync.done_secret_sharing()

        self.data.sync.wait_online()

        # TODO: do Eval 1 and Comm 1

        self.data.sync.done_online()

        self.data.sync.wait_phase_2()
        # TODO: Eval 2 and Comm 2
        self.data.sync.done_phase_2()

        # TODO: output reconstruction