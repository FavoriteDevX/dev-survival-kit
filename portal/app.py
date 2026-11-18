import os
import socket
import psutil
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

MANUALS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "manuals"))


def get_system_stats():
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "127.0.0.1"

    return {
        "hostname": hostname,
        "local_ip": local_ip,
        "cpu_percent": psutil.cpu_percent(interval=0.2),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
    }


@app.route("/")
def index():
    os.makedirs(MANUALS_DIR, exist_ok=True)
    manuals = sorted([f for f in os.listdir(MANUALS_DIR) if f.endswith(".pdf")])
    stats = get_system_stats()

    offline_tools = [
        {
            "name": "Gitea (Local Git Forge)",
            "port": 3000,
            "desc": "Self-hosted Git repositories, issue tracking, and code browser.",
            "status": "Local Container"
        },
        {
            "name": "Kiwix / Offline Docs",
            "port": 8081,
            "desc": "Offline StackOverflow, MDN Web Docs, and technical wikis.",
            "status": "Local Container"
        },
        {
            "name": "Local File & Binary Vault",
            "port": 8082,
            "desc": "Browser-based file manager for ISOs, Docker tarballs, and SDKs.",
            "status": "Local Container"
        }
    ]

    return render_template("index.html", manuals=manuals, stats=stats, tools=offline_tools)


@app.route("/manuals/<path:filename>")
def download_manual(filename):
    return send_from_directory(MANUALS_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
