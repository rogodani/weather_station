resistance = [33000, 6570, 8200, 891,
              1000, 688, 2200, 1410,
              3900, 3140, 16000, 14120,
              120000, 42120, 64900, 21880]

VOLTS = {
    0.4: [33000, 0.0, "N"],
    1.4: [6570, 22.5, "NNE"],
    1.2: [8200, 45, "NE"],
    2.8: [891, 67.5, "ENE"],
    2.7: [1000, 90, "E"],
    2.9: [688, 112.5, "ESE"],
    2.2: [2200, 135, "SE"],
    2.6: [1410, 157.5, "SSE"],
    1.8: [3900, 180, "S"],
    2.0: [3140, 202.5, "SSW"],
    0.7: [16000, 225, "SW"],
    0.8: [14120, 247.5, "WSW"],
    0.1: [120000, 270, "W"],
    0.3: [42120, 292.5, "WNW"],
    0.2: [64900, 315, "NW"],
    0.6: [21880, 337.5, "NNW"]
}


def voltage_divider(r1, r2, vin):
    vout = (vin * r2) / (r1 + r2)
    return round(vout, 1)


for x in range(len(resistance)):
    print(resistance[x], voltage_divider(resistance[x], 4700, 3.3))

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
    print(values)
