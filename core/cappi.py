import numpy as np

def generate_cappi(xg, level=4):
    return xg['DBZ'][:, level, :, :].values[0]
