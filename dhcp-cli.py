#!/usr/bin/env python3
import os
import sys
import ipaddress
import re
import random
import socket

class Option:
    def __init__(self, option_name, option_text):
        self.option_name = option_name
        self.option_text = option_text

class LAN:
    def __init__(self, range_start, range_end, cidr, mask, router):
        self.range_start = range_start
        self.range_end = range_end
        self.cidr = cidr
        self.mask = mask
        self.router = router


class Host:
    def __init__(self, name, mac, address):
        self.name = name
        self.mac = mac
        self.address = address


lan_list = []
host_list = []

def readConfig(pathToConfig):
    file = open(pathToConfig, 'r')
    lines = file.readlines()
    position = 0
    for line in lines:
        position = position + 1
        if(line.startswith('subnet')):
            range_start = lines[position][:-1].split()[1]
            range_end = lines[position][:-1].split()[2]
            cidr = line.split()[1]
            mask = line.split()[3]
            router = lines[position+1][:-1].split()[2]
            lan_temp = LAN(range_start, range_end, cidr, mask, router)
            lan_list.append(lan_temp)

        if(line.startswith('host')):

            host_name = line.replace("host ",' ')[:-2].strip()
            mac_address = lines[position].replace("  hardware ethernet", ' ').replace(";",' ').strip()
            ip_address = lines[position+1].replace(" fixed-address", ' ').replace(";",' ').strip()
            act_host = Host(host_name, mac_address, ip_address)
            host_list.append(act_host)

    file.close()

def addHost(name, mac, ip):
    host = Host(name, mac, ip)
    for current_host in host_list:
        if(current_host.name == name or current_host.mac == mac or current_host.address == ip):
            print("The host already exists\n")
            exit()
    
    host_list.append(host)

def addLan(cidr, mask, range_start, range_end, router):
    lan = LAN(range_start, range_end, cidr, mask, router)
    # Check if address range is ok
    for current_lan in lan_list:
        if(current_lan.cidr == cidr):
            print("This LAN already exists\n")
            exit()    
    lan_list.append(lan)


def delHost(name):
    found = 0
    for current_host in host_list:
        if(current_host.name == name):
            found = 1
            host_list.remove(current_host)
    if(found != 1):
        print("Such host does not exist")
        exit()


def modHost(name, new_mac, new_ip):
    found = 0
    for current_host in host_list:
        if(current_host.name == name):
            found = 1
            current_host.address = new_ip
            current_host.mac = new_mac

    if(found != 1):
        print("Such host does not exist")
        exit()

def createConfig(lans, hosts):
    new_lan_list = []
    new_host_list = []
    for host in hosts:
        host_record = 'host '+ host.name + '{\n' + '  hardware ethernet ' + host.mac + ';\n' + '  fixed-address ' + host.address + ';\n' + '}\n'
        new_host_list.append(host_record)
    for lan in lans:
        lan_record = 'subnet ' + lan.cidr + ' netmask ' + lan.mask + '{\n' + '  range ' + lan.range_start + ' ' + lan.range_end + ';\n' + '  option router' + lan.router + ';\n' + '}\n'
        new_lan_list.append(lan_record)

    print(host_list)
    print(lan_list)

    configFile = open("/etc/dhcp/dhcpd.conf", 'w')
    configFile.write(new_lan_list + new_host_list)
    sysoutput = os.system("systemctl restart isc-dhcp-server")
    if(sysoutput != 0):
        print("Error applying configuration\n")
    else:
        print("Finished!")

def printConfig():
    for act_lan in lan_list:
        print("CIDR: %s, Mask: %s, Option: router %s" % (act_lan.cidr, act_lan.mask, act_lan.router))
    ip_entry = []
    header = ['Hostname','MAC','IP']
    format_string = "{: >20} {: >25} {: >15}"
    info_string = "IP Range: \n 0...10: Infrastructural Devices and VMs \n 11...20: Network Devices \n 21...40: Persistent VMs \n 41...50: Desktop and Laptop PCs \n 51...60: Mobile and Wearables \n 61...70: Docker Hosts \n 71...80: Persistent Embedded Devices \n 81...90: Home Assistant Sensors \n 90...100: Reserved \n"
    print(info_string)
    print(format_string.format(*header))
    print("=================================================================")
    for act_host in host_list:
        entry = [act_host.name, act_host.mac, act_host.address]
        #print("Name: %s, MAC: %s, IP: %s" % (act_host.name, act_host.mac, act_host.address))
        ip_entry.append(entry)
    ip_entry_sorted = sorted(ip_entry, key=lambda item: socket.inet_aton(item[2]))

    for i in range(len(ip_entry_sorted)):
        print(format_string.format(*ip_entry_sorted[i]))    




def main():
    command = sys.argv[1]
    match command:
        case "add":
            readConfig("dhcpd.conf")
            try:
                ip = ipaddress.ip_address(sys.argv[4])
            except ValueError:
                print('address/netmask is invalid: %s' % sys.argv[4])
                exit()
            except:
                print("Missing input. Usage: addDHCP <HOSTNAME> <MAC> <IP>\n")
                exit()            
            ip = sys.argv[4]
            name = sys.argv[2]
            if not name:
                print("Missing input.")
                exit()

            mac = sys.argv[3]
            if not mac:
                mac = os.system("genMAC")

            if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()) == False:
                print("Invalid mac\n")
                exit()

            addHost(name, mac, ip)
            printConfig()

        case "del":
            if(sys.argv[2] == ""):
                print("USAGE: dhcp-util del \n")
                exit()
            readConfig("dhcpd.conf")
            delHost(sys.argv[2])
            printConfig()
        case "show":
            readConfig("dhcpd.conf")
            printConfig()
        case "mod":
            print("d")
        case "lan":
            print("e")
        case _:
            print("USAGE: dhcp-util <add/del/show/mod> <name> \n")
            exit()


if __name__ == "__main__":
    main()

