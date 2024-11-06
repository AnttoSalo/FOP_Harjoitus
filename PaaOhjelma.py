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

import HTPerusKirjasto
import time
import calendar

class SDATA:
    paiva = None
    kuukausi = None
    vuosi = None
    tunti = None
    kWhPaiva = None
    kWhYo = None
class KKDATA:
    kuukausi = None
    kWhPaiva = None
    kWhYo = None
    kWhYhteensa = None 

def valikko():
    print("Valitse haluamasi toiminto:")
    print("1) Lue tiedosto")
    print("2) Analysoi")
    print("3) Kirjoita tiedosto")
    print("4) Analysoi viikonpäivittäiset tulokset")
    print("0) Lopeta")
    valinta = int(input("Valintasi: "))
    return valinta

def find_kkdata(kkData, kuukausi):
    for kkdata in kkData:
        if kkdata.kuukausi == kuukausi:
            return kkdata
    return None

def analysoi(tiedot):
    sdatalista = []
    sdatalista:list[SDATA] = HTPerusKirjasto.luoLista(tiedot, SDATA)
    kkData = []
    for alkio in sdatalista:
        kk = alkio.kuukausi
        olemassaoleva_data:KKDATA = HTPerusKirjasto.etsiListasta(kkData, kk)
        if olemassaoleva_data is None:
            uusi_kkdata = KKDATA()
            uusi_kkdata.kuukausi = kk
            uusi_kkdata.kWhPaiva = alkio.kWhPaiva
            uusi_kkdata.kWhYo = alkio.kWhYo
            uusi_kkdata.kWhYhteensa = alkio.kWhPaiva + alkio.kWhYo
            kkData.append(uusi_kkdata)
        else:
            data = olemassaoleva_data
            data.kWhPaiva += alkio.kWhPaiva
            data.kWhYo += alkio.kWhYo
            data.kWhYhteensa += alkio.kWhPaiva + alkio.kWhYo
    return kkData

def paaOhjelma():
    tiedot = []
    while True:
        valinta = valikko()
        if valinta == 0: return
        elif valinta == 1:
            tiedosto = HTPerusKirjasto.kysyTiedosto()
            tiedot = HTPerusKirjasto.lueListaan(tiedosto, tiedot)
            print("Tiedostosta {} luettiin {} riviä".format(tiedosto, len(tiedot))) # -1 koska ensimmäinen rivi on otsikko
            print(tiedot)
        elif valinta == 2: 
            tiedot = analysoi(tiedot)
        elif valinta == 3: 
            HTPerusKirjasto.kirjoitaLista(HTPerusKirjasto.kysyTiedosto(), tiedot)
        elif valinta == 4: analysoiViikonpaivittain()
        else: print("Virheellinen valinta")
    
paaOhjelma()

def analysoiViikonpaivittain():
    print("Analysoi viikonpäivittäin")
    return None



# eof