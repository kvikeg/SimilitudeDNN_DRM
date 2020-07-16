import random 
import math
import sys
import threading
from DBO_NV_Party import PartyThread

MAXINT = 1 << 64
MAXTRY = 1000

def isPrime(candidate):
    """ Returns True if candidate is a prime number else False """
    # Make sure n is a positive integer
    # if not then make it positive intger
    candidate = abs(int(candidate))
 
    # ----- some simple and fast tests ---------
    
    # The number n is less 2 i-e 0 or 1
    if candidate < 2: 
        return False
    
    # The number n is 2
    if candidate == 2: 
        return True
 
    # The number n is even then not prime
    if candidate % 2 == 0: 
        return False
 
    # Check odd numbers less than the square root of the given number n for possible factors 
    r = math.sqrt( candidate )
    
    # start from 3, we have already test for 0, 1 and 2
    x = 3 
    while x <= r:
        if candidate % x == 0: 
            return False 
        x += 2 # Increment to the next odd number
 
    # No factors found, so number is prime  
    return True 

def get_prime():
    random.seed(17)
    shouldStop = False
    cycle = 0 
    while not shouldStop:
        candidate = random.randint(0, MAXINT)
        cycle += 1
        if cycle % 10 == 0:
            print("Attempt:" + str(cycle) + "\tcandidate:" + str(candidate))
        shouldStop = isPrime(candidate)
        if cycle >= MAXTRY:
            raise ValueError()

    print("Found prime number:" + str(candidate))
    return candidate


def start_parties(parties: int, party_data):
    threads = []
    thread = None
    for i in range(parties):
        thread = PartyThread(i, str("thread " + str(i)), party_data[i])
        thread.start() 
        threads.append(thread) 

    return threads

def close_parties(threads):
    for t in threads:
        t.join()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(get_prime())
    else:
        print(sys.argv[1] + " is prime: " + str(isPrime(int(sys.argv[1]))))