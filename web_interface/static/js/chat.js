// Chat Application JavaScript
class TourismChatbot {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.isLoading = false;
        this.currentLanguage = 'en';
        
        this.initializeElements();
        this.bindEvents();
        this.checkServerHealth();
    }

    initializeElements() {
        // Main elements
        this.welcomeSection = document.getElementById('welcomeSection');
        this.chatContainer = document.getElementById('chatContainer');
        this.startChatBtn = document.getElementById('startChatBtn');
        this.backBtn = document.getElementById('backBtn');
        
        // Chat elements
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.charCount = document.getElementById('charCount');
        this.voiceBtn = document.getElementById('voiceBtn');
        
        // Loading and modal elements
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.errorModal = document.getElementById('errorModal');
        this.errorMessage = document.getElementById('errorMessage');
        this.retryBtn = document.getElementById('retryBtn');
        this.closeModalBtn = document.getElementById('closeModalBtn');
        this.closeErrorModal = document.getElementById('closeErrorModal');
        
        // Language selector
        this.languageSelect = document.getElementById('languageSelect');
        
        // Quick action buttons
        this.quickBtns = document.querySelectorAll('.quick-btn');
    }

    bindEvents() {
        // Start chat button
        this.startChatBtn.addEventListener('click', () => this.startChat());
        
        // Back button
        this.backBtn.addEventListener('click', () => this.showWelcome());
        
        // Send message
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Character count
        this.messageInput.addEventListener('input', () => this.updateCharCount());
        
        // Voice button
        this.voiceBtn.addEventListener('click', () => this.toggleVoiceInput());
        
        // Quick action buttons
        this.quickBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const question = e.currentTarget.dataset.question;
                this.startChat();
                setTimeout(() => {
                    this.messageInput.value = question;
                    this.sendMessage();
                }, 300);
            });
        });
        
        // Modal events
        this.closeErrorModal.addEventListener('click', () => this.hideErrorModal());
        this.closeModalBtn.addEventListener('click', () => this.hideErrorModal());
        this.retryBtn.addEventListener('click', () => this.retryConnection());
        
        // Language selector
        this.languageSelect.addEventListener('change', (e) => {
            this.currentLanguage = e.target.value;
            this.updateLanguage();
        });
        
        // Click outside modal to close
        this.errorModal.addEventListener('click', (e) => {
            if (e.target === this.errorModal) {
                this.hideErrorModal();
            }
        });
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    async checkServerHealth() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            if (data.status === 'healthy') {
                console.log('✅ Server is healthy');
            } else {
                console.warn('⚠️ Server health check failed:', data.message);
            }
        } catch (error) {
            console.error('❌ Health check failed:', error);
        }
    }

    startChat() {
        this.welcomeSection.style.display = 'none';
        this.chatContainer.style.display = 'flex';
        this.startChatBtn.style.display = 'none';
        
        // Add welcome message
        this.addBotMessage("Hello! Welcome to Sri Lanka Tourism Assistant. How can I help you today? You can ask me about attractions, food, transportation, accommodation, emergency services, and more!");
        
        // Focus on input
        setTimeout(() => {
            this.messageInput.focus();
        }, 100);
    }

    showWelcome() {
        this.chatContainer.style.display = 'none';
        this.welcomeSection.style.display = 'block';
        this.startChatBtn.style.display = 'flex';
        
        // Clear chat
        this.chatMessages.innerHTML = '';
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || this.isLoading) {
            return;
        }

        // Add user message to chat
        this.addUserMessage(message);
        
        // Clear input
        this.messageInput.value = '';
        this.updateCharCount();
        
        // Show loading
        this.setLoading(true);
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });

            const data = await response.json();
            
            if (data.success) {
                // Add bot responses
                data.messages.forEach(msg => {
                    this.addBotMessage(msg.content);
                });
            } else {
                throw new Error(data.error || 'Failed to get response');
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            this.showError(`Failed to send message: ${error.message}`);
            this.addBotMessage("I'm sorry, I'm having trouble connecting right now. Please try again in a moment.");
        } finally {
            this.setLoading(false);
        }
    }

    addUserMessage(content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user';
        
        const time = new Date().toLocaleTimeString();
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-user"></i>
            </div>
            <div class="message-content">
                ${this.escapeHtml(content)}
                <div class="message-time">${time}</div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addBotMessage(content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        
        const time = new Date().toLocaleTimeString();
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                ${this.formatBotMessage(content)}
                <div class="message-time">${time}</div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatBotMessage(content) {
        // Convert markdown-style formatting to HTML
        let formatted = this.escapeHtml(content);
        
        // Bold text
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Italic text
        formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Line breaks
        formatted = formatted.replace(/\n/g, '<br>');
        
        // Emojis
        formatted = formatted.replace(/🇱🇰/g, '<span style="font-size: 1.2em;">🇱🇰</span>');
        formatted = formatted.replace(/🚨/g, '<span style="font-size: 1.2em;">🚨</span>');
        formatted = formatted.replace(/🚑/g, '<span style="font-size: 1.2em;">🚑</span>');
        formatted = formatted.replace(/🚒/g, '<span style="font-size: 1.2em;">🚒</span>');
        formatted = formatted.replace(/👮/g, '<span style="font-size: 1.2em;">👮</span>');
        formatted = formatted.replace(/🏥/g, '<span style="font-size: 1.2em;">🏥</span>');
        formatted = formatted.replace(/🍛/g, '<span style="font-size: 1.2em;">🍛</span>');
        formatted = formatted.replace(/🥘/g, '<span style="font-size: 1.2em;">🥘</span>');
        formatted = formatted.replace(/🥞/g, '<span style="font-size: 1.2em;">🥞</span>');
        formatted = formatted.replace(/🍜/g, '<span style="font-size: 1.2em;">🍜</span>');
        formatted = formatted.replace(/🍖/g, '<span style="font-size: 1.2em;">🍖</span>');
        formatted = formatted.replace(/🥥/g, '<span style="font-size: 1.2em;">🥥</span>');
        formatted = formatted.replace(/🚂/g, '<span style="font-size: 1.2em;">🚂</span>');
        formatted = formatted.replace(/🚌/g, '<span style="font-size: 1.2em;">🚌</span>');
        formatted = formatted.replace(/🚕/g, '<span style="font-size: 1.2em;">🚕</span>');
        formatted = formatted.replace(/🚗/g, '<span style="font-size: 1.2em;">🚗</span>');
        formatted = formatted.replace(/✈️/g, '<span style="font-size: 1.2em;">✈️</span>');
        formatted = formatted.replace(/🏨/g, '<span style="font-size: 1.2em;">🏨</span>');
        formatted = formatted.replace(/🏠/g, '<span style="font-size: 1.2em;">🏠</span>');
        formatted = formatted.replace(/🏡/g, '<span style="font-size: 1.2em;">🏡</span>');
        formatted = formatted.replace(/🏕️/g, '<span style="font-size: 1.2em;">🏕️</span>');
        formatted = formatted.replace(/🏛️/g, '<span style="font-size: 1.2em;">🏛️</span>');
        formatted = formatted.replace(/🍽️/g, '<span style="font-size: 1.2em;">🍽️</span>');
        formatted = formatted.replace(/🚌/g, '<span style="font-size: 1.2em;">🚌</span>');
        formatted = formatted.replace(/📞/g, '<span style="font-size: 1.2em;">📞</span>');
        
        return formatted;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    updateCharCount() {
        const count = this.messageInput.value.length;
        this.charCount.textContent = `${count}/500`;
        
        // Change color when approaching limit
        if (count > 450) {
            this.charCount.style.color = '#dc3545';
        } else if (count > 400) {
            this.charCount.style.color = '#ffc107';
        } else {
            this.charCount.style.color = '#999';
        }
    }

    setLoading(loading) {
        this.isLoading = loading;
        this.sendBtn.disabled = loading;
        this.messageInput.disabled = loading;
        
        if (loading) {
            this.loadingOverlay.style.display = 'flex';
        } else {
            this.loadingOverlay.style.display = 'none';
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorModal.style.display = 'flex';
    }

    hideErrorModal() {
        this.errorModal.style.display = 'none';
    }

    async retryConnection() {
        this.hideErrorModal();
        await this.checkServerHealth();
    }

    toggleVoiceInput() {
        // Voice input functionality (placeholder for future implementation)
        alert('Voice input feature coming soon!');
    }

    updateLanguage() {
        // Update UI based on selected language
        const languageNames = {
            'en': 'English',
            'si': 'සිංහල',
            'ta': 'தமிழ்'
        };
        
        console.log(`Language changed to: ${languageNames[this.currentLanguage]}`);
        
        // Here you could update the UI text based on language
        // For now, we'll just log the change
    }

    // Utility method to add typing indicator
    addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-indicator';
        typingDiv.id = 'typing-indicator';
        
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }

    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
}

// Add typing indicator styles
const style = document.createElement('style');
style.textContent = `
    .typing-indicator .message-content {
        background: #f8f9fa !important;
        border: 2px solid #e9ecef !important;
        border-bottom-left-radius: 5px !important;
    }
    
    .typing-dots {
        display: flex;
        gap: 4px;
        padding: 10px 0;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #667eea;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% {
            transform: scale(0.8);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// Initialize the chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.tourismChatbot = new TourismChatbot();
});

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TourismChatbot;
}