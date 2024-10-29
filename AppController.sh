#!/bin/bash

# Update and install BIND
sudo apt update
sudo apt install -y bind9 dnsutils

# Define variables
ZONE="database.contoso.com"
ZONE_FILE="/etc/bind/db.$ZONE"
BIND_CONF="/etc/bind/named.conf.local"

# Create BIND configuration for the zone
echo "zone \"$ZONE\" {
    type master;
    file \"$ZONE_FILE\";
};" | sudo tee -a $BIND_CONF

# Create the zone file with initial records
sudo bash -c "cat > $ZONE_FILE" <<EOF
\$TTL 86400
@       IN      SOA     ns1.$ZONE. admin.$ZONE. (
                              2024102901 ; Serial
                              3600       ; Refresh
                              1800       ; Retry
                              604800     ; Expire
                              86400 )    ; Minimum TTL
;
@       IN      NS      ns1.$ZONE.
ns1     IN      A       10.0.0.12
dbprimary   IN      A       10.0.0.21
dbwrite     IN      A       10.0.0.21
dball       IN      A       10.0.0.21
dball       IN      A       10.0.0.22
EOF

# Restart BIND service
sudo systemctl restart bind9

# Enable BIND service to start on boot
sudo systemctl enable bind9

echo "BIND installation and configuration complete!"
