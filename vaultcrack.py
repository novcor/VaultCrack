import json
from collections import defaultdict

def scan_r_reuse(input_file, output_file=None):
    r_map = defaultdict(list)
    results = []

    # Read each transaction from JSONL
    with open(input_file, 'r') as f:
        for line in f:
            tx = json.loads(line)
            txid = tx.get('txid')
            r = tx.get('r')
            if not txid or not r:
                continue
            r_map[r].append(txid)

    # Detect reused r-values
    for r_value, txids in r_map.items():
        if len(txids) > 1:
            results.append({
                "r_value": r_value,
                "txids": txids,
                "suspected_duplicate": True
            })

    # Output
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
    else:
        for entry in results:
            print(f"[!] R-value reuse detected: {entry['r_value']}")
            print(f"    Transactions: {', '.join(entry['txids'])}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="VaultCrack R-value Reuse Scanner")
    parser.add_argument('--input', type=str, required=True, help='Path to input JSONL file')
    parser.add_argument('--output', type=str, help='Path to save results as JSON')
    args = parser.parse_args()

    scan_r_reuse(args.input, args.output)
