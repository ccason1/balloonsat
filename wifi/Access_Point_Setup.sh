#!/bin/sh
DHCPCD_CONFIG="/etc/dhcpcd.conf"
DNSMASQ_CONFIG="/etc/dnsmasq.conf"
HOSTAPD_CONFIG="/etc/hostapd/hostapd.conf"
STATIC_HOST_IP="192.168.4.1/24"
DHCP_RANGE="192.168.4.2,192.168.4.20,255.255.255.0,24h"
HOST_ALIAS="/MSUSAT/$STATIC_HOST_IP"
NET_SSID="MSUSAT"
NET_PASS="raspberry"
apt-get install hostapd -y
systemctl unmask hostapd
systemctl enable hostapd
apt-get install dnsmasq -y
DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent
if grep -Fq "interface wlan0" $DHCPCD_CONFIG
then
echo "Wlan0 is already there"
else
echo "interface wlan0" >> $DHCPCD_CONFIG
fi
if grep -Fq "static ip_address" $DHCPCD_CONFIG
then
echo "IP Address already defined, setting to new ip_address"
sed -i "s|static ip_address=*|static ip_address=$STATIC_HOST_IP|g" $DHCPCD_CONFIG
else
echo "static ip_address=$STATIC_HOST_IP" >> $DHCPCD_CONFIG
fi
if grep -Fq "nohook wpa_supplicant" $DHCPCD_CONFIG
then
echo "No hook wpa_supplicant is already there"
else
echo "nohook wpa_supplicant" >> $DHCPCD_CONFIG
fi
mv $DNSMASQ_CONFIG /etc/dnsmasq.conf.orig
echo "interface=wlan0" >> $DNSMASQ_CONFIG
echo "dhcp-range=$DHCP_RANGE" >> $DNSMASQ_CONFIG
echo "domain=wlan" >> $DNSMASQ_CONFIG
echo "address=$HOST_ALIAS" >> $DNSMASQ_CONFIG
rfkill unblock wlan
if [ -s $HOSTAPD_CONFIG ]
then
mv $HOSTAPD_CONFIG $HOSTAPD_CONFIG.orig
fi
echo "country_code=US" >> $HOSTAPD_CONFIG
echo "interface=wlan0" >> $HOSTAPD_CONFIG
echo "ssid=$NET_SSID" >> $HOSTAPD_CONFIG
echo "hw_mode=g" >> $HOSTAPD_CONFIG
echo "channel=7" >> $HOSTAPD_CONFIG
echo "macaddr_acl=0" >> $HOSTAPD_CONFIG
echo "auth_algs=1" >> $HOSTAPD_CONFIG
echo "ignore_broadcast_ssid=0" >> $HOSTAPD_CONFIG
echo "wpa=2" >> $HOSTAPD_CONFIG
echo "wpa_passphrase=$NET_PASS" >> $HOSTAPD_CONFIG
echo "wpa_key_mgmt=WPA-PSK" >> $HOSTAPD_CONFIG
echo "wpa_pairwise=TKIP" >> $HOSTAPD_CONFIG
echo "rsn_pairwise=CCMP" >> $HOSTAPD_CONFIG
if [ "$NET_PASS" = "raspberry" ]
then
echo "WARNING DEFAULT PASSWORD IS BEING USED"
fi
