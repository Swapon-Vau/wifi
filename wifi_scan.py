#!/usr/bin/env python3
def banner():
print("""


██████╗ ██╗ ██╗██████╗ ███████╗██████╗ ██╗ ██╗ ██████╗ ██╗ ██████╗
██╔═══██╗██║ ██║██╔══██╗██╔════╝██╔══██╗ ██║ ██║██╔═══██╗██║ ██╔══██╗
██║ ██║██║ ██║██████╔╝█████╗ ██████╔╝ ███████║██║ ██║██║ ██║ ██║
██║ ██║██║ ██║██╔═══╝ ██╔══╝ ██╔═══╝ ██╔══██║██║ ██║██║ ██║ ██║
╚██████╔╝╚██████╔╝██║ ███████╗██║ ██║ ██║╚██████╔╝███████╗██████╔╝
╚═════╝ ╚═════╝ ╚═╝ ╚══════╝╚═╝ ╚═╝ ╚═╝ ╚═════╝ ╚══════╝╚═════╝


Tool by Cyber 71
""")


# --- Ping Function ---
def ping_host(ip, timeout):
try:
proc = subprocess.run(["ping", "-c", "1", "-W", str(int(timeout)), str(ip)],
stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
return proc.returncode == 0
except Exception:
return False


# --- Sweep Function ---
def sweep(network, workers=50, timeout=1.0):
net = ipaddress.ip_network(network, strict=False)
results = []
with ThreadPoolExecutor(max_workers=workers) as ex:
futures = {ex.submit(ping_host, str(ip), timeout): str(ip) for ip in net.hosts()}
for fut in as_completed(futures):
ip = futures[fut]
try:
alive = fut.result()
if alive:
results.append({"ip": ip})
except Exception:
pass
return results


# --- Main ---
if __name__ == '__main__':
banner()


parser = argparse.ArgumentParser()
parser.add_argument('network', help='Subnet to scan, e.g., 192.168.1.0/24')
parser.add_argument('--workers', type=int, default=50, help='Number of parallel threads')
parser.add_argument('--timeout', type=float, default=1.0, help='Ping timeout per host in seconds')
parser.add_argument('--output', choices=['json','text','none'], default='none', help='Output format')
parser.add_argument('--file', help='Output filename')
args = parser.parse_args()


print(f"\n[*] Scanning network {args.network} with {args.workers} workers...")
start = time.time()
res = sweep(args.network, workers=args.workers, timeout=args.timeout)
elapsed = time.time() - start


print(f"\n[+] Found {len(res)} responsive hosts in {elapsed:.1f}s\n")


if args.output == 'json':
fname = args.file or 'wifi_scan.json'
with open(fname,'w') as f:
json.dump(res,f,indent=2)
print('[+] Results saved to', fname)
elif args.output == 'text':
fname = args.file or 'wifi_scan.txt'
with open(fname,'w') as f:
for r in res:
f.write(r['ip'] + "\n")
print('[+] Results saved to', fname)
else:
table = [[i+1, r['ip']] for i, r in enumerate(res)]
print(tabulate(table, headers=["#","IP Address"]))
