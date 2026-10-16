#!/bin/bash
set -euo pipefail
APP_DIR="/opt/saffron-smoke-backend"
sudo dnf install -y python3 python3-pip git
sudo mkdir -p "$APP_DIR"
sudo cp app.py requirements.txt "$APP_DIR/"
sudo chown -R ec2-user:ec2-user "$APP_DIR"
if [ ! -x "$APP_DIR/venv/bin/python" ]; then python3 -m venv "$APP_DIR/venv"; fi
"$APP_DIR/venv/bin/pip" install --upgrade pip
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"
if ! sudo test -s /etc/saffron-smoke.env; then
  TOKEN=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
  echo "ADMIN_TOKEN=$TOKEN" | sudo tee /etc/saffron-smoke.env >/dev/null
  sudo chmod 600 /etc/saffron-smoke.env
  echo "IMPORTANT: Save this one-time admin token securely: $TOKEN"
else
  echo "Existing admin token preserved in /etc/saffron-smoke.env"
fi
sudo tee /etc/systemd/system/saffron-smoke-backend.service >/dev/null <<'SERVICE'
[Unit]
Description=Saffron and Smoke API
After=network.target
[Service]
User=ec2-user
WorkingDirectory=/opt/saffron-smoke-backend
EnvironmentFile=/etc/saffron-smoke.env
ExecStart=/opt/saffron-smoke-backend/venv/bin/python /opt/saffron-smoke-backend/app.py
Restart=always
RestartSec=3
[Install]
WantedBy=multi-user.target
SERVICE
sudo systemctl daemon-reload
sudo systemctl enable saffron-smoke-backend
sudo systemctl restart saffron-smoke-backend
sudo systemctl --no-pager --full status saffron-smoke-backend
printf '\nHealth test: '; curl --fail --silent http://localhost:8000/api/health
printf '\nMenu count: '; curl --fail --silent http://localhost:8000/api/menu | python3 -c 'import json,sys; print(json.load(sys.stdin)["count"], "menu items")'
