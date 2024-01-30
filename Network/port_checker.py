import socket

def port_checker(ip_address_or_domain, port_number):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((str(ip_address_or_domain), int(port_number)))
        return "PORT {0} is OPEN on '{1}'.".format(port_number, ip_address_or_domain)
    except Exception as e:
        print(str(e))
        return "PORT {0} is CLOSED on '{1}'.".format(port_number, ip_address_or_domain)
    finally:
        sock.close()

website = "example.com"
for i in range(8000, 9000):
    print("checking", i)
    print(port_checker(website, i))
