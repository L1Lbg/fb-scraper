# THANKS TO:
# https://github.com/ahervias77/portscanner


import socket

ports = [
    80, #HTTP
    443, #HTTPS

    25,#SMTP
    110,#POP3
    143, #IMAP
    465,# SMTPS
    587, # SUBMISSION
    993, #IMAPS
    995,#POP3S
]

def tcp_scan(ip):
    """ Creates a TCP socket and attempts to connect via supplied ports """
    for port in ports:

        try:
            # Create a new socket
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # If wanted port is open
            if not tcp.connect_ex((ip, port)):
                if port in [443,80]:
                    return False

                tcp.close()
                return 'No website'
                
        
        
        except Exception as e:
            # print(e)
            # print(f'Website {ip} not working')
            return f'Website {ip} not working'

if __name__ == '__main__':
    print(tcp_scan(input('')))


