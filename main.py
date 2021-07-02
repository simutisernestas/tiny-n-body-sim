
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


BIGGEST = 9e7
bodies = [Body(0, 0, 5e6, -19, -52), Body(0, 1, 7e6, 60, -30),
          Body(1, 1, BIGGEST, -0.1, -0.2), Body(2, 2, 2e7, 10, -30)]
G = 0.0000031
dt = 0.003


def step():
    for body1 in bodies:
        body1.a = np.array([[0],
                            [0]], dtype='float64')

        for body2 in bodies:
            if body1 == body2:
                continue
            body1.a += (G * body2.m * (body2.p - body1.p)) / \
                LA.norm(body2.p - body1.p)

        body1.v += body1.a * dt
        body1.p += body1.v * dt


s = [b.m/BIGGEST*1e3 for b in bodies]
c = [0, 1, 2, 3]

filenames = []
for i in range(500):
    filename = f'{i}.png'
    filenames.append(filename)
    step()
    plt.scatter([b.p[0] for b in bodies], [b.p[1] for b in bodies],
                s=s, color=['#FF00E6', '#00FFFF', '#0202D5', '#CC0000'])
    plt.savefig(filename)
    plt.pause(0.01)
    plt.clf()
    delta_x = max([abs(b.p[0][0] - bodies[2].p[0][0]) for b in bodies]) + 1.5
    delta_y = max([abs(b.p[1][0] - bodies[2].p[1][0]) for b in bodies]) + 1.5
    plt.axis([bodies[2].p[0][0] - delta_x, bodies[2].p[0][0] + delta_x,
              bodies[2].p[1][0] - delta_y, bodies[2].p[1][0] + delta_y])
    plt.grid(True, alpha=0.1)

with imageio.get_writer('mygif.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)

for filename in set(filenames):
    os.remove(filename)
