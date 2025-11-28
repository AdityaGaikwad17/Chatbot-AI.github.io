// FAQ Database - Add your own questions and answers here
const faqDatabase = [
    {
        keywords: ['hours', 'open', 'opening', 'timing', 'schedule', 'when'],
        answer: 'We are open Monday to Friday, 9 AM to 6 PM, and Saturday 10 AM to 4 PM. We are closed on Sundays.'
    },
    {
        keywords: ['price', 'cost', 'pricing', 'fee', 'charge', 'expensive', 'cheap'],
        answer: 'Our pricing starts at $29/month for the basic plan, $79/month for professional, and $149/month for enterprise. We also offer custom pricing for large organizations.'
    },
    {
        keywords: ['contact', 'email', 'phone', 'reach', 'call'],
        answer: 'You can reach us at support@example.com or call us at +1-555-0123. We typically respond within 24 hours.'
    },
    {
        keywords: ['location', 'address', 'where', 'office'],
        answer: 'Our main office is located at 123 Tech Street, San Francisco, CA 94102. We also have remote support available worldwide.'
    },
    {
        keywords: ['return', 'refund', 'money back', 'cancel'],
        answer: 'We offer a 30-day money-back guarantee. If you are not satisfied, you can request a full refund within 30 days of purchase.'
    },
    {
        keywords: ['shipping', 'delivery', 'ship', 'deliver'],
        answer: 'We offer free shipping on orders over $50. Standard delivery takes 3-5 business days, and express delivery takes 1-2 business days.'
    },
    {
        keywords: ['payment', 'pay', 'credit card', 'paypal', 'visa', 'mastercard'],
        answer: 'We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and bank transfers.'
    },
    {
        keywords: ['support', 'help', 'assistance', 'problem', 'issue'],
        answer: 'Our support team is available 24/7 via email and chat. You can also check our help center at help.example.com for instant answers.'
    },
    {
        keywords: ['account', 'register', 'signup', 'login', 'create'],
        answer: 'You can create an account by clicking the "Sign Up" button on our homepage. Registration is free and takes less than a minute!'
    },
    {
        keywords: ['feature', 'features', 'what do', 'capabilities', 'functionality'],
        answer: 'Our platform offers real-time analytics, automated reporting, team collaboration tools, API access, and mobile apps for iOS and Android.'
    },
    {
        keywords: ['hello', 'hi', 'hey', 'greetings'],
        answer: 'Hello! How can I help you today?'
    },
    {
        keywords: ['thank', 'thanks', 'appreciate'],
        answer: 'You\'re welcome! Is there anything else I can help you with?'
    },
    {
        keywords: ['bye', 'goodbye', 'see you'],
        answer: 'Goodbye! Feel free to come back if you have more questions. Have a great day!'
    }
];

// Simple NLP - Text preprocessing
function preprocessText(text) {
    return text.toLowerCase()
        .replace(/[^\w\s]/g, '') // Remove punctuation
        .trim();
}

// Find best matching FAQ
function findBestMatch(userInput) {
    const processed = preprocessText(userInput);
    const words = processed.split(/\s+/);
    
    let bestMatch = null;
    let maxScore = 0;

    faqDatabase.forEach(faq => {
        let score = 0;
        faq.keywords.forEach(keyword => {
            if (processed.includes(keyword)) {
                score += 2; // Exact keyword match
            }
            words.forEach(word => {
                if (keyword.includes(word) || word.includes(keyword)) {
                    score += 1; // Partial match
                }
            });
        });

        if (score > maxScore) {
            maxScore = score;
            bestMatch = faq;
        }
    });

    // Threshold for confidence
    if (maxScore > 0) {
        return bestMatch.answer;
    }
    
    return "I'm sorry, I don't have information about that. Please try rephrasing your question or contact our support team at support@example.com for personalized assistance.";
}

// UI Functions
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');

function addMessage(content, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    typingIndicator.style.display = 'block';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

function handleSend() {
    const message = userInput.value.trim();
    
    if (message === '') return;
    
    // Add user message
    addMessage(message, true);
    userInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Simulate thinking time and get response
    setTimeout(() => {
        hideTypingIndicator();
        const response = findBestMatch(message);
        addMessage(response, false);
    }, 500 + Math.random() * 1000);
}

sendBtn.addEventListener('click', handleSend);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSend();
    }
});

// Focus input on load
userInput.focus();