"""
Smart Parking System - Unified Startup Manager
Starts all required services (Bridge, Scanner) in separate processes
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("\n" + "="*70)
    print("  🚗 SMART PARKING SYSTEM - UNIFIED STARTUP MANAGER")
    print("="*70)
    print(f"  Python: {sys.version}")
    print(f"  Working Directory: {os.getcwd()}")
    print("="*70 + "\n")

def check_files():
    """Check if required files exist"""
    required_files = [
        'Bridge_Updated.py',
        'BridgeCode_FIrebase_&_Gate(webcam OCR - Firebase auth check - entry push).py',
        'config.json',
        'smartparking.json',  # Firebase service account key
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print("❌ Missing required files:")
        for f in missing:
            print(f"   • {f}")
        return False
    
    print("✅ All required files found")
    return True

def start_bridge():
    """Start the Flask Bridge server"""
    print("\n[1/2] Starting Bridge (Flask Server)...")
    print("      Command: python Bridge_Updated.py")
    
    try:
        bridge_process = subprocess.Popen(
            [sys.executable, 'Bridge_Updated.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("      ✅ Bridge started (PID: {})".format(bridge_process.pid))
        return bridge_process
    except Exception as e:
        print(f"      ❌ Failed to start Bridge: {e}")
        return None

def start_scanner():
    """Start the Camera Scanner"""
    print("\n[2/2] Starting Camera Scanner (EasyOCR)...")
    scanner_file = 'BridgeCode_FIrebase_&_Gate(webcam OCR - Firebase auth check - entry push).py'
    print(f"      Command: python \"{scanner_file}\"")
    
    try:
        scanner_process = subprocess.Popen(
            [sys.executable, scanner_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("      ✅ Scanner started (PID: {})".format(scanner_process.pid))
        return scanner_process
    except Exception as e:
        print(f"      ❌ Failed to start Scanner: {e}")
        return None

def main():
    """Main startup routine"""
    print_banner()
    
    # Check prerequisites
    print("Checking prerequisites...")
    if not check_files():
        print("\n❌ Setup incomplete. Please ensure all files are present.")
        sys.exit(1)
    
    print("✅ All checks passed\n")
    
    # Start services
    bridge = start_bridge()
    time.sleep(3)  # Let bridge initialize
    scanner = start_scanner()
    
    print("\n" + "="*70)
    print("  ✅ SYSTEM STARTED SUCCESSFULLY")
    print("="*70)
    print("\n📡 Services Running:")
    print("   • Bridge:  http://localhost:5000")
    print("   • Scanner: Camera detection active")
    print("\n🌐 Open Dashboard:")
    print("   • UI Dashboard: file:///...}/UI(camera OCR + Slot Map + Records Table)/UI.html")
    print("   • Gate Node: Open Gate Node(shows plate on authorized entry).html")
    print("\n⚙️  Check Endpoints:")
    print("   • http://localhost:5000/health - System health")
    print("   • http://localhost:5000/config - Current config")
    print("   • http://localhost:5000/gate-status - Gate status")
    print("\n📋 To stop services:")
    print("   • Press Ctrl+C in each window, or")
    print("   • Close the command windows directly")
    print("="*70 + "\n")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
            
            # Check if processes are still alive
            if bridge and bridge.poll() is not None:
                print("⚠️  Bridge process stopped unexpectedly!")
            if scanner and scanner.poll() is not None:
                print("⚠️  Scanner process stopped unexpectedly!")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Shutting down...")
        if bridge:
            bridge.terminate()
            bridge.wait(timeout=5)
        if scanner:
            scanner.terminate()
            scanner.wait(timeout=5)
        print("✅ All services stopped\n")

if __name__ == '__main__':
    main()
