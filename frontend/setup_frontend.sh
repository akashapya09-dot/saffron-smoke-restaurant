#!/bin/bash
set -euo pipefail
if [ "$#" -ne 1 ]; then echo "Usage: ./setup_frontend.sh <BACKEND_PRIVATE_IPV4>"; exit 1; fi
BACKEND_IP="$1"; APP_DIR="/var/www/html"
sudo dnf install -y httpd
sudo mkdir -p "$APP_DIR"
sudo cp index.html style.css script.js config.js admin.html admin.css admin.js "$APP_DIR/"
sudo tee /etc/httpd/conf.d/saffron-smoke-api.conf >/dev/null <<EOF
ProxyRequests Off
ProxyPreserveHost On
ProxyPass /api/ http://${BACKEND_IP}:8000/api/
ProxyPassReverse /api/ http://${BACKEND_IP}:8000/api/
ProxyPass /docs http://${BACKEND_IP}:8000/docs
ProxyPassReverse /docs http://${BACKEND_IP}:8000/docs
ProxyPass /openapi.json http://${BACKEND_IP}:8000/openapi.json
ProxyPassReverse /openapi.json http://${BACKEND_IP}:8000/openapi.json
EOF
printf 'window.API_BASE_URL = "";\n' | sudo tee "$APP_DIR/config.js" >/dev/null
sudo chown -R apache:apache "$APP_DIR"
sudo apachectl configtest
sudo systemctl enable --now httpd
sudo systemctl restart httpd
echo "Frontend deployed. Browse http://$(curl -fsS https://checkip.amazonaws.com)/"
echo "API proxy target: http://${BACKEND_IP}:8000"
