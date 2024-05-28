#!/usr/bin/env python

import socket


file = open('/etc/dhcp/dhcpd.conf', 'r')
lines = file.readlines()
position = 0
header = ['Hostname','MAC','IP']
format_string = "{: >20} {: >25} {: >15}"
info_string = "IP Range: \n 0...10: Infrastructural Devices and VMs \n 11...20: Network Devices \n 21...40: Persistent VMs \n 41...50: Desktop and Laptop PCs \n 51...60: Mobile and Wearables \n 61...70: Docker Hosts \n 71...80: Persistent Embedded Devices \n 81...90: Home Assistant Sensors \n 90...100: Reserved \n"
print(info_string)
print(format_string.format(*header))
print("=================================================================")
ip_entry = []

for line in lines:
        position = position + 1
        if(line.startswith('host')):

                host_name = line.replace("host ",' ')[:-2].strip()
                mac_address = lines[position].replace("  hardware ethernet", ' ').replace(";",' ').strip()
                ip_address = lines[position+1].replace(" fixed-address", ' ').replace(";",' ').strip()
                entry = [host_name, mac_address, ip_address]
                ip_entry.append(entry)


ip_entry_sorted = sorted(ip_entry, key=lambda item: socket.inet_aton(item[2]))

for i in range(len(ip_entry_sorted)):
    print(format_string.format(*ip_entry_sorted[i]))

file.close()
