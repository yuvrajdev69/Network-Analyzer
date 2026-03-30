# analyzer.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import nmap
import csv
from datetime import datetime

# ----------------- Functions -----------------
def scan_network():
    subnet = subnet_entry.get()
    if not subnet:
        messagebox.showwarning("Input Error", "Please enter subnet (e.g., 192.168.1.0/24)")
        return

    # Clear previous results
    for row in result_table.get_children():
        result_table.delete(row)
    log_text.delete(1.0, tk.END)

    nm = nmap.PortScanner()
    log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Scanning {subnet}...\n")
    log_text.update()

    try:
        nm.scan(hosts=subnet, arguments='-F')
        for host in nm.all_hosts():
            status = nm[host].state()
            ports = list(nm[host]['tcp'].keys()) if 'tcp' in nm[host] else []
            hostname = nm[host].hostname() if nm[host].hostname() else "-"
            
            # Insert into table
            result_table.insert("", tk.END, values=(host, hostname, status, ", ".join(map(str, ports))),
                                tags=('active',) if status=='up' else ('down',))
            
            # Insert into log
            log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {host} -> {status.upper()}, Ports: {ports}\n")
            log_text.update()
    except Exception as e:
        messagebox.showerror("Scan Error", str(e))

    log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Scan complete!\n")

def export_csv():
    if not result_table.get_children():
        messagebox.showwarning("No Data", "No results to export!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files","*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["IP Address", "Hostname", "Status", "Open Ports"])
            for row_id in result_table.get_children():
                writer.writerow(result_table.item(row_id)['values'])
        messagebox.showinfo("Export Successful", f"Results saved to {file_path}")

# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("LAN Network Analyzer")
root.geometry("800x500")
root.configure(bg="black")

# ----------------- Treeview Style (Hacker Vibe) -----------------
style = ttk.Style()
style.theme_use("default")  # default theme
style.configure("Treeview",
                background="#0a0a0a",   # black background
                foreground="#00ff00",   # bright green text
                fieldbackground="#0a0a0a",
                rowheight=25,
                font=("Consolas", 12))
style.map('Treeview', background=[('selected', '#004400')])  # selected row color

# Fonts and colors
font_main = ("Consolas", 12)
font_title = ("Consolas", 18, "bold")
color_active = "#00ff00"
color_down = "#ff3333"
color_header = "#00ffff"
bg_color = "#0a0a0a"

# Top section - Title
title_label = tk.Label(root, text="LAN Network Analyzer", font=font_title, fg=color_active, bg=bg_color)
title_label.pack(pady=5)

subtitle_label = tk.Label(root, text="Scan your LAN and view devices + ports", font=font_main, fg="#33ff33", bg=bg_color)
subtitle_label.pack(pady=2)

# Middle section - Controls
control_frame = tk.Frame(root, bg=bg_color)
control_frame.pack(pady=5)

tk.Label(control_frame, text="Subnet:", font=font_main, fg=color_active, bg=bg_color).pack(side=tk.LEFT, padx=5)
subnet_entry = tk.Entry(control_frame, font=font_main, fg=color_active, bg="#111111", insertbackground=color_active)
subnet_entry.pack(side=tk.LEFT, padx=5)
subnet_entry.insert(0, "192.168.1.0/24")

scan_btn = tk.Button(control_frame, text="Scan Network", font=font_main, fg=color_active, bg="#111111",
                     command=scan_network)
scan_btn.pack(side=tk.LEFT, padx=5)

export_btn = tk.Button(control_frame, text="Export CSV", font=font_main, fg=color_active, bg="#111111",
                       command=export_csv)
export_btn.pack(side=tk.LEFT, padx=5)

# Bottom section - Results Table
table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

columns = ("IP Address", "Hostname", "Status", "Open Ports")
result_table = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
for col in columns:
    result_table.heading(col, text=col)
    result_table.column(col, anchor=tk.CENTER, width=150)
result_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add scrollbar
scrollbar = tk.Scrollbar(table_frame, orient=tk.VERTICAL, command=result_table.yview)
result_table.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Color tags
result_table.tag_configure('active', foreground=color_active)
result_table.tag_configure('down', foreground=color_down)

# Scan Log Textbox
log_text = tk.Text(root, height=8, bg="black", fg=color_active, font=font_main)
log_text.pack(fill=tk.BOTH, padx=10, pady=5)
log_text.insert(tk.END, "[INFO] Ready to scan your network...\n")

root.mainloop()