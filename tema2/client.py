# inainte de toate trebuie adaugata o regula de ignorare 
# a pachetelor RST pe care ni le livreaza kernelul automat
# iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
from scapy.all import *

ip = IP()
ip.src = '198.13.0.15'
ip.dst = '198.13.0.14'

tcp = TCP()
tcp.sport = 54321
tcp.dport = 10000

tcp.seq = 100
tcp.flags = 'S' # SYN

raspuns_syn_ack = sr1(ip/tcp)
print("Received SYN_ACK")

tcp.seq += 1
tcp.ack = raspuns_syn_ack.seq + 1
tcp.flags = 'A'
send(ip/tcp)
print("Sent ACK")

TCPOptions[1]['MSS'] = 2
print TCPOptions[1]
# DSCP = 011 110 (AF33); ECN = 11
ip.tos = int('011110' + '11', 2) 
ip.show()

for ch in "ABC":
    tcp.flags = 'ECPA' # ECE, CWR
    rcv = sr1(ip/tcp/ch)
    rcv.show()
    tcp.seq += 1

rcv = sr1(ip/tcp/"DEF")
rcv.show()

tcp.seq += 1
tcp.flags = 'R' # RST
send(ip/tcp)
print("Sent RST")