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

class SDATA:
    paiva = None
    kuukausi = None
    kuukausiStr = None
    vuosi = None
    tunti = None
    kWhPaiva = None
    kWhYo = None
class KKDATA:
    kuukausi = None
    MWhPaiva = None
    MWhYo = None
    MWhYhteensa = None 
class VPDATA:
    viikonpaiva = None
    MWhYhteensa = None

def kirjoitaListaKk(Nimi, Tiedot):
    try:
        Tiedosto = open(Nimi, "w")
        Tiedosto.write("Kuukausittaiset kulutukset (MWh):\nKuukausi;Yö;Päivä;Yhteensä\n")
        for olio in Tiedot:
            Tiedosto.write("{};{:.1f};{:.1f};{:.1f}\n".format(olio.kuukausiStr,olio.MWhPaiva,olio.MWhYo,olio.MWhYhteensa))
        Tiedosto.close()
    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(Nimi))
        sys.exit(0)
    return None

def kirjoitaListaVp(Nimi, Tiedot):
    try:
        Tiedosto = open(Nimi, "w")
        Tiedosto.write("Viikonpäivä;Kulutus (MWh)\n")
        for Olio in Tiedot:
            Tiedosto.write("{};{:.1f}\n".format(Olio.viikonpaiva,Olio.MWhYhteensa))
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

def luoLista(tiedot):
    # Muuntaa listan merkkijonot SDATA objekteiksi
    lista = []
    for Rivi in tiedot:
        osat = Rivi.split(";")
        Sdata = SDATA()
        Aikaleima = time.strptime(osat[0], "%d-%m-%Y %H:%M")
    
        Sdata.paiva = Aikaleima.tm_mday
        Sdata.kuukausi = Aikaleima.tm_mon
        Sdata.kuukausiStr = time.strftime("%b", Aikaleima)
        Sdata.vuosi = Aikaleima.tm_year
        Sdata.tunti = Aikaleima.tm_hour
        Sdata.kWhPaiva = float(osat[1])
        Sdata.kWhYo = float(osat[2])
    
        lista.append(Sdata)
    return lista

def etsiListastaKk(kkData, kuukausi):
    #Etsii listasta olemassaolevan arvon, jos löytyy
    for Data in kkData:
        if Data.kuukausi == kuukausi:
            return Data
    return None

def etsiListastaVp(VpData, viikonpaiva):
    #Etsii listasta olemassaolevan arvon, jos löytyy
    for Data in VpData:
        if Data.viikonpaiva == viikonpaiva:
            return Data
    return None

def analysoiKuukausiTiedot(tiedot):
    sdatalista = []
    # Listan merkkijonoista tehdään SDATA objekteja
    sdatalista = luoLista(tiedot)
    kkData = []
    # Käydään läpi SDATA objektit ja lasketaan kuukausittaiset kulutukset
    for alkio in sdatalista:
        kk = alkio.kuukausi
        olemassaoleva_data = etsiListastaKk(kkData, kk)
        if olemassaoleva_data is None:
            UusiData = KKDATA()
            UusiData.kuukausi = kk
            UusiData.MWhPaiva = alkio.kWhPaiva/1000
            UusiData.MWhYo = alkio.kWhYo/1000
            UusiData.MWhYhteensa = (alkio.kWhPaiva + alkio.kWhYo)/1000
            kkData.append(UusiData)
        else:
            Data = olemassaoleva_data
            Data.MWhPaiva += alkio.kWhPaiva/1000
            Data.MWhYo += alkio.kWhYo/1000
            Data.MWhYhteensa += (alkio.kWhPaiva + alkio.kWhYo)/1000
    return kkData

def analysoiViikonpaivittain(Tiedot):
    VIIKONPAIVAT = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
    sdatalista = []
    # Listan merkkijonoista tehdään SDATA objekteja
    sdatalista = luoLista(Tiedot)
    vpData = []
    # Käydään läpi SDATA objektit ja lasketaan kuukausittaiset kulutukset
    for alkio in sdatalista:
        pvmStr = "{}-{}-{}".format(alkio.paiva,alkio.kuukausi,alkio.vuosi)
        aikaleima = time.strptime(pvmStr, "%d-%m-%Y")
        ViikonPaiva = VIIKONPAIVAT[aikaleima.tm_wday]

        olemassaoleva_data = etsiListastaVp(vpData, ViikonPaiva)
        if olemassaoleva_data is None:
            UusiData = VPDATA()
            UusiData.viikonpaiva = ViikonPaiva
            UusiData.MWhYhteensa = (alkio.kWhPaiva + alkio.kWhYo)/1000
            vpData.append(UusiData)
        else:
            Data = olemassaoleva_data
            Data.MWhYhteensa += (alkio.kWhPaiva + alkio.kWhYo)/1000
    #Lähde: Stack Overflow       
    vpData.sort(key=lambda x: VIIKONPAIVAT.index(x.viikonpaiva))
    return vpData

def kysyTiedosto():
    Nimi = input("Anna tiedoston nimi: ")
    return Nimi
# eof 