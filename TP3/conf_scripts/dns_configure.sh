cp bind9 /etc/default/bind9
cp dns_conf/primary/* /etc/bind/
mkdir /etc/bind/zones
cp dns_conf/zones/* /etc/bind/zones/
