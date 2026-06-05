# 🚗 Smart Parking System - Setup & Usage Guide

## 📋 System Overview

The Smart Parking System is an **Automated Number Plate Recognition (ANPR)** system that:
- **Detects** vehicle license plates via webcam
- **Authenticates** registered vehicles via Firebase
- **Controls** automated gate entry/exit
- **Tracks** parking occupancy in real-time

---

## 🔧 Hardware Requirements

### Arduino Setup
- **Arduino Board**: UNO, MEGA, or compatible
- **RFID Module**: MFRC522
- **Servo Motor**: Standard 5V servo (SG90 or equivalent)
- **Buzzer**: Passive buzzer (5V)
- **USB Cable**: For Arduino connection to computer

### Camera & Sensors
- **Webcam**: 1080p minimum (USB connection)
- **RFID Card**: For testing

### Connections
```
Arduino Pin Layout:
├── Pin 4  → RST_PIN (RFID Reset)
├── Pin 8  → BUZZER (Audio feedback)
├── Pin 9  → SERVO (Gate control)
├── Pin 10 → SS_PIN (RFID Chip Select)
├── Pin 11 → SPI MOSI
├── Pin 12 → SPI MISO
└── Pin 13 → SPI SCK
```

---

## 💻 Software Requirements

### Prerequisites
- **Python 3.8+** (from [python.org](https://www.python.org))
- **Arduino IDE** (from [arduino.cc](https://www.arduino.cc))

### Python Packages
```bash
pip install flask flask-cors pyserial opencv-python easyocr firebase-admin
```

### Arduino Libraries
Install via Arduino IDE → Library Manager:
- MFRC522 (GithubCommunity by miguelbalboa)
- Servo (Built-in)
- SPI (Built-in)

---

## 📦 Project Structure

```
Smart-parking-System/
├── Arduino_Firebase_config.ino              # Arduino firmware
├── Bridge_Updated.py                        # Flask API server (gate control)
├── BridgeCode_Firebase_&_Gate.py            # Camera scanner (ANPR)
├── startup_manager.py                       # Python startup script
├── START_SYSTEM.bat                         # Batch startup script (Windows)
├── config.json                              # System configuration
├── smartparking.json                        # Firebase credentials
├── Gate Node.html                           # Gate monitor display
└── UI/
    ├── UI.html                              # Main dashboard
    ├── UI.js                                # Dashboard logic
    └── UI.css                               # Dashboard styling
```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Upload Arduino Firmware

1. **Open Arduino IDE**
2. **File** → **Open** → Select `Arduino_Firebase_config.ino`
3. **Select Board**: Tools → Board → Arduino UNO (or your board)
4. **Select Port**: Tools → Port → COM4 (or your Arduino's port)
5. **Upload**: Click Upload button (Ctrl+U)
6. ✅ Watch for "Uploading..." and "Done uploading"

**🔊 Expected Behavior:**
- Arduino automatically **beeps 3 times** on startup
- Serial Monitor shows: `🚗 SMART PARKING SYSTEM - ARDUINO CONNECTED ✓`

### Step 2: Start the Backend Services

#### Option A: Windows Batch (Easiest)
```bash
Double-click: START_SYSTEM.bat
```

#### Option B: Command Line
```bash
# Terminal 1 - Start Bridge (Flask server)
python Bridge_Updated.py

# Terminal 2 - Start Scanner (Camera detection)
python "BridgeCode_FIrebase_&_Gate(webcam OCR - Firebase auth check - entry push).py"
```

#### Option C: Python Manager
```bash
python startup_manager.py
```

**🔊 Expected Behavior:**
- Bridge shows: `✅ Arduino Connected Successfully!` + beep sound
- Bridge displays: `Flask Server: http://localhost:5000`
- Scanner shows: `Scanner ON...`

### Step 3: Open Dashboard

1. **Main Dashboard**: Open `UI/UI.html` in browser
   - Or navigate to: `file:///C:/.../Smart-parking-System/UI/UI.html`
   
2. **Gate Monitor**: Open `Gate Node.html` in another tab
   - Shows real-time plate detection

---

## 🎯 Data Flow & How It Works

### Entry Process
```
1. Vehicle Approaches Gate
2. Webcam captures frame
3. Scanner runs EasyOCR to detect plate
4. Check Firebase: Is plate registered?
   ├─ YES → Push entry to Firebase + Send "pay" command to Arduino
   └─ NO  → Log unauthorized, don't open
5. Arduino receives "pay" → Opens gate (servo moves, beeps)
6. Gate Node.html displays plate info in real-time
```

### Exit Process
```
1. User clicks "PAYMENT CONFIRMED" in Dashboard
2. Dashboard sends HTTP GET → http://localhost:5000/open-gate
3. Bridge receives request → Sends "pay\n" to Arduino
4. Arduino opens gate
5. Firebase records exit timestamp
6. Dashboard updates occupied slots
```

### Real-time Sync
- All devices listen to Firebase
- When one vehicle record changes:
  - Dashboard updates slot count
  - Gate Node updates status
  - Automatic refresh across all tabs

---

## 📡 API Endpoints (Flask Bridge)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check system status |
| `/open-gate` | GET | Open parking gate |
| `/gate-status` | GET | Get current gate status |
| `/config` | GET | Get system configuration |

**Example Requests:**
```bash
# Check if system is running
curl http://localhost:5000/health

# Open the gate (from payment system)
curl http://localhost:5000/open-gate

# Check gate connectivity
curl http://localhost:5000/gate-status
```

---

## ⚙️ Configuration (config.json)

Edit `config.json` to customize:

```json
{
  "arduino": {
    "com_port": "COM4",           // Change if using different port
    "baud_rate": 9600,            // Match Arduino Serial.begin()
    "timeout": 1,
    "auto_detect": true           // Auto-find Arduino
  },
  "flask": {
    "host": "localhost",
    "port": 5000,                 // Change if port conflicts
    "debug": false
  },
  "camera": {
    "index": 0,                   // 0 = default camera, 1 = USB camera
    "resolution": [1280, 720]
  }
}
```

---

## 🐛 Troubleshooting

### Arduino Not Connecting
**Problem**: "Arduino not found"
- ✅ Check USB cable is properly connected
- ✅ Check COM port: Device Manager → Ports → Find Arduino
- ✅ Update `config.json` with correct COM port
- ✅ Install CH340 driver if using clone Arduino

**Command to find port:**
```bash
python -c "import serial.tools.list_ports; [print(p) for p in serial.tools.list_ports.comports()]"
```

### Camera Not Detecting Plates
**Problem**: "No plate found — retrying..."
- ✅ Ensure adequate lighting (OCR requires clear images)
- ✅ Position camera at 30-45° angle to plate
- ✅ Verify camera is working: `python -c "import cv2; c = cv2.VideoCapture(0); print(c.isOpened())"`
- ✅ Try changing camera index in `config.json` (0, 1, 2, etc.)

### Firebase Connection Issues
**Problem**: "Firebase error" or no data syncing
- ✅ Verify `smartparking.json` is in project directory
- ✅ Check internet connection
- ✅ Verify Firebase database URL in `config.json`
- ✅ Check Firebase security rules allow reads/writes

### Port Already in Use
**Problem**: "Address already in use" on port 5000
- ✅ Change port in `config.json`: `"port": 5001`
- ✅ Or kill process using port:
  ```bash
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F
  ```

### Serial Communication Errors
**Problem**: Arduino disconnects randomly
- ✅ Check USB cable (not a data-only cable)
- ✅ Reduce baud rate: change to 9600 in both Arduino sketch and config
- ✅ Add 2-second delay after Serial.begin() (already added)

---

## 📊 Firebase Database Structure

```
smartparkingsystembyabhay/
├── registered_cars/
│   ├── "MH12AB1234": true
│   ├── "KA01CD5678": true
│   └── (Add your authorized plates here)
│
└── parking/cars/
    └── {auto-generated-key}:
        ├── carNo: "MH12AB1234"
        ├── entryTime: 1715784000000
        ├── payment: "Pending"
        └── status: "AUTHORIZED"
```

**Add Registered Car:**
1. Open Firebase Console
2. Click `registered_cars` node
3. Click `+` to add new entry
4. Key: License plate (e.g., "MH12AB1234")
5. Value: `true`

---

## 🔐 Security Notes

- **Firebase Key**: Keep `smartparking.json` private (not in public repos)
- **COM Port**: Default COM4 - verify before production
- **Authorized Vehicles**: Manage in Firebase console
- **RFID UID**: Change `validUID` in Arduino code for your card

---

## 📱 Testing Checklist

- [ ] Arduino firmware uploaded (check beep on startup)
- [ ] Serial connection established (check Bridge console)
- [ ] Dashboard loads without errors
- [ ] Camera feed appears in dashboard
- [ ] Firebase connection working
- [ ] Test plate detection (hold sign to camera)
- [ ] Payment button triggers gate open
- [ ] Gate Node displays detected plates
- [ ] Slot count updates correctly
- [ ] All endpoints responding (use curl)

---

## 🆘 Getting Help

**Check Logs:**
- Bridge console: Shows HTTP requests and Arduino commands
- Scanner console: Shows plate detections and Firebase pushes
- Browser console (F12): Shows JavaScript errors
- Arduino Serial Monitor: Shows Arduino debug messages

**Debug Mode:**
```bash
# Set debug in config.json
"flask": {"debug": true}

# Then check http://localhost:5000/config
```

---

## 📝 License & Credits

**Smart Parking System v1.0**
- ANPR Engine: EasyOCR
- Backend: Flask, Firebase
- Hardware: Arduino
- Frontend: HTML/CSS/JavaScript

---

## 🎯 Next Steps

1. ✅ **Customize**: Update registered vehicles in Firebase
2. ✅ **Deploy**: Set up on a Raspberry Pi for 24/7 operation
3. ✅ **Integrate**: Connect to your payment gateway
4. ✅ **Monitor**: Set up alerts for unauthorized vehicles

---

**Last Updated**: May 15, 2026
**Version**: 1.0
