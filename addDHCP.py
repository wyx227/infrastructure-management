#!/usr/bin/env python3
import os
import sys
import ipaddress
import re
import random

file = open('/etc/dhcp/dhcpd.conf', 'r')
lines = file.readlines()

try:
    ip = ipaddress.ip_address(sys.argv[3])
    mac = sys.argv[2]
    host_name = sys.argv[1]
    
#    print('%s is a correct IPv%s address.' % (ip, ip.version))
except ValueError:
    print('address/netmask is invalid: %s' % sys.argv[3])
    exit()
except:
     print("Missing input. Usage: addDHCP <HOSTNAME> <MAC> <IP>\n")
     exit()     

if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()) == False:
    print("Invalid mac\n")
    exit()

position = 0
found = 0
host_name_found = ""
mac_address_found = ""
ip_address_found = ""
message_found = ""
ip = sys.argv[3]

for line in lines:
        position = position + 1
        if(line.startswith('host ' + host_name)):
            found = 1
            host_name_found = lines[position-1].replace("host ",' ')[:-2].strip()
            mac_address_found = lines[position].replace("  hardware ethernet", ' ').replace(";",' ').strip()
            ip_address_found = lines[position+1].replace(" fixed-address", ' ').replace(";",' ').strip()
        elif(line.startswith('  hardware ethernet ' + mac)):
            found = 1
            host_name_found = lines[position-2].replace("host ",' ')[:-2].strip()
            mac_address_found = lines[position-1].replace("  hardware ethernet", ' ').replace(";",' ').strip()
            ip_address_found = lines[position].replace(" fixed-address", ' ').replace(";",' ').strip()
        elif(line.startswith('  fixed-address ' + ip)):
            found = 1
            host_name_found = lines[position-3].replace("host ",' ')[:-2].strip()
            mac_address_found = lines[position-2].replace("  hardware ethernet", ' ').replace(";",' ').strip()
            ip_address_found = lines[position-1].replace(" fixed-address", ' ').replace(";",' ').strip()
            
            
message_found = "Found host: \n" + "Host Name: " + host_name_found + "\n" + "MAC: " + mac_address_found + "\n" + "IP: " + ip_address_found + "\n"

file.close()        
        
if(found == 1):
    print("Host exists already")
    print(message_found)
else:
    success_message = "Adding host to configuration: \n" + "Host: " + host_name + "\n" + "MAC: " + mac +"\n" + "IP: " + ip + "\n"
    print(success_message)
    out = open('dhcpd.conf', 'a')
    entry = 'host '+ host_name + '{\n' + '  hardware ethernet ' + mac + ';\n' + '  fixed-address ' + ip + ';\n' + '}\n'
    out.writelines(entry)
    out.close()
     
os.system('systemctl restart isc-dhcp-server')
print("Finished!\n")