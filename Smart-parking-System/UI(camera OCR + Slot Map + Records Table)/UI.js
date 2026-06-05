
  /* ── Firebase Initialization ──
     Connect to the project's Realtime Database using project credentials */
  const firebaseConfig = {
    apiKey: "AIzaSyCImmlGPsLIMyTGxpPjI7SC80wNCA9T-Ao",
    databaseURL: "https://smartparkingsystembyabhay-default-rtdb.firebaseio.com/",
    projectId: "smartparkingsystembyabhay",
  };

  if (!firebase.apps.length) firebase.initializeApp(firebaseConfig);  // Avoid re-initializing if already done
  const db = firebase.database();  // Database reference used for all reads/writes

  let stream = null;          // Holds the active camera MediaStream (used to stop tracks later)
  let occupiedSlots = new Set(); // Tracks which slot numbers are currently occupied

  const TOTAL_SLOTS = 20;  // Total parking capacity — used for slot assignment and stats

  /* ── Slot Map Renderer ──
     Clears and rebuilds all 20 slot cells based on current occupiedSlots set
     Called on page load and every time Firebase data updates */
  function renderSlots() {
    const grid = document.getElementById('slots-grid');
    grid.innerHTML = '';  // Clear previous render before rebuilding

    for (let i = 1; i <= TOTAL_SLOTS; i++) {
      const free = !occupiedSlots.has(i);  // True if slot not in occupied set
      const div = document.createElement('div');
      div.className = 'slot ' + (free ? 'free' : 'occupied');
      div.title = 'Slot ' + i + (free ? ' — Available' : ' — Occupied');
      // Parking icon for free slots, car icon for occupied slots
      div.innerHTML = `<i class="ti ${free ? 'ti-parking' : 'ti-car'}"></i>${i}`;
      grid.appendChild(div);
    }
  }
  renderSlots();  // Initial render — all slots free before Firebase data loads

  /* ── Status Updater ──     Updates the status pill text + color, and the camera overlay label
     type: 'blue' | 'green' | 'amber' | 'red' */
  function setStatus(msg, type) {
    const pill  = document.getElementById('status-pill');
    const text  = document.getElementById('status-text');
    const label = document.getElementById('cam-label');
    text.textContent = msg;
    pill.className = 'status-pill ' + type;  // Swaps color class dynamically
    // Update camera label text to match current state
    if (type === 'green')      label.textContent = 'PLATE REGISTERED';
    else if (type === 'amber') label.textContent = 'CHECK INPUT...';
    else if (type === 'red')   label.textContent = 'ERROR';
    else                       label.textContent = 'READY TO SCAN';
  }

  let processing = false;  // Guard flag — prevents multiple simultaneous OCR calls

  /* ── Camera Starter ──
     Requests camera access, pipes stream to <video>, then schedules first OCR scan
     Uses 'environment' facing mode to prefer rear camera on mobile devices */
  async function startCamera() {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
      document.getElementById('video').srcObject = stream;
      setStatus('Scanning for plate...', 'blue');
      processing = false;
      setTimeout(detectCar, 3000);  // Wait 3s for camera to stabilize before first scan
    } catch (e) {
      setStatus('Camera unavailable', 'red');  // Permission denied or no camera found
    }
  }

  /* ── OCR Plate Detector ──
     Captures a full frame from the video, applies greyscale+contrast, runs Tesseract OCR.
     Validates the result and registers if a real plate is found.
     Retries automatically every 2s if no valid plate is detected. */
//   async function detectCar() {
//     if (processing) return;  // Skip if a scan is already in progress
//     processing = true;
//     setStatus('Detecting plate...', 'blue');

//     const video = document.getElementById('video');
//     if (!video.videoWidth) {
//       // Video not ready yet — retry shortly
//       processing = false;
//       setTimeout(detectCar, 1500);
//       return;
//     }

//     // Capture full camera frame — 100% width and height for maximum scan coverage
//     const vw = video.videoWidth;
//     const vh = video.videoHeight;

//     const canvas = document.createElement('canvas');
//     canvas.width  = vw;
//     canvas.height = vh;
//     const ctx = canvas.getContext('2d');

//     // Draw entire video frame onto the canvas
//     ctx.drawImage(video, 0, 0, vw, vh);

//     // ── Greyscale + Contrast Enhancement ──
//     // Converts each pixel to greyscale and amplifies contrast
//     // Bright pixels get brighter, dark pixels get darker — improves OCR accuracy
//     const imgData = ctx.getImageData(0, 0, vw, vh);
//     const d = imgData.data;
//     for (let i = 0; i < d.length; i += 4) {
//       const grey = 0.299 * d[i] + 0.587 * d[i+1] + 0.114 * d[i+2];  // Luminance formula
//       const contrast = grey > 128
//         ? Math.min(255, grey * 1.4)   // Boost highlights
//         : Math.max(0,   grey * 0.6);  // Deepen shadows
//       d[i] = d[i+1] = d[i+2] = contrast;  // Apply greyscale+contrast to R, G, B channels
//     }
//     ctx.putImageData(imgData, 0, 0);  // Write processed pixels back to canvas

//     try {
//       // ── Tesseract OCR ──
//       // Restrict character set to alphanumeric only (no symbols/punctuation)
//       // Page segmentation mode 7: treat image as a single line of text (ideal for plates)
//     //   const result = await Tesseract.recognize(canvas.toDataURL('image/png'), 'eng', {
//     //     tessedit_char_whitelist: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
//     //     tessedit_pageseg_mode: '7'
//     //   });

//       // Clean OCR output — strip any non-alphanumeric characters, force uppercase
//       let plate = result.data.text.replace(/[^A-Z0-9]/gi, '').toUpperCase();

//       // ── Noise Rejection ──
//       // Discard result if it's too short (< 4 chars), too long (> 13 chars),
//       // or looks like repeated noise (e.g. "AAAA", "1111")
//       const isNoise = plate.length < 4 || plate.length > 13 || /^(.)\1{3,}$/.test(plate);

//       if (isNoise) {
//         setStatus('No plate found — retrying...', 'amber');
//         processing = false;
//         setTimeout(detectCar, 2000);  // Retry after 2 seconds
//         return;
//       }

//       // Valid plate found — stop camera and register the entry
//       setStatus('Plate detected: ' + plate, 'green');
//       document.getElementById('cam-label').textContent = 'PLATE DETECTED';
//       if (stream) stream.getTracks().forEach(t => t.stop());  // Release camera
//       await registerEntry(plate);

//     } catch (e) {
//       // Tesseract error — retry after delay
//       setStatus('Scan error — retrying...', 'amber');
//       processing = false;
//       setTimeout(detectCar, 2000);
//     }
//     processing = false;
//   }
/* =========================================================
   CAMERA DETECTION FUNCTION
   ========================================================= */

async function detectCar() {

  if (processing) return;

  processing = true;

  setStatus('Detecting plate...', 'blue');

  const video = document.getElementById('video');

  if (!video.videoWidth) {

    processing = false;

    setTimeout(detectCar, 1500);

    return;
  }

  const vw = video.videoWidth;
  const vh = video.videoHeight;

  const canvas = document.createElement('canvas');

  canvas.width = vw;
  canvas.height = vh;

  const ctx = canvas.getContext('2d');

  ctx.drawImage(video, 0, 0, vw, vh);


  // -------------------------------------------------------
  // IMAGE ENHANCEMENT FOR OCR
  // -------------------------------------------------------
  const imgData = ctx.getImageData(0, 0, vw, vh);

  const d = imgData.data;

  for (let i = 0; i < d.length; i += 4) {

    const grey =
      0.299 * d[i] +
      0.587 * d[i + 1] +
      0.114 * d[i + 2];

    const contrast = grey > 128
      ? Math.min(255, grey * 1.4)
      : Math.max(0, grey * 0.6);

    d[i] = d[i + 1] = d[i + 2] = contrast;
  }

  ctx.putImageData(imgData, 0, 0);


  try {

    // -------------------------------------------------------
    // OCR PROCESS
    // -------------------------------------------------------

    /*
    const result = await Tesseract.recognize(
      canvas.toDataURL('image/png'),
      'eng',
      {
        tessedit_char_whitelist:
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',

        tessedit_pageseg_mode: '7'
      }
    );
    */

    let plate = result.data.text
      .replace(/[^A-Z0-9]/gi, '')
      .toUpperCase();


    // -------------------------------------------------------
    // NOISE FILTER
    // -------------------------------------------------------
    const isNoise =
      plate.length < 4 ||
      plate.length > 13 ||
      /^(.)\1{3,}$/.test(plate);

    if (isNoise) {

      setStatus('No plate found — retrying...', 'amber');

      processing = false;

      setTimeout(detectCar, 2000);

      return;
    }


    // -------------------------------------------------------
    // VALID PLATE DETECTED
    // -------------------------------------------------------
    setStatus(`Plate detected: ${plate}`, 'green');

    document.getElementById('cam-label').textContent =
      'PLATE DETECTED';

    // Stop camera stream
    if (stream) {
      stream.getTracks().forEach(t => t.stop());
    }

    // Register entry / exit
    await registerEntry(plate);

  } catch (e) {

    setStatus('Scan error — retrying...', 'amber');

    processing = false;

    setTimeout(detectCar, 2000);
  }

  processing = false;
}

  /* ── Manual Registration Handler ──
     Validates the typed plate number, cleans it, then calls registerEntry()
     Acts as a reliable fallback when OCR cannot detect the plate automatically */
//   async function handleManualRegister() {
//     const input = document.getElementById('plateInput');
//     const btn   = document.getElementById('registerBtn');

//     // Remove non-alphanumeric chars and uppercase
//     const raw = input.value.trim().toUpperCase().replace(/[^A-Z0-9]/g, '');

//     if (raw.length < 4) {
//       setStatus('Enter a valid plate number', 'amber');
//       input.focus();
//       return;
//     }

//     btn.disabled = true;  // Prevent double-submit during async registration
//     setStatus('Registering...', 'blue');

//     await registerEntry(raw);

//     btn.disabled = false;
//     input.value = '';  // Clear input after successful registration
//   }


  // Enter key triggers registration — same as clicking the Register button
  
/* =========================================================
   MANUAL VEHICLE ENTRY
   ========================================================= */

async function handleManualRegister() {

  const input = document.getElementById('plateInput');

  const btn = document.getElementById('registerBtn');


  // -------------------------------------------------------
  // CLEAN INPUT
  // -------------------------------------------------------
  const raw = input.value
    .trim()
    .toUpperCase()
    .replace(/[^A-Z0-9]/g, '');


  // -------------------------------------------------------
  // VALIDATION
  // -------------------------------------------------------
  if (raw.length < 4) {

    setStatus('Enter a valid plate number', 'amber');

    input.focus();

    return;
  }


  // -------------------------------------------------------
  // PREVENT MULTIPLE CLICKS
  // -------------------------------------------------------
  btn.disabled = true;

  setStatus('Processing vehicle...', 'blue');


  // -------------------------------------------------------
  // REGISTER ENTRY / EXIT
  // -------------------------------------------------------
  await registerEntry(raw);


  // -------------------------------------------------------
  // RESET INPUT
  // -------------------------------------------------------
  btn.disabled = false;

  input.value = '';
}
  
  document.getElementById('plateInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') handleManualRegister();
  });

  // Auto-uppercase every character as the user types (visual feedback)
  document.getElementById('plateInput').addEventListener('input', function() {
    const pos = this.selectionStart;
    this.value = this.value.toUpperCase();
    this.setSelectionRange(pos, pos);  // Preserve cursor position after transform
  });

  /* =========================================================
   REGISTER VEHICLE ENTRY / EXIT
   ========================================================= */

async function registerEntry(plate) {

  // -------------------------------------------------------
  // STEP 1 : FETCH EXISTING VEHICLE RECORDS
  // -------------------------------------------------------
  const snap = await db.ref('parking/cars').once('value');

  let existingVehicle = null;
  let existingKey = null;

  const occupiedSlots = [];

  snap.forEach(car => {

    const data = car.val();

    // Store occupied slots only for active parked vehicles
    if (data.payment === 'Pending') {
      occupiedSlots.push(parseInt(data.slot));
    }

    // Check if same vehicle already exists with pending payment
    if (
      data.carNo === plate &&
      data.payment === 'Pending'
    ) {
      existingVehicle = data;
      existingKey = car.key;
    }
  });


  // -------------------------------------------------------
  // STEP 2 : VEHICLE ALREADY PARKED → PROCESS EXIT
  // -------------------------------------------------------
  if (existingVehicle) {

    // Update vehicle record as exited
    await db.ref(`parking/cars/${existingKey}`).update({
      payment: 'Completed',
      status: 'Exited',
      exitTime: Date.now()
    });

    setStatus(`Exit completed for ${plate}`, 'green');

    // Optional popup for exit
    showPopup(plate, existingVehicle.slot);

    return;
  }


  // -------------------------------------------------------
  // STEP 3 : FIND AVAILABLE SLOT
  // -------------------------------------------------------
  let slot = null;

  for (let i = 1; i <= TOTAL_SLOTS; i++) {

    if (!occupiedSlots.includes(i)) {
      slot = i;
      break;
    }
  }


  // -------------------------------------------------------
  // STEP 4 : REGISTER NEW ENTRY
  // -------------------------------------------------------
  if (slot) {

    await db.ref('parking/cars').push({

      // Vehicle Details
      carNo: plate,

      // Assigned Parking Slot
      slot: slot,

      // Entry Timestamp
      entryTime: Date.now(),

      // Default Status
      payment: 'Pending',
      status: 'Parked'
    });

    setStatus(`Entry registered for ${plate}`, 'green');

    // Success popup
    showPopup(plate, slot);

  } else {

    // Parking Full
      playBeep();                              // 🔔 alert beep
      setStatus('Parking is full!', 'red');
      showPopup(plate, null, 'full');   // ← show the modal too
  }
}
// -------------------------------------------------------
// HELPER : BEEP using Web Audio API (no external assets needed)
// -------------------------------------------------------
function playBeep() {
  const ctx = new (window.AudioContext || window.webkitAudioContext)();

  const oscillator = ctx.createOscillator();
  const gainNode   = ctx.createGain();

  oscillator.connect(gainNode);
  gainNode.connect(ctx.destination);

  oscillator.type      = 'square'; // harsh, attention-grabbing tone
  oscillator.frequency.setValueAtTime(880, ctx.currentTime); // 880 Hz

  gainNode.gain.setValueAtTime(1, ctx.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.6); // fade out after 0.6s

  oscillator.start(ctx.currentTime);
  oscillator.stop(ctx.currentTime + 0.6);
}


  

 function showPopup(plate, slot, type = 'entry') {

  const title    = document.getElementById('popup-title');
  const subtitle = document.getElementById('popup-subtitle');
  const icon     = document.getElementById('popup-icon');
  const carEl    = document.getElementById('carNumber');
  const slotEl   = document.getElementById('slotNumber');

if (type === 'full') {

  if (title)    title.textContent    = 'Parking Full';
  if (subtitle) subtitle.textContent = 'No slots available right now';
  if (icon)     setIconStyle(icon, 'icon-red', 'ti-x');
  carEl.textContent  = plate || '—';
  slotEl.textContent = 'N/A';

} else if (type === 'exit') {

  if (title)    title.textContent    = 'Exit Registered';
  if (subtitle) subtitle.textContent = 'Have a safe journey!';
  if (icon)     setIconStyle(icon, 'icon-blue', 'ti-logout');
  carEl.textContent  = plate;
  slotEl.textContent = slot;
  setStatus('Exit completed for ' + plate, 'green');

} else {

  if (title)    title.textContent    = 'Vehicle Registered';
  if (subtitle) subtitle.textContent = 'Slot assigned successfully';
  if (icon)     setIconStyle(icon, 'icon-green', 'ti-check');
  carEl.textContent  = plate;
  slotEl.textContent = slot;
  setStatus('Plate registered: ' + plate, 'green');
}

  document.getElementById('popup').classList.add('open');
}

// Helper to reset icon classes cleanly
function setIconStyle(icon, colorClass, iconClass) {
  icon.classList.remove('icon-red', 'icon-blue', 'icon-green');
  icon.classList.add(colorClass);
  icon.innerHTML = `<i class="ti ${iconClass}"></i>`;
}


  /* Closes the modal and restarts the camera scanner for the next vehicle */
  function closePopup() {
    document.getElementById('popup').classList.remove('open');  // Hide modal
    startCamera();  // Restart camera and begin scanning for next vehicle
  }

  /* ── Live Firebase Table Listener ──
     Subscribes to all records under "parking/cars" with real-time updates.
     Rebuilds the table, slot map, and stats counters on every data change. */
  db.ref('parking/cars').on('value', snap => {
    const occ = new Set();  // Rebuild occupied set fresh on each update
    let html = '';
    let count = 0;

    snap.forEach(c => {
      const d = c.val();
      if (d.payment === 'Pending') occ.add(parseInt(d.slot));  // Track occupied slots

      // Format entry timestamp as HH:MM — shows "—" if timestamp missing
      const time = d.entryTime
        ? new Date(d.entryTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        : '—';

      // Payment badge class — amber for pending, blue for paid
      const payClass = d.payment === 'Pending' ? 'pending' : 'paid';

      // Build table row HTML for this record
      html += `
        <tr>
          <td><span class="plate-chip"><i class="ti ti-car" style="font-size:13px;"></i>${d.carNo}</span></td>
          <td><span class="slot-chip"><i class="ti ti-parking" style="font-size:12px;"></i>${d.slot}</span></td>
          <td><span class="badge parked">${d.status}</span></td>
          <td><span class="badge ${payClass}">${d.payment}</span></td>
          <td class="time-text">${time}</td>
        
        </tr>`;
      count++;
    });

    // Update slot map and stat counters with latest Firebase data
    occupiedSlots = occ;
    renderSlots();

    document.getElementById('stat-total').textContent = TOTAL_SLOTS;
    document.getElementById('stat-free').textContent  = TOTAL_SLOTS - occ.size;
    document.getElementById('stat-occ').textContent   = occ.size;

    // Render rows or empty state if no records exist
    document.getElementById('carTable').innerHTML = count === 0
      ? `<tr><td colspan="5"><div class="empty-state"><i class="ti ti-car-off"></i><p>No vehicles parked yet</p></div></td></tr>`
      : html;
  });

  startCamera();  // Start camera and OCR scanner on page load
