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

import HTTavoiteKirjasto

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
    Lista = []
    Sanakirja = {}
    Tila = ""
    LampatilaLadattu = False
    while True:
        Valinta = valikko()
        if Valinta == 0: 
            return None

        elif Valinta == 1:
            Tiedosto = HTTavoiteKirjasto.kysyTiedosto()
            Lista = HTTavoiteKirjasto.lueListaan(Tiedosto, Tiedot)
            print("Tiedostosta {} luettiin {} riviä".format(Tiedosto, len(Tiedot)))
            Sanakirja = HTTavoiteKirjasto.lueSanakirjaan(Tiedot)

            Kirjoitettavat_tiedot = []
            Tila = ""
            LampatilaLadattu = False

        elif Valinta == 2: 
            Kirjoitettavat_tiedot = HTTavoiteKirjasto.analysoiKuukausiTiedot(Sanakirja)
            Tila = "kk"

        elif Valinta == 3: 
            if not Kirjoitettavat_tiedot:
                print("Ei analysoitua dataa tallennettavaksi. Suorita ensin analyysi.")
            if Tila == "kk":
                HTTavoiteKirjasto.kirjoitaListaKk(HTTavoiteKirjasto.kysyTiedosto(), Kirjoitettavat_tiedot)
            elif Tila == "vp":
                HTTavoiteKirjasto.kirjoitaListaVp(HTTavoiteKirjasto.kysyTiedosto(), Kirjoitettavat_tiedot)

        elif Valinta == 4:
            Kirjoitettavat_tiedot = HTTavoiteKirjasto.analysoiViikonpaivittain(Sanakirja)
            Tila = "vp"
        elif Valinta == 5:
            Tiedosto = HTTavoiteKirjasto.kysyTiedosto()            
            Kirjoitettavat_tiedot = HTTavoiteKirjasto.yhdistaLampotila(Sanakirja, Tiedosto)
        elif Valinta == 6:
            if not Kirjoitettavat_tiedot:
                print("Ei analysoitua dataa tallennettavaksi. Suorita ensin analyysi.")
            HTTavoiteKirjasto.kirjoitaYhdistettyData(HTTavoiteKirjasto.kysyTiedosto(), Kirjoitettavat_tiedot)
        elif Valinta == 7:
            Kirjoitettavat_tiedot = HTTavoiteKirjasto.analysoiViikoittain(Lista)
            print("Matriisianalyysi suoritettu.")
            HTTavoiteKirjasto.kirjoitaMatriisi(HTTavoiteKirjasto.kysyTiedosto(), Kirjoitettavat_tiedot)

        else: print("Virheellinen valinta")
    return None
    
paaohjelma()

# eof