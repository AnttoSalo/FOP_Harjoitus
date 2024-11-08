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
# Tehtävä Harjoitustyö

import time
import sys
import numpy

class SDATA:
    Pvm = None
    kWhPaiva = None
    kWhYo = None
    Lampotila = None

class KKDATA:
    Kuukausi = None
    MWhPaiva = None
    MWhYo = None
    MWhYhteensa = None 

class VPDATA:
    Viikonpaiva = None
    MWhYhteensa = None

def kirjoitaListaKk(Nimi, Tiedot:list[KKDATA]):
    try:
        Tiedosto = open(Nimi, "w")
        Tiedosto.write("Kuukausittaiset kulutukset (MWh):\nKuukausi;Yö;Päivä;Yhteensä\n")
        for olio in Tiedot:
            Tiedosto.write("{};{:.1f};{:.1f};{:.1f}\n".format(olio.Kuukausi,olio.MWhYo,olio.MWhPaiva,olio.MWhYhteensa))
        Tiedosto.close()
    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(Nimi))
        sys.exit(0)
    return None

def kirjoitaListaVp(Nimi, Tiedot:list[VPDATA]):
    try:
        Tiedosto = open(Nimi, "w")
        Tiedosto.write("Viikonpäivä;Kulutus (MWh)\n")
        for Olio in Tiedot:
            Tiedosto.write("{};{:.1f}\n".format(Olio.Viikonpaiva,Olio.MWhYhteensa))
        Tiedosto.close()
    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(Nimi))
        sys.exit(0)
    return None

def lueListaan(Nimi, Rivit):
    # Palauttaa listan, johon on luettu tiedoston rivit
    try:
        Rivit.clear()
        Tiedosto = open(Nimi, "r")
        Rivi = Tiedosto.readline()
        Rivi = Tiedosto.readline() # Skipataan otsikkorivi
        while (len(Rivi) > 0):
            Rivit.append(Rivi[:-1])
            Rivi = Tiedosto.readline()
        Tiedosto.close()
    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(Nimi))
        sys.exit(0)
    return Rivit

def lueSanakirjaan(Rivit):
    # Palauttaa sanakirjan, johon on luettu tiedoston rivit, avaimena pvm
    Sanakirja = {}
    for Rivi in Rivit:
        osat = Rivi.strip().split(";")
        Pvm = osat[0]
        PvmObj = time.strptime(Pvm, "%d-%m-%Y %H:%M")
        Pvm = time.strftime("%d-%m-%Y %H:%M", PvmObj)
        Avain = time.strftime("%d-%m-%Y", PvmObj)
        if Avain not in Sanakirja:
            Sdata = SDATA()
            Sdata.Pvm = Pvm
            Sdata.kWhYo = float(osat[1])
            Sdata.kWhPaiva = float(osat[2])
            Sanakirja[Avain] = Sdata
        else:
            Sdata = Sanakirja[Avain]
            Sdata.kWhYo += float(osat[1])
            Sdata.kWhPaiva += float(osat[2])
    return Sanakirja


def etsiListastaKk(kkData, kuukausi):
    #Etsii listasta olemassaolevan arvon, jos löytyy
    for Data in kkData:
        if Data.Kuukausi == kuukausi:
            return Data
    return None

def etsiListastaVp(VpData, Viikonpaiva):
    #Etsii listasta olemassaolevan arvon, jos löytyy
    for Data in VpData:
        if Data.Viikonpaiva == Viikonpaiva:
            return Data
    return None

def analysoiKuukausiTiedot(tiedot):
    kkData = {}
    # Process SDATA objects and calculate monthly consumption
    for pvm_str, alkio in tiedot.items():
        pvm = time.strptime(pvm_str, "%d-%m-%Y")
        kk = pvm.tm_mon

        if kk not in kkData:
            UusiData = KKDATA()
            kuukausi_nimi = time.strftime("%b", pvm)
            UusiData.Kuukausi = kuukausi_nimi
            UusiData.MWhPaiva = alkio.kWhPaiva / 1000
            UusiData.MWhYo = alkio.kWhYo / 1000
            UusiData.MWhYhteensa = (alkio.kWhPaiva + alkio.kWhYo) / 1000
            kkData[kk] = UusiData
        else:
            Data = kkData[kk]
            Data.MWhPaiva += alkio.kWhPaiva / 1000
            Data.MWhYo += alkio.kWhYo / 1000
            Data.MWhYhteensa += (alkio.kWhPaiva + alkio.kWhYo) / 1000
    # Return a list of KKDATA objects
    return list(kkData.values())


def analysoiViikonpaivittain(tiedot):
    VIIKONPAIVAT = ["Maanantai", "Tiistai", "Keskiviikko",
                    "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
    # Initialize vpData with all weekdays, consumption set to zero
    vpData = {}
    for ViikonPaiva in VIIKONPAIVAT:
        UusiData = VPDATA()
        UusiData.Viikonpaiva = ViikonPaiva
        UusiData.MWhYhteensa = 0.0
        vpData[ViikonPaiva] = UusiData
    # Now process the data
    for pvm_str, alkio in tiedot.items():
        pvm = time.strptime(pvm_str, "%d-%m-%Y %H:%M")
        ViikonPaiva = VIIKONPAIVAT[pvm.tm_wday]
        Data = vpData[ViikonPaiva]
        Data.MWhYhteensa += (alkio.kWhPaiva + alkio.kWhYo) / 1000
    # Convert dictionary to list and sort by day of the week
    vpDataList = list(vpData.values())
    vpDataList.sort(key=lambda x: VIIKONPAIVAT.index(x.Viikonpaiva))
    return vpDataList

def yhdistaLampotila(Tiedot, Tiedosto):
    # Yhdistää lämpötilatiedoston sähkönkulutustietoihin
    # Palauttaa listan, johon on yhdistetty tiedot
    try:
        Tiedosto = open(Tiedosto, "r")
        Rivi = Tiedosto.readline()
        Rivi = Tiedosto.readline() # Skipataan otsikkorivi
        while (len(Rivi) > 0):
            osat = Rivi.strip().split(",")
            Pvm = osat[0]
            PvmObj = time.strptime(Pvm, "%Y.%m.%d")
            PvmStr = time.strftime("%d-%m-%Y", PvmObj)
            if PvmStr in Tiedot:
                Sdata = Tiedot[PvmStr]
                Sdata.Lampotila = float(osat[1])
            Rivi = Tiedosto.readline()
        Tiedosto.close()
    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(Tiedosto))
        sys.exit(0)
    return Tiedot

def kirjoitaYhdistettyData(Nimi, Tiedot):
    try:
        Tiedosto = open(Nimi, "w")
        Tiedosto.write("Päivittäiset kulutukset (kWh) ja lämpötila:\nPvm;Yö;Päivä;Yhteensä;Lämpötila\n")
        for Pvm, Olio in Tiedot.items():
            PvmObj = time.strptime(Pvm, "%d-%m-%Y")
            PvmStr = time.strftime("%d.%m.%Y", PvmObj)
            Tiedosto.write("{};{:.1f};{:.1f};{:.1f};{:.1f}\n".format(PvmStr, Olio.kWhYo,Olio.kWhPaiva,Olio.kWhYo+Olio.kWhPaiva, Olio.Lampotila))
        Tiedosto.close()
    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(Nimi))
        sys.exit(0)
    return None

def analysoiViikoittain(Tiedot):
    # Initialize the NumPy matrix with zeros
    matriisi = numpy.zeros((54, 3))

    # Process the input data
    for Rivi in Tiedot:
        Rivi = Rivi.split(";")
        pvm = time.strptime(Rivi[0], "%d-%m-%Y %H:%M")
        viikko = int(time.strftime("%W", pvm))
        if pvm.tm_hour < 8:
            i = 0  # Klo 0-8
        elif pvm.tm_hour < 16:
            i = 1  # Klo 8-16
        else:
            i = 2  # Klo 16-24
        matriisi[viikko][i] += (float(Rivi[1]) + float(Rivi[2]))
    return matriisi

def viikkoSumma(Viikko):
    sum = 0
    for i in Viikko:
        sum += i
    return sum

def matriisiSumma(Matriisi):
    summa1 = 0
    summa2 = 0
    summa3 = 0
    for Viikko in Matriisi:
        summa1 += Viikko[0]
        summa2 += Viikko[1]
        summa3 += Viikko[2]
    kokonaisSumma = summa1 + summa2 + summa3
    return "{:.1f};{:.1f};{:.1f};{:.1f}\n".format(summa1/1000, summa2/1000, summa3/1000,kokonaisSumma/1000)


def kirjoitaMatriisi(Tiedosto, Tiedot):
    try:
        Tiedosto = open(Tiedosto, "w")
        Tiedosto.write("Viikko;Klo 0-8;Klo 8-16;Klo 16-24;Viikkosumma\n")
        for index, Viikko in enumerate(Tiedot):
            Tiedosto.write("Vko {};{:.1f};{:.1f};{:.1f};{:.1f}\n".format(index, Viikko[0]/1000, Viikko[1]/1000, Viikko[2]/1000, viikkoSumma(Viikko)/1000))
        Tiedosto.write("Yhteensä;{}".format(matriisiSumma(Tiedot)))
        Tiedosto.close()
    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(Tiedosto))
        sys.exit(0)
    return None

def kysyTiedosto():
    Nimi = input("Anna tiedoston nimi: ")
    return Nimi
# eof 