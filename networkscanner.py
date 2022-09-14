from socket import timeout
import scapy.all as scapy
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-p', '--ip', dest='ip', help="TARGET IP")
parser.add_option('-t', '--time', dest='time', help="Timeout default = 1")
args = parser.parse_args()[0]

def scan(ip, timeout = 1):
    arp = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request = broadcast/arp
    answers = scapy.srp(arp_request, timeout=int(timeout))[0]
    print('-' * 50)
    for i, j in enumerate(answers):
        print(f"{i+1}) Ip = {j[1].psrc}\tMac = {j[1].hwsrc}")

ip = args.ip
timeout = args.time

scan(ip, timeout=timeout if timeout else 1)