import cv2          # OpenCV — used for capturing webcam frames and displaying the live feed window
import easyocr      # EasyOCR — deep learning OCR engine for reading text from images (more accurate than Tesseract for plates)
import firebase_admin                        # Firebase Admin SDK — server-side Firebase access
from firebase_admin import credentials, db  # credentials: loads service account key | db: Realtime Database interface
import time         # Standard library — used for timestamps and cooldown tracking

# ── Firebase Initialization ──
# Loads the service account key JSON file to authenticate as an admin (bypasses browser auth)
# This gives the script full read/write access to the Firebase Realtime Database
cred = credentials.Certificate("smartparking.json")

# Guard check — prevents re-initializing Firebase if the app is already running
# (Useful when this module is imported elsewhere or restarted in the same process)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smartparkingsystembyabhay-default-rtdb.firebaseio.com/'
    })

# ── EasyOCR Reader ──
# Initializes the OCR engine with English language support
# First run downloads the model (~100MB); subsequent runs load from cache
# GPU is auto-detected — if available, inference runs significantly faster
reader = easyocr.Reader(['en'])


def start_auto_scanning():
    # ── Camera Initialization ──
    # Opens the default webcam (index 0)
    # Change to 1, 2, etc. if using an external/USB camera
    cap = cv2.VideoCapture(0)
    #   print(" Scanner ON... .")

    # ── Cooldown Tracker ──
    # Dictionary mapping plate_number → last_detected_timestamp
    # Prevents the same plate from being registered multiple times
    # within a 10-second window (avoids duplicate Firebase entries)
    processed_plates = {}

    # ── Main Scanning Loop ──
    # Runs continuously, processing one frame at a time from the webcam
    while True:
        ret, frame = cap.read()  # ret: True if frame captured successfully | frame: raw BGR image array
        if not ret: break        # Exit loop if camera disconnects or fails to read

        # ── OCR Text Detection ──
        # Runs EasyOCR on the current frame
        # Returns a list of tuples: (bounding_box, detected_text, confidence_score)
        results = reader.readtext(frame)

        # Iterate over every text region detected in this frame
        for (bbox, text, prob) in results:
            # ── Plate Cleaning ──
            # Strip all non-alphanumeric characters (spaces, dashes, dots, etc.)
            # and convert to uppercase to normalize plate format (e.g. "MH-12 AB 1234" → "MH12AB1234")
            plate_no = "".join(e for e in text if e.isalnum()).upper()

            # ── Length Filter ──
            # Ignore short strings (single words, noise, stickers, signs)
            # Only process strings longer than 5 characters — likely a real plate
            if len(plate_no) > 5:
                curr_time = time.time()  # Current Unix timestamp in seconds (float)

                # ── Cooldown Check ──
                # Process this plate only if:
                #   1. It has never been seen before, OR
                #   2. It was last processed more than 10 seconds ago
                # This prevents spamming Firebase when a car sits in frame for multiple frames
                if plate_no not in processed_plates or (curr_time - processed_plates[plate_no] > 10):

                    # ── Firebase Authorization Check ──
                    # Look up this plate number in the "registered_cars" node
                    # Returns the stored value if the plate exists, or None if not registered
                    # Example DB structure: registered_cars/MH12AB1234 → true
                    is_reg = db.reference(f'registered_cars/{plate_no}').get()

                    if is_reg:
                        # ── Authorized Vehicle ──
                        # Plate found in registered_cars — push an entry record to Firebase
                        print(f"Authorized: {plate_no}")
                        db.reference('parking/cars').push({
                            'carNo'     : plate_no,              # Cleaned plate number
                            'entryTime' : int(curr_time * 1000), # Millisecond timestamp (matches JS Date.now() format)
                            'payment'   : 'Pending',             # Default payment state on entry
                            'status'    : 'AUTHORIZED'           # Marks this as a verified entry
                        })
                        # Record timestamp to start the 10-second cooldown for this plate
                        processed_plates[plate_no] = curr_time

                    else:
                        # ── Unauthorized Vehicle ──
                        # Plate not found in registered_cars — log and skip without writing to Firebase
                        print(f"Unauthorized: {plate_no}")
                        # Still record timestamp to prevent repeated "Unauthorized" log spam
                        processed_plates[plate_no] = curr_time

        # ── Live Preview Window ──
        # Displays the raw camera frame in a window so the operator can see what's being scanned
        # Runs in the background — does not block the OCR loop
        cv2.imshow('Python Scanner (Background)', frame)

        # ── Exit Condition ──
        # Press 'q' to cleanly stop the scanner
        # waitKey(1) waits 1ms per frame — keeps the display responsive without slowing OCR
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    # ── Cleanup ──
    # Release the webcam so other applications can use it
    cap.release()
    # Close the OpenCV preview window
    cv2.destroyAllWindows()


# ── Entry Point ──
# Only runs start_auto_scanning() when this file is executed directly
# If imported as a module by another script, this block is skipped
if __name__ == "__main__":
    start_auto_scanning()