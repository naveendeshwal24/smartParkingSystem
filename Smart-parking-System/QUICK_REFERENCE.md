# ⚡ Quick Reference Guide

## 🚀 5-Minute Setup

### 1. Dependencies
```bash
pip install -r requirements.txt
```

### 2. Arduino Upload
- Open Arduino IDE
- Load: `Arduino_Firebase_config.ino`
- Select Port & Board
- Click Upload
- **Expect: 3 beeps + Serial message**

### 3. Start Services
```bash
# Windows: Double-click
START_SYSTEM.bat

# Or Linux/Mac:
python startup_manager.py
```

### 4. Open Dashboard
```
file:///[path]/Smart-parking-System/UI/UI.html
```

**✅ Done!** System is ready to use.

---

## 🔧 Common Tasks

### Find Arduino COM Port
```bash
python -c "import serial.tools.list_ports; [print(f'{p.device}: {p.description}') for p in serial.tools.list_ports.comports()]"
```

### Change COM Port
Edit `config.json`:
```json
"arduino": {
  "com_port": "COM5"  // Change this
}
```

### Install Missing Python Packages
```bash
pip install flask flask-cors pyserial opencv-python easyocr firebase-admin
```

### Test Flask Bridge
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "ok",
  "arduino_connected": true,
  "port": "COM4"
}
```

### Add Registered Vehicle
1. Open Firebase Console
2. Go to `registered_cars`
3. Add: Key = License Plate, Value = `true`
4. Example: `"MH12AB1234": true`

### Change Camera
Edit `config.json`:
```json
"camera": {
  "index": 0  // 0=default, 1=USB camera, 2=external cam
}
```

---

## ❌ Quick Fixes

| Problem | Solution |
|---------|----------|
| Arduino not connecting | Check USB cable, update COM port in config.json |
| No camera feed | Enable webcam access, verify camera index |
| Firebase sync not working | Check internet, verify credentials in smartparking.json |
| Port 5000 already in use | Change to different port in config.json |
| "No module named 'flask'" | Run: `pip install -r requirements.txt` |
| OCR not detecting plates | Ensure good lighting, position camera at 30-45° |

---

## 📊 File Checklist

```
Required Files:
✅ Arduino_Firebase_config.ino (upload to Arduino)
✅ Bridge_Updated.py (Flask server)
✅ BridgeCode_FIrebase_&_Gate.py (Camera scanner)
✅ config.json (Configuration)
✅ smartparking.json (Firebase credentials)
✅ UI/UI.html (Dashboard)
✅ UI/UI.js (Dashboard logic)
✅ UI/UI.css (Dashboard styling)
✅ Gate Node.html (Gate monitor)
✅ requirements.txt (Python packages)
```

---

## 🎯 Testing Steps

1. Upload Arduino firmware
2. Connect Arduino via USB
3. Verify 3 beeps + serial message
4. Start Bridge server: `python Bridge_Updated.py`
5. Check: `curl http://localhost:5000/health`
6. Open Dashboard in browser
7. Check camera feed appears
8. Verify Firebase data syncing
9. Test: Click payment button → gate should open

---

## 📞 Support

**Check Logs:**
- Bridge: Shows "Arduino Connected" and requests
- Scanner: Shows "Unauthorized/Authorized" detections
- Browser (F12): Shows any JavaScript errors
- Arduino Serial Monitor: Shows system messages

**Debug Mode:**
```json
{
  "flask": {"debug": true}
}
```

---

## 🔗 Useful Links

- Arduino IDE: https://www.arduino.cc/en/software
- Python: https://www.python.org/downloads
- Firebase Console: https://console.firebase.google.com
- EasyOCR: https://github.com/JaidedAI/EasyOCR

---

**Last Updated**: May 15, 2026
