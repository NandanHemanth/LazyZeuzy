// Chat Page JavaScript - Athena's Wisdom

let chatHistory = [];
let sources = [];

// Initialize chat functionality
document.addEventListener('DOMContentLoaded', function() {
    initializeChat();
    loadSources();
    initializeChatInput();
});

function initializeChat() {
    // Auto-resize chat input
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('input', autoResizeTextarea);
        chatInput.addEventListener('keydown', handleChatKeydown);
    }

    // Initialize starter buttons
    initializeStarterButtons();
}

function autoResizeTextarea(e) {
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

function handleChatKeydown(e) {
    // Send message on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

function initializeStarterButtons() {
    const starterButtons = document.querySelectorAll('.starter-btn');
    starterButtons.forEach(button => {
        button.addEventListener('click', function() {
            startConversation(this);
        });
    });
}

function startConversation(button) {
    const promptText = button.querySelector('span').textContent.trim();
    const chatInput = document.getElementById('chatInput');

    // Clear welcome message
    const welcomeMessage = document.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.style.display = 'none';
    }

    // Add the starter prompt as user message
    addMessageToChat('user', promptText);

    // Auto-send the message
    setTimeout(() => {
        sendAIResponse(promptText);
    }, 500);
}

async function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();

    if (!message) return;

    // Clear input and reset height
    chatInput.value = '';
    chatInput.style.height = 'auto';

    // Hide welcome message if visible
    const welcomeMessage = document.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.style.display = 'none';
    }

    // Add user message to chat
    addMessageToChat('user', message);

    // Send to AI
    await sendAIResponse(message);
}

async function sendAIResponse(message) {
    // Show typing indicator
    showTypingIndicator();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                sources: sources.map(s => s.id)
            })
        });

        const result = await response.json();

        if (result.success) {
            // Add AI response to chat
            addMessageToChat('assistant', result.response);
        } else {
            addMessageToChat('assistant', 'I apologize, divine seeker. The oracle is temporarily clouded. Please try again.');
        }
    } catch (error) {
        console.error('Chat error:', error);
        addMessageToChat('assistant', 'The divine connection has been disrupted. Please try again shortly.');
    } finally {
        hideTypingIndicator();
    }
}

function addMessageToChat(type, content) {
    const chatMessages = document.getElementById('chatMessages');

    const messageElement = document.createElement('div');
    messageElement.className = `message ${type} fade-in`;

    const avatar = type === 'user'
        ? '<i class="fas fa-user"></i>'
        : '<i class="fas fa-crown"></i>';

    const timestamp = formatTime(new Date());

    messageElement.innerHTML = `
        <div class="message-avatar">
            ${avatar}
        </div>
        <div class="message-content">
            <div class="message-text">${formatMessageContent(content)}</div>
            <div class="message-time">${timestamp}</div>
        </div>
    `;

    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Add to history
    chatHistory.push({
        type: type,
        content: content,
        timestamp: new Date().toISOString()
    });
}

function formatMessageContent(content) {
    // Basic markdown-like formatting
    return content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');
}

function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.style.display = 'flex';
        indicator.innerHTML = `
            <i class="fas fa-sparkles"></i>
            Athena is thinking...
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
    }
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.style.display = 'none';
    }
}

async function loadSources() {
    try {
        const response = await fetch('/api/files');
        const result = await response.json();

        if (result.files) {
            sources = result.files;
            updateSourceCount(sources.length);
        }
    } catch (error) {
        console.error('Error loading sources:', error);
    }
}

function updateSourceCount(count) {
    const sourceCountElement = document.querySelector('.source-count');
    if (sourceCountElement) {
        sourceCountElement.textContent = `${count} source${count !== 1 ? 's' : ''} available`;
    }
}

function attachFile() {
    // Redirect to upload page or open file picker
    window.location.href = '/upload';
}

function formatTime(date) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Add CSS for typing animation
const style = document.createElement('style');
style.textContent = `
    .message {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
        padding: 1rem;
        border-radius: 15px;
        transition: all 0.3s ease;
    }

    .message:hover {
        background: rgba(248, 246, 240, 0.05);
    }

    .message.user {
        flex-direction: row-reverse;
    }

    .message.user .message-content {
        text-align: right;
    }

    .message-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
    }

    .message.user .message-avatar {
        background: var(--divine-gradient);
        color: white;
    }

    .message.assistant .message-avatar {
        background: var(--goddess-gradient);
        color: var(--temple-stone);
    }

    .message-content {
        flex: 1;
        min-width: 0;
    }

    .message-text {
        color: var(--marble-white);
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }

    .message-text strong {
        color: var(--olympus-gold);
    }

    .message-text em {
        color: var(--divine-blue);
    }

    .message-text code {
        background: rgba(212, 175, 55, 0.2);
        color: var(--olympus-gold);
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
    }

    .message-time {
        color: var(--marble-white);
        opacity: 0.6;
        font-size: 0.8rem;
    }

    .typing-dots {
        display: inline-flex;
        gap: 0.2rem;
        margin-left: 0.5rem;
    }

    .typing-dots span {
        width: 4px;
        height: 4px;
        background: var(--olympus-gold);
        border-radius: 50%;
        animation: typing-bounce 1.4s infinite ease-in-out;
    }

    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }

    @keyframes typing-bounce {
        0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }

    .fade-in {
        animation: messageSlideIn 0.4s ease-out;
    }

    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .input-wrapper {
        position: relative;
        background: rgba(248, 246, 240, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 20px;
        padding: 1rem;
    }

    .input-wrapper:focus-within {
        border-color: var(--olympus-gold);
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
    }

    .chat-input {
        width: 100%;
        background: transparent;
        border: none;
        color: var(--marble-white);
        font-family: var(--font-modern);
        font-size: 1rem;
        resize: none;
        outline: none;
        padding-right: 5rem;
    }

    .chat-input::placeholder {
        color: var(--marble-white);
        opacity: 0.5;
    }

    .input-actions {
        position: absolute;
        right: 1rem;
        top: 50%;
        transform: translateY(-50%);
        display: flex;
        gap: 0.5rem;
    }

    .action-btn {
        background: rgba(212, 175, 55, 0.2);
        border: none;
        color: var(--marble-white);
        width: 36px;
        height: 36px;
        border-radius: 50%;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .action-btn:hover {
        background: rgba(212, 175, 55, 0.4);
        transform: scale(1.1);
    }

    .send-btn {
        background: var(--goddess-gradient);
        color: var(--temple-stone);
    }

    .send-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
    }
`;

document.head.appendChild(style);

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Focus chat input with /
    if (e.key === '/' && !e.target.closest('input, textarea')) {
        e.preventDefault();
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.focus();
        }
    }

    // Quick navigation
    if (e.ctrlKey && e.key === 'u') {
        e.preventDefault();
        window.location.href = '/upload';
    }

    if (e.ctrlKey && e.key === 'h') {
        e.preventDefault();
        window.location.href = '/';
    }
});