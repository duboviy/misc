Send TCP packet (SYN/ACK) with payload from file ‘foo’ to target’s ssh port from 192.168.1.1 to 192.168.2.2. (-v allows a stdout visual of current injected packet):
```
sudo nemesis tcp -v -S 192.168.1.1 -D 192.168.2.2 -fSA -y 22 -P foo
```
Send UDP packet from 10.11.12.13:11111 to 10.1.1.2’s name-service port with a payload read from a file ‘bindpkt’. (again -v is used in order to see confirmation of our injected packet):
```
sudo nemesis udp -v -S 10.11.12.13 -D 10.1.1.2 -x 11111 -y 53 -P bindpkt
```
Send ICMP REDIRECT (network) packet from 10.10.10.3 to 10.10.10.1 with preferred gateway as source address. Here we want no output to go to stdout – which would be ideal as a component in a batch job via a shell script:
```
sudo nemesis icmp -S 10.10.10.3 -D 10.10.10.1 -G 10.10.10.3 -qR
```
Send ARP packet through device ne0 (eg. my OpenBSD pcmcia nic) from hardware source address 00:01:02:03:04:05 with IP source address 10.11.30.5 to destination IP address 10.10.15.1 with broadcast destination hardware address. In other words, who-has the mac address of 10.10.15.1, tell 10.11.30.5 – assuming 00:01:02:03:04:05 is the source mac address of our ne0 device:
```
sudo nemesis arp -v -d ne0 -H 0:1:2:c0:ff:ee -S 10.11.30.5 -D 10.10.15.1`
```
ARP poisoning #1, setup gateway --> me --> victim traffic redirect (poison gateway’s ARP table):
```
sudo nemesis arp -v -r -d eth0 -S victim -D gateway -h myMAC
```
ARP poisoning #2, Setup victim --> me --> gateway traffic redirect (poison victim’s ARP table):
```
sudo nemesis arp -v -r -d eth0 -S gateway -D victim -h myMAC
```
and more:
```
sudo nemesis arp -v -S 10.0.0.1 -D 10.0.1.2 -H 0:1:2:3:4:5 -h de:ad:be:ef:0:0 \
    -M 00:60:b0:dc:5c:c0 -m 00:60:b0:dc:5c:c0 -d eth0 -T

sudo nemesis icmp -S 10.10.10.3 -D 10.10.10.1 -G 10.10.10.3 -i 5
```
IGMP, join a multicast stream (example from Bluewin TV Enviroment):
```
sudo nemesis igmp -v -p 22 -S 192.168.1.20 -i 239.186.39.5 -D 239.186.39.5
```
IGMP v2 join for group 239.186.39.5:
```
sudo nemesis igmp -v -p 22 -S 192.168.1.20 -i 239.186.39.5 -D 239.186.39.5
```
IGMP v2 query, max resp. time 10 sec, with Router Alert IP option:
```
echo -ne '\x94\x04\x00\x00' >RA
sudo nemesis igmp -v -p 0x11 -c 100 -D 224.0.0.1 -O RA
```
or:
```
echo -ne '\x94\x04\x00\x00' | sudo nemesis igmp -v -p 0x11 -c 100 -D 224.0.0.1 -O -
```
IGMP v3 query, with Router Alert IP option:
```
echo -ne '\x03\x64\x00\x00' > v3
sudo nemesis igmp -p 0x11 -c 100 -i 0.0.0.0 -P v3 -D 224.0.0.1 -O RA
```
DHCP Discover (must use sudo and -d to send with source IP 0.0.0.0):
```
sudo nemesis dhcp -d eth0
```
Random TCP packet:
```
sudo nemesis tcp
```
DoS and DDoS testing:
```
sudo nemesis tcp -v -S 192.168.1.1 -D 192.168.2.2 -fSA -y 22 -P foo
sudo nemesis udp -v -S 10.11.12.13 -D 10.1.1.2 -x 11111 -y 53 -P bindpkt
sudo nemesis icmp redirect -S 10.10.10.3 -D 10.10.10.1 -G 10.10.10.3 -qR
sudo nemesis arp -v -d ne0 -H 0:1:2:3:4:5 -S 10.11.30.5 -D 10.10.15.1
```
