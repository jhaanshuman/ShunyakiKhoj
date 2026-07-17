import http.server
import socketserver
import urllib.request
import urllib.error
import json
import os

PORT = 8000
API_TARGET = "https://sanskritai.vercel.app/api/calculate"

class LocalProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/cached_panchang":
            res_data = None
            
            # 1. Try to fetch from remote Vercel API
            try:
                req = urllib.request.Request(
                    "https://sanskritai.vercel.app/api/cached_panchang",
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req, timeout=3) as response:
                    res_data = response.read()
            except Exception as e:
                print("Remote Vercel fetch failed, trying local engine:", e)
                
            # 2. Try to calculate locally if remote failed
            if not res_data:
                try:
                    import sys
                    root_dir = os.path.dirname(os.path.abspath(__file__))
                    if root_dir not in sys.path:
                        sys.path.append(root_dir)
                    from api.calculate import get_new_delhi_panchang_cached
                    calc_data = get_new_delhi_panchang_cached()
                    if calc_data:
                        res_data = json.dumps(calc_data).encode('utf-8')
                except Exception as e:
                    print("Local engine calculation failed, serving fallback mock data:", e)
            
            # 3. Serving static mock fallback if both remote and local calculation failed
            if not res_data:
                mock_data = {
                    "status": "success",
                    "panchang": {
                        "tithi": "Dwitiya",
                        "nakshatra": "Punarvasu",
                        "sunrise": "05:33",
                        "sunset": "19:12",
                        "vara": "Friday",
                        "month": "Ashadha",
                        "paksha": "Shukla"
                    },
                    "panchang_extended": {
                        "rahu_kalam": "10:44 - 12:26",
                        "abhijit": "11:58 - 12:51",
                        "brahma_muhurta": "04:12 - 04:58",
                        "paksha": "Shukla"
                    },
                    "regional": {
                        "lunar_month": "Ashadha",
                        "chandramasa": "Ashadha"
                    },
                    "d1_chart": {
                        "Sun": {"sign": "Gemini", "lon": 28.5},
                        "Moon": {"sign": "Cancer", "lon": 12.3},
                        "Mars": {"sign": "Leo", "lon": 4.7},
                        "Mercury": {"sign": "Gemini", "lon": 15.2},
                        "Jupiter": {"sign": "Taurus", "lon": 22.8},
                        "Venus": {"sign": "Cancer", "lon": 2.1},
                        "Saturn": {"sign": "Aquarius", "lon": 1.4},
                        "Rahu": {"sign": "Pisces", "lon": 14.5},
                        "Ketu": {"sign": "Virgo", "lon": 14.5}
                    },
                    "divisional_charts": {
                        "D1": {
                            "Asc": {"sign": "Leo"},
                            "Sun": {"sign": "Gemini"},
                            "Moon": {"sign": "Cancer"},
                            "Mars": {"sign": "Leo"},
                            "Mercury": {"sign": "Gemini"},
                            "Jupiter": {"sign": "Taurus"},
                            "Venus": {"sign": "Cancer"},
                            "Saturn": {"sign": "Aquarius"},
                            "Rahu": {"sign": "Pisces"},
                            "Ketu": {"sign": "Virgo"}
                        }
                    }
                }
                res_data = json.dumps(mock_data).encode('utf-8')
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(res_data)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path in ("/api/calculate", "/api/calculate_month"):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            res_data = None
            
            # 1. Try to forward to the remote API
            try:
                target_url = "https://sanskritai.vercel.app" + self.path
                req = urllib.request.Request(
                    target_url, 
                    data=post_data, 
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    res_data = response.read()
            except Exception as e:
                print(f"Remote proxy for {self.path} failed: {e}")
            
            # 2. Try to calculate locally if remote failed
            if not res_data:
                try:
                    import sys
                    root_dir = os.path.dirname(os.path.abspath(__file__))
                    if root_dir not in sys.path:
                        sys.path.append(root_dir)
                    import json
                    req_json = json.loads(post_data.decode('utf-8'))
                    
                    if self.path == "/api/calculate":
                        from api.calculate import BirthDetails, calculate_chart
                        details = BirthDetails(**req_json)
                        calc_res = calculate_chart(details)
                        res_data = json.dumps(calc_res).encode('utf-8')
                    elif self.path == "/api/calculate_month":
                        from api.calculate import MonthDetails, calculate_month
                        details = MonthDetails(**req_json)
                        calc_res = calculate_month(details)
                        res_data = json.dumps(calc_res).encode('utf-8')
                except Exception as e:
                    print(f"Local calculation for {self.path} failed: {e}")
                    
            if res_data:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(res_data)
            else:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "detail": "Both remote and local calculations failed."}).encode('utf-8'))
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
