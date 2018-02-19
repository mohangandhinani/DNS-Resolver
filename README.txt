# DNS-Resolver
libraries :
1)pycrypto
2)dnspython

instructions to run program:

PART A
python mydig.py cs.stonybrook.edu NS
other commands and detailed output has been explained in the mydig_output.txt

PART B
python dns_sec.py  www.dnssec-failed.org (dnssec failed)
python dns_sec.py  www.dnssec.com  A (dnssec supported and verified output)
python dns_sec.py  www.google.com  A (dnssec not supported)
python dns_sec.py www.verisigninc.com  A (dnssec supported)


PART C
analysis has been performed on localdns,googledns and my dns resolver
cdf graph  has been presented in the report documnet