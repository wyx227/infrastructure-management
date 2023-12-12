#!/bin/bash

MAC=$3

if [ -z "$3" ]
then
        MAC=$(genMAC)
fi

#[[ "$MAC" =~ "^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$" ]] && echo "valid" || exit 1

echo -e "host $1{\n  hardware ethernet $MAC;\n  fixed-address $2; \n}" >> /etc/dhcp/dhcpd.conf

systemctl restart isc-dhcp-server
