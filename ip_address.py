import netifaces as ni

# inspect network interfaces

print('\n--- network interfaces -------------------')
print(ni.interfaces())

for interface in ni.interfaces():
    print('\n---',interface,'----------------------')
    print(ni.ifaddresses(interface))

print('\n--- address on local subnet --------------')
print(ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr'])