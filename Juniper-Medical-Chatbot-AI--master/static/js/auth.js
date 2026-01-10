// Authentication Handler for Juniper

class AuthManager {
    constructor() {
        this.sessionToken = localStorage.getItem('juniper-session');
        this.currentUser = null;
        this.isGuest = !this.sessionToken;

        this.initElements();
        this.setupEventListeners();
        this.checkSession();
    }

    initElements() {
        // Modal elements
        this.authModal = document.getElementById('authModal');
        this.authModalClose = document.getElementById('authModalClose');
        this.loginForm = document.getElementById('loginForm');
        this.signupForm = document.getElementById('signupForm');
        this.userProfile = document.getElementById('userProfile');

        // Account button
        this.userAccountBtn = document.getElementById('userAccountBtn');
        this.userAccountText = document.getElementById('userAccountText');

        // Form elements
        this.loginFormElement = document.getElementById('loginFormElement');
        this.signupFormElement = document.getElementById('signupFormElement');
        this.logoutBtn = document.getElementById('logoutBtn');
    }

    setupEventListeners() {
        // Modal controls
        this.userAccountBtn?.addEventListener('click', () => this.openAuthModal());
        this.authModalClose?.addEventListener('click', () => this.closeAuthModal());

        // Close modal on backdrop click
        this.authModal?.addEventListener('click', (e) => {
            if (e.target === this.authModal) {
                this.closeAuthModal();
            }
        });

        // Form switches
        document.getElementById('showSignup')?.addEventListener('click', () => this.showSignupForm());
        document.getElementById('showLogin')?.addEventListener('click', () => this.showLoginForm());
        document.getElementById('continueAsGuest')?.addEventListener('click', () => this.continueAsGuest());
        document.getElementById('continueAsGuestSignup')?.addEventListener('click', () => this.continueAsGuest());

        // Form submissions
        this.loginFormElement?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        this.signupFormElement?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSignup();
        });

        this.logoutBtn?.addEventListener('click', () => this.handleLogout());
    }

    async checkSession() {
        if (!this.sessionToken) {
            this.updateUIForGuest();
            return;
        }

        try {
            const response = await fetch('/api/auth/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_token: this.sessionToken })
            });

            const data = await response.json();

            if (data.success && data.user) {
                this.currentUser = data.user;
                this.isGuest = false;
                this.updateUIForUser();
            } else {
                localStorage.removeItem('juniper-session');
                this.sessionToken = null;
                this.updateUIForGuest();
            }
        } catch (error) {
            console.error('Session validation error:', error);
            this.updateUIForGuest();
        }
    }

    async handleLogin() {
        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;
        const errorDiv = document.getElementById('loginError');

        errorDiv.textContent = '';

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (data.success) {
                // Save current guest conversations before switching user
                const guestConversations = localStorage.getItem('juniper-conversations');

                this.sessionToken = data.session_token;
                this.currentUser = data.user;
                this.isGuest = false;

                localStorage.setItem('juniper-session', this.sessionToken);

                // Switch to user-specific storage
                this.switchToUserStorage();

                this.updateUIForUser();
                this.closeAuthModal();

                // Reset form
                this.loginFormElement.reset();

                // Reload page to load user's chat history
                window.location.reload();
            } else {
                errorDiv.textContent = data.message || 'Login failed';
            }
        } catch (error) {
            console.error('Login error:', error);
            errorDiv.textContent = 'Login failed. Please try again.';
        }
    }

    async handleSignup() {
        const username = document.getElementById('signupUsername').value.trim();
        const email = document.getElementById('signupEmail').value.trim();
        const password = document.getElementById('signupPassword').value;
        const errorDiv = document.getElementById('signupError');

        errorDiv.textContent = '';

        if (password.length < 6) {
            errorDiv.textContent = 'Password must be at least 6 characters';
            return;
        }

        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });

            const data = await response.json();

            if (data.success) {
                // Auto-login after successful signup
                errorDiv.textContent = 'Account created! Logging in...';
                errorDiv.style.color = '#48bb78';

                setTimeout(() => {
                    document.getElementById('loginEmail').value = email;
                    document.getElementById('loginPassword').value = password;
                    this.showLoginForm();
                    this.handleLogin();
                }, 1000);
            } else {
                errorDiv.textContent = data.message || 'Signup failed';
                errorDiv.style.color = '#f56565';
            }
        } catch (error) {
            console.error('Signup error:', error);
            errorDiv.textContent = 'Signup failed. Please try again.';
            errorDiv.style.color = '#f56565';
        }
    }

    async handleLogout() {
        try {
            await fetch('/api/auth/logout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_token: this.sessionToken })
            });
        } catch (error) {
            console.error('Logout error:', error);
        }

        // Save current user's chat history before logout
        this.saveUserChatHistory();

        localStorage.removeItem('juniper-session');
        this.sessionToken = null;
        this.currentUser = null;
        this.isGuest = true;

        // Switch back to guest storage (clear current conversations)
        this.switchToGuestStorage();

        this.updateUIForGuest();
        this.closeAuthModal();

        // Reload page to clear chat
        window.location.reload();
    }

    openAuthModal() {
        if (this.currentUser) {
            this.showProfile();
        } else {
            this.showLoginForm();
        }
        this.authModal.classList.add('active');
    }

    closeAuthModal() {
        this.authModal.classList.remove('active');
    }

    showLoginForm() {
        this.loginForm.classList.remove('hidden');
        this.signupForm.classList.add('hidden');
        this.userProfile.classList.add('hidden');
        document.getElementById('loginError').textContent = '';
    }

    showSignupForm() {
        this.loginForm.classList.add('hidden');
        this.signupForm.classList.remove('hidden');
        this.userProfile.classList.add('hidden');
        document.getElementById('signupError').textContent = '';
    }

    showProfile() {
        this.loginForm.classList.add('hidden');
        this.signupForm.classList.add('hidden');
        this.userProfile.classList.remove('hidden');

        document.getElementById('profileUsername').textContent = this.currentUser.username;
        document.getElementById('profileEmail').textContent = this.currentUser.email;
    }

    continueAsGuest() {
        this.closeAuthModal();
    }

    updateUIForUser() {
        if (this.userAccountText) {
            this.userAccountText.textContent = this.currentUser.username;
        }
    }

    updateUIForGuest() {
        if (this.userAccountText) {
            this.userAccountText.textContent = 'Login / Sign up';
        }
    }

    isLoggedIn() {
        return !this.isGuest && this.currentUser !== null;
    }

    getSessionToken() {
        return this.sessionToken;
    }

    getCurrentUser() {
        return this.currentUser;
    }

    switchToUserStorage() {
        // When switching to logged-in user, load their specific chat history
        if (this.currentUser && this.currentUser.id) {
            const userKey = `juniper-conversations-user-${this.currentUser.id}`;
            const userConversations = localStorage.getItem(userKey);

            if (userConversations) {
                // Load user's saved conversations
                localStorage.setItem('juniper-conversations', userConversations);
            } else {
                // Clear conversations for new user
                localStorage.removeItem('juniper-conversations');
            }
        }
    }

    switchToGuestStorage() {
        // When logging out, clear the active conversations
        localStorage.removeItem('juniper-conversations');
    }

    saveUserChatHistory() {
        // Save current chat history to user-specific key
        if (this.currentUser && this.currentUser.id) {
            const currentConversations = localStorage.getItem('juniper-conversations');
            if (currentConversations) {
                const userKey = `juniper-conversations-user-${this.currentUser.id}`;
                localStorage.setItem(userKey, currentConversations);
            }
        }
    }
}

// Initialize auth manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.authManager = new AuthManager();
    console.log('🔐 Auth manager initialized');
});
