#!/bin/bash

MAC=$3

if [ -z "$2" ]
then
        echo "Usage: addHost <HOSTNAME> <IP> <MAC>"
        exit 1
fi

if [ -z "$3" ]
then
        echo "No MAC given, a random MAC will be generated"
        MAC=$(genMAC)
        echo "MAC address: $MAC"
fi

if [[ "$2" =~ ^(([1-9]?[0-9]|1[0-9][0-9]|2([0-4][0-9]|5[0-5]))\.){3}([1-9]?[0-9]|1[0-9][0-9]|2([0-4][0-9]|5[0-5]))$ ]]; then
        echo "IP Address: $2"
else
        echo "Invalid IP address"
        exit 1
fi


re="^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$"
[[ $MAC =~ $re ]] && echo "Adding record to config" || echo "Invalid MAC" && exit 1



echo -e "host $1{\n  hardware ethernet $MAC;\n  fixed-address $2; \n}" >> /etc/dhcp/dhcpd.conf

systemctl restart isc-dhcp-server
