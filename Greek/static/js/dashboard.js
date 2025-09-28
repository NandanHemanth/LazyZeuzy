// Dashboard JavaScript - Athena's Wisdom

let chatHistory = [];
let selectedSources = [];

// Initialize dashboard functionality
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    loadSources();
    loadChatHistory();
    initializeChatInput();
    initializeSourceSelection();
    initializeSlideshow();
    initializeFileUpload();
});

function initializeDashboard() {
    // Auto-resize chat input
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('input', autoResizeTextarea);
        chatInput.addEventListener('keydown', handleChatKeydown);
    }

    // Initialize tooltips and interactions
    initializeTooltips();

    // Start periodic updates
    setInterval(updateTimestamps, 60000); // Update every minute
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

async function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();

    if (!message) return;

    // Clear input and reset height
    chatInput.value = '';
    chatInput.style.height = 'auto';

    // Add user message to chat
    addMessageToChat('user', message);

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
                sources: selectedSources
            })
        });

        const result = await response.json();

        if (result.success) {
            // Add AI response to chat
            addMessageToChat('assistant', result.response);
        } else {
            addMessageToChat('assistant', 'I apologize, but I cannot provide wisdom at this moment. Please try again.');
        }
    } catch (error) {
        console.error('Chat error:', error);
        addMessageToChat('assistant', 'The divine connection has been disrupted. Please try again.');
    } finally {
        hideTypingIndicator();
    }
}

function addMessageToChat(type, content, scrollToBottom = true, timestamp = null) {
    const chatMessages = document.getElementById('chatMessages');
    const welcomeMessage = chatMessages.querySelector('.welcome-message');

    // Remove welcome message if it exists
    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    const messageElement = document.createElement('div');
    messageElement.className = `message ${type} slide-up`;

    const avatar = type === 'user'
        ? '<i class="fas fa-user"></i>'
        : '<i class="fas fa-crown"></i>';

    // Format content for markdown-like styling
    const formattedContent = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                   .replace(/\n/g, '<br>');

    const messageTime = timestamp ? formatTime(timestamp) : formatTime(new Date());

    messageElement.innerHTML = `
        <div class="message-avatar">
            ${avatar}
        </div>
        <div class="message-content">
            <div class="message-text">${formattedContent}</div>
            <div class="message-time">${messageTime}</div>
        </div>
    `;

    chatMessages.appendChild(messageElement);

    if (scrollToBottom) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Add to local history only if it's a new message (not from server history)
    if (!timestamp) {
        chatHistory.push({
            type: type,
            content: content,
            timestamp: new Date().toISOString()
        });
    }
}

function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.style.display = 'flex';
    }
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.style.display = 'none';
    }
}

function usePrompt(button) {
    const promptText = button.textContent.trim();
    const chatInput = document.getElementById('chatInput');

    chatInput.value = promptText;
    chatInput.focus();

    // Auto resize
    autoResizeTextarea({ target: chatInput });
}

async function loadSources() {
    try {
        const response = await fetch('/api/files');
        const result = await response.json();

        if (result.files) {
            updateSourcesList(result.files);
            updateSourceCount(result.files.length);
        }
    } catch (error) {
        console.error('Error loading sources:', error);
    }
}

async function loadChatHistory() {
    try {
        const response = await fetch('/api/chat-history');
        const result = await response.json();

        if (result.chat_history && result.chat_history.length > 0) {
            const chatMessages = document.getElementById('chatMessages');
            const welcomeMessage = chatMessages.querySelector('.welcome-message');

            // Remove welcome message if it exists
            if (welcomeMessage) {
                welcomeMessage.remove();
            }

            // Clear existing messages
            chatMessages.innerHTML = '';

            // Add all messages from history
            result.chat_history.forEach(message => {
                addMessageToChat(message.type, message.content, false, new Date(message.timestamp));
            });
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

function updateSourcesList(files) {
    const sourcesList = document.getElementById('sourcesList');
    if (!sourcesList) return;

    if (files.length === 0) {
        sourcesList.innerHTML = `
            <div class="empty-sources">
                <i class="fas fa-scroll"></i>
                <p>No sacred texts yet</p>
                <button onclick="window.location.href='/upload'" class="divine-btn">Upload First Source</button>
            </div>
        `;
        return;
    }

    sourcesList.innerHTML = files.map(file => `
        <div class="source-item" data-file-id="${file.id}">
            <div class="source-icon">
                <i class="fas fa-file-${getFileIcon(file.type)}"></i>
            </div>
            <div class="source-info">
                <span class="source-name">${file.original_name}</span>
                <span class="source-meta">${file.type.toUpperCase()}</span>
            </div>
            <input type="checkbox" class="source-checkbox" data-file-id="${file.id}">
        </div>
    `).join('');

    // Re-initialize source selection
    initializeSourceSelection();
}

function getFileIcon(fileType) {
    const iconMap = {
        'pdf': 'pdf',
        'txt': 'alt',
        'md': 'markdown',
        'mp3': 'audio',
        'wav': 'audio',
        'png': 'image',
        'jpg': 'image',
        'jpeg': 'image',
        'pptx': 'powerpoint'
    };
    return iconMap[fileType] || 'alt';
}

function initializeSourceSelection() {
    const selectAllCheckbox = document.getElementById('selectAllSources');
    const sourceCheckboxes = document.querySelectorAll('.source-checkbox');

    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            sourceCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateSelectedSources();
        });
    }

    sourceCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateSelectedSources();

            // Update select all checkbox
            if (selectAllCheckbox) {
                const checkedCount = document.querySelectorAll('.source-checkbox:checked').length;
                selectAllCheckbox.checked = checkedCount === sourceCheckboxes.length;
                selectAllCheckbox.indeterminate = checkedCount > 0 && checkedCount < sourceCheckboxes.length;
            }
        });
    });
}

function updateSelectedSources() {
    const checkedBoxes = document.querySelectorAll('.source-checkbox:checked');
    selectedSources = Array.from(checkedBoxes).map(cb => cb.dataset.fileId);

    // Update UI to show selection
    updateSourceCount();
}

function updateSourceCount(totalCount) {
    const sourceIndicator = document.querySelector('.source-indicator');
    if (sourceIndicator) {
        const count = totalCount !== undefined ? totalCount : selectedSources.length;
        const text = selectedSources.length > 0
            ? `${selectedSources.length} selected`
            : `${count} source${count !== 1 ? 's' : ''}`;
        sourceIndicator.textContent = text;
    }
}

function generateContent(type) {
    if (selectedSources.length === 0) {
        showNotification('Please select sources first to create divine content', 'warning');
        return;
    }

    showNotification(`Creating divine ${type}... The muses are at work`, 'info');

    // In a real implementation, you would call your API
    fetch('/api/generate-content', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            type: type,
            sources: selectedSources,
            prompt: `Generate ${type} from selected sources`
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showNotification(result.message, 'success');
            // You could redirect to the generated content or update the UI
        } else {
            showNotification('Creation failed - The gods require more power', 'error');
        }
    })
    .catch(error => {
        console.error('Generation error:', error);
        showNotification('Divine creation interrupted', 'error');
    });
}

function initializeTooltips() {
    // Add hover effects and tooltips
    const actionBtns = document.querySelectorAll('.action-btn[title]');
    actionBtns.forEach(btn => {
        btn.addEventListener('mouseenter', showTooltip);
        btn.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = e.target.title;
    tooltip.style.cssText = `
        position: absolute;
        background: var(--temple-gradient);
        color: var(--marble-white);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.8rem;
        border: 1px solid var(--olympus-gold);
        z-index: 1000;
        pointer-events: none;
        transform: translateX(-50%);
        white-space: nowrap;
    `;

    document.body.appendChild(tooltip);

    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + rect.width / 2 + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';

    e.target._tooltip = tooltip;
}

function hideTooltip(e) {
    if (e.target._tooltip) {
        document.body.removeChild(e.target._tooltip);
        delete e.target._tooltip;
    }
}

function formatTime(date) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function updateTimestamps() {
    const timestamps = document.querySelectorAll('.message-time');
    // Update relative timestamps if needed
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;

    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--temple-gradient);
        border: 2px solid var(--olympus-gold);
        border-radius: 15px;
        padding: 1rem 1.5rem;
        color: var(--marble-white);
        z-index: 3000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 350px;
        box-shadow: var(--divine-shadow);
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

function getNotificationIcon(type) {
    const iconMap = {
        'success': 'check-circle',
        'error': 'exclamation-triangle',
        'info': 'info-circle',
        'warning': 'exclamation-circle'
    };
    return iconMap[type] || 'info-circle';
}

// Panel collapse functionality
function togglePanel(panelClass) {
    const panel = document.querySelector(`.${panelClass}`);
    if (panel) {
        panel.classList.toggle('collapsed');
    }
}

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

    // Quick upload with Ctrl+U
    if (e.ctrlKey && e.key === 'u') {
        e.preventDefault();
        triggerFileUpload();
    }
});

// File Upload Functions
function initializeFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadZone = document.getElementById('uploadZone');

    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            handleFiles(e.target.files);
        });
    }

    if (uploadZone) {
        // Drag and drop functionality
        uploadZone.addEventListener('dragover', function(e) {
            e.preventDefault();
            uploadZone.classList.add('drag-over');
        });

        uploadZone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            uploadZone.classList.remove('drag-over');
        });

        uploadZone.addEventListener('drop', function(e) {
            e.preventDefault();
            uploadZone.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            handleFiles(files);
        });

        uploadZone.addEventListener('click', function() {
            fileInput.click();
        });
    }
}

function triggerFileUpload() {
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.click();
    }
}

function handleFiles(files) {
    Array.from(files).forEach(file => {
        if (isAllowedFile(file)) {
            uploadFile(file);
        } else {
            showNotification(`File type ${file.type} is not blessed by the gods`, 'error');
        }
    });
}

function isAllowedFile(file) {
    const allowedTypes = [
        'application/pdf',
        'text/plain',
        'text/markdown',
        'audio/mpeg',
        'audio/wav',
        'audio/mp3',
        'image/png',
        'image/jpeg',
        'image/jpg',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    ];

    return allowedTypes.includes(file.type) ||
           file.name.endsWith('.md') ||
           file.name.endsWith('.txt') ||
           file.name.endsWith('.pptx');
}

async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        showUploadProgress(file.name);

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            showNotification(result.message, 'success');
            // Refresh sources and chat history
            await loadSources();
            await loadChatHistory();
        } else {
            showNotification(result.error || 'Upload failed', 'error');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showNotification('Upload failed - The gods are displeased', 'error');
    } finally {
        hideUploadProgress();
    }
}

function showUploadProgress(filename) {
    showNotification(`Uploading ${filename}...`, 'info');
}

function hideUploadProgress() {
    // Progress is handled by notifications
}

// Slideshow functionality
function initializeSlideshow() {
    const slideshowContainer = document.getElementById('headerSlideshow');
    if (!slideshowContainer) return;

    // Array of image filenames
    const images = [
        'greek1.png', 'greek2.png', 'greek3.png', 'greek4.png',
        'greek5.png', 'greek6.png', 'greek7.png', 'greek8.png',
        'greek9.png', 'greek10.png', 'greek11.png', 'greek12.png'
    ];

    let currentImageIndex = 0;

    // Shuffle images array for random order
    const shuffledImages = [...images].sort(() => Math.random() - 0.5);

    // Create img elements
    shuffledImages.forEach((imageName, index) => {
        const img = document.createElement('img');
        img.src = `/static/images/${imageName}`;
        img.alt = `Greek themed image ${index + 1}`;
        img.loading = 'lazy';

        // First image starts as active
        if (index === 0) {
            img.classList.add('active');
        }

        slideshowContainer.appendChild(img);
    });

    // Start slideshow rotation
    setInterval(() => {
        const images = slideshowContainer.querySelectorAll('img');

        // Remove active class from current image
        images[currentImageIndex].classList.remove('active');

        // Move to next image
        currentImageIndex = (currentImageIndex + 1) % images.length;

        // Add active class to new image
        images[currentImageIndex].classList.add('active');
    }, 4000); // Change image every 4 seconds
}