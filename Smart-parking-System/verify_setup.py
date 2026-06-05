#!/usr/bin/env python3
"""
Smart Parking System - Setup Verification Tool
Checks if all required components are installed and configured
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.END}\n")

def check_file(filename):
    """Check if file exists"""
    exists = os.path.exists(filename)
    status = f"{Colors.GREEN}✓{Colors.END}" if exists else f"{Colors.RED}✗{Colors.END}"
    print(f"  {status} {filename}")
    return exists

def check_python_package(package_name, import_name=None):
    """Check if Python package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"  {Colors.GREEN}✓{Colors.END} {package_name}")
        return True
    except ImportError:
        print(f"  {Colors.RED}✗{Colors.END} {package_name}")
        return False

def main():
    print_header("🚗 SMART PARKING SYSTEM - SETUP VERIFICATION")
    
    # Check Python version
    print("1. Python Environment")
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"  {Colors.GREEN}✓{Colors.END} Python {version}")
    
    # Check required files
    print("\n2. Required Files")
    files_ok = True
    required_files = [
        'Arduino_Firebase_config(servo gate + RFID + serial listener).ino',
        'Bridge_Updated.py',
        'BridgeCode_FIrebase_&_Gate(webcam OCR - Firebase auth check - entry push).py',
        'config.json',
        'smartparking.json',
        'Gate Node(shows plate on authorized entry).html',
        'UI(camera OCR + Slot Map + Records Table)/UI.html',
        'UI(camera OCR + Slot Map + Records Table)/UI.js',
        'UI(camera OCR + Slot Map + Records Table)/UI.css',
    ]
    
    for file in required_files:
        if not check_file(file):
            files_ok = False
    
    # Check configuration
    print("\n3. Configuration")
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print(f"  {Colors.GREEN}✓{Colors.END} config.json loaded")
        print(f"    - Arduino COM Port: {config['arduino']['com_port']}")
        print(f"    - Flask Port: {config['flask']['port']}")
    except Exception as e:
        print(f"  {Colors.RED}✗{Colors.END} config.json error: {e}")
        files_ok = False
    
    # Check Python packages
    print("\n4. Python Dependencies")
    packages = [
        ('Flask', 'flask'),
        ('Flask-CORS', 'flask_cors'),
        ('PySerial', 'serial'),
        ('OpenCV', 'cv2'),
        ('EasyOCR', 'easyocr'),
        ('Firebase Admin', 'firebase_admin'),
    ]
    
    packages_ok = True
    for display_name, import_name in packages:
        if not check_python_package(display_name, import_name):
            packages_ok = False
    
    if not packages_ok:
        print(f"\n  {Colors.YELLOW}Install missing packages:{Colors.END}")
        print(f"  pip install -r requirements.txt")
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    if files_ok and packages_ok:
        print(f"{Colors.GREEN}✅ System is ready to use!{Colors.END}\n")
        print("Next steps:")
        print("  1. Upload Arduino firmware:")
        print("     - Open Arduino IDE")
        print("     - Load: Arduino_Firebase_config(servo gate + RFID + serial listener).ino")
        print("     - Select your port and board")
        print("     - Click Upload")
        print("\n  2. Start the system:")
        print("     Windows: Double-click START_SYSTEM.bat")
        print("     Linux/Mac: python startup_manager.py")
        print("\n  3. Open dashboard:")
        print("     file:///[path]/UI(camera OCR + Slot Map + Records Table)/UI.html")
    else:
        print(f"{Colors.RED}❌ Setup incomplete!{Colors.END}\n")
        if not files_ok:
            print("Missing required files. Check file paths above.")
        if not packages_ok:
            print("Missing Python packages. Run: pip install -r requirements.txt")
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}\n")

if __name__ == '__main__':
    main()
