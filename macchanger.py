from re import sub
import subprocess
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-i', '--interface', dest='interface', help="")
parser.add_option('-m', '--mac', dest='mac', help="")
(option, values) = parser.parse_args()

interface = option.interface
new_mac = option.mac

try:
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])
except:
    print(f"[!] Check that you already have {interface} or that {new_mac} is a valid mac address")
    print("Mac address example 00:11:22:33:44:55")

