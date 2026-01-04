# sync/lan_sync.py
# 2Aether Day 5 — Cloudless LAN Sync (No Internet, No Cloud)
# Built by @realdavejags — Ships Nov 11 2025

import socket
import json
import threading
import os
from pathlib import Path
from datetime import datetime

HOST = "0.0.0.0"
PORT = 9999
SYNC_DIR = Path("recordings")
PEERS = []


def broadcast_report(report_path):
	report_path = Path(report_path)
	if not report_path.exists():
		return

	with open(report_path, "rb") as f:
		data = f.read()

	message = {
		"type": "new_report",
		"filename": report_path.name,
		"size": len(data),
		"timestamp": datetime.now().isoformat(),
		"builder": "@realdavejags"
	}

	for peer in PEERS:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(2)
			s.connect(peer)
			s.sendall(json.dumps(message).encode() + b"\n")
			s.sendall(data)
			s.close()
		except:
			pass


def receive_reports():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen()
		print(f"2Aether LAN sync listening on {HOST}:{PORT}")

		while True:
			try:
				conn, addr = s.accept()
				threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
			except:
				break


def handle_client(conn, addr):
	print(f"2Aether peer connected: {addr}")
	data = b""
	with conn:
		while True:
			chunk = conn.recv(4096)
			if not chunk:
				break
			data += chunk

	try:
		header, payload = data.split(b"\n", 1)
		message = json.loads(header.decode())

		if message["type"] == "new_report":
			filename = message["filename"]
			save_path = SYNC_DIR / filename
			with open(save_path, "wb") as f:
				f.write(payload)
			print(f"SYNC RECEIVED: {filename} from {addr[0]}")

			if filename.endswith(".2aether.html"):
				os.startfile(save_path.absolute())
	except Exception as e:
		print(f"Sync error: {e}")


def start_sync():
	os.makedirs(SYNC_DIR, exist_ok=True)
	threading.Thread(target=receive_reports, daemon=True).start()
	print("DAY 5 COMPLETE — CLOUDLESS LAN SYNC LIVE")


def add_peer(ip):
	if (ip, PORT) not in PEERS:
		PEERS.append((ip, PORT))
		print(f"Peer added: {ip}")


if __name__ == "__main__":
	start_sync()
	print("Run on every machine. Reports sync instantly.")
	print("Add peer: add_peer('192.168.1.100')")

	try:
		while True:
			cmd = input("\n> ")
			if cmd.startswith("add_peer"):
				ip = cmd.split("'")[1]
				add_peer(ip)
			elif cmd == "exit":
				break
	except:
		pass