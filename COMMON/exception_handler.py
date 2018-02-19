def exception_handler(e):
    print(e.message)

class DNSSecException(Exception):
    """Exception is raised if dnssec validation fails"""