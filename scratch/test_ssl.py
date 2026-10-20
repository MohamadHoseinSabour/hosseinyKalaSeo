import socket, ssl

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

s = socket.socket()
s.settimeout(5)
s.connect(('hosseinykala.ir', 443))
try:
    ss = context.wrap_socket(s, server_hostname='hosseinykala.ir')
    print("SSL wrap successful!")
    print("Cipher:", ss.cipher())
    print("Version:", ss.version())
    ss.sendall(b"GET /wp-json/wp/v2/tags?per_page=1 HTTP/1.1\r\nHost: hosseinykala.ir\r\nUser-Agent: curl/7.88.1\r\n\r\n")
    data = ss.recv(2048)
    print("Response:\n", data.decode('utf-8', errors='ignore'))
except Exception as e:
    print("SSL wrap error:", type(e), e)
finally:
    s.close()
