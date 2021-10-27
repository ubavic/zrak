import numpy as np
import matplotlib.pyplot
import math

sirina = 1000
visina = 600

sfere = [
    {'centar': np.array([0, 0, -4]), 'pprecnik': 1, 'boja': np.array([1, 0, 0])},
    {'centar': np.array([-1, 0, -3]), 'pprecnik': 0.5, 'boja': np.array([0, 1, 0])},
    {'centar': np.array([0.8, 1, -4]),'pprecnik': 0.3, 'boja': np.array([0, 0, 1])},
    {'centar': np.array([0, -10001, 0]),'pprecnik': 10000, 'boja': np.array([1, 1, 1])},
]

izvorSvetlosti = {
    'centar': np.array([-2, 5, 0]),
    'boja': np.array([30, 30, 30])
}


def duzina(vektor):
    return math.sqrt(np.dot(vektor, vektor))


def normiraj(vektor):
    d = duzina(vektor)

    if d == 0:
        return vektor
    else:
        return vektor/d


def kosinusUgla(vektorA, vektorB):
    a = duzina(vektorA)
    b = duzina(vektorB)

    if a == 0 or b == 0:
        return 1
    else:
        return np.dot(vektorA, vektorB)/(a * b)


def resenjaKvadratneJednacine(a, b, c):
    D = b**2 - 4 * a * c

    if D < 0:
        return (None, None)
    else:
        return ((-b - math.sqrt(D))/(2 * a), (-b + math.sqrt(D))/(2 * a))


def presekZrakaISfere(zrak, sfera):
    sz = np.dot(sfera['centar'] - zrak['tacka'], zrak['pravac'])

    if sz > 0:
        a = np.dot(zrak['pravac'], zrak['pravac'])
        b = 2 * np.dot(zrak['pravac'], zrak['tacka'] - sfera['centar'])
        c = np.dot(zrak['tacka'] - sfera['centar'],
                   zrak['tacka'] - sfera['centar']) - sfera['pprecnik']**2
        t1, _ = resenjaKvadratneJednacine(a, b, c)

        if t1 is None:
            return (0, None)

        return (1, zrak['tacka'] + t1 * zrak['pravac'])

    return (0, None)


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
        udaljenostPrvogPreseka = math.inf
        boja = np.array([0, 0, 0])
        tackaPrvogPreseka = None
        najblizaSfera = None

        for sfera in sfere:
            zrakSeceSferu, tackaPreseka = presekZrakaISfere(zrak, sfera)

            if not zrakSeceSferu:
                continue

            duzinaZraka = duzina(tackaPreseka - zrak['tacka'])

            if duzinaZraka < udaljenostPrvogPreseka:
                udaljenostPrvogPreseka = duzinaZraka
                tackaPrvogPreseka = tackaPreseka
                najblizaSfera = sfera

        if tackaPrvogPreseka is not None:
            normalaSfere = normiraj(tackaPrvogPreseka - najblizaSfera['centar'])
            pravacKaSvetlu = normiraj(izvorSvetlosti['centar'] - tackaPrvogPreseka)
            kosinus = kosinusUgla(pravacKaSvetlu, normalaSfere)
            rastojanje = duzina(izvorSvetlosti['centar'] - tackaPrvogPreseka)
            osvetljenje = kosinus * izvorSvetlosti['boja'] / rastojanje**2
            boja = najblizaSfera['boja'] * osvetljenje

        slika[i, j] = np.clip(boja, 0, 1)

matplotlib.pyplot.imsave('slika.png', slika)
