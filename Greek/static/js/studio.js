// Studio Page JavaScript - Athena's Wisdom

let createdContent = [];

// Initialize studio functionality
document.addEventListener('DOMContentLoaded', function() {
    initializeStudio();
    loadCreatedContent();
    initializeToolCards();
});

function initializeStudio() {
    // Add hover effects to tool cards
    const toolCards = document.querySelectorAll('.tool-card');
    toolCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 15px 35px rgba(212, 175, 55, 0.3)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });

    // Initialize creation cards
    initializeCreationCards();
}

function initializeToolCards() {
    // Tool card click handlers
    document.querySelectorAll('.tool-card').forEach(card => {
        card.addEventListener('click', function() {
            const toolType = this.getAttribute('onclick')?.match(/openTool\('(.+?)'\)/)?.[1];
            if (toolType) {
                openTool(toolType);
            }
        });
    });

    // Create button handlers
    document.querySelectorAll('.create-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const toolCard = this.closest('.tool-card');
            const toolType = toolCard.getAttribute('onclick')?.match(/openTool\('(.+?)'\)/)?.[1];
            if (toolType) {
                createContent(toolType);
            }
        });
    });
}

function initializeCreationCards() {
    // Creation card interactions
    const creationCards = document.querySelectorAll('.creation-card');
    creationCards.forEach(card => {
        // Action button handlers
        const actionBtns = card.querySelectorAll('.action-btn');
        actionBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                const action = this.title || this.textContent.trim();
                handleCreationAction(action, card);
            });
        });

        // Add note button
        const addNoteBtn = card.querySelector('.add-note-btn');
        if (addNoteBtn) {
            addNoteBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                openAddNoteModal(card);
            });
        }
    });
}

function openTool(toolType) {
    showNotification(`Opening divine ${toolType} tool...`, 'info');

    // In a real implementation, you would:
    // 1. Check if sources are available
    // 2. Open the specific tool interface
    // 3. Pre-populate with source data

    switch (toolType) {
        case 'audio':
            openAudioTool();
            break;
        case 'video':
            openVideoTool();
            break;
        case 'mindmap':
            openMindMapTool();
            break;
        case 'reports':
            openReportsTool();
            break;
        case 'flashcards':
            openFlashcardsTool();
            break;
        case 'quiz':
            openQuizTool();
            break;
        default:
            showNotification('Tool not yet blessed by the gods', 'warning');
    }
}

function openAudioTool() {
    openToolModal('Audio Overview', `
        <div class="tool-form">
            <h4>Create Divine Audio Overview</h4>
            <div class="form-group">
                <label>Narrator Voice:</label>
                <select id="narratorVoice" class="form-control">
                    <option value="athena">Athena (Wise Female)</option>
                    <option value="zeus">Zeus (Powerful Male)</option>
                    <option value="apollo">Apollo (Melodic Male)</option>
                    <option value="artemis">Artemis (Clear Female)</option>
                </select>
            </div>
            <div class="form-group">
                <label>Audio Style:</label>
                <select id="audioStyle" class="form-control">
                    <option value="overview">Overview Summary</option>
                    <option value="detailed">Detailed Analysis</option>
                    <option value="story">Story Format</option>
                    <option value="lecture">Lecture Style</option>
                </select>
            </div>
            <div class="form-group">
                <label>Background Music:</label>
                <select id="backgroundMusic" class="form-control">
                    <option value="none">None</option>
                    <option value="ambient">Ambient Temple</option>
                    <option value="classical">Classical Greek</option>
                    <option value="nature">Divine Nature</option>
                </select>
            </div>
            <button class="divine-btn" onclick="generateAudio()">
                <i class="fas fa-music"></i>
                Create Divine Audio
            </button>
        </div>
    `);
}

function openVideoTool() {
    openToolModal('Video Overview', `
        <div class="tool-form">
            <h4>Create Divine Video Overview</h4>
            <div class="form-group">
                <label>Video Style:</label>
                <select id="videoStyle" class="form-control">
                    <option value="presentation">Presentation Style</option>
                    <option value="documentary">Documentary</option>
                    <option value="animated">Animated Explanation</option>
                    <option value="slideshow">Enhanced Slideshow</option>
                </select>
            </div>
            <div class="form-group">
                <label>Visual Theme:</label>
                <select id="visualTheme" class="form-control">
                    <option value="greek">Greek Temple</option>
                    <option value="modern">Modern Academic</option>
                    <option value="cosmic">Cosmic Divine</option>
                    <option value="nature">Natural Elements</option>
                </select>
            </div>
            <div class="form-group">
                <label>Duration:</label>
                <select id="videoDuration" class="form-control">
                    <option value="short">2-3 minutes</option>
                    <option value="medium">5-7 minutes</option>
                    <option value="long">10-15 minutes</option>
                    <option value="detailed">20+ minutes</option>
                </select>
            </div>
            <button class="divine-btn" onclick="generateVideo()">
                <i class="fas fa-video"></i>
                Create Divine Video
            </button>
        </div>
    `);
}

function openMindMapTool() {
    openToolModal('Mind Map', `
        <div class="tool-form">
            <h4>Create Divine Mind Map</h4>
            <div class="form-group">
                <label>Map Style:</label>
                <select id="mapStyle" class="form-control">
                    <option value="hierarchical">Hierarchical Tree</option>
                    <option value="radial">Radial Constellation</option>
                    <option value="network">Network Web</option>
                    <option value="timeline">Timeline Flow</option>
                </select>
            </div>
            <div class="form-group">
                <label>Focus Area:</label>
                <input type="text" id="focusArea" class="form-control" placeholder="e.g., Key Concepts, Relationships, Timeline">
            </div>
            <div class="form-group">
                <label>Complexity Level:</label>
                <select id="complexityLevel" class="form-control">
                    <option value="simple">Simple Overview</option>
                    <option value="moderate">Moderate Detail</option>
                    <option value="complex">Complex Analysis</option>
                    <option value="comprehensive">Comprehensive Map</option>
                </select>
            </div>
            <button class="divine-btn" onclick="generateMindMap()">
                <i class="fas fa-project-diagram"></i>
                Create Divine Map
            </button>
        </div>
    `);
}

function openReportsTool() {
    openToolModal('Divine Reports', `
        <div class="tool-form">
            <h4>Generate Divine Reports</h4>
            <div class="form-group">
                <label>Report Type:</label>
                <select id="reportType" class="form-control">
                    <option value="summary">Executive Summary</option>
                    <option value="analysis">Detailed Analysis</option>
                    <option value="comparison">Comparative Study</option>
                    <option value="research">Research Report</option>
                </select>
            </div>
            <div class="form-group">
                <label>Focus Areas:</label>
                <div class="checkbox-group">
                    <label><input type="checkbox" value="key-points"> Key Points</label>
                    <label><input type="checkbox" value="statistics"> Statistics</label>
                    <label><input type="checkbox" value="trends"> Trends</label>
                    <label><input type="checkbox" value="recommendations"> Recommendations</label>
                </div>
            </div>
            <div class="form-group">
                <label>Output Format:</label>
                <select id="outputFormat" class="form-control">
                    <option value="pdf">PDF Document</option>
                    <option value="word">Word Document</option>
                    <option value="html">Web Report</option>
                    <option value="presentation">Presentation</option>
                </select>
            </div>
            <button class="divine-btn" onclick="generateReport()">
                <i class="fas fa-scroll"></i>
                Generate Divine Report
            </button>
        </div>
    `);
}

function openFlashcardsTool() {
    openToolModal('Divine Flashcards', `
        <div class="tool-form">
            <h4>Create Divine Flashcards</h4>
            <div class="form-group">
                <label>Card Type:</label>
                <select id="cardType" class="form-control">
                    <option value="definition">Definition Cards</option>
                    <option value="qa">Question & Answer</option>
                    <option value="concept">Concept Cards</option>
                    <option value="formula">Formula Cards</option>
                </select>
            </div>
            <div class="form-group">
                <label>Number of Cards:</label>
                <select id="cardCount" class="form-control">
                    <option value="10">10 Cards</option>
                    <option value="25">25 Cards</option>
                    <option value="50">50 Cards</option>
                    <option value="100">100 Cards</option>
                </select>
            </div>
            <div class="form-group">
                <label>Difficulty Level:</label>
                <select id="difficultyLevel" class="form-control">
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                    <option value="expert">Expert</option>
                </select>
            </div>
            <button class="divine-btn" onclick="generateFlashcards()">
                <i class="fas fa-layer-group"></i>
                Create Divine Flashcards
            </button>
        </div>
    `);
}

function openQuizTool() {
    openToolModal('Divine Quiz', `
        <div class="tool-form">
            <h4>Create Divine Quiz</h4>
            <div class="form-group">
                <label>Question Types:</label>
                <div class="checkbox-group">
                    <label><input type="checkbox" value="multiple-choice" checked> Multiple Choice</label>
                    <label><input type="checkbox" value="true-false"> True/False</label>
                    <label><input type="checkbox" value="short-answer"> Short Answer</label>
                    <label><input type="checkbox" value="essay"> Essay Questions</label>
                </div>
            </div>
            <div class="form-group">
                <label>Number of Questions:</label>
                <select id="questionCount" class="form-control">
                    <option value="5">5 Questions</option>
                    <option value="10">10 Questions</option>
                    <option value="20">20 Questions</option>
                    <option value="50">50 Questions</option>
                </select>
            </div>
            <div class="form-group">
                <label>Quiz Difficulty:</label>
                <select id="quizDifficulty" class="form-control">
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                    <option value="mixed">Mixed Difficulty</option>
                </select>
            </div>
            <button class="divine-btn" onclick="generateQuiz()">
                <i class="fas fa-question-circle"></i>
                Create Divine Quiz
            </button>
        </div>
    `);
}

function openToolModal(title, content) {
    const modal = document.createElement('div');
    modal.className = 'modal tool-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-magic"></i> ${title}</h3>
                <button class="close-btn" onclick="closeToolModal()">&times;</button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
        </div>
    `;

    modal.style.display = 'flex';
    document.body.appendChild(modal);

    // Close on backdrop click
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeToolModal();
        }
    });

    window.currentToolModal = modal;
}

function closeToolModal() {
    if (window.currentToolModal) {
        document.body.removeChild(window.currentToolModal);
        window.currentToolModal = null;
    }
}

// Content generation functions
async function generateAudio() {
    const voice = document.getElementById('narratorVoice').value;
    const style = document.getElementById('audioStyle').value;
    const music = document.getElementById('backgroundMusic').value;

    await createContentAPI('audio', {
        voice,
        style,
        backgroundMusic: music
    });

    closeToolModal();
}

async function generateVideo() {
    const style = document.getElementById('videoStyle').value;
    const theme = document.getElementById('visualTheme').value;
    const duration = document.getElementById('videoDuration').value;

    await createContentAPI('video', {
        style,
        theme,
        duration
    });

    closeToolModal();
}

async function generateMindMap() {
    const style = document.getElementById('mapStyle').value;
    const focus = document.getElementById('focusArea').value;
    const complexity = document.getElementById('complexityLevel').value;

    await createContentAPI('mindmap', {
        style,
        focusArea: focus,
        complexity
    });

    closeToolModal();
}

async function generateReport() {
    const type = document.getElementById('reportType').value;
    const format = document.getElementById('outputFormat').value;
    const focusAreas = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
        .map(cb => cb.value);

    await createContentAPI('reports', {
        type,
        format,
        focusAreas
    });

    closeToolModal();
}

async function generateFlashcards() {
    const type = document.getElementById('cardType').value;
    const count = document.getElementById('cardCount').value;
    const difficulty = document.getElementById('difficultyLevel').value;

    await createContentAPI('flashcards', {
        type,
        count: parseInt(count),
        difficulty
    });

    closeToolModal();
}

async function generateQuiz() {
    const types = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
        .map(cb => cb.value);
    const count = document.getElementById('questionCount').value;
    const difficulty = document.getElementById('quizDifficulty').value;

    await createContentAPI('quiz', {
        questionTypes: types,
        count: parseInt(count),
        difficulty
    });

    closeToolModal();
}

async function createContentAPI(type, options) {
    showNotification(`Creating divine ${type}... The muses are at work`, 'info');

    try {
        const response = await fetch('/api/generate-content', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: type,
                options: options
            })
        });

        const result = await response.json();

        if (result.success) {
            showNotification(result.message, 'success');
            addToCreatedContent(type, result);
            loadCreatedContent();
        } else {
            showNotification('Creation failed - The gods require more power', 'error');
        }
    } catch (error) {
        console.error('Generation error:', error);
        showNotification('Divine creation interrupted', 'error');
    }
}

function createContent(type) {
    openTool(type);
}

function handleCreationAction(action, card) {
    const creationTitle = card.querySelector('h4, h5').textContent;

    switch (action.toLowerCase()) {
        case 'play':
        case 'take quiz':
        case 'study':
            showNotification(`Opening ${creationTitle}...`, 'info');
            break;
        case 'edit':
            showNotification(`Editing ${creationTitle}...`, 'info');
            break;
        case 'share':
            showNotification(`Sharing ${creationTitle}...`, 'info');
            break;
        default:
            showNotification(`Action: ${action} on ${creationTitle}`, 'info');
    }
}

function openAddNoteModal(card) {
    const creationTitle = card.querySelector('h4, h5').textContent;

    const modal = document.createElement('div');
    modal.className = 'modal note-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-sticky-note"></i> Add Note to ${creationTitle}</h3>
                <button class="close-btn" onclick="closeNoteModal()">&times;</button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label>Note:</label>
                    <textarea id="noteText" class="form-control" rows="5" placeholder="Add your divine insights..."></textarea>
                </div>
                <div class="form-group">
                    <label>Note Type:</label>
                    <select id="noteType" class="form-control">
                        <option value="insight">Insight</option>
                        <option value="question">Question</option>
                        <option value="improvement">Improvement</option>
                        <option value="reminder">Reminder</option>
                    </select>
                </div>
                <button class="divine-btn" onclick="saveNote('${creationTitle}')">
                    <i class="fas fa-save"></i>
                    Save Note
                </button>
            </div>
        </div>
    `;

    modal.style.display = 'flex';
    document.body.appendChild(modal);

    window.currentNoteModal = modal;
}

function closeNoteModal() {
    if (window.currentNoteModal) {
        document.body.removeChild(window.currentNoteModal);
        window.currentNoteModal = null;
    }
}

function saveNote(creationTitle) {
    const noteText = document.getElementById('noteText').value;
    const noteType = document.getElementById('noteType').value;

    if (noteText.trim()) {
        showNotification(`Note added to ${creationTitle}`, 'success');
        closeNoteModal();
    } else {
        showNotification('Please enter a note', 'warning');
    }
}

function addToCreatedContent(type, result) {
    const newContent = {
        id: generateId(),
        type: type,
        title: result.title || `${capitalizeFirst(type)} Creation`,
        description: result.description || `Divine ${type} created by the muses`,
        url: result.url,
        createdAt: new Date().toISOString()
    };

    createdContent.unshift(newContent);
}

function loadCreatedContent() {
    // In a real implementation, this would load from your API
    // For now, we'll just refresh the display
    updateCreatedContentDisplay();
}

function updateCreatedContentDisplay() {
    // This would update the recent creations section
    // with any new content that has been created
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
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

// Add dynamic styles for tool modal
const toolModalStyle = document.createElement('style');
toolModalStyle.textContent = `
    .tool-modal .modal-content {
        max-width: 600px;
        width: 90%;
    }

    .tool-form {
        padding: 1rem 0;
    }

    .tool-form h4 {
        color: var(--olympus-gold);
        font-family: var(--font-divine);
        margin-bottom: 1.5rem;
        text-align: center;
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-group label {
        display: block;
        color: var(--marble-white);
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    .form-control {
        width: 100%;
        background: rgba(248, 246, 240, 0.1);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 8px;
        padding: 0.75rem;
        color: var(--marble-white);
        font-family: var(--font-modern);
    }

    .form-control:focus {
        outline: none;
        border-color: var(--olympus-gold);
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
    }

    .form-control option {
        background: var(--temple-stone);
        color: var(--marble-white);
    }

    .checkbox-group {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 0.5rem;
    }

    .checkbox-group label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0;
        cursor: pointer;
    }

    .checkbox-group input[type="checkbox"] {
        width: auto;
        margin: 0;
    }

    .divine-btn {
        width: 100%;
        margin-top: 1rem;
        justify-content: center;
    }
`;

document.head.appendChild(toolModalStyle);

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // ESC to close modals
    if (e.key === 'Escape') {
        if (window.currentToolModal) {
            closeToolModal();
        }
        if (window.currentNoteModal) {
            closeNoteModal();
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

    if (e.ctrlKey && e.key === 'c' && !e.target.closest('input, textarea')) {
        e.preventDefault();
        window.location.href = '/chat';
    }
});