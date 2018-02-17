import sys

import dns.query

from config import *
from exception_handler import exception_handler


class DnsResolve(object):
    def __init__(self):
        self.query, self.query_type = self.arg_parse()

    def execute(self):
        self.launch_queries()

    def arg_parse(self):
        if len(sys.argv) == 2:
            name, addr_type = sys.argv[1], None
        elif len(sys.argv) >= 3:
            name, addr_type = sys.argv[1], sys.argv[2]
        else:
            name, addr_type = None, None
        return name, addr_type

    def launch_queries(self, query_type=None, servers_to_resolve=root_servers):
        query_type = query_type if query_type else self.query_type
        for server_ip in servers_to_resolve:
            query_type, qname_object = self.build_query(self.query, query_type)
            try:
                dns_query = dns.message.make_query(qname=qname_object, rdtype=query_type)
                dns_response = dns.query.udp(q=dns_query, where=server_ip, timeout=5)
                rv = self.response_handler(dns_response)
            except Exception as e:
                exception_handler(e)
            else:
                if rv:
                    return rv

    def build_query(self, query, query_type):
        return getattr(dns.rdatatype, query_type, None), dns.name.from_text(query)

    def response_handler(self, dns_response):
        if dns_response.rcode() == SUCCESS:
            if dns_response.answer:
                self.answer_section_handler(dns_response.answer)
            elif dns_response.additional:
                self.additional_section_handler(dns_response.additional)
            elif dns_response.authority:
                self.authority_section_handler(dns_response.authority)
        else:
            return None, "dns response failed with rcode {0}".format(dns_response.rcode())

    def answer_section_handler(self, ans_section):
        pass

    def authority_section_handler(self, auth_section):
        auth_sever_names = [server_name for server_obj in auth_section for server_name in server_obj.items]
        for auth_sever_name in auth_sever_names:
            message, ip_list = self.launch_queries(query_type='A', servers_to_resolve=ip_add_list)

    def additional_section_handler(self, add_section):
        ip_add_list = []
        additional_objs = []
        for additional_obj in add_section:
            additional_objs.append(additional_obj)
        additional_objs = filter(lambda x: x.rdtype == A, additional_objs)
        for additional_obj in additional_objs:
            for message_obj in additional_obj.items:
                ip_add_list.append(message_obj.address)
        return self.launch_queries(query_type='A', servers_to_resolve=ip_add_list)


if __name__ == "__main__":
    dns_obj = DnsResolve()
    message, ip_list = dns_obj.execute()
    print message
