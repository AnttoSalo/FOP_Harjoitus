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

import HTPerusKirjasto

def valikko():
    print("Valitse haluamasi toiminto:")
    print("1) Lue tiedosto")
    print("2) Analysoi")
    print("3) Kirjoita tiedosto")
    print("4) Analysoi viikonpäivittäiset tulokset")
    print("5) Lue ja yhdistä lämpötilatiedosto")
    print("6) Kirjoita yhdistetty data tiedostoon")
    print("7) Analysoi viikoittaiset tulokset")
    print("0) Lopeta")
    Valinta = int(input("Valintasi: "))
    return Valinta

def paaohjelma():
    Tiedot = []
    Kirjoitettavat_tiedot = []
    Sanakirja = {}
    Tila = ""
    while True:
        Valinta = valikko()
        if Valinta == 0: 
            return None

        elif Valinta == 1:
            Tiedosto = HTPerusKirjasto.kysyTiedosto()
            Tiedot = HTPerusKirjasto.lueListaan(Tiedosto, Tiedot)
            print("Tiedostosta {} luettiin {} riviä".format(Tiedosto, len(Tiedot))) # -1 koska ensimmäinen rivi on otsikko
            Sanakirja = HTPerusKirjasto.lueSanakirjaan(Tiedot)

        elif Valinta == 2: 
            Kirjoitettavat_tiedot = HTPerusKirjasto.analysoiKuukausiTiedot(Sanakirja)
            Tila = "kk"

        elif Valinta == 3: 
            if not Kirjoitettavat_tiedot:
                print("Ei analysoitua dataa tallennettavaksi. Suorita ensin analyysi.")
            if Tila == "kk":
                HTPerusKirjasto.kirjoitaListaKk(HTPerusKirjasto.kysyTiedosto(), Kirjoitettavat_tiedot)
            elif Tila == "vp":
                HTPerusKirjasto.kirjoitaListaVp(HTPerusKirjasto.kysyTiedosto(), Kirjoitettavat_tiedot)

        elif Valinta == 4:
            Kirjoitettavat_tiedot = HTPerusKirjasto.analysoiViikonpaivittain(Sanakirja)
            Tila = "vp"
        elif Valinta == 5:
            Tiedosto = HTPerusKirjasto.kysyTiedosto()            
            Kirjoitettavat_tiedot = HTPerusKirjasto.yhdistaLampotila(Sanakirja, Tiedosto)
        elif Valinta == 6:
            if not Kirjoitettavat_tiedot:
                print("Ei analysoitua dataa tallennettavaksi. Suorita ensin analyysi.")
            HTPerusKirjasto.kirjoitaYhdistettyData(HTPerusKirjasto.kysyTiedosto(), Kirjoitettavat_tiedot)
        elif Valinta == 7:
            Kirjoitettavat_tiedot = HTPerusKirjasto.analysoiViikoittain(Sanakirja)
            print("Matriisianalyysi suoritettu.")
            HTPerusKirjasto.kirjoitaMatriisi(HTPerusKirjasto.kysyTiedosto(), Kirjoitettavat_tiedot)

        else: print("Virheellinen valinta")
    return None
    
paaohjelma()

# eof