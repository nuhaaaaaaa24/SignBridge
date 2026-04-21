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

    if (sender === 'system') {
        const div = document.createElement('div');
        div.style.cssText = 'text-align:center;color:#666;font-style:italic;font-size:0.78rem;margin:4px 0;';
        div.textContent = message;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
        return;
    }

    const isMe = sender === 'me';
    const wrapper = document.createElement('div');
    wrapper.style.cssText = `display:flex;flex-direction:column;align-items:${isMe ? 'flex-end' : 'flex-start'};margin:4px 0;`;

    if (showName && !isMe) {
        const label = document.createElement('span');
        label.style.cssText = 'font-size:0.72rem;color:#888;margin-bottom:2px;padding:0 4px;';
        label.textContent = sender;
        wrapper.appendChild(label);
    }

    const bubble = document.createElement('div');
    bubble.style.cssText = `
        padding:8px 12px;
        border-radius:${isMe ? '14px 14px 4px 14px' : '14px 14px 14px 4px'};
        max-width:78%;font-size:0.88rem;line-height:1.4;word-wrap:break-word;
        background:${isMe ? '#2d6cdf' : '#2a2a2a'};
        color:${isMe ? '#fff' : '#ddd'};
    `;
    bubble.textContent = message;
    wrapper.appendChild(bubble);
    chatBox.appendChild(wrapper);
    chatBox.scrollTop = chatBox.scrollHeight;
}