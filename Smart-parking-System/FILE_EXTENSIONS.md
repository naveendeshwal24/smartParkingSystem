# 📂 File Extension Reference

## Project Files by Type & Extension

### 🤖 Arduino Firmware
```
Arduino_Firebase_config(servo gate + RFID + serial listener).ino
  └─ Extension: .ino (Arduino sketch)
  └─ Purpose: Microcontroller firmware for gate control
  └─ Upload: Via Arduino IDE
```

### 🐍 Python Backend Services
```
Bridge_Updated.py
  ├─ Extension: .py (Python 3.8+)
  ├─ Purpose: Flask API server for gate control
  ├─ Run: python Bridge_Updated.py
  └─ Port: 5000 (configurable)

BridgeCode_FIrebase_&_Gate(webcam OCR - Firebase auth check - entry push).py
  ├─ Extension: .py (Python 3.8+)
  ├─ Purpose: Camera scanner with ANPR
  ├─ Run: python "BridgeCode_Firebase_&_Gate(...).py"
  └─ Uses: OpenCV, EasyOCR, Firebase

startup_manager.py
  ├─ Extension: .py (Python 3.8+)
  ├─ Purpose: Start all services automatically
  ├─ Run: python startup_manager.py
  └─ Cross-platform: Windows, Linux, Mac

verify_setup.py
  ├─ Extension: .py (Python 3.8+)
  ├─ Purpose: Verify setup and dependencies
  ├─ Run: python verify_setup.py
  └─ Output: Check status of all components
```

### 🌐 Web Frontend
```
UI(camera OCR + Slot Map + Records Table)/UI.html
  ├─ Extension: .html (HyperText Markup Language)
  ├─ Purpose: Dashboard main structure
  ├─ Open: In modern web browser
  └─ Requires: JavaScript enabled

UI(camera OCR + Slot Map + Records Table)/UI.js
  ├─ Extension: .js (JavaScript ES6+)
  ├─ Purpose: Dashboard logic, Firebase sync, camera control
  ├─ Included: In UI.html via <script> tag
  └─ Framework: Vanilla JavaScript (no dependencies)

UI(camera OCR + Slot Map + Records Table)/UI.css
  ├─ Extension: .css (Cascading Style Sheets)
  ├─ Purpose: Dashboard styling and layout
  ├─ Included: In UI.html via <link> tag
  └─ Features: Dark theme, responsive design

Gate Node(shows plate on authorized entry).html
  ├─ Extension: .html (HyperText Markup Language)
  ├─ Purpose: Gate monitor display
  ├─ Open: In separate browser tab/window
  └─ Displays: Real-time vehicle plate info
```

### 📋 Configuration Files
```
config.json
  ├─ Extension: .json (JavaScript Object Notation)
  ├─ Purpose: System configuration (COM port, settings, etc.)
  ├─ Edit: With any text editor (VS Code, Notepad, etc.)
  ├─ Format: JSON (must be valid JSON syntax)
  └─ Changes: Take effect on service restart

smartparking.json
  ├─ Extension: .json (Firebase service account)
  ├─ Purpose: Firebase authentication credentials
  ├─ Edit: Never (download fresh from Firebase)
  ├─ Contains: Private service account key
  └─ Location: Keep in project root

requirements.txt
  ├─ Extension: .txt (Plain text)
  ├─ Purpose: Python package dependencies list
  ├─ Edit: Only if adding new packages
  ├─ Install: pip install -r requirements.txt
  └─ Format: package_name==version
```

### 📖 Documentation Files
```
README.md
  ├─ Extension: .md (Markdown)
  ├─ Purpose: Complete setup and usage guide
  ├─ View: GitHub, VS Code, any text editor
  ├─ Sections: 25+, covers all aspects
  └─ Read: Before starting setup

QUICK_REFERENCE.md
  ├─ Extension: .md (Markdown)
  ├─ Purpose: 5-minute quick start
  ├─ Covers: Essential commands and troubleshooting
  └─ Best for: Getting started quickly

SETUP_COMPLETE.md
  ├─ Extension: .md (Markdown)
  ├─ Purpose: What was done and next steps
  ├─ Contains: Summary of all changes
  └─ Read: Right after setup

TROUBLESHOOTING_GUIDE.md
  ├─ Extension: .md (Markdown)
  ├─ Purpose: Problem solutions
  ├─ Covers: 20+ common issues
  └─ Reference: When something doesn't work

FILE_EXTENSIONS.md
  ├─ Extension: .md (Markdown)
  ├─ Purpose: This file - extension reference
  └─ Lists: All files with their types
```

### 🎯 Startup Scripts
```
START_SYSTEM.bat
  ├─ Extension: .bat (Batch script)
  ├─ OS: Windows only
  ├─ Purpose: One-click startup for all services
  ├─ Usage: Double-click the file
  └─ Action: Opens Bridge & Scanner in new windows
```

### 📁 Directory Structure with Extensions

```
Smart-parking-System/
│
├── .ino files (Arduino sketches)
│   └── Arduino_Firebase_config(servo gate + RFID + serial listener).ino
│
├── .py files (Python scripts)
│   ├── Bridge_Updated.py
│   ├── BridgeCode_FIrebase_&_Gate(webcam OCR - Firebase auth check - entry push).py
│   ├── startup_manager.py
│   └── verify_setup.py
│
├── .html files (Web pages)
│   ├── Gate Node(shows plate on authorized entry).html
│   └── UI(camera OCR + Slot Map + Records Table)/
│       └── UI.html
│
├── .js files (JavaScript)
│   └── UI(camera OCR + Slot Map + Records Table)/
│       └── UI.js
│
├── .css files (Stylesheets)
│   └── UI(camera OCR + Slot Map + Records Table)/
│       └── UI.css
│
├── .json files (Configuration)
│   ├── config.json
│   └── smartparking.json
│
├── .txt files (Text)
│   └── requirements.txt
│
├── .md files (Markdown documentation)
│   ├── README.md
│   ├── QUICK_REFERENCE.md
│   ├── SETUP_COMPLETE.md
│   ├── TROUBLESHOOTING_GUIDE.md
│   └── FILE_EXTENSIONS.md (this file)
│
└── .bat files (Batch scripts - Windows)
    └── START_SYSTEM.bat
```

---

## 📊 File Count by Type

| Extension | Count | Purpose |
|-----------|-------|---------|
| `.ino` | 1 | Arduino firmware |
| `.py` | 4 | Python backends |
| `.html` | 2 | Web pages |
| `.js` | 1 | Dashboard logic |
| `.css` | 1 | Dashboard styling |
| `.json` | 2 | Configuration |
| `.txt` | 1 | Dependencies |
| `.md` | 5 | Documentation |
| `.bat` | 1 | Windows startup |
| **TOTAL** | **18** | **Complete system** |

---

## 🔄 File Dependencies & Relationships

```
Hardware Layer:
  Arduino_Firebase_config.ino
    ↓ (USB Serial)
  Bridge_Updated.py ← config.json (COM port, baud)
    ↓ (HTTP API)
  UI.html/UI.js ← UI.css (styling)
    ↓ (Firebase)
  Gate Node.html

Data Flow:
  BridgeCode_Firebase_&_Gate.py (camera detection)
    ↓ (push records)
  smartparking.json (Firebase auth)
    ↓ (read/write)
  Firebase Cloud Database
    ↓ (realtime sync)
  UI.html/UI.js & Gate Node.html (display)

Configuration Flow:
  config.json ← read by:
    - Bridge_Updated.py
    - startup_manager.py
    - verify_setup.py
    - BridgeCode_Firebase_&_Gate.py

Dependencies:
  requirements.txt ← install via:
    pip install -r requirements.txt
```

---

## ✅ Proper File Extensions for This Project

### Do NOT Change Extensions

❌ **WRONG**:
```
Arduino_Firebase_config.txt  (should be .ino)
Bridge_Updated.txt           (should be .py)
UI.txt                       (should be .html)
config.txt                   (should be .json)
```

✅ **CORRECT**:
```
Arduino_Firebase_config.ino
Bridge_Updated.py
UI.html
config.json
```

### Why Extensions Matter

- **`.ino`** → Arduino IDE recognizes as sketch
- **`.py`** → Python interprets as script
- **`.html`** → Browser renders as web page
- **`.js`** → Browser executes as JavaScript
- **`.css`** → Browser applies as stylesheet
- **`.json`** → Proper JSON parsing/validation
- **`.bat`** → Windows recognizes as batch script

---

## 🛠️ How to Edit Files by Type

### `.ino` (Arduino Code)
```
Edit in: Arduino IDE (recommended) or VS Code + Arduino extension
Compile: In Arduino IDE (Ctrl+R)
Upload: In Arduino IDE (Ctrl+U)
Don't open in: Notepad (loses formatting)
```

### `.py` (Python Scripts)
```
Edit in: VS Code, PyCharm, Notepad++, or any text editor
Run: Command line: python filename.py
Debug: Use print() statements
Dependencies: Managed in requirements.txt
```

### `.html` (Web Pages)
```
Edit in: VS Code, Notepad++, or any text editor
Open in: Web browser (Chrome, Firefox, Edge, Safari)
Debug: Press F12 for Developer Tools
Run: Double-click or drag into browser
```

### `.js` (JavaScript)
```
Edit in: VS Code, Notepad++, or any text editor
Debug: Browser Developer Tools (F12)
Must link: In .html file via <script> tag
Don't run: Directly from command line
```

### `.css` (Stylesheets)
```
Edit in: VS Code, Notepad++, or any text editor
Link: In .html file via <link> tag
Debug: Browser Inspector (F12 → Elements)
Changes: Reload page to see (Ctrl+R)
```

### `.json` (Configuration)
```
Edit in: VS Code, Notepad++, any text editor (not Word!)
Format: Must be valid JSON (use jsonlint.com to validate)
Syntax: Key: value, comma-separated, quoted strings
Read by: Python, JavaScript, config loaders
```

### `.bat` (Batch Scripts - Windows)
```
Edit in: Notepad, VS Code, Notepad++
Run: Double-click or: cmd > filename.bat
Syntax: Batch commands (set, echo, start, etc.)
Unix: Use .sh script instead
```

### `.md` (Markdown Documentation)
```
Edit in: Any text editor
View: GitHub, VS Code, any markdown viewer
Syntax: Markdown formatting (#, **, -, etc.)
Purpose: Documentation and guides
```

---

## 💾 File Management Tips

### Backup Important Files
```bash
# Before making changes
xcopy config.json config.json.backup
xcopy smartparking.json smartparking.json.backup

# Version control
git add .
git commit -m "Backup before changes"
```

### Check File Integrity
```python
import hashlib

def file_hash(filename):
    return hashlib.md5(open(filename, 'rb').read()).hexdigest()

print(file_hash('config.json'))  # Should not change
```

### Verify Syntax
```bash
# Python
python -m py_compile Bridge_Updated.py

# JSON
python -m json.tool config.json

# JavaScript
npm install -g eslint  # If using Node.js
eslint UI.js
```

---

## 🎓 Quick File Reference

**Need to:**
- Upload to Arduino? → Edit `.ino` file, use Arduino IDE
- Start backend? → Run `.py` files via terminal
- View dashboard? → Open `.html` in browser
- Fix styling? → Edit `.css` file, refresh browser
- Change settings? → Edit `config.json` file
- Install packages? → Run `pip install -r requirements.txt`
- Get help? → Read `.md` documentation files

---

**Last Updated**: May 15, 2026  
**Version**: 1.0  
**Status**: Complete File Reference
