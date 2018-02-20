import dns.dnssec as sec

from config import *


class TrustChain(object):
    def __init__(self, parent, child, query):
        # print "query", query
        # print "parent", "child", parent, child,"\n"
        self.parent = parent
        self.child = child
        self.query = query

    def validate(self):
        # print("hey..")
        digest_algo_list = self.parent_data_digest()
        ksk_list = self.child_data_digest()
        for ksk in ksk_list:
            for p_digest, p_algo in digest_algo_list:
                if p_digest == sec.make_ds(name = self.query, key = ksk, algorithm = p_algo).digest:
                    return True
        else:
            return False

    def parent_data_digest(self):
        p_q = dns.message.make_query(qname=self.query, want_dnssec=True, rdtype=DS)
        p_r = dns.query.tcp(where=self.parent, q=p_q, timeout=MAX_TIME)
        return self.get_digest_algo(p_r)

    def get_digest_algo(self, p_r):
        digest_algo_list = []
        if p_r.answer:
            for rrset in p_r.answer:
                for rdata in rrset.items:
                    if rdata.rdtype == DS:
                        digest_algo_list.append((rdata.digest, algo.get(rdata.digest_type, None)))

        if p_r.authority:
            for rrset in p_r.authority:
                for rdata in rrset.items:
                    if rdata.rdtype == DS:
                        digest_algo_list.append((rdata.digest, algo.get(rdata.digest_type, None)))
        if p_r.additional:
            for rrset in p_r.additional:
                for rdata in rrset.items:
                    if rdata.rdtype == DS:
                        digest_algo_list.append((rdata.digest, algo.get(rdata.digest_type, None)))
        return digest_algo_list

    def child_data_digest(self):
        c_q = dns.message.make_query(qname=self.query, want_dnssec=True, rdtype=DNSKEY)
        c_r = dns.query.tcp(where=self.child, q=c_q, timeout=MAX_TIME)
        return self.validate_child_response(c_r)

    def validate_child_response(self, c_r):
        return self.extract_ksk(c_r)

    def extract_ksk(self, c_r):
        ksk_list = []
        if c_r.additional:
            for rrset in c_r.additional:
                if rrset.rdtype == DNSKEY:
                    for rdata in rrset.items:
                        if rdata.flags == KSK_FLAG:
                            ksk_list.append(rdata)

        if c_r.answer:
            for rrset in c_r.answer:
                if rrset.rdtype == DNSKEY:
                    for rdata in rrset.items:
                        if rdata.flags == KSK_FLAG:
                            ksk_list.append(rdata)

        if c_r.authority:
            for rrset in c_r.authority:
                if rrset.rdtype == DNSKEY:
                    for rdata in rrset.items:
                        if rdata.flags == KSK_FLAG:
                            ksk_list.append(rdata)


        return ksk_list
