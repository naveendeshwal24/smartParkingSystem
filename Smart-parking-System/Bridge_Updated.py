"""
Smart Parking System - Bridge Controller
Connects to Arduino via Serial and provides Flask API for gate control
Handles payment commands and sends control signals to the gate
"""

from flask import Flask, jsonify
from flask_cors import CORS
import serial
import serial.tools.list_ports
import time
import winsound
import json
import os
from datetime import datetime

# ──────────────────────────────────────────────────────────────
# CONFIGURATION LOADER
# ──────────────────────────────────────────────────────────────
def load_config():
    """Load configuration from config.json"""
    config_path = 'config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        print("⚠️  config.json not found! Using default settings...")
        return {
            'arduino': {'com_port': 'COM4', 'baud_rate': 9600, 'timeout': 1, 'auto_detect': True},
            'flask': {'host': 'localhost', 'port': 5000, 'debug': False}
        }

config = load_config()
ARDUINO_CONFIG = config.get('arduino', {})
FLASK_CONFIG = config.get('flask', {})

# ──────────────────────────────────────────────────────────────
# ARDUINO COM PORT DETECTION
# ──────────────────────────────────────────────────────────────
def find_arduino_port():
    """
    Auto-detect Arduino COM port
    Returns COM port if found, otherwise returns configured port
    """
    ports = serial.tools.list_ports.comports()
    arduino_port = None
    
    print("\n📡 Available COM Ports:")
    for port in ports:
        print(f"   • {port.device} - {port.description}")
        # Look for Arduino (CH340, FTDI, or Arduino in description)
        if 'Arduino' in port.description or 'CH340' in port.description or 'FTDI' in port.description:
            arduino_port = port.device
            print(f"   ✓ Arduino detected on {arduino_port}")
    
    if arduino_port:
        return arduino_port
    else:
        return ARDUINO_CONFIG.get('com_port', 'COM4')

# ──────────────────────────────────────────────────────────────
# ARDUINO CONNECTION
# ──────────────────────────────────────────────────────────────
def connect_arduino():
    """
    Attempt to establish serial connection with Arduino
    Plays beep sound on successful connection
    """
    try:
        # Auto-detect or use configured port
        com_port = find_arduino_port() if ARDUINO_CONFIG.get('auto_detect', True) else ARDUINO_CONFIG.get('com_port', 'COM4')
        baud_rate = ARDUINO_CONFIG.get('baud_rate', 9600)
        timeout = ARDUINO_CONFIG.get('timeout', 1)
        
        print(f"\n🔌 Connecting to Arduino on {com_port} at {baud_rate} baud...")
        arduino = serial.Serial(com_port, baud_rate, timeout=timeout)
        
        # Wait for Arduino to initialize
        time.sleep(2)
        
        # Clear any buffered data
        arduino.flushInput()
        arduino.flushOutput()
        
        print("✅ Arduino Connected Successfully!")
        
        # Play connection confirmation beeps
        try:
            for i in range(3):
                winsound.Beep(1000, 200)  # 1000Hz for 200ms
                time.sleep(0.1)
        except:
            print("   (Audio beep skipped - running on non-Windows or audio unavailable)")
        
        return arduino
    
    except serial.SerialException as e:
        print(f"❌ Failed to connect Arduino: {e}")
        print("   Ensure Arduino is connected via USB and using correct COM port")
        print("   Check config.json for COM port settings")
        return None

# ──────────────────────────────────────────────────────────────
# FLASK APP INITIALIZATION
# ──────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

# Global Arduino connection
arduino = None

# ──────────────────────────────────────────────────────────────
# API ENDPOINTS
# ──────────────────────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    is_connected = arduino is not None and arduino.is_open
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "arduino_connected": is_connected,
        "port": ARDUINO_CONFIG.get('com_port', 'Unknown')
    }), 200

@app.route('/open-gate', methods=['GET'])
def open_gate():
    """
    Open the parking gate
    Sends 'pay' command to Arduino via serial
    """
    global arduino
    
    if arduino is None or not arduino.is_open:
        print("❌ [OPEN-GATE] Arduino not connected!")
        return jsonify({"status": "error", "message": "Arduino not connected"}), 500
    
    try:
        print(f"🚗 [OPEN-GATE] Opening gate... (Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        arduino.write(b'pay\n')
        
        # Play success beep
        try:
            winsound.Beep(1200, 150)
        except:
            pass
        
        return jsonify({
            "status": "success",
            "message": "Gate Opened",
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        print(f"❌ [OPEN-GATE] Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/gate-status', methods=['GET'])
def gate_status():
    """Get current gate/Arduino status"""
    is_connected = arduino is not None and arduino.is_open
    return jsonify({
        "gate_status": "connected" if is_connected else "disconnected",
        "arduino_port": ARDUINO_CONFIG.get('com_port', 'Unknown'),
        "baud_rate": ARDUINO_CONFIG.get('baud_rate', 9600),
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/config', methods=['GET'])
def get_config():
    """Get current configuration (public info only)"""
    return jsonify({
        "arduino_port": ARDUINO_CONFIG.get('com_port', 'Unknown'),
        "baud_rate": ARDUINO_CONFIG.get('baud_rate', 9600),
        "flask_port": FLASK_CONFIG.get('port', 5000),
        "auto_detect": ARDUINO_CONFIG.get('auto_detect', True)
    }), 200

# ──────────────────────────────────────────────────────────────
# STARTUP & SHUTDOWN
# ──────────────────────────────────────────────────────────────

def startup():
    """Initialize and start the bridge service"""
    global arduino
    
    print("\n" + "="*60)
    print("  🚗 SMART PARKING SYSTEM - BRIDGE CONTROLLER")
    print("="*60)
    print(f"  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Connect to Arduino
    arduino = connect_arduino()
    
    if arduino:
        print("\n✅ Bridge Ready!")
        print(f"   Flask Server: http://localhost:{FLASK_CONFIG.get('port', 5000)}")
        print("   Endpoints:")
        print("      • GET /health - Check system status")
        print("      • GET /open-gate - Open parking gate")
        print("      • GET /gate-status - Get gate status")
        print("      • GET /config - Get configuration\n")
    else:
        print("\n⚠️  Arduino not connected, but Flask server is running")
        print("   Reconnect Arduino and refresh to retry\n")

def shutdown():
    """Cleanup on shutdown"""
    global arduino
    if arduino and arduino.is_open:
        print("\n🔌 Closing Arduino connection...")
        arduino.close()
    print("👋 Bridge controller stopped\n")

# ──────────────────────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    try:
        startup()
        
        # Start Flask server
        flask_port = FLASK_CONFIG.get('port', 5000)
        app.run(
            host=FLASK_CONFIG.get('host', 'localhost'),
            port=flask_port,
            debug=FLASK_CONFIG.get('debug', False),
            use_reloader=False
        )
    
    except KeyboardInterrupt:
        print("\n⏹️  Bridge interrupted by user")
        shutdown()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        shutdown()
