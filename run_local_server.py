import http.server
import socketserver
import urllib.request
import urllib.error
import json
import os

PORT = 8000
API_TARGET = "https://sanskritai.vercel.app/api/calculate"

class LocalProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/calculate":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Forward to the remote API
                req = urllib.request.Request(
                    API_TARGET, 
                    data=post_data, 
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req) as response:
                    res_data = response.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(res_data)
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "detail": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def translate_path(self, path):
        root = os.path.dirname(os.path.abspath(__file__))
        path = http.server.SimpleHTTPRequestHandler.translate_path(self, path)
        rel = os.path.relpath(path, os.getcwd())
        return os.path.join(root, rel)

if __name__ == "__main__":
    print(f"Starting server at http://localhost:{PORT}")
    print("Serving files from the current directory.")
    print("Proxying POST /api/calculate requests to Sanskrit AI API server.")
    print("Press Ctrl+C to stop.")
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), LocalProxyHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
