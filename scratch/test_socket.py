import socket

for port in [80, 443]:
    s = socket.socket()
    s.settimeout(5)
    try:
        s.connect(('hosseinykala.ir', port))
        print(f"Port {port}: Connected!")
        s.sendall(b"HEAD / HTTP/1.1\r\nHost: hosseinykala.ir\r\nUser-Agent: curl/7.88.1\r\n\r\n")
        res = s.recv(1024)
        print(f"Port {port} raw response:\n{res.decode(errors='ignore')}")
    except Exception as e:
        print(f"Port {port} error: {e}")
    finally:
        s.close()
