import os
from fpdf import FPDF

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "manuals")
os.makedirs(OUTPUT_DIR, exist_ok=True)


class SurvivalPDF(FPDF):
    def __init__(self, title_text):
        super().__init__()
        self.title_text = title_text
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"DEV SURVIVAL KIT // {self.title_text.upper()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.line(10, 18, 200, 18)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"OFFLINE FIELD MANUAL - PAGE {self.page_no()}", align="C")

    def add_chapter(self, heading, body_paragraphs):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(20, 20, 20)
        self.ln(4)
        self.cell(0, 10, heading, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(40, 40, 40)
        for p in body_paragraphs:
            if p.startswith("CMD:"):
                self.set_font("Courier", "B", 10)
                self.set_fill_color(240, 240, 240)
                self.multi_cell(0, 7, p.replace("CMD:", "").strip(), fill=True)
                self.ln(2)
                self.set_font("Helvetica", "", 11)
            else:
                self.multi_cell(0, 6, p)
                self.ln(3)


def build_manual(filename, main_title, subtitle, chapters):
    pdf = SurvivalPDF(main_title)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 22)
    pdf.ln(10)
    pdf.multi_cell(0, 12, main_title)
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(90, 90, 90)
    pdf.multi_cell(0, 8, subtitle)
    pdf.ln(8)

    for heading, content in chapters:
        pdf.add_chapter(heading, content)

    filepath = os.path.join(OUTPUT_DIR, filename)
    pdf.output(filepath)
    print(f"[OK] Generated: {filepath}")


def main():
    # Manual 1: Cloud & Bare-Metal Server Survival
    m1_chapters = [
        ("1. Emergency Server Hardening", [
            "When deploying a standalone Linux server without managed cloud firewalls, lock down SSH and network ports immediately.",
            "CMD: ufw default deny incoming && ufw default allow outgoing && ufw allow 22/tcp && ufw enable",
            "Disable root password login by editing /etc/ssh/sshd_config and setting PermitRootLogin prohibit-password and PasswordAuthentication no."
        ]),
        ("2. Reverse Proxy & Local SSL Without Internet", [
            "Use Caddy or Nginx with self-signed certificates to serve internal apps securely over HTTPS.",
            "CMD: openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/ssl/private/local.key -out /etc/ssl/certs/local.crt -subj '/CN=survival.local'",
            "Configure Nginx to route local subdomains (*.survival.local) to internal Docker ports."
        ]),
        ("3. Automated Bare-Metal Backups", [
            "Never rely solely on cloud snapshots. Use rsync over SSH or local external drives with incremental hardlinks.",
            "CMD: rsync -aAXv --delete --exclude={'/dev/*','/proc/*','/sys/*','/tmp/*'} / /mnt/backup_drive/"
        ])
    ]
    build_manual(
        "01_cloud_and_server_field_guide.pdf",
        "Practical Guide: Cloud & Bare-Metal Servers",
        "Hardening, local networking, and zero-dependency server administration.",
        m1_chapters
    )

    # Manual 2: Emergency Micro-Servers
    m2_chapters = [
        ("1. Repurposing Hardware into Micro-Servers", [
            "Any x86_64 laptop, Raspberry Pi, or Android device (via Termux/Linux Deploy) can act as a tactical micro-server.",
            "If using a laptop, disable lid-close sleep so it functions as a headless unit:",
            "CMD: sed -i 's/#HandleLidSwitch=suspend/HandleLidSwitch=ignore/' /etc/systemd/logind.conf && systemctl restart systemd-logind"
        ]),
        ("2. Power Management & Low-Wattage Tuning", [
            "To maximize battery or solar runtime during grid outages, force CPU frequency governors into powersave mode.",
            "CMD: echo 'powersave' | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor",
            "Disable unused hardware radios (Bluetooth, Wi-Fi if wired) using rfkill block bluetooth."
        ]),
        ("3. Ad-Hoc Wi-Fi Access Point (Offline LAN)", [
            "Turn your micro-server into a standalone Wi-Fi router so team devices can connect and access local Git, docs, and chat.",
            "CMD: nmcli dev wifi hotspot ifname wlan0 ssid DevSurvivalNet password EmergencyKey123"
        ])
    ]
    build_manual(
        "02_emergency_micro_servers.pdf",
        "Emergency Micro-Server Construction",
        "Building low-power, portable servers from spare hardware during outages.",
        m2_chapters
    )

    # Manual 3: Cloud Independence & Offline Tooling
    m3_chapters = [
        ("1. Escaping Cloud Lock-In", [
            "Maintain local mirrors of critical repositories, container images, and language packages (PyPI, NPM, Cargo).",
            "Export Docker images into portable tarballs before going offline:",
            "CMD: docker save -o offline_stack.tar gitea/gitea:latest nginx:alpine python:3.11-slim"
        ]),
        ("2. Local DNS Resolution (dnsmasq)", [
            "Run dnsmasq on your micro-server to resolve custom local domains without external DNS servers.",
            "CMD: echo 'address=/survival.lan/192.168.1.1' >> /etc/dnsmasq.conf && systemctl restart dnsmasq"
        ]),
        ("3. Offline Documentation & Knowledge Base", [
            "Store static HTML/Markdown docs, RFCs, and Wikipedia dumps (Kiwix ZIM files) on local NVMe/SD storage.",
            "Always keep local copies of language standard libraries and man-pages installed via apt install manpages-dev."
        ])
    ]
    build_manual(
        "03_cloud_independence_offline_access.pdf",
        "Cloud Independence & Offline Platforms",
        "Running full development workflows in air-gapped and zero-cloud environments.",
        m3_chapters
    )


if __name__ == "__main__":
    main()
