/* SignBridge Application*/

//mobile nav
function toggleMenu() {
  const nav = document.getElementById('navLinks');
  if (nav) nav.classList.toggle('open');
}

//Helper functions
//Generates a random room code (eg: ABC-1234)
function generateRoomCode() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let code = '';
  for (let i = 0; i < 3; i++) code += chars[Math.floor(Math.random() * chars.length)];
  code += '-';
  for (let i = 0; i < 4; i++) code += chars[Math.floor(Math.random() * chars.length)];
  return code;
}

//Gets the URL parameter by key
function getParam(key) {
  return new URLSearchParams(window.location.search).get(key);
}

//Goes back or to the landing page
function goBack() {
  if (window.history.length > 1) {
    window.history.back();
  } else {
    window.location.href = '/landing';
  }
}

//Home page
//Joins existing room
function joinRoom() {
  const name = document.getElementById('userName')?.value.trim();
  const room = document.getElementById('roomCode')?.value.trim();

  if (!name) return alert('Please enter your name.');
  if (!room) return alert('Please enter a room code.');

  window.location.href = `/waiting?name=${encodeURIComponent(name)}&room=${encodeURIComponent(room)}`;
}

//Creates new session (calls backend)
async function createSession() {
    const name = document.getElementById('userName')?.value.trim() || 'Guest';

    try {
        const res = await fetch('/create-room', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: name })
        });

        if (res.status === 429) { // Handle rate limiting response for too many room creation attempts
            alert("Too many room creation attempts. Please wait 1 minute and try again.");
            return;
        }

        const data = await res.json();

        if (!data.success) {
            alert(data.message || 'Failed to create room');
            return;
        }

        const room = data.room_code;
        window.location.href = `/waiting?name=${encodeURIComponent(name)}&room=${encodeURIComponent(room)}`;
    } catch (err) {
        console.error(err);
    }
}

//Waiting room
//Displays the room code on the waiting page
function initWaitingRoom() {
  const roomEl = document.getElementById('waitRoomCode');
  const nameEl = document.getElementById('userNameDisplay');

  const room = getParam('room') || 'N/A';
  const name = getParam('name') || 'Guest';

  if (roomEl) roomEl.textContent = room;
  if (nameEl) nameEl.textContent = name;
}

//Joins the call from the waiting room
function joinCall() {
  const room = getParam('room') || 'ABC-1234';
  const name = getParam('name') || 'Guest';
  window.location.href = `/call?name=${encodeURIComponent(name)}&room=${encodeURIComponent(room)}`;
}

//Call page
let recognitionActive = false;  // Tracks if recognition is running

//Sets the room code on the call page
function initCallPage() {
  const roomEl = document.getElementById('callRoomCode');
  const room = getParam('room') || 'N/A';
  if (roomEl) roomEl.textContent = room;
}

//Starts the sign language recognition
function startRecognition() {
  const btnStart = document.getElementById('btnStartRecog');
  const btnStop = document.getElementById('btnStopRecog');
  const statusEl = document.getElementById('recognitionStatus');
  const letterEl = document.getElementById('detectedLetter');
  const transcriptBox = document.getElementById('transcriptBox');

  if (recognitionActive) return;

  // Update button states
  if (btnStart) btnStart.disabled = true;
  if (btnStop) btnStop.disabled = false;
  if (statusEl) statusEl.textContent = 'Ready for recognition...';
  
  // Clear placeholder text in transcript
  if (transcriptBox && transcriptBox.querySelector('span')) {
    transcriptBox.innerHTML = '';
  }

  recognitionActive = true;
  
  // Placeholder the actual logic will go here
  if (letterEl) letterEl.textContent = '?';
  if (transcriptBox && transcriptBox.innerHTML === '') {
    transcriptBox.innerHTML = '<span style="color:#aaa;font-style:italic;">Waiting for sign language input...</span>';
  }
}

//Stops the sign language recognition
function stopRecognition() {
  const btnStart = document.getElementById('btnStartRecog');
  const btnStop = document.getElementById('btnStopRecog');
  const statusEl = document.getElementById('recognitionStatus');
  const letterEl = document.getElementById('detectedLetter');

  recognitionActive = false;

  //Reset button states
  if (btnStart) btnStart.disabled = false;
  if (btnStop) btnStop.disabled = true;
  if (statusEl) statusEl.textContent = 'No hand detected';
  if (letterEl) letterEl.textContent = '—';
}

//Clears the transcript
function clearTranscript() {
  const transcriptBox = document.getElementById('transcriptBox');
  if (transcriptBox) {
    transcriptBox.innerHTML = '<span style="color:#aaa;font-style:italic;">Recognized text will appear here…</span>';
  }
}

//Leaves the call and returns to the landing page
function leaveCall() {
  stopRecognition();
  if (confirm('Are you sure you want to leave the call?')) {
    window.location.href = '/landing';
  }
}

//Contact Page
//Sends contact form (just a demo only)
function sendContactForm() {
  const name = document.getElementById('contactName')?.value.trim();
  const email = document.getElementById('contactEmail')?.value.trim();
  const message = document.getElementById('contactMessage')?.value.trim();

  if (!name || !email || !message) {
    return alert('Please fill in all fields.');
  }

  alert('Thank you! Your message has been sent.');
  document.getElementById('contactName').value = '';
  document.getElementById('contactEmail').value = '';
  document.getElementById('contactMessage').value = '';
}

//Runs when the page loads
document.addEventListener('DOMContentLoaded', function () {
  const path = window.location.pathname;

  if (path.includes('waiting')) initWaitingRoom();
  if (path.includes('call')) initCallPage();
});