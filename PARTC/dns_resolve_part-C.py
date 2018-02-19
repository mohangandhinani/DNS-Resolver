'''
REFERENCE : for cdf
https://stackoverflow.com/questions/24575869/read-file-and-plot-cdf-in-python

'''
import numpy as np
import matplotlib.pyplot as plt
import time

import dns.query

# from config import *
# from mydig import DnsResolve
#
# avg_mydns = []
# avg_google_dns = []
# avg_local_dns = []
#
#
# def launch_queries(query_type=None, query=None, server_to_resolve=None):
#     start = time.time()
#     dns_query = dns.message.make_query(qname=dns.name.from_text(query), rdtype=dns.rdatatype.A)
#     r = dns.query.udp(q=dns_query, where=server_to_resolve, timeout=10)
#     # print(r)
#     # print(time.time()-start)
#     return time.time() - start
#
#
# def google_dns_list():
#     l = []
#     for wb in top_25_sites:
#         s = 0
#         for _ in xrange(10):
#             s += 1000 * launch_queries(query=wb, server_to_resolve=google_dns)
#         l.append(s / 10)
#     return l
#
#
# def local_dns_list():
#     l = []
#     for wb in top_25_sites:
#         s = 0
#         for _ in xrange(10):
#             s += 1000 * launch_queries(query=wb, server_to_resolve=stony_brook_dns)
#         l.append(s / 10)
#     return l
#
#
# def my_dns_list():
#     l = []
#     for wb in top_25_sites:
#         s = 0
#         for _ in xrange(10):
#             dns_obj = DnsResolve(query=wb, query_type="A")
#             dns_obj.execute()
#             s += dns_obj.query_time
#         l.append(s / 10)
#     return l
#
#
# print google_dns_list()
# print local_dns_list()
# print my_dns_list()

google =[78.60000133514404, 68.30000877380371, 6.799983978271484, 21.500015258789062, 7.799983024597168, 33.59999656677246, 7.700014114379883, 8.099985122680664, 7.800006866455078, 33.89997482299805, 11.300015449523926, 9.400010108947754, 14.699983596801758, 9.599995613098145, 14.199995994567871, 32.69999027252197, 14.300012588500977, 18.899989128112793, 7.000017166137695, 7.299995422363281, 9.89999771118164, 6.599998474121094, 10.899996757507324, 8.700013160705566, 10.500001907348633]
local = [2.599978446960449, 2.3000001907348633, 3.1999826431274414, 3.2000064849853516, 2.9000043869018555, 4.200005531311035, 2.79998779296875, 2.500009536743164, 3.6999940872192383, 4.900002479553223, 2.80001163482666, 14.299988746643066, 2.9000043869018555, 2.3999929428100586, 4.900002479553223, 12.2999906539917, 4.200005531311035, 4.2999982833862305, 2.599978446960449, 2.6000022888183594, 3.7000179290771484, 2.8999805450439453, 2.700018882751465, 5.199980735778809, 3.7000179290771484]
mydns = [593.7000036239624, 160.80000400543213, 224.4999885559082, 171.50001525878906, 199.00000095367432, 503.79998683929443, 205.40001392364502, 198.00000190734863, 180.9999704360962, 174.9000072479248, 162.5999927520752, 184.99999046325684, 1741.5000200271606, 158.39998722076416, 206.9000005722046, 212.1000051498413, 215.89999198913574, 427.30000019073486, 201.20000839233398, 569.4000005722046, 155.9000015258789, 1586.6000175476074, 207.99999237060547, 221.09999656677246, 410.20002365112305]


plt.xlabel('time(in ms)')
plt.ylabel('CDF')
#P1
sd1 = np.sort(google)
y1= np.arange(len(sd1)) / float(len(sd1) - 1)
h1 =plt.plot(sd1, y1,label = "google")

#P2
sd2 = np.sort(local)
y2= np.arange(len(sd2)) / float(len(sd2) - 1)
h2 =plt.plot(sd2, y2,label ="local")

#P3
sd3 = np.sort(mydns)
y2= np.arange(len(sd3)) / float(len(sd3) - 1)
h3 =plt.plot(sd3, y2,label = "mydns")
plt.legend()
# plt.show()
plt.savefig('cdf.png')