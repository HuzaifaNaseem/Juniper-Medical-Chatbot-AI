// ==========================================
// JUNIPER - MEDICAL RESEARCH ASSISTANT
// Frontend JavaScript
// ==========================================

class JuniperChat {
    constructor() {
        // DOM Elements
        this.chatContainer = document.getElementById('chatContainer');
        this.chatForm = document.getElementById('chatForm');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.clearChatButton = document.getElementById('clearChat');
        this.themeToggle = document.getElementById('themeToggle');
        this.charCount = document.getElementById('charCount');
        this.statusIndicator = document.getElementById('statusIndicator');
        this.loadingOverlay = document.getElementById('loadingOverlay');

        // State
        this.conversationId = this.generateConversationId();
        this.isProcessing = false;
        this.messageHistory = [];
        this.theme = localStorage.getItem('juniper-theme') || 'light';

        // Initialize
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.applyTheme();
        this.setupAutoResize();
        this.loadChatHistory();
    }

    // ==========================================
    // EVENT LISTENERS
    // ==========================================
    setupEventListeners() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSendMessage();
        });

        // Input character count
        this.messageInput.addEventListener('input', () => {
            this.updateCharCount();
        });

        // Enter to send (Shift+Enter for new line)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSendMessage();
            }
        });

        // Clear chat
        this.clearChatButton.addEventListener('click', () => {
            this.clearChat();
        });

        // Theme toggle
        this.themeToggle.addEventListener('click', () => {
            this.toggleTheme();
        });

        // Suggested query buttons
        document.querySelectorAll('.query-button').forEach(button => {
            button.addEventListener('click', () => {
                const query = button.getAttribute('data-query');
                this.messageInput.value = query;
                this.handleSendMessage();
            });
        });
    }

    setupAutoResize() {
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
        });
    }

    // ==========================================
    // MESSAGE HANDLING
    // ==========================================
    async handleSendMessage() {
        const message = this.messageInput.value.trim();

        if (!message || this.isProcessing) {
            return;
        }

        if (message.length > 2000) {
            this.showError('Message is too long. Maximum 2000 characters.');
            return;
        }

        // Hide welcome message if visible
        this.hideWelcomeMessage();

        // Add user message to UI
        this.addMessage('user', message);

        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        this.updateCharCount();

        // Show typing indicator
        this.showTypingIndicator();

        // Update status
        this.setStatus('processing', 'Processing...');
        this.isProcessing = true;
        this.sendButton.disabled = true;

        try {
            // Send to backend
            const response = await this.sendMessageToBackend(message);

            // Remove typing indicator
            this.removeTypingIndicator();

            // Add assistant response
            this.addMessage('assistant', response.response, response.sources);

            // Save to history
            this.saveMessageToHistory('user', message);
            this.saveMessageToHistory('assistant', response.response);

        } catch (error) {
            console.error('Error:', error);
            this.removeTypingIndicator();
            this.addMessage('assistant',
                'I apologize, but I encountered an error processing your request. Please try again or rephrase your question.',
                [],
                true
            );
            this.setStatus('error', 'Error occurred');
        } finally {
            this.isProcessing = false;
            this.sendButton.disabled = false;
            this.setStatus('ready', 'Ready');
        }
    }

    async sendMessageToBackend(message) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_id: this.conversationId
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to get response');
        }

        return await response.json();
    }

    // ==========================================
    // UI MESSAGE RENDERING
    // ==========================================
    addMessage(sender, text, sources = [], isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'user'
            ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>'
            : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"></path><path d="M2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const headerDiv = document.createElement('div');
        headerDiv.className = 'message-header';

        const senderSpan = document.createElement('span');
        senderSpan.className = 'message-sender';
        senderSpan.textContent = sender === 'user' ? 'You' : 'Juniper';

        const timeSpan = document.createElement('span');
        timeSpan.className = 'message-time';
        timeSpan.textContent = this.getCurrentTime();

        headerDiv.appendChild(senderSpan);
        headerDiv.appendChild(timeSpan);

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.textContent = text;

        if (isError) {
            textDiv.style.background = 'rgba(245, 101, 101, 0.1)';
            textDiv.style.borderLeft = '3px solid var(--error)';
        }

        contentDiv.appendChild(headerDiv);
        contentDiv.appendChild(textDiv);

        // Add sources if available
        if (sources && sources.length > 0) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'message-sources';

            sources.forEach((source, index) => {
                const badge = document.createElement('span');
                badge.className = 'source-badge';
                badge.innerHTML = `
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                    </svg>
                    Source ${index + 1}
                `;
                sourcesDiv.appendChild(badge);
            });

            contentDiv.appendChild(sourcesDiv);
        }

        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);

        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typingIndicator';

        typingDiv.innerHTML = `
            <div class="message-avatar">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                    <path d="M2 17l10 5 10-5M2 12l10 5 10-5"></path>
                </svg>
            </div>
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;

        this.chatContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }

    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    hideWelcomeMessage() {
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.display = 'none';
        }
    }

    // ==========================================
    // CHAT MANAGEMENT
    // ==========================================
    clearChat() {
        if (confirm('Are you sure you want to clear the conversation?')) {
            // Remove all messages
            const messages = this.chatContainer.querySelectorAll('.message, .typing-indicator');
            messages.forEach(msg => msg.remove());

            // Show welcome message again
            const welcomeMessage = document.querySelector('.welcome-message');
            if (welcomeMessage) {
                welcomeMessage.style.display = 'flex';
            }

            // Clear history
            this.messageHistory = [];
            localStorage.removeItem('juniper-chat-history');

            // Generate new conversation ID
            this.conversationId = this.generateConversationId();

            // Reset status
            this.setStatus('ready', 'Ready');
        }
    }

    saveMessageToHistory(sender, text) {
        this.messageHistory.push({
            sender,
            text,
            timestamp: new Date().toISOString()
        });

        // Save to localStorage (last 50 messages)
        const historyToSave = this.messageHistory.slice(-50);
        localStorage.setItem('juniper-chat-history', JSON.stringify(historyToSave));
    }

    loadChatHistory() {
        const savedHistory = localStorage.getItem('juniper-chat-history');
        if (savedHistory) {
            try {
                this.messageHistory = JSON.parse(savedHistory);

                if (this.messageHistory.length > 0) {
                    this.hideWelcomeMessage();
                    this.messageHistory.forEach(msg => {
                        this.addMessage(msg.sender, msg.text);
                    });
                }
            } catch (error) {
                console.error('Error loading chat history:', error);
                localStorage.removeItem('juniper-chat-history');
            }
        }
    }

    // ==========================================
    // THEME MANAGEMENT
    // ==========================================
    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme();
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.theme);
        localStorage.setItem('juniper-theme', this.theme);
    }

    // ==========================================
    // UI UTILITIES
    // ==========================================
    updateCharCount() {
        const count = this.messageInput.value.length;
        this.charCount.textContent = count;

        if (count > 1800) {
            this.charCount.style.color = 'var(--error)';
        } else if (count > 1500) {
            this.charCount.style.color = 'var(--warning)';
        } else {
            this.charCount.style.color = 'var(--text-tertiary)';
        }
    }

    setStatus(type, text) {
        this.statusIndicator.className = `status-indicator ${type}`;
        this.statusIndicator.querySelector('.status-text').textContent = text;
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
        }, 100);
    }

    showError(message) {
        // Simple alert for now - can be enhanced with a toast notification
        alert(message);
    }

    // ==========================================
    // UTILITIES
    // ==========================================
    generateConversationId() {
        return 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// ==========================================
// INITIALIZE APPLICATION
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    window.juniperChat = new JuniperChat();
    console.log('🌿 Juniper Medical Research Assistant initialized');
});

// ==========================================
// SERVICE WORKER (for PWA support - optional)
// ==========================================
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment when service worker is implemented
        // navigator.serviceWorker.register('/sw.js')
        //     .then(reg => console.log('Service Worker registered'))
        //     .catch(err => console.log('Service Worker registration failed'));
    });
}
