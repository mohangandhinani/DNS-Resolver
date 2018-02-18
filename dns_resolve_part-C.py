'''
REFERENCE : for cdf
https://stackoverflow.com/questions/24575869/read-file-and-plot-cdf-in-python

'''
import numpy as np
import matplotlib.pyplot as plt
# import time
#
# import dns.query
#
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
#             s += 100 * launch_queries(query=wb, server_to_resolve=google_dns)
#         l.append(s / 10)
#     return l
#
#
# def local_dns_list():
#     l = []
#     for wb in top_25_sites:
#         s = 0
#         for _ in xrange(10):
#             s += 100 * launch_queries(query=wb, server_to_resolve=stony_brook_dns)
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


google = [1.7400002479553223, 1.7400002479553223, 0.690000057220459, 0.8999991416931152, 1.0199999809265137, 2.130000591278076, 0.7399988174438477, 0.6800007820129395, 0.8599996566772461, 2.3000001907348633, 0.840001106262207, 0.8299994468688965, 1.0599994659423828, 0.8100008964538574, 1.419999599456787, 3.509998321533203, 1.4100003242492676, 1.699998378753662, 0.6700015068054199, 0.6200003623962402, 0.7199978828430176, 0.6700015068054199, 0.7800006866455078, 0.8499979972839355, 0.8700013160705566]
local = [0.37999868392944336, 0.35000085830688477, 0.3600001335144043, 0.32000064849853516, 0.3600001335144043, 0.279998779296875, 0.410001277923584, 0.690000057220459, 0.48999786376953125, 0.5299997329711914, 0.32000064849853516, 0.48999786376953125, 0.29000043869018555, 0.279998779296875, 0.5999994277954102, 0.5299997329711914, 0.4200005531311035, 0.2500009536743164, 0.279998779296875, 0.29000043869018555, 0.34000158309936523, 0.26999950408935547, 0.26000022888183594, 0.39999961853027344, 0.29000043869018555]
mydns = [63.13999891281128, 18.320000171661377, 18.000001907348633, 23.539998531341553, 18.05000066757202, 35.22000074386597, 41.630001068115234, 25.259997844696045, 19.560000896453857, 17.699999809265137, 16.80999994277954, 18.20000171661377, 149.11999940872192, 17.259998321533203, 21.380000114440918, 42.56999969482422, 19.590001106262207, 94.94999885559082, 54.83000040054321, 16.609997749328613, 15.939998626708984, 156.3100004196167, 18.299999237060547, 16.740000247955322, 18.11000108718872]


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