LAN Network Analyzer

A simple Python-based GUI tool to scan your local network and display active devices, hostnames, and open ports.

---

🚀 Features

- Scan a subnet (e.g., 192.168.1.0/24)
- Detect active and inactive hosts
- Show hostnames and open ports
- Export scan results to CSV
- Real-time scan logs
- Clean hacker-style GUI (because aesthetics matter)

---

🛠️ Requirements

- Python 3.x
- Nmap (must be installed on your system)

Install Python dependency:
pip install -r requirements.txt

---

⚙️ Install Nmap

Windows:

Download and install from: https://nmap.org/download.html

Linux:

sudo apt install nmap

---

▶️ How to Run

1. Clone the repository:
   git clone https://github.com/your-username/network-analyzer.git

2. Go to project folder:
   cd network-analyzer

3. Install dependencies:
   pip install -r requirements.txt

4. Run the app:
   python analyzer.py

---

📊 How It Works

- Enter subnet (default: 192.168.1.0/24)
- Click Scan Network
- View devices, status, and open ports
- Export results using Export CSV

---

📁 Output Example

The exported CSV contains:

- IP Address
- Hostname
- Status (Up/Down)
- Open Ports

---

⚠️ Notes

- Make sure Nmap is installed and accessible from terminal
- Run with proper permissions if scan fails
- Scanning large networks may take time

---

📌 Disclaimer

This tool is for educational and authorized network scanning only. Do not use it on networks without permission.

---

👨‍💻 Author

Yuvraj

---

⭐ Support

If you like this project, consider giving it a star on GitHub.
