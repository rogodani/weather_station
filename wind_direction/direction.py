resistance = [33000, 6570, 8200, 891,
              1000, 688, 2200, 1410,
              3900, 3140, 16000, 14120,
              120000, 42120, 64900, 21880]


def voltage_divider(r1, r2, vin):
    vout = (vin * r1) / (r1 + r2)
    return round(vout, 3)


for x in range(len(resistance)):
    print(resistance[x], voltage_divider(10000, resistance[x], 3.3))

from gpiozero import MCP3008
import time

adc = MCP3008(channel=0)

count = 0
values = []

while True:
    wind = round(adc.value * 3.3, 1)
    print(wind)
    if not wind in values:
        values.append(wind)
        count += 1
        print(count)
