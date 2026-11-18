# 🛠️ Dev Survival Kit (Offline-First & Emergency Infrastructure)

A complete, self-hosted, and air-gap-ready survival toolkit for developers, sysadmins, and infrastructure engineers. Designed to operate independently of external cloud providers during internet outages, grid failures, or emergency deployments.

---

## 📦 What's Included in This Repository

### 1. Automated PDF Field Manuals (`scripts/generate_manuals.py`)
Generates printable, offline-ready technical field manuals stored in the `manuals/` directory:
* **`01_cloud_and_server_field_guide.pdf`**: Emergency Linux firewall hardening (`ufw`), SSH lockdown, local self-signed SSL/TLS generation, and bare-metal `rsync` backups.
* **`02_emergency_micro_servers.pdf`**: Repurposing spare hardware into headless servers, CPU power-saving tuning for battery/solar operation, and ad-hoc Wi-Fi hotspot creation (`nmcli`).
* **`03_cloud_independence_offline_access.pdf`**: Exporting portable Docker image tarballs, local DNS resolution (`dnsmasq`), and offline documentation storage.

### 2. Offline Command Center Portal (`portal/`)
A zero-dependency Flask web application (`http://localhost:8080`) featuring:
* **Real-Time Node Telemetry**: Displays local IP address, hostname, CPU load, RAM usage, and disk capacity without external scripts or CDNs.
* **One-Click Manual Downloads**: Direct local HTTP downloads for all generated PDF field guides.
* **Local Service Launcher**: Quick-access dashboard linking to self-hosted offline services running on the local network.

### 3. Self-Hosted Zero-Cloud Stack (`docker-compose.yml`)
Pre-configured containerized services designed to run completely offline:
* **Survival Portal (`:8080`)**: The main web interface and manual generator.
* **Gitea (`:3000` / `:2222`)**: Self-hosted Git repositories, issue tracking, and code browsing in strict `OFFLINE_MODE`.
* **Static File & Binary Vault (`:8082`)**: Lightweight HTTP file server for sharing ISOs, SDKs, and `.tar` container images across a local LAN.

### 4. Bare-Metal Bootstrap Script (`scripts/bootstrap_offline.sh`)
An automated bash setup script for Debian/Ubuntu systems that installs essential CLI recovery utilities (`tmux`, `htop`, `rsync`, `dnsmasq`, `ufw`), builds an isolated Python virtual environment, generates the PDF manuals, and launches the portal in the background.

---

## ⚙️ Required Software & System Prerequisites

To build and run this kit, your host machine needs:
* **Operating System**: Linux (Debian, Ubuntu, Raspberry Pi OS, or Alpine recommended; macOS/WSL2 supported for portal testing).
* **Python**: Python `3.9+` with `pip` and `venv`.
* **Python Libraries** (listed in `requirements.txt`):
  * `flask==3.0.3` (Offline web portal)
  * `fpdf2==2.7.9` (PDF manual generation engine)
  * `psutil==6.0.0` (Hardware telemetry monitoring)
* **Container Runtime (Optional but Recommended)**: Docker Engine `24.0+` and Docker Compose `v2+`.
* **Core CLI Utilities**: `openssl`, `rsync`, `ufw`, `dnsmasq`, `network-manager` (`nmcli`), and `git`.

---

## 🧰 Recommended Hardware Components (Physical Survival Kit)

To deploy this repository as a true portable "go-bag" micro-server, pair this codebase with the following hardware:

* **Compute Node**: Raspberry Pi 4/5 (4GB+ RAM), Intel NUC, or a repurposed x86_64 laptop with a healthy battery.
* **High-Endurance Storage**:
  * Primary OS/Data: 128GB+ Industrial MicroSD card or NVMe SSD.
  * Cold Backup / Vault: 256GB+ ruggedized USB 3.2 flash drive or external SSD pre-loaded with OS ISOs, Docker `.tar` archives, and Kiwix `.zim` Wikipedia/StackOverflow dumps.
* **Networking Gear**:
  * Dual-band USB Wi-Fi adapter (supporting AP/Master mode for broadcasting an emergency offline hotspot).
  * Short Cat6 Ethernet patch cable (1m) and a compact 5-port Gigabit unmanaged switch.
* **Power & Resilience**:
  * 20,000mAh+ USB-C Power Delivery (PD) power bank (capable of 45W–65W output for laptops/SBCs).
  * Foldable 28W+ USB-C solar panel charger for extended off-grid operation.
* **Physical Documentation**:
  * Printed and laminated copies of the generated PDF manuals stored inside a waterproof sleeve.

---

## 🚀 Quick Start

### 1. Clone & Generate PDF Manuals
```bash
git clone https://github.com
cd dev-survival-kit
pip install -r requirements.txt
python3 scripts/generate_manuals.py
```

### 2. Run via Docker Compose (Full Stack)
```bash
docker-compose up -d
```
Open `http://localhost:8080` in your browser to access the Offline Command Center.

### 3. Run Bare-Metal Setup (No Docker)
```bash
chmod +x scripts/bootstrap_offline.sh
sudo ./scripts/bootstrap_offline.sh
```

---

## 📁 Repository Structure

```text
dev-survival-kit/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── scripts/
│   ├── generate_manuals.py
│   └── bootstrap_offline.sh
├── portal/
│   ├── app.py
│   └── templates/
│       └── index.html
├── manuals/          # Auto-generated PDF field manuals
└── vault/            # Place offline ISOs, SDKs, and Docker tarballs here
```

---

