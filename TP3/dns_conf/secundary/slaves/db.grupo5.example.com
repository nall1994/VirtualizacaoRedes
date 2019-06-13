;
; BIND data file for local loopback interface
;
$TTL	604800
@	IN	SOA	dns1.grupo5.example.com. admin.grupo5.example.com. (
			      3		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
; name servers - D records
     IN      NS     dns1.grupo5.example.com.
     IN      NS	    dns2.grupo5.example.com.

; name servers - A records
dns1.grupo5.example.com.          IN      A       10.0.0.20
dns2.grupo5.example.com.          IN      A       10.0.0.21

; 10.0.0.0/16 - A records
cl1.grupo5.example.com.        IN      A      10.0.0.14
cl2.grupo5.example.com.        IN      A      10.0.0.15