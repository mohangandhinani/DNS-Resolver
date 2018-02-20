import dns.dnssec as sec

from config import *


class TrustChain(object):
    def __init__(self, parent, child, query):
        self.parent = parent
        self.child = child
        self.query = query

    def validate(self):
        p_digest_l, p_algo = self.parent_data_digest()
        ksk_list, message = self.child_data_digest()
        for ksk in ksk_list:
            for p_digest in p_digest_l:
                if p_digest == sec.make_ds(self.query, ksk, p_algo).digest:
                    return True
        else:
            return False, "parent and child digest did not match"

    def parent_data_digest(self):
        p_q = dns.message.make_query(qname=self.query, want_dnssec=True, rdtype=DS)
        p_r = dns.query.tcp(where=self.parent, q=p_q, timeout=MAX_TIME)
        p_digest, p_algo = self.get_digest_algo(p_r)
        if p_digest and p_algo:
            return p_digest, p_algo
        else:
            return None, "one of digest,algo misiing"

    def get_digest_algo(self, p_r):
        if p_r.answer[0].items:
            obj_list = p_r.answer[0].items[0]
            return [d.digest for d in obj_list[0]], algo.get(obj_list[0].digest_type, None)
        else:
            return None, None

    def child_data_digest(self):
        c_q = dns.message.make_query(qname=self.query, want_dnssec=True, rdtype=DNSKEY)
        c_r = dns.query.tcp(where=self.child, q=c_q, timeout=MAX_TIME)
        return self.validate_child_response(c_r)

    def validate_child_response(self, c_r):
        if c_r.answer:
            ksk = TrustChain.extract_ksk(c_r)
            if ksk:
                return ksk, "ksk present"
            else:
                return False, "KSK not configured"
        else:
            return False, "NO DNSSEC"

    @staticmethod
    def extract_ksk(c_r):
        ksk_objs = [obj for obj in c_r.answer[0].items if obj.flags == KSK_FLAG]
        return ksk_objs if ksk_objs else False
