import sys
import ipaddress

try:
    ip = ipaddress.ip_address(sys.argv[2])
    print('%s is a correct IPv%s address.' % (ip, ip.version))
except ValueError:
    print('address/netmask is invalid: %s' % sys.argv[1])
    exit()
except:
    print("Usage: addDNS <FQDN> <IP>")
    exit()


file = open('/etc/dnsmasq.conf', 'a')
fqdn = sys.argv[1]
ip = sys.argv[2]
record = "address/" + fqdn + "/" + ip
file.write(record)
file.close()
