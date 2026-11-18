#!/usr/bin/env bash
set -euo pipefail

echo "=========================================="
echo " DEV SURVIVAL KIT - BARE-METAL BOOTSTRAP  "
echo "=========================================="

# 1. Create required local directories
mkdir -p manuals vault data/gitea

# 2. Install base offline utilities if apt is available
if command -v apt-get &> /dev/null; then
    echo "[*] Installing essential CLI tools..."
    apt-get update -y || true
    apt-get install -y python3 python3-pip python3-venv curl git tmux htop rsync dnsmasq ufw net-tools || true
fi

# 3. Setup Python virtual environment & generate manuals
echo "[*] Setting up Python environment and generating PDF manuals..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 scripts/generate_manuals.py

# 4. Start Portal in background via systemd or nohup
echo "[*] Starting Offline Survival Portal on port 8080..."
nohup .venv/bin/python3 portal/app.py > portal.log 2>&1 &

LOCAL_IP=$(hostname -I | awk '{print $1}')
echo "=========================================="
echo " [SUCCESS] Survival Node Ready!"
echo " Access Portal: http://${LOCAL_IP:-127.0.0.1}:8080"
echo " PDF Manuals saved in: ./manuals/"
echo "=========================================="
