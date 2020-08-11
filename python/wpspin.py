def zeroPad(num, places):
    return str(num).zfill(int(places))

def wpsgen(mac):
    # presuming mac is valid
    accum = 0
    pin = int(mac.replace(':','')[-6:],16) % 10000000
    p = pin
    while pin:
        accum = int(accum + (3 * (pin %10))) + int(int(pin/10) % 10)
        pin = int(pin/100)
    accum = (10 - accum % 10) % 10
    value = zeroPad(p,7)+""+str(accum)
    return value

mac = input('').strip()
print(wpsgen(mac))
