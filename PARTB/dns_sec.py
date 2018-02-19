import re
import sys
import time

import dns.query

from COMMON.config import *
from trust_chain import TrustChain


class DnsResolveDnsSec(object):
    def __init__(self, query=None, query_type=None):
        if not query and not query_type:
            self.query, self.query_type = self.arg_parse()
        else:
            self.query, self.query_type = query, query_type
        self.query_time = None
        self.zone_name = None
        self.keys_record = None
        self.from_ip = None

    def execute(self):
        self.start = time.time()
        ans_section, ip_list = self.launch_queries()
        self.formatter(str(ans_section))

    def arg_parse(self):
        print(sys.argv)
        if len(sys.argv) == 2:
            name, addr_type = sys.argv[1], None
        elif len(sys.argv) == 3:
            name, addr_type = sys.argv[1], sys.argv[2]
        else:
            print "please provide input arguments <name> <type> format"
            exit(0)
        return name, addr_type

    def launch_queries(self, query_type=None, query=None, servers_to_resolve=root_servers):
        query_type = query_type if query_type else self.query_type
        query = query if query else self.query
        for server_ip in servers_to_resolve:
            query_type, qname_object = self.build_query(query, query_type)
            # try:
            self.dnssec(qname_object, query_type, server_ip)
            dns_query = dns.message.make_query(qname=qname_object, rdtype=query_type)
            dns_response = dns.query.udp(q=dns_query, where=server_ip, timeout=10)
            v = self.response_handler(dns_response, query)
            if v:
                ans_section, ip_list = v
                if ip_list:
                    return ans_section, ip_list
            # except Exception as e:
            #     exception_handler(e)

    def dnssec(self, qname_object, query_type, server_ip):
        try:
            self.verify_keys(server_ip)
            self.verify_response(qname_object, query_type, server_ip)
        except Exception as e:
            print  "DNSSec verification failed"
            exit(0)

    def verify_keys(self, server_ip):
        key_q = dns.message.make_query(rdtype=DNSKEY, want_dnssec=True, qname=self.get_zone_name_obj())
        key_resp = dns.query.udp(where=server_ip, q=key_q, timeout=MAX_TIME)
        if key_resp.answer:
            self.keys_record = [i for i in key_resp.answer if self.typ(i) == DNSKEY][0]
            self.validate_record(key_resp.answer[0], key_resp.answer[1])

    def verify_response(self, qname_object, query_type, server_ip):
        dns_query_message = dns.message.make_query(want_dnssec=True, qname=qname_object, rdtype=query_type)
        dns_response = dns.query.udp(q=dns_query_message, where=server_ip, timeout=MAX_TIME)
        if self.nsec_check(dns_response):
            print"DNSSEC not supported"
            exit(0)

        if dns_response.answer:
            try:
                self.validate_record(dns_response.answer[0], dns_response.answer[1])
            except IndexError as e:
                print "DNSSEC not supported"
                exit(0)
            except Exception as e:
                print "DNSSec verification failed"
                exit(0)

        if dns_response.authority:
            self.zone_name = dns_response.authority[0].name
            # to do : validate authority
        self.verify_chain_of_trust(to_ip=server_ip)

    def nsec_check(self,dns_response):
        if dns_response.answer:
            for rd in dns_response.answer:
                if self.typ(rd) in (NSEC,NSEC3):
                    return True
        if dns_response.additional:
            for rd in dns_response.additional:
                if self.typ(rd) in (NSEC,NSEC3):
                    return True
        return False

    def verify_chain_of_trust(self, to_ip):
        if not self.from_ip:  # root check
            self.validate_ksk_keys()
        else:
            rc,message = TrustChain(parent=self.from_ip, child=to_ip, query=self.get_zone_name_obj()).validate()
            if not rc:
                print "DNSSec verification failedd"
                exit(0)

    def validate_ksk_keys(self):
        if self.keys_record:
            return
            for key in self.keys_record.items:
                if key.flags == KSK_FLAG:
                    # key = str(key).split()[-1]
                    if key not in root_ksk:
                        print "present keys",key
                        print"list1",root_ksk[0]
                        print"list2", root_ksk[1]
                        print "DNSException :ksk key not valid  root key"
                        exit(0)
        else:
            print("DNSSec verification failed")
            exit(0)

    def validate_record(self, r1, r2):
        zone_name_obj = self.get_zone_name_obj()
        keys_record = self.keys_record
        z_d = {zone_name_obj: keys_record}
        dns.dnssec.validate(r1, r2, z_d)

    def get_zone_name_obj(self):
        return (self.zone_name if self.zone_name else dns.name.from_text("."))

    def build_query(self, query, query_type):
        return q_type.get(query_type, dns.rdatatype.CNAME), dns.name.from_text(query) if query.isalpha() else query

    def response_handler(self, dns_response, query):
        if dns_response.rcode() == SUCCESS:
            if dns_response.answer:
                return self.answer_section_handler(dns_response)
            elif dns_response.additional:
                v = self.additional_section_handler(dns_response.additional, query)
                if v:
                    return v
            elif dns_response.authority:
                v = self.authority_section_handler(dns_response.authority, query)
                if v:
                    return v
        else:
            return None, "DNSSec verification failed"

    def answer_section_handler(self, dns_response):
        if self.query_type in ("NS", "MX"):
            return dns_response, ["127.0.0.1"]
        ans_section = dns_response.answer
        for answer in ans_section:
            if self.typ(answer) == CNAME:
                if self.query_type != "CNAME":
                    return self.launch_queries(query_type="CNAME", query=str(answer.items[0]))
                else:
                    return dns_response, ["127.0.0.1"]
            else:
                ip_list = []
                for ans in ans_section:
                    if self.typ(ans) == A:
                        ip_list.append(str(ans).split()[-1])
                return dns_response, ip_list

    def typ(self, ans):
        return ans.rdtype

    def authority_section_handler(self, auth_section, query):
        final_ip_list = []
        auth_sever_names = [server_name for server_obj in auth_section for server_name in server_obj.items]
        for auth_sever_name in auth_sever_names:
            message, ip_list = self.launch_queries(query_type='A', query=str(auth_sever_name))
            final_ip_list.extend(ip_list)
        return self.launch_queries(servers_to_resolve=final_ip_list)

    def additional_section_handler(self, add_section, query):
        ip_add_list = []
        additional_objs = [additional_obj for additional_obj in add_section]
        additional_objs = filter(lambda x: x.rdtype == A, additional_objs)
        for additional_obj in additional_objs:
            for message_obj in additional_obj.items:
                # if not TrustChain(parent, child = message_obj.address, query).validate()
                # result = verify_hash(item.address, r.authority[0].name, ns)
                ip_add_list.append(message_obj.address)
        return self.launch_queries(servers_to_resolve=ip_add_list, query=query)

    def formatter(self, ans_section):
        print "DNSSEC verified,supported"
        regex = r"ANSWER(.*?);"
        ans = re.findall(regex, ans_section, re.MULTILINE | re.DOTALL)
        ans = "\n".join([self.transform(i) for i in ans[0].lstrip().split("\n") if i])
        end = time.time()
        self.query_time = (end - self.start) * 100
        date = time.strftime("%c")
        print text_template.format(question=self.query, question_type=self.query_type, answer=ans,
                                   query_time=self.query_time, date=date, message_size=62)

    def transform(self, txt):
        return self.query + " " + " ".join(txt.split()[1:])


if __name__ == "__main__":
    dns_obj = DnsResolveDnsSec()
    dns_obj.execute()
