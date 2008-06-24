hav call wireless_tools Net.Link setConnection "Dağıt" ""
hav call wireless_tools Net.Link setConnectionMode "Dağıt"  "ad-hoc"
hav call wireless_tools Net.Link setAddress "Dağıt"  "manual"  "192.168.3.1"  "255.255.255.0"  ""
hav call wireless_tools Net.Link setRemote "Dağıt"  "Pardus"
hav call wireless_tools Net.Link setAuthentication "Dağıt"  "wep"  ""  "pardus"
hav call wireless_tools Net.Link setState "Dağıt"  "up"


/sbin/ifconfig wmaster0 down
/sbin/ifconfig wmaster0 192.168.111.1 netmask 255.255.255.0  
/sbin/iwconfig wmaster0 mode ad-hoc  
/sbin/iwconfig wmaster0 key 6572747975  
/sbin/iwconfig wmaster0 channel auto  
/sbin/iwconfig wmaster0 essid ADHOC  
/sbin/ifconfig wmaster0 up