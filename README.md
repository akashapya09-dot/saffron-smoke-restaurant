# Saffron & Smoke — Full-stack restaurant application

Preserves the Saffron & Smoke visual design and adds a real Flask/SQLite API, order checkout with server-calculated totals, reservation requests, contact messages, API docs, and a token-protected staff dashboard.

## Features
- 24-dish menu with category filters/search and premium food image URLs.
- Basket with quantity controls, subtotal, illustrative 5% GST estimate, and final total. The server recalculates the bill from authoritative menu prices. Verify applicable tax rates with a qualified accountant before commercial use.
- Takeaway or dine-in checkout; dine-in requires selecting a table. Orders persist in SQLite with references, status and unpaid payment state. No online payment is taken.
- Reservation requests persist with reference and initial `requested` status. Staff must set `confirmed` in dashboard; request acceptance is not represented as automatic confirmation. The current capacity information is a request tracker, not a real-time booking guarantee.
- Contact messages stored in SQLite.
- `/docs` interactive API docs and `/openapi.json`.
- Staff dashboard at `/admin.html`, protected by a random `ADMIN_TOKEN` created by backend setup.

## GitHub layout
Upload the contents of this directory to the repository root: `frontend/`, `backend/`, `README.md`.

## Deploy backend EC2 (Amazon Linux 2023)
1. Connect via EC2 Instance Connect. Install Git: `sudo dnf install -y git`.
2. Clone your repository and `cd <repo>/backend`.
3. Run `chmod +x setup_backend.sh && ./setup_backend.sh`.
4. Save the admin token printed by the script securely. The service is installed at `/opt/saffron-smoke-backend`; SQLite DB is stored alongside the app at `/opt/saffron-smoke-backend/saffron_smoke.db`.
5. In the backend security group, allow TCP 8000 from the **frontend security group** only. Do not leave port 8000 open to the whole internet.

## Deploy frontend EC2
1. Install Git/Apache: `sudo dnf install -y git httpd`. Clone the same repository.
2. In `frontend/`, run `chmod +x setup_frontend.sh && ./setup_frontend.sh <BACKEND_PRIVATE_IPV4>`.
3. Frontend security group allows HTTP 80 from internet. Backend security group permits 8000 from frontend security group. Both instances should be in a network that can route between their private IPs.
4. Open `http://<FRONTEND_PUBLIC_IPV4>/`. API calls are same-origin and Apache proxies `/api/` to backend private IP.

## Admin dashboard
Open `http://<FRONTEND_PUBLIC_IPV4>/admin.html` and enter the backend `ADMIN_TOKEN` printed once by the setup script. Admin APIs require `Authorization: Bearer <token>`. Keep the token private. Rotate it by updating `/etc/saffron-smoke.env` and restarting `sudo systemctl restart saffron-smoke-backend`.

## Test endpoints
- `GET /api/health`
- `GET /api/menu`
- `POST /api/orders`
- `GET /api/orders/<reference>`
- `POST /api/reservations`
- `GET /api/reservations/availability?date=YYYY-MM-DD`
- `POST /api/contact`
- `GET /api/admin/summary` (requires token)
- `POST /api/admin/orders/<reference>/status` (requires token)
- `POST /api/admin/reservations/<reference>/status` (requires token)
- `GET /docs`

## Limitations / production readiness
This is a deployable learning/demo project, not a certified production point-of-sale system. Online payments, transactional email/SMS, inventory decrement, true table-slot locking, backups, HTTPS/domain, rate limiting, CSRF strategy, audit logs, and production database hosting must be configured before commercial launch. The example 5% GST is illustrative and should be confirmed for the actual restaurant.
