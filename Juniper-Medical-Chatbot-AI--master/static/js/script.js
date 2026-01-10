// Juniper - Modern UI JavaScript

class JuniperChat {
    constructor() {
        // Elements
        this.chatArea = document.getElementById('chatArea');
        this.chatForm = document.getElementById('chatForm');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.voiceBtn = document.getElementById('voiceBtn');
        this.charCount = document.getElementById('charCount');
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        this.welcomeScreen = document.getElementById('welcomeScreen');
        this.sidebar = document.getElementById('sidebar');
        this.menuBtn = document.getElementById('menuBtn');
        this.sidebarClose = document.getElementById('sidebarClose');

        // State
        this.conversationId = this.generateId();
        this.isProcessing = false;
        this.theme = localStorage.getItem('juniper-theme') || 'light';
        this.conversations = this.loadConversations();
        this.currentMessages = [];
        this.historyList = document.getElementById('historyList');

        // Voice recognition state
        this.isRecording = false;
        this.recognition = null;
        this.selectedLanguage = 'en'; // Default to English
        this.initVoiceRecognition();

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.applyTheme();
        this.setupAutoResize();
        this.renderHistory();
    }

    setupEventListeners() {
        // Form submit
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSend();
        });

        // Character count
        this.messageInput.addEventListener('input', () => {
            this.updateCharCount();
            this.autoResize();
        });

        // Enter to send
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSend();
            }
        });

        // Query cards
        document.querySelectorAll('.query-card').forEach(card => {
            card.addEventListener('click', () => {
                const query = card.getAttribute('data-query');
                this.messageInput.value = query;
                this.handleSend();
            });
        });

        // Sidebar controls
        if (this.menuBtn) {
            this.menuBtn.addEventListener('click', () => {
                this.sidebar.classList.add('active');
            });
        }

        if (this.sidebarClose) {
            this.sidebarClose.addEventListener('click', () => {
                this.sidebar.classList.remove('active');
            });
        }

        // Action buttons
        document.getElementById('newChat')?.addEventListener('click', () => this.newChat());
        document.getElementById('clearHistory')?.addEventListener('click', () => this.clearHistory());
        document.getElementById('themeToggle')?.addEventListener('click', () => this.toggleTheme());

        // Voice button
        if (this.voiceBtn) {
            this.voiceBtn.addEventListener('click', () => this.toggleVoiceRecording());
        }

        // Language selector buttons
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const lang = e.target.getAttribute('data-lang');
                this.switchLanguage(lang);
            });
        });
    }

    setupAutoResize() {
        this.messageInput.addEventListener('input', () => {
            this.autoResize();
        });
    }

    autoResize() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 150) + 'px';
    }

    updateCharCount() {
        const count = this.messageInput.value.length;
        this.charCount.textContent = count;
    }

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
        timeSpan.textContent = this.getTime();

        headerDiv.appendChild(senderSpan);
        headerDiv.appendChild(timeSpan);

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.textContent = text;

        if (isError) {
            textDiv.style.background = 'rgba(245, 101, 101, 0.1)';
            textDiv.style.borderLeft = '3px solid #f56565';
        }

        contentDiv.appendChild(headerDiv);
        contentDiv.appendChild(textDiv);

        // Add sources
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

        this.chatArea.appendChild(messageDiv);
        this.scrollToBottom();

        // Save message to current messages array for chat history
        this.currentMessages.push({
            sender: sender,
            text: text,
            sources: sources,
            isError: isError,
            timestamp: Date.now()
        });
    }

    showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing';
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

        this.chatArea.appendChild(typingDiv);
        this.scrollToBottom();
    }

    removeTyping() {
        const typing = document.getElementById('typingIndicator');
        if (typing) typing.remove();
    }

    newChat() {
        // Save current conversation if it has messages
        if (this.currentMessages.length > 0) {
            this.saveConversation();
        }

        const messages = this.chatArea.querySelectorAll('.message, .typing');
        messages.forEach(msg => msg.remove());

        if (this.welcomeScreen) {
            this.welcomeScreen.classList.remove('hidden');
        }

        this.conversationId = this.generateId();
        this.currentMessages = [];
        this.setStatus('ready', 'Ready');
        this.renderHistory();

        // Close sidebar on mobile
        if (this.sidebar) {
            this.sidebar.classList.remove('active');
        }
    }

    clearHistory() {
        if (confirm('Clear all conversation history? This cannot be undone.')) {
            localStorage.removeItem('juniper-conversations');
            this.conversations = [];
            this.renderHistory();
            this.newChat();
        }
    }

    saveConversation() {
        const firstMessage = this.currentMessages[0];
        if (!firstMessage) return;

        const conversation = {
            id: this.conversationId,
            title: firstMessage.text.substring(0, 50) + (firstMessage.text.length > 50 ? '...' : ''),
            messages: this.currentMessages,
            timestamp: Date.now()
        };

        // Add to beginning of array
        this.conversations.unshift(conversation);

        // Keep only last 10 conversations
        if (this.conversations.length > 10) {
            this.conversations = this.conversations.slice(0, 10);
        }

        localStorage.setItem('juniper-conversations', JSON.stringify(this.conversations));

        // Also save to user-specific storage if logged in
        this.saveToUserStorage();

        this.renderHistory();
    }

    loadConversations() {
        try {
            const saved = localStorage.getItem('juniper-conversations');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.error('Error loading conversations:', error);
            return [];
        }
    }

    renderHistory() {
        if (!this.historyList) return;

        if (this.conversations.length === 0) {
            this.historyList.innerHTML = `
                <div class="empty-history">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                    <p>No conversations yet</p>
                </div>
            `;
            return;
        }

        this.historyList.innerHTML = this.conversations.map(conv => `
            <div class="history-item ${conv.id === this.conversationId ? 'active' : ''}" data-id="${conv.id}">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
                <div class="history-item-content">
                    <div class="history-item-title">${conv.title}</div>
                    <div class="history-item-time">${this.formatTime(conv.timestamp)}</div>
                </div>
                <button class="history-item-delete" data-id="${conv.id}">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                </button>
            </div>
        `).join('');

        // Add click listeners
        this.historyList.querySelectorAll('.history-item').forEach(item => {
            item.addEventListener('click', (e) => {
                if (!e.target.closest('.history-item-delete')) {
                    const convId = item.getAttribute('data-id');
                    this.loadConversation(convId);
                }
            });
        });

        // Add delete listeners
        this.historyList.querySelectorAll('.history-item-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const convId = btn.getAttribute('data-id');
                this.deleteConversation(convId);
            });
        });
    }

    loadConversation(convId) {
        const conversation = this.conversations.find(c => c.id === convId);
        if (!conversation) return;

        // Clear current chat
        const messages = this.chatArea.querySelectorAll('.message, .typing');
        messages.forEach(msg => msg.remove());

        if (this.welcomeScreen) {
            this.welcomeScreen.classList.add('hidden');
        }

        this.conversationId = conversation.id;
        this.currentMessages = conversation.messages;

        // Render messages
        conversation.messages.forEach(msg => {
            this.addMessage(msg.sender, msg.text, msg.sources || [], msg.isError || false);
        });

        this.renderHistory();

        // Close sidebar on mobile
        if (this.sidebar) {
            this.sidebar.classList.remove('active');
        }
    }

    deleteConversation(convId) {
        if (!confirm('Delete this conversation?')) return;

        this.conversations = this.conversations.filter(c => c.id !== convId);
        localStorage.setItem('juniper-conversations', JSON.stringify(this.conversations));

        // Also update user-specific storage if logged in
        this.saveToUserStorage();

        this.renderHistory();

        if (convId === this.conversationId) {
            this.newChat();
        }
    }

    formatTime(timestamp) {
        const now = Date.now();
        const diff = now - timestamp;
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) return 'Just now';
        if (minutes < 60) return `${minutes}m ago`;
        if (hours < 24) return `${hours}h ago`;
        if (days < 7) return `${days}d ago`;

        const date = new Date(timestamp);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }

    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme();
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.theme);
        localStorage.setItem('juniper-theme', this.theme);
    }

    setStatus(type, text) {
        this.statusText.textContent = text;
        this.statusDot.style.background = type === 'ready' ? '#48bb78' : type === 'processing' ? '#ed8936' : '#f56565';
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatArea.scrollTop = this.chatArea.scrollHeight;
        }, 100);
    }

    getTime() {
        const now = new Date();
        return now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }

    generateId() {
        return 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    saveToUserStorage() {
        // Save current conversations to user-specific storage if user is logged in
        if (window.authManager && window.authManager.getCurrentUser()) {
            const user = window.authManager.getCurrentUser();
            if (user && user.id) {
                const userKey = `juniper-conversations-user-${user.id}`;
                const currentConversations = localStorage.getItem('juniper-conversations');
                if (currentConversations) {
                    localStorage.setItem(userKey, currentConversations);
                }
            }
        }
    }

    initVoiceRecognition() {
        // Check if browser supports Web Speech API
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            console.warn('Speech recognition not supported in this browser');
            if (this.voiceBtn) {
                this.voiceBtn.style.display = 'none';
            }
            return;
        }

        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US'; // Will be updated based on selected language
        this.recognition.maxAlternatives = 1;

        this.recognition.onstart = () => {
            this.isRecording = true;
            this.voiceBtn.classList.add('recording');
            this.setStatus('processing', 'Listening...');
            this.messageInput.placeholder = 'Listening... Speak now';
        };

        this.recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            // Update textarea with interim results
            if (interimTranscript) {
                this.messageInput.value = finalTranscript + interimTranscript;
                this.updateCharCount();
                this.autoResize();
            }

            // If final result, update textarea
            if (finalTranscript) {
                this.messageInput.value = finalTranscript.trim();
                this.updateCharCount();
                this.autoResize();
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isRecording = false;
            this.voiceBtn.classList.remove('recording');
            this.setStatus('ready', 'Ready');
            this.messageInput.placeholder = 'Ask about medical topics...';

            if (event.error === 'no-speech') {
                this.setStatus('error', 'No speech detected');
                setTimeout(() => this.setStatus('ready', 'Ready'), 2000);
            } else if (event.error === 'not-allowed') {
                alert('Microphone access denied. Please enable microphone permissions in your browser settings.');
            } else {
                this.setStatus('error', 'Error: ' + event.error);
                setTimeout(() => this.setStatus('ready', 'Ready'), 2000);
            }
        };

        this.recognition.onend = () => {
            this.isRecording = false;
            this.voiceBtn.classList.remove('recording');
            this.setStatus('ready', 'Ready');
            this.updatePlaceholder();

            // Auto-send if there's text
            const message = this.messageInput.value.trim();
            if (message && message.length > 0) {
                // Small delay before sending to show the final transcript
                setTimeout(() => {
                    this.handleSend();
                }, 500);
            }
        };
    }

    toggleVoiceRecording() {
        if (!this.recognition) {
            alert('Voice input is not supported in your browser. Please use Chrome, Edge, or Safari.');
            return;
        }

        if (this.isProcessing) {
            return;
        }

        if (this.isRecording) {
            // Stop recording
            this.recognition.stop();
        } else {
            // Start recording
            try {
                this.messageInput.value = '';
                this.updateCharCount();
                // Update recognition language based on selected language
                this.recognition.lang = this.selectedLanguage === 'ur' ? 'ur-PK' : 'en-US';
                this.recognition.start();
            } catch (error) {
                console.error('Error starting recognition:', error);
                alert('Failed to start voice recognition. Please try again.');
            }
        }
    }

    switchLanguage(lang) {
        this.selectedLanguage = lang;

        // Update active state on buttons
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`.lang-btn[data-lang="${lang}"]`).classList.add('active');

        // Update placeholder text
        this.updatePlaceholder();

        // Save preference
        localStorage.setItem('juniper-language', lang);
    }

    updatePlaceholder() {
        if (this.selectedLanguage === 'ur') {
            this.messageInput.placeholder = 'Tibbi mawzoo ke bare mein poochen...';
        } else {
            this.messageInput.placeholder = 'Ask about medical topics...';
        }
    }

    async handleSend() {
        const message = this.messageInput.value.trim();

        if (!message || this.isProcessing) return;

        if (message.length > 2000) {
            alert('Message too long (max 2000 characters)');
            return;
        }

        // Hide welcome
        if (this.welcomeScreen) {
            this.welcomeScreen.classList.add('hidden');
        }

        // Add user message
        this.addMessage('user', message);

        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        this.updateCharCount();

        // Show typing
        this.showTyping();

        // Update status
        this.setStatus('processing', 'Processing...');
        this.isProcessing = true;
        this.sendBtn.disabled = true;

        try {
            const response = await this.sendToAPI(message, this.selectedLanguage);
            this.removeTyping();
            this.addMessage('assistant', response.response, response.sources);
        } catch (error) {
            console.error('Error:', error);
            this.removeTyping();
            const errorMsg = this.selectedLanguage === 'ur'
                ? 'Maafi, mujhe aik masla hua hai. Mehrbani karke dobara koshish karein.'
                : 'Sorry, I encountered an error. Please try again.';
            this.addMessage('assistant', errorMsg, [], true);
            this.setStatus('error', 'Error');
        } finally {
            this.isProcessing = false;
            this.sendBtn.disabled = false;
            this.setStatus('ready', 'Ready');
        }
    }

    async sendToAPI(message, language) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                conversation_id: this.conversationId,
                language: language
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to get response');
        }

        return await response.json();
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.juniperChat = new JuniperChat();
    console.log('🌿 Juniper initialized');
});
