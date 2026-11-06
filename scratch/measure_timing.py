import time
import socket
import ssl
import http.client
import urllib.parse

def measure_detailed_timing(target_url):
    parsed = urllib.parse.urlparse(target_url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    path = parsed.path or '/'
    if parsed.query:
        path += '?' + parsed.query

    t0 = time.time()
    # 1. DNS
    ip = socket.gethostbyname(host)
    t_dns = time.time()

    # 2. TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(15)
    sock.connect((ip, port))
    t_tcp = time.time()

    # 3. TLS
    if parsed.scheme == 'https':
        ctx = ssl.create_default_context()
        ssock = ctx.wrap_socket(sock, server_hostname=host)
    else:
        ssock = sock
    t_tls = time.time()

    # 4. Send request
    req = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)\r\nAccept-Encoding: gzip\r\nConnection: close\r\n\r\n"
    ssock.sendall(req.encode('utf-8'))
    t_sent = time.time()

    # 5. TTFB (first byte of response)
    first_byte = ssock.recv(1)
    t_first_byte = time.time()

    # 6. Read rest of response
    buf = [first_byte]
    while True:
        chunk = ssock.recv(16384)
        if not chunk:
            break
        buf.append(chunk)
    t_done = time.time()

    ssock.close()

    total_data = b''.join(buf)

    dns_time = t_dns - t0
    tcp_time = t_tcp - t_dns
    tls_time = t_tls - t_tcp
    ttfb = t_first_byte - t_sent
    download_time = t_done - t_first_byte
    total_time = t_done - t0

    print(f"Target: {target_url} (IP: {ip})")
    print(f"  DNS Lookup:      {dns_time*1000:6.1f} ms")
    print(f"  TCP Connect:     {tcp_time*1000:6.1f} ms")
    print(f"  TLS Handshake:   {tls_time*1000:6.1f} ms")
    print(f"  TTFB:            {ttfb*1000:6.1f} ms ({ttfb:4.2f} s)")
    print(f"  Content Transfer:{download_time*1000:6.1f} ms ({download_time:4.2f} s)")
    print(f"  Total Time:      {total_time*1000:6.1f} ms ({total_time:4.2f} s)")
    print(f"  Response Size:   {len(total_data)} bytes")
    
    header_end = total_data.find(b"\r\n\r\n")
    if header_end != -1:
        headers_str = total_data[:header_end].decode('iso-8859-1')
        print("  Status line:", headers_str.splitlines()[0])
        for line in headers_str.splitlines()[1:]:
            if any(h in line.lower() for h in ['x-hosseinykala', 'cache', 'server', 'content-encoding', 'content-length']):
                print(f"    {line}")

for i in range(3):
    print(f"\n--- Run {i+1} ---")
    measure_detailed_timing("https://hosseinykala.ir/")
