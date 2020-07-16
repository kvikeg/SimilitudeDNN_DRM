import SecretSharing
from numpy.polynomial import Polynomial as P
from Measure import Counters
import utils
from DBO_NV_Party import PartyData, PartySync

num_parties = 3
num_secrets = 1

prime = 18014398241046527

party_data = []

sync_obj = PartySync(num_parties)

def send_to_party(share, party):
    print("Sending to "+ str(party) + str(share))
    party_data[party].set_share(share)

def send_shares_to_all(cmatrix, parties: int, counters: Counters):
    for i in range(parties):
        send_to_party(cmatrix[:, i], i)
        counters.send_bytes(len(cmatrix[:, i].tobytes())) 

# DB scheme (with pre-processing) and Non-Vanishing 
def DBO_NV(parties: int, poly, counters):
    # start participating parties
    for i in range(parties):
        party_data.append(PartyData(sync_obj, poly.degree()))

    threads = utils.start_parties(parties, party_data)

    counters.start_test()
    # pre-processing stage
    for i in range(poly.degree() + 1):    
        cmatrix = SecretSharing.DRM(prime, poly.coef[i], parties)

        # send drm_share column to each participating party
        send_shares_to_all(cmatrix, parties, counters)

        ######################################
        # done with correlated randomness
        ######################################
        sync_obj.start_secret_sharing()
        # Each party secret shares s_i using Multi share
        sync_obj.wait_stage_done()

        # online stage:
        sync_obj.start_online()
        # each party computes alpha
        # send j'th part to party J
        sync_obj.wait_stage_done()

        sync_obj.start_online_phase_2()
        # for each monomial compute multiplication
        # send summation result
        sync_obj.wait_stage_done()
        # compute output

    utils.close_parties(threads)
    counters.stop_test()
    counters.print_results()

if __name__ == '__main__':
    counters = Counters()
    pol = P([1, 2, 3])
    DBO_NV(3, pol, counters)