
import random
import imageio
import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import os


class Body:
    def __init__(self, x, y, m, vx, vy):
        self.p = np.array([[x],
                           [y]], dtype='float64')
        self.m = m
        self.a = None
        self.v = np.array([[vx],
                           [vy]], dtype='float64')


GIF = True
bodies = [
    Body(-0.97000436, 0.24308753, 1, 0.4662036850, 0.4323657300),
    Body(0, 0, 1, -0.93240737, -0.8647314),
    Body(0.97000436, -0.24308753, 1, 0.4662036850, 0.4323657300),
]
G = 1
dt = 0.01


def step():
    for body1 in bodies:
        body1.a = np.array([[0],
                            [0]], dtype='float64')

        for body2 in bodies:
            if body1 == body2:
                continue
            body1.a += (G * body2.m * (body2.p - body1.p)) / \
                LA.norm(body2.p - body1.p) ** 3

        body1.v += body1.a * dt
        body1.p += body1.v * dt


def r():
    return random.randint(0, 255)


c = ['#%02X%02X%02X' % (r(), r(), r()) for _ in bodies]
s = [b.m*1e2 for b in bodies]
filenames = []
for i in range(500):
    if GIF:
        filename = f'{i}.png'
        filenames.append(filename)
    step()
    plt.scatter([b.p[0] for b in bodies], [b.p[1] for b in bodies],
                s=s, color=c)
    if GIF:
        plt.savefig(filename)
    plt.pause(0.001)
    plt.clf()
    # delta_x = max([abs(b.p[0][0] - bodies[2].p[0][0]) for b in bodies]) + 1.5
    # delta_y = max([abs(b.p[1][0] - bodies[2].p[1][0]) for b in bodies]) + 1.5
    # plt.axis([bodies[2].p[0][0] - delta_x, bodies[2].p[0][0] + delta_x,
    #           bodies[2].p[1][0] - delta_y, bodies[2].p[1][0] + delta_y])
    plt.axis([-2, 2, -2, 2])
    plt.grid(True, alpha=0.1)

if GIF:
    with imageio.get_writer('mygif.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    for filename in set(filenames):
        os.remove(filename)
