import socket
import argparse

PORTS_TO_SCAN = {
    21: "FTP", 22: "SSH", 80: "HTTP",
    443: "HTTPS", 3306: "MySQL", 8080: "Proxy"
}

def scan_target(target, log_callback=None):
    if not log_callback:
        def simple_print(x): print(x)
        log_callback = simple_print

    log_callback(f"\n[*] Starting Scan on host: {target}")
    log_callback(f"[*] Scanning top {len(PORTS_TO_SCAN)} common ports...")
    
    open_ports = []

    for port, service in PORTS_TO_SCAN.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) 
        
        result = s.connect_ex((target, port))
        
        if result == 0:
            log_callback(f"[+] Port {port} is OPEN ({service})")
            open_ports.append(port)
        
        s.close()

    if not open_ports:
        log_callback("No common open ports found.")
    else:
        log_callback(f"Scan complete. Found {len(open_ports)} open ports.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Python Port Scanner")
    parser.add_argument("target", nargs='?', default="127.0.0.1", help="Target IP")
    args = parser.parse_args()
    
    scan_target(args.target)
