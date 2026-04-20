import matplotlib.pyplot as plt

def show_3d(dbz):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    z, y, x = dbz.shape

    ax.scatter(x, y, z, c=dbz.flatten(), cmap='jet', s=1)

    plt.show()
