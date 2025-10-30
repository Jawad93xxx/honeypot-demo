import sys
import json
from collections import Counter
from pathlib import Path
import hashlib

def anonymize_ip(ip):
    # hash de l'IP pour anonymiser mais rester stable
    return hashlib.sha256(ip.encode()).hexdigest()[:8]

def analyze(path):
    total = 0
    ips = Counter()
    paths = Counter()
    methods = Counter()

    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            total += 1
            ip = obj.get("remote_addr", "")
            p = obj.get("path", "")
            m = obj.get("method", "")
            ips[ip] += 1
            paths[p] += 1
            methods[m] += 1

    print(f"Fichier: {path}")
    print(f"Total requêtes: {total}\n")
    print("Top IPs (anonymisées):")
    for ip, cnt in ips.most_common(10):
        print(f"  {anonymize_ip(ip)}  — {cnt}")
    print("\nTop chemins:")
    for p, cnt in paths.most_common(20):
        print(f"  {p}  — {cnt}")
    print("\nRépartition méthodes:")
    for m, cnt in methods.most_common():
        print(f"  {m}  — {cnt}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze.py path/to/requests.log")
        sys.exit(1)
    analyze(sys.argv[1])