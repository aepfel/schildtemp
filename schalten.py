#!flask/bin/python
#import smbus

#bus=smbus.SMBus(2)
#address=0x20
#bus.write_byte_data(address,0x0c,0xff) #pullup aktivieren
#bus.write_byte_data(address,0x0d,0xff) #pullup aktivieren


# todo:
# smbus import
# in pyro object umwandeln

# relaise schalten mit 
# mask: 0=nix,1=erstes,2=zweites,3=erstes und zweites,4=drittes, usw.
# mode: 0=aus 1=an 2=um

def getrelaise():
    # i2c-code lesen
    relstat = 170
    return(relstat)


def setrelaise(rel):
    # i2c-code schreiben
    return(getrelaise())


def gettemp(sensor):
    # i2c-code sensor lesen
    sdata = 0
    return(sdata)


def schalten(mask = 0, mode = 0):
    erg = getrelaise()
    x = 0
    while (x<9):
        if ((mask & pow(2,x)) > 0):
            if (mode == 0) & ((erg & pow(2,x)) > 0):
                #bit mit werigkeit x ausschalten
                erg = erg - pow(2,x)
                print("0 erg:"+str(erg))

            elif (mode == 1) & ((erg & pow(2,x)) == 0):
                #bit mit wertigkeit x einschalten
                erg = erg + pow(2,x)
                print("1 erg:"+str(erg))

            elif (mode == 2):
                if ((erg & pow(2,x)) == 0):
                    erg = erg + pow(2,x)
                elif ((erg & pow(2,x)) > 0):
                    erg = erg - pow(2,x)
                print("2 erg:"+str(erg))

        x = x + 1

    print(erg)
    setrelaise(erg)
    return(0)
