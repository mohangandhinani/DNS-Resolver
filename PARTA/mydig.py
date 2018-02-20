import re
import sys
import time

import dns.query

from config import *


class DnsResolve(object):
    def __init__(self,query=None,query_type=None):
        if not query and not query_type:
            self.query, self.query_type = self.arg_parse()
        else:
            self.query, self.query_type = query,query_type
        self.query_time = None

    def execute(self):
        self.start = time.time()
        ans_section, ip_list = self.launch_queries()
        self.formatter(str(ans_section))

    def arg_parse(self):
        if len(sys.argv) == 2:
            name, addr_type = sys.argv[1], None
        elif len(sys.argv) >= 3:
            name, addr_type = sys.argv[1], sys.argv[2]
        else:
            name, addr_type = None, None
        return name, addr_type

    def launch_queries(self, query_type=None, query=None, servers_to_resolve=root_servers):
        query_type = query_type if query_type else self.query_type
        query = query if query else self.query
        for server_ip in servers_to_resolve:
            query_type, qname_object = self.build_query(query, query_type)
            # try:
            dns_query = dns.message.make_query(qname=qname_object, rdtype=query_type)
            dns_response = dns.query.udp(q=dns_query, where=server_ip, timeout=MAX_TIME)
            v = self.response_handler(dns_response, query)
            if v:
                ans_section, ip_list = v
                if ip_list:
                    return ans_section, ip_list
            # except Exception as e:
            #     exception_handler(e)

    def build_query(self, query, query_type):
        return q_type.get(query_type,dns.rdatatype.CNAME), dns.name.from_text(query) if query.isalpha() else query

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
            return None, "dns response failed with rcode {0}".format(dns_response.rcode())

    def answer_section_handler(self, dns_response):
        if self.query_type in("NS","MX"):
            return dns_response,["127.0.0.1"]
        ans_section = dns_response.answer
        for answer in ans_section:
            if self.typ(answer) == CNAME:
                if self.query_type!="CNAME":
                    return self.launch_queries(query_type="CNAME", query=str(answer.items[0]))
                else:
                    return dns_response,["127.0.0.1"]
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
                ip_add_list.append(message_obj.address)
        return self.launch_queries(servers_to_resolve=ip_add_list, query=query)

    def formatter(self, ans_section):
        # print(ans_section)
        regex = r"ANSWER(.*?);"
        ans = re.findall(regex, ans_section, re.MULTILINE | re.DOTALL)
        ans = "\n".join([self.transform(i) for i in ans[0].lstrip().split("\n") if i])
        end = time.time()
        self.query_time = (end - self.start) * 1000
        date = time.strftime("%c")
        print text_template.format(question=self.query, question_type=self.query_type, answer=ans,
                                   query_time=self.query_time, date=date, message_size=62)

    def transform(self, txt):
        return self.query + " " + " ".join(txt.split()[1:])


if __name__ == "__main__":
    dns_obj = DnsResolve()
    dns_obj.execute()
