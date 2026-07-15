from fastapi import FastAPI
import sys
import os

app = FastAPI()

@app.get("/api/test")
@app.get("/")
def test_imports():
    report = {
        "python_version": sys.version,
        "current_dir": os.getcwd(),
        "dir_contents": os.listdir("."),
        "sys_path": sys.path,
        "imports": {}
    }
    
    modules = ["fastapi", "pydantic", "geopy", "pytz", "swisseph", "timezonefinder"]
    for mod in modules:
        try:
            __import__(mod)
            report["imports"][mod] = "OK"
        except Exception as e:
            report["imports"][mod] = f"ERROR: {str(e)}"
            
    return report
