// Upload Page JavaScript - Athena's Wisdom

let uploadedFiles = [];

// Initialize upload functionality
document.addEventListener('DOMContentLoaded', function() {
    initializeUploadZone();
    initializeFileInput();
    updateSourceCount();
});

function initializeUploadZone() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');

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

    // Click to upload
    uploadZone.addEventListener('click', function() {
        fileInput.click();
    });
}

function initializeFileInput() {
    const fileInput = document.getElementById('fileInput');

    fileInput.addEventListener('change', function(e) {
        handleFiles(e.target.files);
    });
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
            uploadedFiles.push(result.file);
            showNotification(result.message, 'success');
            displayUploadedFiles();
            updateSourceCount();
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
    // Add visual feedback for upload progress
    const uploadZone = document.getElementById('uploadZone');
    uploadZone.style.opacity = '0.7';
    uploadZone.style.pointerEvents = 'none';

    // You can add a progress spinner here
}

function hideUploadProgress() {
    const uploadZone = document.getElementById('uploadZone');
    uploadZone.style.opacity = '1';
    uploadZone.style.pointerEvents = 'auto';
}

function displayUploadedFiles() {
    const uploadedFilesDiv = document.getElementById('uploadedFiles');
    const filesList = document.getElementById('filesList');

    if (uploadedFiles.length > 0) {
        uploadedFilesDiv.style.display = 'block';

        filesList.innerHTML = uploadedFiles.map(file => `
            <div class="file-item">
                <div class="file-icon">
                    <i class="fas fa-file-${getFileIcon(file.type)}"></i>
                </div>
                <div class="file-info">
                    <div class="file-name">${file.original_name}</div>
                    <div class="file-meta">${file.type.toUpperCase()} • ${formatFileSize(file.size)}</div>
                </div>
                <button class="action-btn" onclick="removeFile('${file.id}')" title="Remove">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');
    }
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

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function removeFile(fileId) {
    uploadedFiles = uploadedFiles.filter(file => file.id !== fileId);
    displayUploadedFiles();
    updateSourceCount();
    showNotification('Sacred text removed from library', 'info');
}

function updateSourceCount() {
    const sourceCountElement = document.getElementById('sourceCount');
    if (sourceCountElement) {
        sourceCountElement.textContent = uploadedFiles.length;
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;

    // Add styles
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

    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    // Remove after delay
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            document.body.removeChild(notification);
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

// Modal functions
function openTextModal() {
    document.getElementById('textModal').style.display = 'flex';
    document.getElementById('textInput').focus();
}

function closeTextModal() {
    document.getElementById('textModal').style.display = 'none';
    document.getElementById('textInput').value = '';
}

function openWebsiteModal() {
    document.getElementById('websiteModal').style.display = 'flex';
    document.getElementById('websiteInput').focus();
}

function closeWebsiteModal() {
    document.getElementById('websiteModal').style.display = 'none';
    document.getElementById('websiteInput').value = '';
}

function openYouTubeModal() {
    document.getElementById('youtubeModal').style.display = 'flex';
    document.getElementById('youtubeInput').focus();
}

function closeYouTubeModal() {
    document.getElementById('youtubeModal').style.display = 'none';
    document.getElementById('youtubeInput').value = '';
}

function saveText() {
    const text = document.getElementById('textInput').value.trim();
    if (text) {
        // Create a virtual file from text
        const file = new Blob([text], { type: 'text/plain' });
        file.name = 'pasted_text.txt';
        uploadFile(file);
        closeTextModal();
    }
}

function saveWebsite() {
    const url = document.getElementById('websiteInput').value.trim();
    if (url) {
        // In a real implementation, you would send this to your backend
        // to scrape the website content
        const fileInfo = {
            id: generateId(),
            filename: 'website_content.txt',
            original_name: url,
            filepath: '',
            uploaded_at: new Date().toISOString(),
            size: 0,
            type: 'website'
        };

        uploadedFiles.push(fileInfo);
        displayUploadedFiles();
        updateSourceCount();
        showNotification('Website content added to divine library', 'success');
        closeWebsiteModal();
    }
}

function saveYouTube() {
    const url = document.getElementById('youtubeInput').value.trim();
    if (url) {
        // In a real implementation, you would send this to your backend
        // to process the YouTube video
        const fileInfo = {
            id: generateId(),
            filename: 'youtube_content.txt',
            original_name: url,
            filepath: '',
            uploaded_at: new Date().toISOString(),
            size: 0,
            type: 'youtube'
        };

        uploadedFiles.push(fileInfo);
        displayUploadedFiles();
        updateSourceCount();
        showNotification('YouTube content added to divine library', 'success');
        closeYouTubeModal();
    }
}

function openGoogleDrive() {
    showNotification('Google Drive integration coming soon by divine decree', 'info');
}

function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Close modals when clicking outside
document.addEventListener('click', function(e) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // ESC to close modals
    if (e.key === 'Escape') {
        const openModal = document.querySelector('.modal[style*="flex"]');
        if (openModal) {
            openModal.style.display = 'none';
        }
    }

    // Ctrl+V to open paste text modal
    if (e.ctrlKey && e.key === 'v' && !e.target.closest('.modal')) {
        e.preventDefault();
        openTextModal();
    }
});