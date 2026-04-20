import pyiwr

def create_grid(file_path):
    return pyiwr.sweeps2gridnc(file_path)
