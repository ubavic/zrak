import numpy as np
import matplotlib.pyplot
import math

sirina = 1000
visina = 600
gledajOd = np.array([2, 1, 0])
gledajKa = np.array([0, -0.5, -6])
nagibKamere = -0.2
zizinaDaljina = 1

sfere = [
    {'centar': np.array([0, 0, -4]), 'pprecnik': 1, 'boja': np.array([1, 0, 0]), 'reflektivnost': 0.2},
    {'centar': np.array([-1, 0, -3]), 'pprecnik': 0.5, 'boja': np.array([0, 1, 0])},
    {'centar': np.array([0.8, 1, -4]), 'pprecnik': 0.3, 'boja': np.array([0, 0, 1])},
    {'centar': np.array([0, -10001, 0]), 'pprecnik': 10000, 'boja': np.array([1, 1, 1])},
    {'centar': np.array([1, -0.7, -3.5]), 'pprecnik': 0.3, 'boja': np.array([1, 1, 1]), 'reflektivnost': 1},
    {'centar': np.array([-1.05, 0, -2]),'pprecnik': 0.3, 'boja': np.array([1, 1, 1]), 'reflektivnost': 1, 'transparentnost': 1, 'indeks': 1.3},
]

izvoriSvetlosti = [
    {'centar': np.array([-2, 5, 0]), 'boja': np.array([20, 20, 20]), 'emisija': True, 'pprecnik': 1},
    {'centar': np.array([3, 0, -6]), 'boja': np.array([0, 0, 1]), 'emisija': True, 'pprecnik': 0.2},
    {'centar': np.array([2.7, 0, -4]), 'boja': np.array([1, 0, 0]), 'emisija': True, 'pprecnik': 0.2},
    {'centar': np.array([4, 0, -5]), 'boja': np.array([0, 1, 0]), 'emisija': True, 'pprecnik': 0.2},
    {'centar': np.array([2, 0, 0]), 'boja': np.array([5, 5, 5]), 'emisija': True, 'pprecnik': 0.2},
]


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
        t1, t2 = resenjaKvadratneJednacine(a, b, c)

        if t1 is None:
            return (0, None)

        if t1 < 0:
            t1 = t2

        return (1, zrak['tacka'] + t1 * zrak['pravac'])

    return (0, None)


def bojaZraka(zrak, dubina):
    udaljenostPrvogPreseka = math.inf
    boja = np.array([0, 0, 0])
    tackaPrvogPreseka = None
    najblizaSfera = None

    if dubina == 0:
        return boja

    for sfera in sfere:
        zrakSeceSferu, tackaPreseka = presekZrakaISfere(zrak, sfera)

        if not zrakSeceSferu:
            continue

        duzinaZraka = duzina(tackaPreseka - zrak['tacka'])

        if duzinaZraka < udaljenostPrvogPreseka:
            udaljenostPrvogPreseka = duzinaZraka
            tackaPrvogPreseka = tackaPreseka
            najblizaSfera = sfera
    
    for izvorSvetlosti in izvoriSvetlosti:
        zrakSeceSferu, tackaPreseka = presekZrakaISfere(zrak, izvorSvetlosti)
        
        if not zrakSeceSferu:
            continue
        
        duzinaZraka = duzina(tackaPreseka - zrak['tacka'])
        
        if duzinaZraka < udaljenostPrvogPreseka:
            udaljenostPrvogPreseka = duzinaZraka
            tackaPrvogPreseka = tackaPreseka
            najblizaSfera = izvorSvetlosti

    if tackaPrvogPreseka is not None:
        normalaSfere = normiraj(tackaPrvogPreseka - najblizaSfera['centar'])

        if 'emisija' in najblizaSfera:
            k = np.clip(1.5 * pow(abs(kosinusUgla(zrak['pravac'], normalaSfere)), 5), 0, 1)
            propustenZrak = {
                'pravac': zrak['pravac'],
                'tacka': tackaPrvogPreseka - 2 * np.dot(zrak['pravac'], normalaSfere) * najblizaSfera['pprecnik'] * zrak['pravac']
            }
            return k * najblizaSfera['boja'] + (1 - k) * bojaZraka(propustenZrak, dubina - 1)

        for izvorSvetlosti in izvoriSvetlosti:
            pravacKaSvetlu = normiraj(izvorSvetlosti['centar'] - tackaPrvogPreseka)
            zrakSenke = {
                'pravac': pravacKaSvetlu,
                'tacka': tackaPrvogPreseka
            }

            for sfera in sfere:
                zrakSenkeSeceSferu, presekZrakaSenke = presekZrakaISfere(zrakSenke, sfera)

                if zrakSenkeSeceSferu and duzina(presekZrakaSenke - tackaPrvogPreseka) < duzina(izvorSvetlosti['centar'] - tackaPrvogPreseka):
                    uSenci = 1
                    break
                else:
                    uSenci = 0

            if not uSenci:
                kosinus = kosinusUgla(pravacKaSvetlu, normalaSfere)
                rastojanje = duzina(izvorSvetlosti['centar'] - tackaPrvogPreseka)
                osvetljenje = kosinus * izvorSvetlosti['boja'] / rastojanje**2
                boja = boja + najblizaSfera['boja'] * osvetljenje

        if 'reflektivnost' in najblizaSfera:
            reflektovanZrak = {
                'pravac': zrak['pravac'] - 2 * np.dot(zrak['pravac'], normalaSfere) * normalaSfere,
                'tacka': tackaPrvogPreseka
            }
            boja = (1 - najblizaSfera['reflektivnost']) * boja + najblizaSfera['reflektivnost'] * bojaZraka(reflektovanZrak, dubina - 1)

        if 'transparentnost' in najblizaSfera:
            if kosinusUgla(normalaSfere, zrak['pravac']) > 0:
                normalaSfere = - normalaSfere
                indeks = najblizaSfera['indeks']
            else:
                indeks = 1 / najblizaSfera['indeks']

            kosinus = min([np.dot(normalaSfere, -1 * zrak['pravac']), 1])
            sinus = math.sqrt(1 - kosinus**2)
            if sinus <= 1:
                vNormalan = indeks * (zrak['pravac'] + kosinus * normalaSfere)
                vTransvezalan = -1 * math.sqrt(abs(1 - np.dot(vNormalan, vNormalan))) * normalaSfere
                propustenZrak = {
                    'pravac': vNormalan + vTransvezalan,
                    'tacka': tackaPrvogPreseka - 0.0001 * najblizaSfera['pprecnik'] * normalaSfere
                }
                boja = (1 - najblizaSfera['transparentnost']) * boja + najblizaSfera['transparentnost'] * bojaZraka(propustenZrak, dubina - 1)
            else:
                reflektovanZrak = {
                    'pravac': zrak['pravac'] - 2 * np.dot(zrak['pravac'], normalaSfere) * normalaSfere,
                    'tacka': tackaPrvogPreseka
                }
                boja = bojaZraka(reflektovanZrak, dubina - 1)

    return boja

gore = np.array([0, 1, 0])
pravacKamere = zizinaDaljina * normiraj(gledajKa - gledajOd)
vv_ = normiraj(np.cross(pravacKamere, gore))
vh_ = np.cross(vv_, pravacKamere)
vv = math.cos(nagibKamere) * vv_ + math.sin(nagibKamere) * vh_
vh = -math.sin(nagibKamere) * vv_ + math.cos(nagibKamere) * vh_
formatSlike = sirina/visina
slika = np.zeros((visina, sirina, 3))

for i in range(visina):
    y = (1 - 2 * i/visina) / formatSlike

    for j in range(sirina):
        x = -1 + 2 * j/sirina
        zrak = {
            'pravac': normiraj(pravacKamere + x * vv + y * vh),
            'tacka': gledajOd
        }
        
        slika[i, j] = np.clip(bojaZraka(zrak, 8), 0, 1)

matplotlib.pyplot.imsave('slika.png', slika)
