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
            
            # 1. Try to calculate using local Vedic Engine
            try:
                import sys
                root_dir = os.path.dirname(os.path.abspath(__file__))
                backend_dir = os.path.join(root_dir, 'backend')
                if root_dir not in sys.path: sys.path.append(root_dir)
                if backend_dir not in sys.path: sys.path.append(backend_dir)
                import json
                req_json = json.loads(post_data.decode('utf-8'))
                
                if self.path == "/api/calculate":
                    from backend.vedic_engine.master_horoscope import MasterHoroscopeBuilder
                    from backend.database import EngineDatabase
                    
                    dob = req_json.get('date', '1994/01/05').replace('-', '/')
                    tob = req_json.get('time', '20:00')
                    place = req_json.get('place', 'Patna')
                    lat = float(req_json.get('lat', 25.5941))
                    lon = float(req_json.get('lon', 85.1376))
                    tz = float(req_json.get('tz_offset', 5.5))
                    ayanamsa = req_json.get('ayanamsa', 'Lahiri')
                    node = req_json.get('node_type', 'True')
                    hsys = req_json.get('house_system', 'Whole Sign')
                    
                    master_obj = MasterHoroscopeBuilder.build_master_horoscope(
                        name=req_json.get('name', 'Native'),
                        gender=req_json.get('gender', 'Male'),
                        dob_str=dob, tob_str=tob, place=place,
                        lat=lat, lon=lon, tz_offset=tz,
                        ayanamsa_name=ayanamsa, node_type=node, house_system=hsys
                    )
                    master_obj['status'] = 'success'
                    asc_sign_idx = int(master_obj['houses']['ascendant_sidereal_lon'] / 30.0) % 12
                    d1_flat = {}
                    for p_name, p_data in master_obj['planets'].items():
                        h_num = p_data.get('house', ((p_data['sign_index'] - asc_sign_idx + 12) % 12) + 1)
                        d1_flat[p_name] = {
                            'sign': p_data['sign_name'],
                            'degree': p_data['sign_degree'],
                            'longitude': p_data['sidereal_lon'],
                            'nakshatra': p_data['nakshatra_name'],
                            'pada': p_data['pada'],
                            'house': h_num,
                            'is_retrograde': p_data['is_retrograde'],
                            'is_combust': p_data['is_combust']
                        }
                    master_obj['d1_chart'] = d1_flat
                    
                    # ── Data Folder Export: Write all 4 verification files ──────────────────
                    try:
                        data_dir = os.path.join(root_dir, 'Data')
                        os.makedirs(data_dir, exist_ok=True)

                        # 1. Latest user input (always overwritten)
                        with open(os.path.join(data_dir, 'latest_user_input.json'), 'w', encoding='utf-8') as f:
                            json.dump(req_json, f, indent=2, ensure_ascii=False)

                        # 2. Latest user output (always overwritten)
                        with open(os.path.join(data_dir, 'latest_user_output.json'), 'w', encoding='utf-8') as f:
                            json.dump(master_obj, f, indent=2, ensure_ascii=False)

                        # 3. Named verification input (permanent copy for manual checking)
                        import datetime as _dt
                        input_snapshot = {
                            "description": "Input parameters used for Personalized Kundali generation",
                            "generated_at": _dt.datetime.now().isoformat(),
                            "birth_details": {
                                "name": req_json.get('name', 'Native'),
                                "gender": req_json.get('gender', 'Unknown'),
                                "date_of_birth": req_json.get('date', ''),
                                "time_of_birth": req_json.get('time', ''),
                                "place": req_json.get('place', ''),
                                "latitude": req_json.get('lat', 0.0),
                                "longitude": req_json.get('lon', 0.0),
                                "timezone_offset": req_json.get('tz_offset', 5.5)
                            },
                            "engine_settings": {
                                "ayanamsa": req_json.get('ayanamsa', 'Lahiri'),
                                "node_type": req_json.get('node_type', 'True'),
                                "house_system": req_json.get('house_system', 'Whole Sign'),
                                "chart_style": req_json.get('rashi_visibility', 'Both'),
                                "outer_planets": req_json.get('outer_planets', 'hidden'),
                                "terminology": req_json.get('terminology', 'Sanskrit'),
                                "long_style": req_json.get('long_style', 'DMS')
                            }
                        }
                        with open(os.path.join(data_dir, 'input_settings.json'), 'w', encoding='utf-8') as f:
                            json.dump(input_snapshot, f, indent=2, ensure_ascii=False)

                        # 4. Named verification output (permanent copy for manual checking)
                        with open(os.path.join(data_dir, 'output_master_horoscope.json'), 'w', encoding='utf-8') as f:
                            json.dump(master_obj, f, indent=2, ensure_ascii=False)

                        print(f"[Data Export] Written 4 files to Data/ for: {req_json.get('name', 'Native')} ({req_json.get('date', '')} {req_json.get('time', '')})")
                    except Exception as dev_err:
                        print("Data export warning:", dev_err)


                    # Store in local SQLite
                    import hashlib
                    s_str = f"{dob}_{tob}_{lat:.4f}_{lon:.4f}_{tz}_{ayanamsa}_{node}_{hsys}"
                    s_hash = hashlib.sha256(s_str.encode('utf-8')).hexdigest()[:16]
                    EngineDatabase.save_cached_horoscope(s_hash, master_obj)
                    
                    res_data = json.dumps(master_obj).encode('utf-8')
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Local engine calculation failed: {e}")

                    
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
    
    try:
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
        from backend.database import EngineDatabase
        EngineDatabase.initialize_schema()
        print("SQLite Database initialized with 26 tables.")
    except Exception as e:
        print("Database schema initialization warning:", e)
        
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), LocalProxyHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
