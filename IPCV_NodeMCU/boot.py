import network

# noinspection PyUnresolvedReferences
ap1 = network.WLAN(network.AP_IF)
ap1.active(False)

# noinspection PyUnresolvedReferences
ap = network.WLAN(network.STA_IF)

ap.active(True)
ap.connect("Marvel", "Spiderman")

while not ap.active():
    print(".", end="")
    pass

print("\nConnection successful!")
print(ap.ifconfig())
