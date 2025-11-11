#!/usr/bin/env python3
"""Find all missing dependencies by trying to import main.py"""
import sys
import importlib.util

missing = []

def try_import(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError as e:
        missing.append(str(e))
        return False

# Try importing main
try:
    import main
    print("✅ main.py imported successfully!")
except ModuleNotFoundError as e:
    print(f"❌ Missing: {e}")
    # Extract module name from error
    module = str(e).split("'")[1] if "'" in str(e) else "unknown"
    print(f"MISSING_MODULE={module}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Other error: {e}")
    sys.exit(2)
