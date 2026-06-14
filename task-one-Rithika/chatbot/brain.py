
import random  

KNOWLEDGE_BASE = {

    "hello": [
        "Hello! I'm DEX — your AI assistant at DecodeLabs. How can I help?",
        "Hey there! DEX online and ready. What's on your mind?",
        "Hello! Great to have you here. Ask me anything!"
    ],
    "hi": [
        "Hi! DEX here. What would you like to know?",
        "Hey! What can I do for you today?"
    ],
    "hey": [
        "Hey! What's up? Ask me something.",
        "Hey there! DEX at your service."
    ],
    "good morning": [
        "Good morning! Hope your day is going great. How can I help?",
        "Morning! Ready to learn something about AI today?"
    ],
    "good afternoon": [
        "Good afternoon! How can I assist you?",
        "Afternoon! What's on your mind today?"
    ],
    "good evening": [
        "Good evening! DEX is still running. What do you need?",
        "Evening! What can I help you with?"
    ],

    "who are you": [
        "I'm DEX — Automated Rule-based Interaction Agent. Built by a DecodeLabs AI intern!",
        "I'm a rule-based chatbot. Project 1 of the DecodeLabs AI Internship 2026."
    ],
    "what are you": [
        "I'm a rule-based AI chatbot. No machine learning — just pure logic and dictionaries!",
        "I'm DEX. I match your input to predefined rules and respond accordingly."
    ],
    "what is your name": [
        "My name is DEX — Automated Rule-based Interaction Agent.",
        "You can call me DEX!"
    ],
    "who made you": [
        "I was built by an AI intern at DecodeLabs as Project 1.",
        "A DecodeLabs intern created me. Their very first AI project!"
    ],
    "how old are you": [
        "I was born this week. Fresh out of the IDE!",
        "Brand new — Project 1, Batch 2026."
    ],

    "how are you": [
        "Running at 100% efficiency. No bugs detected... yet.",
        "All systems operational! Thanks for asking.",
        "I don't have feelings, but my logic gates are firing perfectly!"
    ],
    "are you okay": [
        "Perfectly fine! No runtime errors to report.",
        "All good on my end. How about you?"
    ],
    "are you real": [
        "Real code? Yes. Real intelligence? That's a philosophical debate.",
        "I'm real in the sense that I run on a real machine. But I'm not sentient!"
    ],

    "what is ai": [
        "AI (Artificial Intelligence) is the simulation of human intelligence by machines — enabling them to learn, reason, and solve problems.",
        "AI refers to systems that perform tasks normally requiring human intelligence: recognizing speech, making decisions, understanding language."
    ],
    "what is machine learning": [
        "Machine Learning is a subset of AI where systems learn from data instead of being explicitly programmed. Unlike me — I follow strict rules!",
        "ML allows computers to learn patterns from data and improve over time without being manually reprogrammed."
    ],
    "what is deep learning": [
        "Deep Learning uses neural networks with many layers to recognize complex patterns. It powers image recognition, voice assistants, and LLMs.",
        "Deep Learning is a subset of ML inspired by the human brain, using layered neural networks to learn from huge amounts of data."
    ],
    "what is a neural network": [
        "A neural network is a system of algorithms loosely modeled after the human brain. It processes data through layers of connected nodes.",
        "Neural networks are the backbone of modern AI. They learn by adjusting weights between neurons during training."
    ],
    "what is nlp": [
        "NLP stands for Natural Language Processing — it's how computers understand and generate human language. I use a very basic version of it!",
        "NLP is the branch of AI that deals with text and speech. Chatbots, translators, and summarizers all use NLP."
    ],
    "what is a chatbot": [
        "A chatbot is a program that simulates conversation. I'm rule-based — the simplest and most transparent kind!",
        "Chatbots interact with users via text or voice. There are two types: rule-based (like me) and AI-powered (like ChatGPT)."
    ],
    "what is llm": [
        "LLM stands for Large Language Model — massive neural networks trained on text. Examples: GPT-4, Claude, Gemini. They're probabilistic, unlike me!",
        "LLMs predict the next word based on patterns from billions of text documents. That's how they generate human-like responses."
    ],
    "difference between ai and ml": [
        "AI is the broad goal of making machines smart. ML is one technique to achieve it. All ML is AI, but not all AI is ML.",
        "Think of AI as the destination and ML as one of the roads to get there."
    ],
    "what is rule based ai": [
        "Rule-based AI uses explicit logic — dictionaries, if-else — to respond. Fully transparent, zero hallucination risk.",
        "Rule-based AI is 100% deterministic. Every response is hand-coded. You always know exactly why it said what it said."
    ],

    "what is this project": [
        "This is Project 1 of the DecodeLabs AI Internship — a Rule-Based Chatbot built using control flow and dictionary logic.",
        "Project 1: Rule-Based AI Chatbot. The goal is mastering deterministic logic before moving to ML models."
    ],
    "what is decodelabs": [
        "DecodeLabs is a tech training organization running a 4-week AI internship for Batch 2026.",
        "DecodeLabs builds real AI projects with interns to create industry-ready portfolios."
    ],
    "help": [
        (
            "\n  Here's what I understand:\n"
            "  ─────────────────────────────────────────\n"
            "  Greetings   : hello, hi, hey, good morning\n"
            "  About me    : who are you, what is your name\n"
            "  Status      : how are you, are you real\n"
            "  AI Concepts : what is ai, what is ml, what is deep learning\n"
            "                what is nlp, what is llm, what is a chatbot\n"
            "                what is a neural network\n"
            "                difference between ai and ml\n"
            "  Project     : what is this project, what is decodelabs\n"
            "  Fun         : tell me a joke, motivate me\n"
            "  Exit        : quit / exit / bye\n"
            "  ─────────────────────────────────────────"
        )
    ],


    "tell me a joke": [
         "Why don't skeletons fight each other? Because they don't have the guts!",
        "Why did the scarecrow win an award? Because he was outstanding in his field.",
        "Why don't eggs tell jokes? They'd crack each other up.",
        "What do you call a bear with no teeth? A gummy bear.",
        "What did one wall say to the other wall? I'll meet you at the corner.",
        "Why can't your nose be 12 inches long? Because then it would be a foot.",
        "What do you call cheese that isn't yours? Nacho cheese.",
        "Why did the cookie go to the doctor? Because it was feeling crumbly."
    ],
    "motivate me": [
        "Every expert was once a beginner. Keep building. 🚀",
        "The best AI engineers didn't start with transformers. They started exactly where you are.",
        "You're not just writing code. You're building the foundation of your career. Keep going."
    ],
    "thank you": [
        "You're welcome! Keep building great things.",
        "Happy to help! That's what I'm here for.",
        "Anytime! Come back if you have more questions."
    ],
    "thanks": [
        "No problem at all!",
        "Glad I could help!"
    ],
    "bye": [
        "Goodbye! Keep coding and keep learning. 👋",
        "See you next session! ARIA signing off.",
    ],
    "goodbye": [
        "Goodbye! Come back anytime.",
        "See you! Stay curious. "
    ],
    "see you": [
        "See you later! Keep building.",
        "Take care!"
    ],
}


EXIT_COMMANDS = {"quit", "exit", "q", "stop", "close"}


FALLBACK_RESPONSES = [
    "I don't have a rule for that yet. Type 'help' to see what I understand.",
    "Hmm, I'm not programmed for that. I only know what I'm taught — I'm rule-based!",
    "That's outside my current knowledge base. Try typing 'help'.",
    "I didn't understand that. Remember: I'm deterministic, not intelligent!",
]

def get_response(clean_input: str) -> str:
    
    if clean_input in KNOWLEDGE_BASE:
        return random.choice(KNOWLEDGE_BASE[clean_input])

    for key in KNOWLEDGE_BASE:
        if key in clean_input:
            return random.choice(KNOWLEDGE_BASE[key])

    return random.choice(FALLBACK_RESPONSES)


def is_exit_command(clean_input: str) -> bool:
   
    return clean_input in EXIT_COMMANDS