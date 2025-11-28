"""
FAQ Chatbot with Simple NLP
Python Backend Version

This can be used with Flask or FastAPI for a web API
or run standalone in terminal
"""

import re
from typing import List, Dict, Optional

# FAQ Database
FAQ_DATABASE = [
    {
        'keywords': ['hours', 'open', 'opening', 'timing', 'schedule', 'when'],
        'answer': 'We are open Monday to Friday, 9 AM to 6 PM, and Saturday 10 AM to 4 PM. We are closed on Sundays.'
    },
    {
        'keywords': ['price', 'cost', 'pricing', 'fee', 'charge', 'expensive', 'cheap'],
        'answer': 'Our pricing starts at $29/month for the basic plan, $79/month for professional, and $149/month for enterprise. We also offer custom pricing for large organizations.'
    },
    {
        'keywords': ['contact', 'email', 'phone', 'reach', 'call'],
        'answer': 'You can reach us at support@example.com or call us at +1-555-0123. We typically respond within 24 hours.'
    },
    {
        'keywords': ['location', 'address', 'where', 'office'],
        'answer': 'Our main office is located at 123 Tech Street, San Francisco, CA 94102. We also have remote support available worldwide.'
    },
    {
        'keywords': ['return', 'refund', 'money back', 'cancel'],
        'answer': 'We offer a 30-day money-back guarantee. If you are not satisfied, you can request a full refund within 30 days of purchase.'
    },
    {
        'keywords': ['shipping', 'delivery', 'ship', 'deliver'],
        'answer': 'We offer free shipping on orders over $50. Standard delivery takes 3-5 business days, and express delivery takes 1-2 business days.'
    },
    {
        'keywords': ['payment', 'pay', 'credit card', 'paypal', 'visa', 'mastercard'],
        'answer': 'We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and bank transfers.'
    },
    {
        'keywords': ['support', 'help', 'assistance', 'problem', 'issue'],
        'answer': 'Our support team is available 24/7 via email and chat. You can also check our help center at help.example.com for instant answers.'
    },
    {
        'keywords': ['account', 'register', 'signup', 'login', 'create'],
        'answer': 'You can create an account by clicking the "Sign Up" button on our homepage. Registration is free and takes less than a minute!'
    },
    {
        'keywords': ['feature', 'features', 'what do', 'capabilities', 'functionality'],
        'answer': 'Our platform offers real-time analytics, automated reporting, team collaboration tools, API access, and mobile apps for iOS and Android.'
    },
    {
        'keywords': ['hello', 'hi', 'hey', 'greetings'],
        'answer': 'Hello! How can I help you today?'
    },
    {
        'keywords': ['thank', 'thanks', 'appreciate'],
        'answer': "You're welcome! Is there anything else I can help you with?"
    },
    {
        'keywords': ['bye', 'goodbye', 'see you'],
        'answer': 'Goodbye! Feel free to come back if you have more questions. Have a great day!'
    }
]


class FAQChatbot:
    """Simple NLP-based FAQ Chatbot"""
    
    def __init__(self, faq_data: List[Dict]):
        self.faq_database = faq_data
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text by converting to lowercase and removing punctuation
        """
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text.strip()
    
    def find_best_match(self, user_input: str) -> str:
        """
        Find the best matching FAQ answer using keyword scoring
        """
        processed = self.preprocess_text(user_input)
        words = processed.split()
        
        best_match = None
        max_score = 0
        
        for faq in self.faq_database:
            score = 0
            
            for keyword in faq['keywords']:
                # Exact keyword match in the input
                if keyword in processed:
                    score += 2
                
                # Partial match - check if any word contains or is contained in keyword
                for word in words:
                    if keyword in word or word in keyword:
                        score += 1
            
            if score > max_score:
                max_score = score
                best_match = faq
        
        # Return answer if we have a confident match
        if max_score > 0 and best_match:
            return best_match['answer']
        
        return "I'm sorry, I don't have information about that. Please try rephrasing your question or contact our support team at support@example.com for personalized assistance."
    
    def chat(self, message: str) -> str:
        """
        Main chat method - returns bot response for given message
        """
        return self.find_best_match(message)


def run_terminal_chatbot():
    """
    Run chatbot in terminal/console mode
    """
    chatbot = FAQChatbot(FAQ_DATABASE)
    
    print("=" * 50)
    print("FAQ Chatbot - Terminal Version")
    print("=" * 50)
    print("\nHi! I'm your FAQ assistant.")
    print("Ask me anything about our services, pricing, support, or general information!")
    print("Type 'quit' or 'exit' to end the conversation.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nBot: Goodbye! Have a great day!")
            break
        
        if not user_input:
            continue
        
        response = chatbot.chat(user_input)
        print(f"\nBot: {response}\n")


# Flask API Example
def create_flask_app():
    """
    Create Flask app for web API
    Install: pip install flask flask-cors
    """
    try:
        from flask import Flask, request, jsonify
        from flask_cors import CORS
    except ImportError:
        print("Flask not installed. Install with: pip install flask flask-cors")
        return None
    
    app = Flask(__name__)
    CORS(app)  # Enable CORS for frontend requests
    
    chatbot = FAQChatbot(FAQ_DATABASE)
    
    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        response = chatbot.chat(message)
        return jsonify({'response': response})
    
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'})
    
    return app


# FastAPI Example
def create_fastapi_app():
    """
    Create FastAPI app for web API
    Install: pip install fastapi uvicorn
    """
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import BaseModel
    except ImportError:
        print("FastAPI not installed. Install with: pip install fastapi uvicorn")
        return None
    
    app = FastAPI()
    
    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    chatbot = FAQChatbot(FAQ_DATABASE)
    
    class ChatRequest(BaseModel):
        message: str
    
    class ChatResponse(BaseModel):
        response: str
    
    @app.post("/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest):
        response = chatbot.chat(request.message)
        return ChatResponse(response=response)
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    return app


if __name__ == "__main__":
    # Run terminal chatbot
    run_terminal_chatbot()
    
    # To run Flask API instead, uncomment:
    # app = create_flask_app()
    # if app:
    #     app.run(debug=True, port=5000)
    
    # To run FastAPI instead, uncomment and run: uvicorn chatbot:app --reload
    # app = create_fastapi_app()