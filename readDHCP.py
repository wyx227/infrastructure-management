file = open('/etc/dhcp/dhcpd.conf', 'r')
lines = file.readlines()
position = 0
header = ['Hostname','MAC','IP']
format_string = "{: >20} {: >25} {: >15}"

print(format_string.format(*header))
print("=================================================================")

for line in lines:
        position = position + 1
        if(line.startswith('host')):

                host_name = line.replace("host ",' ')[:-2].strip()
                mac_address = lines[position].replace("  hardware ethernet", ' ').replace(";",' ').strip()
                ip_address = lines[position+1].replace(" fixed-address", ' ').replace(";",' ').strip()
                entry = [host_name, mac_address, ip_address]
                print(format_string.format(*entry))





file.close()
