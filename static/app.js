/* ── SignBridge Application ── */

// ── Helpers ──

// Mobile navigation toggle
function toggleMenu() {
    const nav = document.getElementById('navLinks');
    if (nav) nav.classList.toggle('open');
}

// Generates a random room code (eg: ABC-1234)
function generateRoomCode() {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    let code = '';
    for (let i = 0; i < 3; i++) code += chars[Math.floor(Math.random() * chars.length)];
    code += '-';
    for (let i = 0; i < 4; i++) code += chars[Math.floor(Math.random() * chars.length)];
    return code;
}

// Gets URL parameter by key
function getParam(key) {
    return new URLSearchParams(window.location.search).get(key);
}

// Go back in history or to landing page
function goBack() {
    if (window.history.length > 1) window.history.back();
    else window.location.href = '/landing';
}

// ── Home Page ──

// Join existing room
function joinRoom() {
    const name = document.getElementById('userName')?.value.trim();
    const room = document.getElementById('roomCode')?.value.trim();

    if (!name) {
        // TODO: Display in-screen message: 'Please enter your name.'
        return;
    }
    if (!room) {
        // TODO: Display in-screen message: 'Please enter a room code.'
        return;
    }

    window.location.href = `/waiting?name=${encodeURIComponent(name)}&room=${encodeURIComponent(room)}`;
}

// Create new session
async function createSession() {
    const name = document.getElementById('userName')?.value.trim() || 'Guest';

    try {
        const res = await fetch('/create-room', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: name })
        });

        if (res.status === 429) {
            // TODO: Display in-screen message: "Too many room creation attempts. Please wait 1 minute and try again."
            return;
        }

        const data = await res.json();
        if (!data.success) {
            // TODO: Display in-screen message: data.message || 'Failed to create room'
            return;
        }

        const room = data.room_code;
        window.location.href = `/waiting?name=${encodeURIComponent(name)}&room=${encodeURIComponent(room)}`;
    } catch (err) {
        console.error(err);
        // TODO: Display in-screen message: 'Error creating room.'
    }
}

// ── Waiting Room ──

// Initialize waiting room
function initWaitingRoom() {
    const roomEl = document.getElementById('waitRoomCode');
    const nameEl = document.getElementById('userNameDisplay');

    const room = getParam('room') || 'N/A';
    const name = getParam('name') || 'Guest';

    if (roomEl) roomEl.textContent = room;
    if (nameEl) nameEl.textContent = name;
}

// Join call from waiting room
function joinCall() {
    const room = getParam('room') || 'ABC-1234';
    const name = getParam('name') || 'Guest';
    window.location.href = `/call?name=${encodeURIComponent(name)}&room=${encodeURIComponent(room)}`;
}

// ── Call Page ──

let recognitionActive = false;

// Initialize call page
function initCallPage() {
    const roomEl = document.getElementById('callRoomCode');
    const room = getParam('room') || 'N/A';
    if (roomEl) roomEl.textContent = room;
}

// Start sign language recognition
function startRecognition() {
    if (recognitionActive) return;

    recognitionActive = true;

    const btnStart = document.getElementById('btnStartRecog');
    const btnStop = document.getElementById('btnStopRecog');
    const statusEl = document.getElementById('recognitionStatus');
    const letterEl = document.getElementById('detectedLetter');
    const transcriptBox = document.getElementById('transcriptBox');

    if (btnStart) btnStart.disabled = true;
    if (btnStop) btnStop.disabled = false;
    if (statusEl) statusEl.textContent = 'Ready for recognition...';
    if (letterEl) letterEl.textContent = '?';
    if (transcriptBox && transcriptBox.innerHTML === '') {
        transcriptBox.innerHTML = '<span style="color:#aaa;font-style:italic;">Waiting for sign language input...</span>';
    }
}

// Stop sign language recognition
function stopRecognition() {
    recognitionActive = false;

    const btnStart = document.getElementById('btnStartRecog');
    const btnStop = document.getElementById('btnStopRecog');
    const statusEl = document.getElementById('recognitionStatus');
    const letterEl = document.getElementById('detectedLetter');

    if (btnStart) btnStart.disabled = false;
    if (btnStop) btnStop.disabled = true;
    if (statusEl) statusEl.textContent = 'No hand detected';
    if (letterEl) letterEl.textContent = '—';
}

// Clear transcript
function clearTranscript() {
    const transcriptBox = document.getElementById('transcriptBox');
    if (transcriptBox) {
        transcriptBox.innerHTML = '<span style="color:#aaa;font-style:italic;">Recognized text will appear here…</span>';
    }
}

// Leave call
function leaveCall() {
    stopRecognition();
    // TODO: Replace confirm() with in-screen modal confirmation
    if (confirm('Are you sure you want to leave the call?')) {
        window.location.href = '/landing';
    }
}

// ── Contact Page ──

// Send contact form
async function sendContactForm() {
    const name = document.getElementById('contactName')?.value.trim();
    const email = document.getElementById('contactEmail')?.value.trim();
    const subject = document.getElementById('contactSubject')?.value.trim();
    const message = document.getElementById('contactMessage')?.value.trim();

    if (!name || !email || !message) {
        // TODO: Display in-screen message: 'Please fill in all required fields.'
        return;
    }

    try {
        const res = await fetch('/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, subject, message })
        });

        const data = await res.json();
        if (data.success) {
            // TODO: Display in-screen message: data.message
            document.getElementById('contactName').value = '';
            document.getElementById('contactEmail').value = '';
            document.getElementById('contactSubject').value = '';
            document.getElementById('contactMessage').value = '';
        } else {
            // TODO: Display in-screen message: data.message || 'Failed to send message.'
        }
    } catch (err) {
        console.error(err);
        // TODO: Display in-screen message: 'Error sending message.'
    }
}

// ── Profile Page ──

// Load profile
async function loadProfile() {
    try {
        const res = await fetch('/profile/data');
        if (!res.ok) throw new Error('Failed to fetch profile');

        const data = await res.json();
        if (data.success && data.user) {
            document.getElementById('usernameDisplay').textContent = data.user.username;
            document.getElementById('emailDisplay').textContent = data.user.email;
            document.getElementById('username').value = data.user.username;
            document.getElementById('email').value = data.user.email;
        } else {
            // TODO: Display in-screen message: 'Failed to load profile.'
        }
    } catch (err) {
        console.error(err);
        // TODO: Display in-screen message: 'Error loading profile. Please refresh.'
    }
}

// Show/hide edit form
function showEditForm() {
    document.getElementById('profileView').style.display = 'none';
    document.getElementById('profileEdit').style.display = 'block';
}
function cancelEdit() {
    document.getElementById('profileEdit').style.display = 'none';
    document.getElementById('profileView').style.display = 'block';
}

// Update profile
async function updateProfile() {
    const username = document.getElementById('username')?.value.trim();
    const email = document.getElementById('email')?.value.trim();
    const password = document.getElementById('password')?.value.trim();

    if (!username || !email) {
        // TODO: Display in-screen message: 'Username and email cannot be empty.'
        return;
    }

    try {
        const res = await fetch('/profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await res.json();
        if (data.success) {
            // TODO: Display in-screen message: 'Profile updated successfully.'
            cancelEdit();
            loadProfile();
            document.getElementById('password').value = '';
        } else {
            // TODO: Display in-screen message: data.message || 'Failed to update profile.'
        }
    } catch (err) {
        console.error(err);
        // TODO: Display in-screen message: 'Error updating profile.'
    }
}

// Logout
async function logout() {
    try {
        const res = await fetch('/logout');
        const data = await res.json();
        if (data.success) window.location.href = '/';
        else {
            // TODO: Display in-screen message: 'Logout failed.'
        }
    } catch (err) {
        console.error(err);
        // TODO: Display in-screen message: 'Error logging out.'
    }
}

// ── Event Listeners ──
document.addEventListener('DOMContentLoaded', function () {
    const path = window.location.pathname;

    if (path.includes('waiting')) initWaitingRoom();
    if (path.includes('call')) initCallPage();
    if (path.includes('profile')) {
        loadProfile();
        document.getElementById('editProfileBtn')?.addEventListener('click', showEditForm);
        document.getElementById('cancelEditBtn')?.addEventListener('click', cancelEdit);
        document.getElementById('updateProfileBtn')?.addEventListener('click', updateProfile);
        document.getElementById('logoutBtn')?.addEventListener('click', logout);
    }
});