# 🔧 Troubleshooting Guide - Smart Parking System

## 🎯 Problem-Solution Matrix

### Arduino Connection Issues

#### ❌ "Arduino not found" or "COM port not found"

**Symptoms:**
- Bridge shows: `Error: Arduino not found`
- No beeping sound when USB connected
- Serial Monitor shows: `SerialException`

**Solutions:**

1. **Check USB Cable**
   - Verify it's a DATA cable (not just power)
   - Try different USB ports
   - Try different computer if available

2. **Find Your COM Port**
   ```bash
   # Windows PowerShell
   [System.IO.Ports.SerialPort]::GetPortNames()
   
   # Or Python
   python -c "import serial.tools.list_ports; [print(p.device + ': ' + p.description) for p in serial.tools.list_ports.comports()]"
   ```

3. **Update config.json**
   ```json
   {
     "arduino": {
       "com_port": "COM5",  // Change to your port
       "auto_detect": false  // Disable auto-detect if issues
     }
   }
   ```

4. **Install Arduino Drivers** (If needed)
   - CH340 Driver: [ch340 driver download](https://sparks.gogo.co.nz/ch340.html)
   - FTDI Driver: [ftdi driver](https://ftdichip.com/drivers/)
   - Official Arduino: Built-in driver

5. **Reset Arduino**
   ```
   Press Reset button on Arduino board
   Wait 2 seconds
   Try connection again
   ```

6. **Check Device Manager** (Windows)
   - Device Manager → Ports (COM & LPT)
   - Should see "Arduino UNO" or "USB-SERIAL CH340"
   - If unknown device: install drivers

---

#### ❌ No Beep Sound on Connection

**Symptoms:**
- Arduino connects but no beeping
- Buzzer connected but silent

**Solutions:**

1. **Check Buzzer Wiring**
   ```
   Buzzer + (longer pin) → Arduino Pin 8
   Buzzer - (shorter pin) → Arduino GND
   ```

2. **Test Buzzer Manually** (Arduino Code)
   ```cpp
   void setup() {
     pinMode(8, OUTPUT);
     digitalWrite(8, HIGH);
     delay(500);
     digitalWrite(8, LOW);
   }
   void loop() {}
   ```

3. **Check Pin 8 isn't Used Elsewhere**
   - Verify no other connections to pin 8
   - Try different pin: Change `#define BUZZER 8` to another pin

4. **Check Buzzer Type**
   - Active Buzzer: Will beep with voltage
   - Passive Buzzer: Needs PWM signal (code already handles this)

5. **Test with Serial Monitor**
   ```
   Arduino IDE → Tools → Serial Monitor
   Should show: "ARDUINO CONNECTED ✓"
   If no message: Firmware upload issue
   ```

---

### Firmware Upload Issues

#### ❌ "Failed to upload" or "timeout" when uploading

**Symptoms:**
- Arduino IDE shows: `avrdude: stk500_recv(): timeout`
- Upload appears to freeze

**Solutions:**

1. **Select Correct Board**
   ```
   Tools → Board → Arduino AVR Boards → Arduino UNO
   (or your specific board type)
   ```

2. **Select Correct Port**
   ```
   Tools → Port → COM[X]
   Make sure it's the right one
   ```

3. **Reduce Upload Speed**
   ```
   Tools → Upload Speed → 115200 (or lower)
   ```

4. **Try Different USB Cable**
   - Current cable may be damaged
   - Try power-only cable is not acceptable

5. **Restart Arduino IDE**
   - Close completely
   - Unplug Arduino
   - Plug back in
   - Reopen IDE and retry

6. **Check Arduino Memory**
   - Verify sketch size is not too large
   - Should see: "Sketch uses X% of program storage"
   - Max ~32KB for UNO

---

### Flask Bridge Issues

#### ❌ "Port 5000 already in use"

**Symptoms:**
- Error: `Address already in use`
- Cannot start Flask server

**Solutions:**

1. **Change Port in config.json**
   ```json
   {
     "flask": {
       "port": 5001  // Change to unused port
     }
   }
   ```

2. **Kill Process Using Port**
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID [PID] /F
   
   # Linux/Mac
   lsof -i :5000
   kill -9 [PID]
   ```

3. **Check What's Using Port**
   ```bash
   # Windows
   netstat -ano | findstr LISTENING
   ```

---

#### ❌ "Flask server not responding"

**Symptoms:**
- `curl localhost:5000/health` → Connection refused
- Dashboard shows "Cannot connect to server"

**Solutions:**

1. **Verify Bridge is Running**
   ```bash
   # Should see output like:
   # ✅ Arduino Connected Successfully!
   # Flask Server: http://localhost:5000
   ```

2. **Check Port in Browser**
   ```
   http://localhost:5000/health
   http://127.0.0.1:5000/health
   ```

3. **Check Firewall**
   - Windows Defender Firewall might block Flask
   - Add Python to firewall exceptions
   - Or disable temporarily for testing

4. **Restart Bridge**
   ```bash
   python Bridge_Updated.py
   ```

---

### Camera & OCR Issues

#### ❌ "Camera unavailable" or "No camera found"

**Symptoms:**
- Dashboard shows: `Camera unavailable`
- No video feed appears

**Solutions:**

1. **Check Camera Permission**
   - Browser must have camera access
   - First load: Browser should prompt for permission
   - Allow access when prompted

2. **Check Camera Index in config.json**
   ```json
   {
     "camera": {
       "index": 0  // 0=default, try 1, 2 if first doesn't work
     }
   }
   ```

3. **Test Camera with OpenCV**
   ```python
   import cv2
   cap = cv2.VideoCapture(0)  # Try 0, 1, 2...
   ret, frame = cap.read()
   if ret:
       print("Camera works!")
   else:
       print("Camera not working")
   cap.release()
   ```

4. **Verify Webcam Works**
   - Windows: Camera app (should see preview)
   - Try different USB port
   - Try external webcam if available

5. **Check if Another App is Using Camera**
   - Close Skype, Teams, Zoom, etc.
   - These may lock the camera

---

#### ❌ "No plate found — retrying..." (Not detecting plates)

**Symptoms:**
- Camera works but OCR never detects plates
- Dashboard keeps showing "Detecting plate..."

**Solutions:**

1. **Improve Lighting**
   - Use bright white light on license plate
   - Avoid shadows on plate
   - Contrast should be high (dark numbers on light background)

2. **Adjust Camera Angle**
   - Position camera 30-45° to plate
   - Not perpendicular (won't read)
   - Distance: 1-3 meters

3. **Clean Camera Lens**
   - Dust or fingerprints reduce clarity
   - Use soft cloth to wipe

4. **Test with Sample Image**
   ```python
   import easyocr
   reader = easyocr.Reader(['en'])
   result = reader.readtext('path/to/plate/image.jpg')
   print(result)
   ```

5. **Lower Noise Filter Threshold** (in UI.js)
   ```javascript
   // Change minimum plate length
   if (plate.length < 4)  // Try changing 4 to 3
   ```

6. **Check Image Preprocessing** (in UI.js)
   ```javascript
   // Verify contrast enhancement is working
   // Look at canvas in F12 Developer Tools
   ```

---

### Firebase Connection Issues

#### ❌ "Firebase error" or "No data syncing"

**Symptoms:**
- Dashboard shows no data from Firebase
- Scanner doesn't push vehicle records
- Slot count not updating

**Solutions:**

1. **Verify Internet Connection**
   ```bash
   ping google.com  # Should respond
   ```

2. **Check Firebase Credentials**
   - Verify `smartparking.json` exists
   - Contains valid Firebase service account
   - Download fresh from Firebase Console if needed

3. **Verify Firebase URL in config.json**
   ```json
   {
     "firebase": {
       "database_url": "https://smartparkingsystembyabhay-default-rtdb.firebaseio.com/"
     }
   }
   ```

4. **Check Firebase Rules** (Console)
   ```json
   // Rules should allow reads/writes
   {
     "rules": {
       ".read": true,
       ".write": true
     }
   }
   ```

5. **Test Firebase Connection**
   ```python
   import firebase_admin
   from firebase_admin import credentials, db
   
   cred = credentials.Certificate("smartparking.json")
   firebase_admin.initialize_app(cred, {
       'databaseURL': 'https://smartparkingsystembyabhay-default-rtdb.firebaseio.com/'
   })
   
   data = db.reference('registered_cars').get()
   print(data)  # Should show registered plates
   ```

---

### Dashboard Issues

#### ❌ "Dashboard loads but appears broken" or "Styling missing"

**Symptoms:**
- Page loads but no colors/styling
- Layout broken
- Fonts wrong

**Solutions:**

1. **Clear Browser Cache**
   ```
   Chrome: Ctrl+Shift+Delete → Clear Browsing Data
   Firefox: Ctrl+Shift+Delete → Clear Recent History
   ```

2. **Hard Refresh**
   ```
   Chrome: Ctrl+Shift+R
   Firefox: Ctrl+Shift+R
   ```

3. **Check CSS File**
   - Verify `UI.css` exists in UI folder
   - Check path is correct in `UI.html`
   - File size should be > 1KB

4. **Open in Different Browser**
   - Try Chrome, Firefox, Edge
   - Some browsers have stricter security

5. **Check Browser Console** (F12)
   - Look for red error messages
   - May show missing file paths

---

#### ❌ "Dashboard stuck on 'Scanning for plate...'"

**Symptoms:**
- Page loads but never progresses
- Status always shows scanning

**Solutions:**

1. **Check Bridge Connection**
   ```bash
   curl http://localhost:5000/health
   # Should return JSON, not error
   ```

2. **Check Firebase Connection**
   - Go to Firebase Console
   - Should see data being written
   - If not: Firebase connection broken

3. **Check Browser Console** (F12)
   - Errors might show what's wrong
   - Check Network tab for failed requests

4. **Restart All Services**
   ```bash
   # Stop Bridge (Ctrl+C)
   # Stop Scanner (Ctrl+C)
   # Restart both
   ```

5. **Reset Dashboard**
   - Close all browser tabs
   - Clear cache (Ctrl+Shift+Delete)
   - Reopen dashboard
   - Refresh (Ctrl+R)

---

### Python Package Issues

#### ❌ "ModuleNotFoundError: No module named 'flask'"

**Symptoms:**
- When running Bridge or Scanner: `ModuleNotFoundError`

**Solutions:**

1. **Install All Requirements**
   ```bash
   pip install -r requirements.txt
   ```

2. **Use Correct Python**
   ```bash
   # Make sure you're using Python 3.8+
   python --version
   
   # If multiple Python versions:
   python3 --version
   
   # Use python3 if needed:
   python3 -m pip install -r requirements.txt
   ```

3. **Check Virtual Environment**
   - If using venv: Activate it first
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install Individual Package**
   ```bash
   pip install flask
   pip install flask-cors
   pip install pyserial
   # etc...
   ```

5. **Verify Installation**
   ```bash
   python -c "import flask; print(flask.__version__)"
   ```

---

### Servo/Gate Issues

#### ❌ Servo not responding or gate not opening

**Symptoms:**
- Payment button clicked but gate doesn't open
- Servo doesn't move
- No error messages

**Solutions:**

1. **Check Servo Wiring**
   ```
   Servo Signal (Orange) → Arduino Pin 9
   Servo Power (Red)     → Arduino 5V
   Servo Ground (Brown)  → Arduino GND
   ```

2. **Test Servo with Arduino Code**
   ```cpp
   #include <Servo.h>
   Servo myservo;
   
   void setup() {
     myservo.attach(9);
     myservo.write(90);  // Test full open
   }
   
   void loop() {
     delay(1000);
     myservo.write(5);   // Close
     delay(1000);
     myservo.write(90);  // Open
   }
   ```

3. **Check 5V Power Supply**
   - Servo needs stable 5V
   - Arduino's 5V might not provide enough current
   - Use external power supply if servo stutters

4. **Verify Arduino Receives "pay" Command**
   - Open Serial Monitor at 9600 baud
   - Click payment button
   - Should see "Opening..." in Serial Monitor

5. **Check Gate-Open API Response**
   ```bash
   curl http://localhost:5000/open-gate
   # Should return: {"status": "success"}
   ```

---

## 🧪 General Debugging Steps

### Step 1: Check All Console Outputs
```
✅ Bridge console: Should show connection message
✅ Scanner console: Should show plate detections
✅ Arduino Serial Monitor: Should show system ready
✅ Browser F12 Console: Should show no red errors
```

### Step 2: Verify API Endpoints
```bash
# Health check
curl http://localhost:5000/health

# Should return something like:
# {"status": "ok", "arduino_connected": true}
```

### Step 3: Check Firebase Console
```
1. Open https://console.firebase.google.com
2. Select your project
3. Go to Realtime Database
4. Should see "parking/cars" and "registered_cars" nodes
5. Check if data is being written
```

### Step 4: Run Setup Verification
```bash
python verify_setup.py
```

---

## 📞 Still Not Working?

### Collect Information:

1. **Error Message** - Copy exact error text
2. **Console Logs** - Screenshot or copy Bridge/Scanner output
3. **Connections** - List what IS working
4. **Hardware** - What Arduino type, what camera
5. **File Paths** - Verify project location

### Create Debug Report:

```bash
# Collect system info
python verify_setup.py > debug_report.txt

# Add error details manually
# Share debug_report.txt with support
```

### Common Fixes in Order:

1. ✅ Restart Arduino (press Reset button)
2. ✅ Restart Bridge (Ctrl+C, run again)
3. ✅ Restart Scanner (Ctrl+C, run again)
4. ✅ Clear browser cache (Ctrl+Shift+Delete)
5. ✅ Restart computer (if all else fails)

---

**Last Updated**: May 15, 2026
**Covers**: All known issues and solutions
**Version**: 1.0
