// API calls use the same origin. Apache proxies /api to the private backend IP.
// This avoids browser CORS failures and keeps port 8000 off the public frontend path.
window.API_BASE_URL = "";
