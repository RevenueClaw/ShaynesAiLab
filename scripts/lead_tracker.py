#!/usr/bin/env python3
"""Shayne's AI Lab — Simple Lead Tracker Server
Accepts lead data via POST, stores in JSON, serves for nurture cron.

Run: python3 lead_tracker.py &
Port: 8092
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leads.json')
PORT = 8092

def load_leads():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)

def save_leads(leads):
    os.makedirs(os.path.dirname(DATA_FILE) or '.', exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(leads, f, indent=2)

class LeadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        
        try:
            data = json.loads(body)
            email = data.get('email', '').strip().lower()
            if not email or '@' not in email:
                self._send(400, {'success': False, 'error': 'Valid email required'})
                return
            
            leads = load_leads()
            source = data.get('source', 'starter-kit')
            
            # Check if we already have this email
            existing = [l for l in leads if l['email'] == email]
            if existing:
                # Just update their latest activity
                existing[0]['last_activity'] = datetime.now(timezone.utc).isoformat()
                existing[0]['source'] = source
                existing[0]['first_name'] = data.get('firstName', data.get('firstName', ''))
                existing[0]['nurture_step'] = existing[0].get('nurture_step', 0)
            else:
                leads.append({
                    'email': email,
                    'first_name': data.get('firstName', data.get('firstName', '')),
                    'source': source,
                    'signup_date': datetime.now(timezone.utc).isoformat(),
                    'last_activity': datetime.now(timezone.utc).isoformat(),
                    'nurture_step': 0,
                    'nurture_sent_at': None,
                })
            
            save_leads(leads)
            self._send(200, {'success': True})
            
        except Exception as e:
            self._send(500, {'success': False, 'error': str(e)})
    
    def do_GET(self):
        if self.path == '/health':
            self._send(200, {'status': 'ok', 'leads': len(load_leads())})
            return
        self._send(404, {'error': 'Not found'})
    
    def _send(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        pass  # Quiet

if __name__ == '__main__':
    print(f"Lead tracker starting on port {PORT}")
    server = HTTPServer(('0.0.0.0', PORT), LeadHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        server.server_close()