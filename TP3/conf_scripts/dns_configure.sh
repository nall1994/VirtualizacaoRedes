cp ../dns_conf/bind9 /etc/default/bind9
cp ../dns_conf/primary/* /etc/bind/
cp ../dns_conf/zones/* /etc/bind/zones/
service bind9 restart
