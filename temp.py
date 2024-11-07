Aikaleima = time.strptime(osat[0], "%d-%m-%Y %H:%M")     

Sdata.paiva = Aikaleima.tm_mday
Sdata.kuukausi = Aikaleima.tm_mon
Sdata.kuukausiStr = time.strftime("%b", Aikaleima)
Sdata.vuosi = Aikaleima.tm_year
Sdata.tunti = Aikaleima.tm_hour

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