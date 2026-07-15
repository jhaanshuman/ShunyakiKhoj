from fastapi import FastAPI
import sys
import os
import traceback

app = FastAPI()

@app.get("/api/test")
@app.get("/")
def test_imports():
    report = {
        "python_version": sys.version,
        "current_dir": os.getcwd(),
        "dir_contents": os.listdir("."),
        "imports": {}
    }
    
    # Try importing kundli_utils
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        import kundli_utils
        report["imports"]["kundli_utils"] = "OK"
    except Exception as e:
        report["imports"]["kundli_utils"] = f"ERROR: {str(e)}"
        report["traceback"] = traceback.format_exc()
            
    return report
