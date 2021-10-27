import numpy as np
import matplotlib.pyplot
import math

sirina = 1000
visina = 600

sfera1 = {
    'centar': np.array([0, 0, -4]),
    'pprecnik': 1
}


def duzina(vektor):
    return math.sqrt(np.dot(vektor, vektor))


def normiraj(vektor):
    d = duzina(vektor)

    if d == 0:
        return vektor
    else:
        return vektor/d


def presekZrakaISfere(zrak, sfera):
    ss = np.dot(sfera['centar'], sfera['centar'])
    sz = np.dot(sfera['centar'], zrak['pravac'])

    if sz > 0 and ss - sz * sz < sfera['pprecnik']:
        return 1

    return 0


formatSlike = sirina/visina
slika = np.zeros((visina, sirina, 3))

for i in range(visina):
    y = (1 - 2 * i/visina) / formatSlike

    for j in range(sirina):
        x = -1 + 2 * j/sirina
        zrak = {
            'pravac': normiraj(np.array([x, y, -1])),
            'tacka': np.array([0, 0, 0])
        }

        if presekZrakaISfere(zrak, sfera1):
            slika[i, j] = np.array([1, 1, 1])
        else:
            slika[i, j] = np.array([0, 0, 0])

matplotlib.pyplot.imsave('slika.png', slika)
