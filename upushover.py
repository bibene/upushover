import socket
try:
    import ussl as ssl
except:
    import ssl
    
PUSHOVER_HOST = 'api.pushover.net'
PUSHOVER_PORT = 443
PUSHOVER_PATH = '/1/messages.json'
SAFE_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.- '

def make_safe(string):
    r = []
    for c in string:
        if c in SAFE_CHARS:
            r.append(c)
        else:
            r.append('%%%x' % ord(c))
    return (''.join(r)).replace(' ', '+')

def sendMessage(user, token, title, msg):    
    data =  'token=' + make_safe(token)
    data += '&user=' + make_safe(user)
    data += '&title=' + make_safe(title)
    data += '&message=' + make_safe(msg) 
             
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SEC)
    sock.settimeout(10)
    s = ssl.wrap_socket(sock)
    s.connect(socket.getaddrinfo(PUSHOVER_HOST, PUSHOVER_PORT)[0][4])
    
    request = '%s %s HTTP/1.0\r\n' % ('POST', PUSHOVER_PATH)
    request += 'Host: %s\r\n' % PUSHOVER_HOST
    request += 'Content-Type: application/x-www-form-urlencoded\r\n'
    request += 'Content-Length: %s\r\n\r\n%s\r\n\r\n' % (len(data), data)
    
    s.send(request)
    response = ''
    while 1:
        recv = s.readline()
        if len(recv) == 0: break
        response += recv.decode()
    s.close()
    return response

