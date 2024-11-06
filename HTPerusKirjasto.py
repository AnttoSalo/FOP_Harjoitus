######################################################################
# CT60A0203 Ohjelmoinnin perusteet
# Tekijä: Antto Salo
# Opiskelijanumero: 002606347
# Päivämäärä: 31.10.2024
# Kurssin oppimateriaalien lisäksi työhön ovat vaikuttaneet seuraavat
# lähteet ja henkilöt, ja se näkyy tehtävässä seuraavalla tavalla:
#
# Mahdollisen vilppiselvityksen varalta vakuutan, että olen tehnyt itse
# tämän tehtävän ja vain yllä mainitut henkilöt sekä lähteet ovat
# vaikuttaneet siihen yllä mainituilla tavoilla.
######################################################################
# Tehtävä Harjaitustyö

import time

def kirjoitaLista(Nimi, Tiedot):
    Tiedosto = open(Nimi, "w")
    for olio in Tiedot:
        Tiedosto.write("{}:{}:{}:{}".format(olio.kuukausi,))
    Tiedosto.close()
    return None

def lueListaan(Nimi, Rivit):
    Rivit.clear()
    Tiedosto = open(Nimi, "r")
    Rivi = Tiedosto.readline()
    Rivi = Tiedosto.readline() # Skipataan otsikkorivi
    while (len(Rivi) > 0):
        Rivit.append(Rivi[:-1])
        Rivi = Tiedosto.readline()
    Tiedosto.close()
    return Rivit

def luoLista(tiedot, SDATA):
    lista = []
    for rivi in tiedot:
        osat = rivi.split(";")
        sdata = SDATA()
        aikaleima = time.strptime(osat[0], "%d-%m-%Y %H:%M")
        sdata.paiva = aikaleima.tm_mday
        sdata.kuukausi = aikaleima.tm_mon
        sdata.vuosi = aikaleima.tm_year
        sdata.tunti = aikaleima.tm_hour
        sdata.kWhPaiva = float(osat[1])
        sdata.kWhYo = float(osat[2])
        # debug
        print("Tunti: {}, Päivä: {}, Kuukausi: {}, Vuosi: {}, kWh Päivä: {}, kWh Yö: {}".format(
            sdata.tunti, sdata.paiva, sdata.kuukausi, sdata.vuosi, sdata.kWhPaiva, sdata.kWhYo))
        lista.append(sdata)
    return lista

def etsiListasta(kkData, kuukausi):
    #Etsii listasta olemassaolevan arvon, jos löytyy
    for kkdata in kkData:
        if kkdata.kuukausi == kuukausi:
            return kkdata
    return None

def kysyTiedosto():
    Nimi = input("Anna tiedoston nimi: ")
    return Nimi
# eof 