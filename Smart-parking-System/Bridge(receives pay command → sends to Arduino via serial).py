from flask import Flask, jsonify  # Flask: web framework to create the API server | jsonify: converts Python dicts to JSON HTTP responses
from flask_cors import CORS        # CORS: allows cross-origin requests — lets the browser-based HTML dashboard call this local API
import serial                      # PySerial — handles serial (USB) communication between Python and the Arduino
import time                        # Standard library — used for the startup delay after opening the serial port
import winsound                    # Windows built-in — used to play a beep sound when Arduino connects successfully

# ── Flask App Initialization ──
# Creates the Flask web server instance
# This server acts as a bridge between the web dashboard and the physical Arduino gate
app = Flask(__name__)

# ── CORS Configuration ──
# Enables Cross-Origin Resource Sharing for all routes
# Without this, the browser blocks requests from the HTML dashboard (different origin)
# to this local Flask server (localhost:5000) — a security restriction called CORS policy
CORS(app)

# ── Arduino Serial Connection ──
# Attempts to open a serial connection to the Arduino on startup
# Wrapped in try/except so the server still starts even if Arduino is unplugged
try:
    # Connect to Arduino on COM10 at 9600 baud rate — must match Serial.begin(9600) in the Arduino sketch
    # timeout=1 means serial read calls wait max 1 second before giving up (prevents indefinite blocking)
    arduino = serial.Serial('COM10', 9600, timeout=1)

    # 2-second delay — required after opening serial port
    # Arduino resets itself when a new serial connection is established
    # Without this delay, any command sent immediately gets lost during the reset
    time.sleep(2)

    print("Arduino Connected!")

    # ── Connection Beep ──
    # Plays a short beep to give audio confirmation that Arduino is connected
    # winsound.Beep(frequency_in_hz, duration_in_ms)
    # 1000 Hz = clean mid-range tone | 300 ms = short, non-intrusive beep
    # Only runs on Windows — winsound is a Windows built-in module
    winsound.Beep(1000, 300)

except Exception as e:
    # Connection failed — Arduino may be on a different COM port, unplugged, or port is in use
    # Server continues running without Arduino; gate commands will return 500 error instead
    print(f" Error: {e}")


# ── Gate Open API Endpoint ──
# GET /open-gate — called by the HTML dashboard when payment is confirmed
# Sends the "pay\n" command to Arduino over serial, which triggers the gate to open
@app.route('/open-gate')
def open_gate():

    # ── Arduino Availability Check ──
    # 'arduino' in globals()  → confirms the serial object was created (connection didn't fail at startup)
    # arduino.is_open         → confirms the port is still actively open (not closed/disconnected mid-session)
    if 'arduino' in globals() and arduino.is_open:

        # Send "pay\n" as bytes to Arduino over USB serial
        # The Arduino's loop() reads this via Serial.readStringUntil('\n')
        # When it receives "pay", it sets paymentReceived = true and opens the gate
        arduino.write(b'pay\n')

        # Return success response to the dashboard — HTTP 200 OK
        return jsonify({"status": "Gate Opened"}), 200

    # Arduino not connected or port closed — return error response to dashboard
    # HTTP 500 indicates a server-side/hardware failure
    return jsonify({"status": "Arduino not found"}), 500


# ── Entry Point ──
# Starts the Flask development server on port 5000
# The HTML dashboard calls http://localhost:5000/open-gate to trigger the gate
# Only runs when this file is executed directly — skipped if imported as a module
if __name__ == '__main__':
    app.run(port=5000)