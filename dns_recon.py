import socket

def get_dns_info(domain):
    """
    Resolves domain to IP and checks for reverse DNS.
    """
    res = {}
    try:
        ip = socket.gethostbyname(domain)
        res["IP"] = ip
        try:
            res["Hostname"] = socket.gethostbyaddr(ip)[0]
        except:
            res["Hostname"] = "N/A"
    except Exception as e:
        res["Error"] = str(e)
    return res
