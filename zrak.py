import numpy as np
import matplotlib.pyplot
import math

sirina = 1000
visina = 600


def duzina(vektor):
    return math.sqrt(np.dot(vektor, vektor))


def normiraj(vektor):
    d = duzina(vektor)

    if d == 0:
        return vektor
    else:
        return vektor/d


slika = np.zeros((visina, sirina, 3))

for i in range(visina):
    for j in range(sirina):
        slika[i, j] = np.array([0, i/visina, j/sirina])

matplotlib.pyplot.imsave('slika.png', slika)
