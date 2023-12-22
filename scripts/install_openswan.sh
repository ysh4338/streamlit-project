#!/bin/bash
sudo yum install openswan -y

LOCAL_NETWORK=$1
REMOTE_NETWORK=$2
NETWORK_CONFIG_FILE="/etc/sysctl.conf"
OPENSWAN_CONFIG_FILE="/etc/ipsec.d/aws.conf"
OPENSWAN_SECRETS_FILE="/etc/ipsec.d/aws.secrets"

echo 'net.ipv4.ip_forward = 1' | sudo tee -a $NETWORK_CONFIG_FILE
echo 'net.ipv4.conf.default.rp_filter = 0' | sudo tee -a $NETWORK_CONFIG_FILE
echo 'net.ipv4.conf.default.accept_source_route = 0' | sudo tee -a $NETWORK_CONFIG_FILE

sed -i 's/^auth=esp/#auth=esp/' $OPENSWAN_CONFIG_FILE
sed -i "s/leftsubnet=<LOCAL NETWORK>/leftsubnet=${LOCAL_NETWORK}/" $OPENSWAN_CONFIG_FILE
sed -i "s/rightsubnet=<REMOTE NETWORK>/rightsubnet=${REMOTE_NETWORK}/" $OPENSWAN_CONFIG_FILE

echo '' | sudo tee -a $OPENSWAN_SECRETS_FILE