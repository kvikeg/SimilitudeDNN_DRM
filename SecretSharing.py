from random import randint
import numpy as np

# perform multiplicative secret sharing
def mult_split(p, s, N, i):
    m = []
    for j in range(N):
        m.append(randint(1, p))
    lam = 1
    for mi in m:
        lam = lam * mi
    lam /= m[i]

    m[i] = s / lam
    return m


# Additive secret sharing procedure
def add_split(p, s, N):
    m = []
    for j in range(N-1):
        m.append(randint(1, p))
    m.append(s - sum(m))
    return m


# Secret Sharing Procedure
def DRM(p, s, N):
    """ p - prime, s - value to split, N - number of parties 
    """
    ma = add_split(p, s, N)
    cmatrix = None
    for i in range(N):
        cn = mult_split(p, ma[i], N, i)
        if i == 0:
            cmatrix = np.array([cn])
        else:
            cmatrix = np.append(cmatrix, [cn], axis=0)
    return cmatrix