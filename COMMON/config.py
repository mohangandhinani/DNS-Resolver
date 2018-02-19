"""
Reference -  https://www.iana.org/domains/root/servers
"""
import dns

text_template = """
QUESTION SECTION:
{question} IN {question_type}

ANSWER SECTION:
{answer}

Query time: {query_time} msec
WHEN: {date}
MSG SIZE rcvd: {message_size}
"""
root_servers = ['198.41.0.4',
                '192.228.79.201',
                '192.33.4.12',
                '199.7.91.13',
                '192.203.230.10',
                '192.5.5.241',
                '192.112.36.4',
                '198.97.190.53',
                '192.36.148.17',
                '192.58.128.30',
                '193.0.14.129',
                '199.7.83.42',
                '202.12.27.33']

CNAME = 5
MX = 15
SUCCESS = 0
KSK_FLAG = 257
ZSK_FLAG = 256
NSEC = 47
NSEC3 = 50
MAX_TIME = 200

#rdtype
A = 1
NS = 2
DS = 43
RRSIG = 46
NSEC = 47
DNSKEY = 48

q_t = {1: "A", 2: "NS", 5: "CNAME", 15: "MX"}
'''
#return codes
 	NOERROR = 0
 	FORMERR = 1
 	SERVFAIL = 2
 	NXDOMAIN = 3
 	NOTIMP = 4
 	REFUSED = 5
 	YXDOMAIN = 6
 	YXRRSET = 7
 	NXRRSET = 8
 	NOTAUTH = 9
 	NOTZONE = 10
 	BADVERS = 16

'''

top_25_sites = [
    "Google.com",
    "Youtube.com",
    "Facebook.com",
    "Reddit.com",
    "Amazon.com",
    "Wikipedia.org",
    "Yahoo.com",
    "Twitter.com",
    "Ebay.com",
    "Netflix.com",
    "Linkedin.com",
    "Instagram.com",
    "Twitch.tv",
    "Imgur.com",
    "Office.com",
    "Diply.com",
    "Microsoftonline.com",
    "Craigslist.org",
    "Live.com",
    "Pornhub.com",
    "Wikia.com",
    "T.co",
    "Espn.com",
    "Cnn.com",
    "Tumblr.com",
]

q_type = {
    "A": dns.rdatatype.A,
    "NS": dns.rdatatype.NS,
    "MX": dns.rdatatype.MX
}

google_dns = "8.8.4.4"
stony_brook_dns = "130.245.255.4"

#takes digest type as key
algo = {1: "SHA1", 2: "SHA256"}


root_ksk =["AwEAAaz/tAm8yTn4Mfeh5eyI96WSVexTBAvkMgJzkKTOiW1vkIbzxeF3 +/4RgWOq7HrxRixHlFlExOLAJr5emLvN7SWXgnLh4+B5xQlNVz8Og8kv ArMtNROxVQuCaSnIDdD5LKyWbRd2n9WGe2R8PzgCmr3EgVLrjyBxWezF 0jLHwVN8efS3rCj/EWgvIWgb9tarpVUDK/b58Da+sqqls3eNbuv7pr+e oZG+SrDK6nWeL3c6H5Apxz7LjVc1uTIdsIXxuOLYA4/ilBmSVIzuDWfd RUfhHdY6+cn8HFRm+2hM8AnXGXws9555KrUB5qihylGa8subX2Nn6UwN R1AkUTV74bU="
,
"AwEAAagAIKlVZrpC6Ia7gEzahOR+9W29euxhJhVVLOyQbSEW0O8gcCjF FVQUTf6v58fLjwBd0YI0EzrAcQqBGCzh/RStIoO8g0NfnfL2MTJRkxoX bfDaUeVPQuYEhg37NZWAJQ9VnMVDxP/VHL496M/QZxkjf5/Efucp2gaD X6RS6CXpoY68LsvPVjR0ZSwzz1apAzvN9dlzEheX7ICJBBtuA6G3LQpz W5hOA2hzCTMjJPJ8LbqF6dsV6DoBQzgul0sGIcGOYl7OyQdXfZ57relS Qageu+ipAdTTJ25AsRTAoub8ONGcLmqrAmRLKBP1dfwhYB4N7knNnulq QxA+Uk1ihz0="]


