import numpy as np
import matplotlib.pyplot

sirina = 1000
visina = 600

slika = np.zeros((visina, sirina, 3))

for i in range(visina):
    for j in range(sirina):
        slika[i, j] = np.array([0, i/visina, j/sirina])

matplotlib.pyplot.imsave('slika.png', slika)
