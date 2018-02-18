"""
Reference -  https://www.iana.org/domains/root/servers
"""
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
A = 1
NS = 2
CNAME = 5
MX = 15
SUCCESS = 0

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
