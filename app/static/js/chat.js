/* app/static/js/chat.js */

// Chat module — shares its Socket.IO connection with call.js.
// Must be initialized by call.js: initChat(App.socket, () => App.room).

let chatSocket   = null;
let roomGetter   = null;
let myUsername   = null;
let wired        = false;

export function initChat(socket, roomCodeGetter, username) {
    if (wired) return;
    chatSocket  = socket;
    roomGetter  = roomCodeGetter;
    myUsername  = username || null;

    // Chat history sent on join (persisted messages)
    chatSocket.on('chat_history', (data) => {
        if (!data || !Array.isArray(data.messages)) return;
        data.messages.forEach(m => {
            const isMe = myUsername && m.sender === myUsername;
            appendMessage(isMe ? 'me' : m.sender, m.message, m.timestamp, !isMe);
        });
        const chatBox = document.getElementById('chatBox');
        if (chatBox && data.messages.length) {
            const sep = document.createElement('div');
            sep.style.cssText = 'text-align:center;color:#555;font-size:0.75rem;' +
                                 'margin:8px 0;border-top:1px solid #333;padding-top:6px;';
            sep.textContent = '— previous messages —';
            chatBox.appendChild(sep);
        }
    });

    // Incoming live messages
    chatSocket.on('chat_message', (data) => {
        if (!data || !data.message) return;
        if (data.sender === 'system') {
            appendMessage('system', data.message, data.timestamp, false);
        } else {
            appendMessage(data.sender, data.message, data.timestamp, true);
        }
    });

    const input = document.getElementById('chatInput');
    if (input) {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') { e.preventDefault(); sendChatMessage(); }
        });
    }

    const sendBtn = document.getElementById('sendChatBtn');
    if (sendBtn) sendBtn.addEventListener('click', sendChatMessage);

    wired = true;
}

export function sendChatMessage() {
    if (!chatSocket || !roomGetter) return;
    const input = document.getElementById('chatInput');
    if (!input) return;
    const message = input.value.trim();
    if (!message) return;

    chatSocket.emit('chat_message', { room: roomGetter(), message });
    appendMessage('me', message, new Date().toISOString(), false);
    input.value = '';
}

function appendMessage(sender, message, timestamp, showName) {
    const chatBox = document.getElementById('chatBox');
    if (!chatBox) return;

    chatBox.classList.remove('empty-chat');

    if (sender === 'system') {
        const div = document.createElement('div');
        div.className = 'chat-system-message';
        div.textContent = message;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
        return;
    }

    const isMe = sender === 'me';

    const wrapper = document.createElement('div');
    wrapper.className = `chat-message-wrap ${isMe ? 'chat-message-wrap--me' : 'chat-message-wrap--peer'}`;

    if (showName && !isMe) {
        const label = document.createElement('span');
        label.className = 'chat-sender-label';
        label.textContent = sender;
        wrapper.appendChild(label);
    }

    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${isMe ? 'chat-bubble--me' : 'chat-bubble--peer'}`;
    bubble.textContent = message;

    wrapper.appendChild(bubble);
    chatBox.appendChild(wrapper);
    chatBox.scrollTop = chatBox.scrollHeight;
}