file = open('/etc/dnsmasq.conf', 'r')
entries = file.readlines()

for entry in entries:
        if(entry.startswith('address')):
                dns_entry = entry
                dns_entry_printout = dns_entry.split("/")
                if(dns_entry_printout[1].startswith('.')):
                        fqdn = '*' + dns_entry_printout[1]
                else:
                        fqdn = dns_entry_printout[1]
                print(dns_entry_printout[2] + ' -> ' + fqdn)

file.close() 
