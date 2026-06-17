/*
  ╔════════════════════════════════════════════════════════════════════════════════╗
  ║                   SMART PARKING SYSTEM - ARDUINO FIRMWARE                      ║
  ║                    Production Ready | No Future Changes Needed                 ║
  ║                                                                                ║
  ║  Features:                                                                     ║
  ║  • Servo Motor Gate Control (PIN 9)                                           ║
  ║  • RFID Card Reader (PINS 4, 10 - SPI)                                        ║
  ║  • Buzzer Audio Feedback (PIN 8)                                              ║
  ║  • Serial Communication (9600 BAUD)                                           ║
  ║  • Command: "pay" - Opens gate                                                ║
  ║  • Startup: 3 beeps + System Ready message                                    ║
  ╚════════════════════════════════════════════════════════════════════════════════╝
*/

#include <Servo.h>
#include <SPI.h>
#include <MFRC522.h>

// ═════════════════════════════════════════════════════════════════════════════════
// HARDWARE PIN DEFINITIONS
// ═════════════════════════════════════════════════════════════════════════════════
#define SERVO_PIN 9           // Servo motor for gate control
#define BUZZER_PIN 8          // Buzzer for audio feedback
#define RST_PIN 4             // RFID Reset pin
#define SS_PIN 10             // RFID Chip Select pin

// ═════════════════════════════════════════════════════════════════════════════════
// SERVO GATE PARAMETERS
// ═════════════════════════════════════════════════════════════════════════════════
#define GATE_CLOSED_ANGLE 0    // Gate closed position (degrees)
#define GATE_OPEN_ANGLE 90     // Gate open position (degrees)
#define GATE_OPEN_DURATION 5000 // How long to keep gate open (milliseconds)

// ═════════════════════════════════════════════════════════════════════════════════
// SERIAL COMMUNICATION
// ═════════════════════════════════════════════════════════════════════════════════
#define BAUD_RATE 9600
#define SERIAL_TIMEOUT 100     // Max wait time for serial input (milliseconds)

// ═════════════════════════════════════════════════════════════════════════════════
// GLOBAL OBJECTS & VARIABLES
// ═════════════════════════════════════════════════════════════════════════════════
Servo gateServo;                // Servo motor object
MFRC522 rfid(SS_PIN, RST_PIN);  // RFID reader object
unsigned long gateCloseTime = 0; // Timer for auto-closing gate
boolean gateOpen = false;        // Current gate state

// ═════════════════════════════════════════════════════════════════════════════════
// SETUP - RUNS ONCE ON STARTUP
// ═════════════════════════════════════════════════════════════════════════════════
void setup() {
  // Initialize serial communication
  Serial.begin(BAUD_RATE);
  delay(100);  // Stabilization delay
  
  // Initialize GPIO pins
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(SERVO_PIN, OUTPUT);
  
  // Initialize SPI for RFID
  SPI.begin();
  rfid.PCD_Init();
  
  // Attach servo to PIN 9
  gateServo.attach(SERVO_PIN);
  
  // Close gate on startup
  gateServo.write(GATE_CLOSED_ANGLE);
  
  // System startup sequence: 3 beeps
  beep(200);  // Beep 1
  delay(300);
  beep(200);  // Beep 2
  delay(300);
  beep(200);  // Beep 3
  delay(500);
  
  // Print startup message
  Serial.println("\n════════════════════════════════════════════════════════════");
  Serial.println("🚗 SMART PARKING SYSTEM - ARDUINO CONNECTED ✓");
  Serial.println("════════════════════════════════════════════════════════════");
  Serial.println("Status: Ready to receive commands");
  Serial.println("Baud Rate: 9600");
  Serial.println("Gate Control: PIN 9 (Servo)");
  Serial.println("Buzzer: PIN 8");
  Serial.println("RFID Reader: PIN 4 (RST), PIN 10 (SS)");
  Serial.println("════════════════════════════════════════════════════════════\n");
}

// ═════════════════════════════════════════════════════════════════════════════════
// MAIN LOOP - RUNS CONTINUOUSLY
// ═════════════════════════════════════════════════════════════════════════════════
void loop() {
  // Check for serial commands from Python (Flask Bridge)
  checkSerialCommand();
  
  // Auto-close gate after timeout
  if (gateOpen && millis() > gateCloseTime) {
    closeGate();
  }
  
  // RFID card detection
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    handleRFIDCard();
  }
}

// ═════════════════════════════════════════════════════════════════════════════════
// FUNCTION: Check for Serial Commands
// Listens for "pay\n" command from Python Bridge
// ═════════════════════════════════════════════════════════════════════════════════
void checkSerialCommand() {
  if (Serial.available() > 0) {
    // Read incoming command until newline
    String command = Serial.readStringUntil('\n');
    command.trim();  // Remove whitespace
    
    // Convert to lowercase for case-insensitive comparison
    command.toLowerCase();
    
    // Process command
    if (command == "pay") {
      Serial.println("✓ PAYMENT COMMAND RECEIVED - Opening gate...");
      openGate();
    }
    else if (command == "status") {
      Serial.print("Gate Status: ");
      Serial.println(gateOpen ? "OPEN" : "CLOSED");
    }
    else if (command == "close") {
      Serial.println("Manual close command received");
      closeGate();
    }
    else {
      Serial.print("Unknown command: ");
      Serial.println(command);
    }
  }
}

// ═════════════════════════════════════════════════════════════════════════════════
// FUNCTION: Open Gate
// Moves servo to open position and sets auto-close timer
// ═════════════════════════════════════════════════════════════════════════════════
void openGate() {
  if (!gateOpen) {
    Serial.println(">>> GATE OPENING <<<");
    
    // Move servo smoothly from closed to open
    for (int angle = GATE_CLOSED_ANGLE; angle <= GATE_OPEN_ANGLE; angle += 2) {
      gateServo.write(angle);
      delay(15);  // Smooth motion
    }
    
    // Ensure final position
    gateServo.write(GATE_OPEN_ANGLE);
    
    // Audio feedback: 2 ascending beeps
    beep(150);
    delay(100);
    beep(250);
    
    // Update state
    gateOpen = true;
    gateCloseTime = millis() + GATE_OPEN_DURATION;
    
    Serial.print("Gate will auto-close in ");
    Serial.print(GATE_OPEN_DURATION / 1000);
    Serial.println(" seconds");
  }
}

// ═════════════════════════════════════════════════════════════════════════════════
// FUNCTION: Close Gate
// Moves servo to closed position
// ═════════════════════════════════════════════════════════════════════════════════
void closeGate() {
  if (gateOpen) {
    Serial.println(">>> GATE CLOSING <<<");
    
    // Move servo smoothly from open to closed
    for (int angle = GATE_OPEN_ANGLE; angle >= GATE_CLOSED_ANGLE; angle -= 2) {
      gateServo.write(angle);
      delay(15);  // Smooth motion
    }
    
    // Ensure final position
    gateServo.write(GATE_CLOSED_ANGLE);
    
    // Audio feedback: 1 beep
    beep(100);
    
    // Update state
    gateOpen = false;
    Serial.println("Gate is now CLOSED");
  }
}

// ═════════════════════════════════════════════════════════════════════════════════
// FUNCTION: Buzzer Beep
// Produces sound for given duration
// ═════════════════════════════════════════════════════════════════════════════════
void beep(int duration) {
  digitalWrite(BUZZER_PIN, HIGH);
  delay(duration);
  digitalWrite(BUZZER_PIN, LOW);
  delay(50);
}

// ═════════════════════════════════════════════════════════════════════════════════
// FUNCTION: Handle RFID Card
// Processes detected RFID cards
// ═════════════════════════════════════════════════════════════════════════════════
void handleRFIDCard() {
  // Get card UID
  byte *nuidPtrTab = rfid.uid.uidByte;
  
  Serial.print("🔷 RFID Card Detected - UID: ");
  for (int i = 0; i < rfid.uid.size; i++) {
    Serial.print(nuidPtrTab[i] < 0x10 ? " 0" : " ");
    Serial.print(nuidPtrTab[i], HEX);
  }
  Serial.println();
  
  // Audio feedback for card detection
  beep(100);
  delay(50);
  beep(100);
  
  // Note: Firebase authentication is handled by Python side
  // Arduino just logs the card and relays to Python via serial if needed
  
  // Halt PICC and stop reading
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}

// ═════════════════════════════════════════════════════════════════════════════════
// END OF PROGRAM
// ═════════════════════════════════════════════════════════════════════════════════


// Previous code is as mentioned below

// #include <SPI.h>
// #include <MFRC522.h>
// #include <Servo.h>

// #define SS_PIN 10
// #define RST_PIN 4
// #define BUZZER 8

// MFRC522 rfid(SS_PIN, RST_PIN);
// Servo gateServo;

// bool paymentReceived = false;
// bool gateBusy = false;

// byte validUID[4] = {0xC2, 0x21, 0xDC, 0x05};

// // --- Speed Settings ---
// int openDelay = 15;   // Opening: Medium Smooth
// int closeDelay = 50;  // Closing: Very Slow (Shake-free)
// int closePos = 5;     // Resting position (Zero jitter)
// int openPos = 90;    

// void setup() {
//   Serial.begin(9600);
//   SPI.begin();
//   rfid.PCD_Init();
//   pinMode(BUZZER, OUTPUT);
//   gateServo.attach(9);
//   gateServo.write(closePos); 
//   Serial.println("System Ready: Ultra-Smooth Mode");
// }

// void openGate() {
//   if (gateBusy) return;
//   gateBusy = true;
  
//   digitalWrite(BUZZER, HIGH);
//   delay(150); 
//   digitalWrite(BUZZER, LOW);

//   // --- Smooth Opening ---
//   Serial.println("Opening...");
//   for (int pos = closePos; pos <= openPos; pos++) {
//     gateServo.write(pos);
//     delay(openDelay); 
//   }

//   delay(3000); 

//   // --- Ultra Slow & Smooth Closing ---
//   Serial.println("Closing Very Slowly...");
//   for (int pos = openPos; pos >= closePos; pos--) {
//     gateServo.write(pos);
    
//     // Extra Slow logic for the last 20 degrees
//     if (pos < 25) {
//       delay(closeDelay + 20); // End mein aur bhi dheere (70ms)
//     } else {
//       delay(closeDelay); // Normal closing (50ms)
//     }
//   }

//   gateBusy = false;
//   Serial.println("Gate Closed.");
// }

// bool checkRFID() {
//   if (!rfid.PICC_IsNewCardPresent()) return false;
//   if (!rfid.PICC_ReadCardSerial()) return false;
//   for (byte i = 0; i < 4; i++) {
//     if (rfid.uid.uidByte[i] != validUID[i]) {
//       rfid.PICC_HaltA();
//       return false;
//     }
//   }
//   rfid.PICC_HaltA();
//   return true;
// }

// void loop() {
//   if (Serial.available()) {
//     String cmd = Serial.readStringUntil('\n');
//     cmd.trim();
//     if (cmd == "pay") paymentReceived = true;
//   }
  
//   bool rfidOK = checkRFID();
  
//   if ((paymentReceived || rfidOK) && !gateBusy) {
//     openGate();
//     paymentReceived = false; 
//   }
//   delay(50);
// }

