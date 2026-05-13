/* app/static/js/call.js */

import { initChat, setUsername } from '/static/js/chat.js';
import { initModel, captureAndInfer } from '/static/js/model.js';

// ================= CONFIG =================
const TOTAL_SECONDS   = 5;
const CAPTURE_AT_SECOND = 2;

const ICE_CONFIG = {
    iceServers: [
        {
            urls: "stun:stun.relay.metered.ca:80",
        },
        {
            urls: "turn:global.relay.metered.ca:443",
            username: "fb1fd4c0bb2b6342d7ae5829",
            credential: "9HXpNy4OK/Zr52Vr",
        },
        {
            urls: "turns:global.relay.metered.ca:443?transport=tcp",
            username: "fb1fd4c0bb2b6342d7ae5829",
            credential: "9HXpNy4OK/Zr52Vr",
        },
    ]
};

// ================= APP STATE =================
const App = {
    room: window.ROOM_CODE || ''
          (document.getElementById('waitRoomCode') &&
           document.getElementById('waitRoomCode').textContent.trim()) || '',

    stream: null,
    streamReady: null,

    socket: null,
    pc: null,

    pendingSignals: [],
    role: null,

    // recognition state
    countdownTimer: null,
    secondsRemaining: TOTAL_SECONDS,
    isRecognizing: false,

    // call state
    callStarted: false,

    // mute state
    micMuted: false,
    camMuted: false,

    // Username to show in call
    peerUsername: 'Participant',
};

// ================= BOOT =================
async function bootApp() {
    try {
        initUI();
        await initMedia();
        await initModel(setRecogStatus, () => {
            const btn = document.getElementById('btnStartRecog');
            if (btn) btn.disabled = false;
        });
        initSocket();
        wireUnloadCleanup();
    } catch (err) {
        console.error('Boot failed:', err);
        setRecogStatus('⚠ Startup failed: ' + (err.message || err));
    }
}

// ================= MEDIA =================
async function initMedia() {
    try {
        App.streamReady = navigator.mediaDevices.getUserMedia({
            video: { width: { ideal: 640 }, height: { ideal: 480 } },
            audio: true
        });
        App.stream = await App.streamReady;

        const preview = document.getElementById('waitPreview');
        if (preview) {
            preview.srcObject   = App.stream;
            preview.muted       = true;
            preview.playsInline = true;
        }

        const waitStatus = document.getElementById('waitPreviewStatus');
        if (waitStatus) waitStatus.textContent = '';
    } catch (err) {
        const waitStatus = document.getElementById('waitPreviewStatus');
        if (waitStatus) waitStatus.textContent = 'Camera/mic access denied.';
        setRecogStatus('⚠ Camera/mic access denied');
        throw err;
    }
}

// ================= SOCKET =================
function initSocket() {
    App.socket = io();

    App.socket.emit('join_room', { room: App.room });
    App.socket.on('role_and_ready', async ({ role, peer_username }) => {
        App.role = role;
        if (peer_username) {
            if (App.callStarted) return;
            App.callStarted = true;
            App.peerUsername = peer_username || 'Participant';
            await startCall();
        }
    });

    App.socket.on('signal', async (msg) => {
        if (!App.pc) {
            App.pendingSignals.push(msg);
            return;
        }
        await handleSignal(msg);
    });

    App.socket.on('peer_left', () => {
        setCallStatus('Peer left', false);
        const remote = document.getElementById('remoteVideo');
        if (remote) remote.srcObject = null;

        if (App.pc) {
            try { App.pc.close(); } catch (_) {}
            App.pc = null;
        }
        App.pendingSignals = [];
        App.callStarted    = false;
        App.role           = null;
    });

    App.socket.on('error', (data) => {
        const msg = (data && data.message) || 'Signaling error';
        setRecogStatus('⚠ ' + msg);
    });

    App.socket.on('transcript_letter', ({ letter, sender }) => {
        appendToTranscript(letter, sender);
    });

    initChat(App.socket, () => App.room);
}

// ================= CALL START =================
async function startCall() {
    enterCallPhase();
    await App.streamReady;

    if (!App.pc) {
        App.pc = new RTCPeerConnection(ICE_CONFIG);

        App.stream.getTracks().forEach(track => {
            App.pc.addTrack(track, App.stream);
        });

        App.pc.ontrack = (event) => {
            const remote = document.getElementById('remoteVideo');
            if (remote) {
                remote.srcObject   = event.streams[0];
                remote.playsInline = true;
            }
        };

        App.pc.onicecandidate = (event) => {
            if (event.candidate) {
                App.socket.emit('signal', {
                    room: App.room,
                    type: 'ice-candidate',
                    candidate: event.candidate
                });
            }
        };

        App.pc.onconnectionstatechange = () => {
            const state = App.pc ? App.pc.connectionState : 'closed';
            if (state === 'connected') {
                setCallStatus('Connected', true);
            } else if (
                state === 'failed' ||
                state === 'disconnected' ||
                state === 'closed'
            ) {
                setCallStatus('Disconnected', false);
            }
        };
    }

    if (App.role === 'caller') {
        try {
            if (App.pc.signalingState !== 'stable') return;
            const offer = await App.pc.createOffer();
            await App.pc.setLocalDescription(offer);
            App.socket.emit('signal', {
                room: App.room,
                type: 'offer',
                sdp: App.pc.localDescription
            });
        } catch (err) {
            console.error('createOffer failed:', err);
        }
    }

    while (App.pendingSignals.length) {
        await handleSignal(App.pendingSignals.shift());
    }
}

// ================= SIGNALING =================
async function handleSignal({ type, sdp, candidate }) {
    if (!App.pc) {
        App.pendingSignals.push({ type, sdp, candidate });
        return;
    }
    try {
        switch (type) {
            case 'offer': {
                await App.pc.setRemoteDescription(new RTCSessionDescription(sdp));
                const answer = await App.pc.createAnswer();
                await App.pc.setLocalDescription(answer);
                App.socket.emit('signal', {
                    room: App.room,
                    type: 'answer',
                    sdp: App.pc.localDescription
                });
                break;
            }
            case 'answer': {
                if (App.pc.signalingState === 'have-local-offer') {
                    await App.pc.setRemoteDescription(new RTCSessionDescription(sdp));
                }
                break;
            }
            case 'ice-candidate': {
                if (candidate) {
                    try {
                        await App.pc.addIceCandidate(new RTCIceCandidate(candidate));
                    } catch (e) {
                        console.warn('addIceCandidate:', e.message);
                    }
                }
                break;
            }
        }
    } catch (err) {
        console.error('Signal error:', err);
    }
}

// ================= UI =================
function initUI() {
    const waitCode = document.getElementById('waitRoomCode');
    const callCode = document.getElementById('callRoomCode');
    if (waitCode) waitCode.textContent = App.room;
    if (callCode) callCode.textContent = App.room;

    const startBtn = document.getElementById('btnStartRecog');
    if (startBtn) startBtn.disabled = true;

    const stopBtn = document.getElementById('btnStopRecog');
    if (stopBtn) stopBtn.disabled = true;
}

function enterCallPhase() {
    const wait = document.getElementById('waiting-room');
    const call = document.getElementById('calling-room');
    if (wait) wait.style.display = 'none';
    if (call) call.style.display = '';

    // Update the remote video name overlay
    const nameOverlay = document.querySelector('.video-overlay-name');
    if (nameOverlay) nameOverlay.textContent = App.peerUsername;

    const local = document.getElementById('localVideo');
    if (local && App.stream) {
        local.srcObject   = App.stream;
        local.muted       = true;
        local.playsInline = true;
    }
}

function setCallStatus(text, ok) {
    const el = document.getElementById('callStatus');
    if (!el) return;

    el.className = `status-badge status-badge--${ok ? 'connected' : 'waiting'}`;

    const dot = el.querySelector('.status-dot');
    if (dot) dot.style.background = ok ? '#27ae60' : '#e74c3c';

    const textEl = document.getElementById('callStatusText');
    if (textEl) textEl.textContent = text;
}

// ================= RECOGNITION =================
function startRecognition() {
    if (App.isRecognizing) return;

    const video = document.getElementById('localVideo');
    if (!video || video.readyState < 2 || !video.videoWidth) {
        return setRecogStatus('Video not ready');
    }

    App.isRecognizing = true;

    const startBtn = document.getElementById('btnStartRecog');
    const stopBtn  = document.getElementById('btnStopRecog');
    if (startBtn) startBtn.disabled = true;
    if (stopBtn)  stopBtn.disabled  = false;

    App.secondsRemaining = TOTAL_SECONDS;
    const timerEl = document.getElementById('timerDisplay');
    if (timerEl) {
        timerEl.style.display = 'block';
        timerEl.textContent   = App.secondsRemaining;
    }

    if (App.countdownTimer) {
        clearInterval(App.countdownTimer);
        App.countdownTimer = null;
    }

    App.countdownTimer = setInterval(() => {
        if (App.secondsRemaining === CAPTURE_AT_SECOND) {
            captureAndInfer(setRecogStatus, appendToTranscript, (letter) => {
            if (App.socket) {
                App.socket.emit('transcript_letter', {
                    room: App.room,
                    letter: letter
                });
            }
        });
        }

        if (timerEl) timerEl.textContent = App.secondsRemaining;
        App.secondsRemaining--;

        if (App.secondsRemaining < 0) {
            finishRecognition('Done — press ▶ again');
        }

        // if (App.secondsRemaining < 0) {
        //     App.secondsRemaining = TOTAL_SECONDS; 
        // }
    }, 1000);
}

function stopRecognition() {
    if (!App.isRecognizing) return;
    finishRecognition('Stopped');
}

function finishRecognition(statusMsg) {
    if (App.countdownTimer) {
        clearInterval(App.countdownTimer);
        App.countdownTimer = null;
    }
    App.isRecognizing = false;

    const timerEl = document.getElementById('timerDisplay');
    if (timerEl) timerEl.style.display = 'none';

    const startBtn = document.getElementById('btnStartRecog');
    const stopBtn  = document.getElementById('btnStopRecog');
    if (startBtn) startBtn.disabled = false;
    if (stopBtn)  stopBtn.disabled  = true;

    setRecogStatus(statusMsg);
}

// ================= TRANSCRIPT =================
// Tracks the last sender so we group consecutive letters under one name header
let lastTranscriptSender = null;

function appendToTranscript(letter, sender = null) {
    const box = document.getElementById('transcriptBox');
    if (!box) return;

    const placeholder = box.querySelector('.transcript-placeholder');
    if (placeholder) placeholder.remove();

    const displayName = sender || window.CURRENT_USER || 'You';

    // Only add a new sender header if the sender has changed
    if (displayName !== lastTranscriptSender) {
        lastTranscriptSender = displayName;

        const header = document.createElement('div');
        header.style.cssText = 'display:flex;align-items:center;gap:8px;margin:12px 0 4px 0;';

        const name = document.createElement('span');
        name.textContent = displayName;
        name.style.cssText = 'font-size:0.78rem;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:0.05em;';

        const time = document.createElement('span');
        time.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        time.style.cssText = 'font-size:0.72rem;color:#555;';

        header.appendChild(name);
        header.appendChild(time);
        box.appendChild(header);

        // Letter container for this sender's block
        const block = document.createElement('div');
        block.className = 'transcript-block';
        block.style.cssText = 'display:flex;flex-wrap:wrap;gap:4px;margin-bottom:4px;';
        box.appendChild(block);
    }

    // Append letter to the current sender's block
    const currentBlock = box.querySelector('.transcript-block:last-of-type');
    const span = document.createElement('span');
    span.textContent = letter;
    span.className = 'transcript-letter';
    span.style.cssText = 'font-size:1.4rem;font-weight:700;cursor:default;';
    currentBlock.appendChild(span);

    box.scrollTop = box.scrollHeight;
}

function clearTranscript() {
    const box = document.getElementById('transcriptBox');
    if (box) {
        box.innerHTML = '<span class="transcript-placeholder">Recognized letters will appear here…</span>';
    }
    lastTranscriptSender = null;
    const letterEl = document.getElementById('detectedLetter');
    if (letterEl) letterEl.textContent = '—';
}

function setRecogStatus(msg) {
    const el = document.getElementById('recognitionStatus');
    if (el) el.textContent = msg;
}

// ================= LEAVE / CLEANUP =================
function leaveCall() {
    const shouldLeave = confirm("Are you sure you want to leave the call?");

    if (!shouldLeave) {
        return;
    }

    cleanup();
    window.location.href = '/';
}

function cancelAndLeave() {
    const shouldCancel = confirm("Are you sure you want to leave this session?");

    if (!shouldCancel) {
        return;
    }
    
    cleanup();
    window.location.href = '/';
}

function cleanup() {
    if (App.countdownTimer) {
        clearInterval(App.countdownTimer);
        App.countdownTimer = null;
    }
    App.isRecognizing = false;

    if (App.pc) {
        try { App.pc.close(); } catch (_) {}
        App.pc = null;
    }

    if (App.stream) {
        App.stream.getTracks().forEach(t => {
            try { t.stop(); } catch (_) {}
        });
        App.stream = null;
    }

    if (App.socket) {
        try { App.socket.disconnect(); } catch (_) {}
    }

    App.pendingSignals = [];
    App.callStarted    = false;
}

function wireUnloadCleanup() {
    window.addEventListener('beforeunload', cleanup);
    window.addEventListener('pagehide',     cleanup);
}

// ================= MUTE CONTROLS =================
function toggleMic() {
    if (!App.stream) return; 
    App.micMuted = !App.micMuted; 
    App.stream.getAudioTracks().forEach(t=>{ t.enabled = !App.micMuted;});

    const iconClass = App.micMuted ? 'bi-mic-mute-fill' : 'bi-mic-fill';

    ['btnToggleMic','btnToggleMicWait'].forEach(id=>{
        const btn=document.getElementById(id);
        if(btn){ btn.innerHTML = `<i class="bi ${iconClass}"></i>`; btn.classList.toggle( 'muted', App.micMuted);
        }
    });
}

function toggleCam() {
    if (!App.stream) return;
    App.camMuted=!App.camMuted;
    App.stream.getVideoTracks().forEach(t=>{ t.enabled=!App.camMuted; });
    const iconClass= App.camMuted ? 'bi-camera-video-off-fill' : 'bi-camera-video-fill';

    ['btnToggleCam','btnToggleCamWait'].forEach(id=>{
        const btn=document.getElementById(id);
        if(btn){ btn.innerHTML= `<i class="bi ${iconClass}"></i>`; btn.classList.toggle( 'muted', App.camMuted );
        }
    });
}

// ================= EXPOSE TO WINDOW =================
window.startRecognition = startRecognition;
window.stopRecognition  = stopRecognition;
window.clearTranscript  = clearTranscript;
window.leaveCall        = leaveCall;
window.cancelAndLeave   = cancelAndLeave;
window.toggleMic        = toggleMic;
window.toggleCam        = toggleCam;

// ================= START =================
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootApp);
} else {
    bootApp();
}