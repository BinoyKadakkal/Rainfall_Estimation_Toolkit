import numpy as np

def marshall_palmer(dbz):
    Z = 10 ** (dbz / 10.0)
    return (Z / 200.0) ** (1 / 1.6)

def convective(dbz):
    Z = 10 ** (dbz / 10.0)
    return (Z / 300.0) ** (1 / 1.4)
