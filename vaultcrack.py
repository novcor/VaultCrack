import tkinter as tk
from tkinter import filedialog, messagebox
import json
from collections import defaultdict
import os

def scan_r_reuse_gui(input_file, output_file):
    r_map = defaultdict(list)
    results = []

    with open(input_file, 'r') as f:
        for line in f:
            tx = json.loads(line)
            txid = tx.get('txid')
            r = tx.get('r')
            if not txid or not r:
                continue
            r_map[r].append(txid)

    for r_value, txids in r_map.items():
        if len(txids) > 1:
            results.append({
                "r_value": r_value,
                "txids": txids,
                "suspected_duplicate": True
            })

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    return output_file

def run_gui():
    def choose_file():
        file_path = filedialog.askopenfilename(title="Select JSONL File", filetypes=[("JSONL Files", "*.jsonl")])
        if file_path:
            input_entry.delete(0, tk.END)
            input_entry.insert(0, file_path)

    def run_scan():
        input_file = input_entry.get()
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Please select a valid input file.")
            return

        output_file = os.path.splitext(input_file)[0] + "_rscan_results.json"
        result_path = scan_r_reuse_gui(input_file, output_file)
        messagebox.showinfo("Scan Complete", f"Scan complete.\nResults saved to:\n{result_path}")

    root = tk.Tk()
    root.title("VaultCrack R-Value Reuse Scanner")

    tk.Label(root, text="Select transaction file (.jsonl):").pack(pady=5)
    input_entry = tk.Entry(root, width=60)
    input_entry.pack(padx=10)
    tk.Button(root, text="Browse", command=choose_file).pack(pady=5)
    tk.Button(root, text="Run Scan", command=run_scan, bg="#66cc66").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
