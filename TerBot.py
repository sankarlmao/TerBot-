import random
import time
from datetime import datetime
import nltk
from nltk.chat.util import Chat, reflections

# --- ANSI Color Codes for Terminal Output ---
class Colors:
    """A class to hold ANSI color codes for terminal text."""
    RESET = '\033[0m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'

def print_bot_message(message):
    """Prints a message from the bot with a typing effect."""
    if not message: return # Don't print empty messages
    print(f"{Colors.BLUE}Bot: ", end='', flush=True)
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print(Colors.RESET)

def main():
    """The main function to run the chatbot loop."""
    chatbot_memory = {}

    # --- NLTK Chatbot Patterns ---
    # The pairs define the patterns and responses.
    # Regular expressions are used for pattern matching.
    # %1, %2, etc., are placeholders for captured groups from the user's input.
    pairs = [
        [
            r"my name is (.*)",
            ["Hello %1, how are you today?", "Nice to meet you, %1! How can I help?",]
        ],
        [
            r"what is my name",
            ["I'm not sure, you haven't told me yet! You can say 'my name is...'",]
        ],
        [
            r"hi|hey|hello",
            ["Hello!", "Hey there!", "Hi! What's on your mind?"]
        ],
        [
            r"how are you ?",
            ["I'm doing great, thanks for asking! I'm a machine, so I'm always at 100%.", "I'm doing well, how about you?",]
        ],
        [
            r"sorry (.*)",
            ["It's alright.", "No need to apologize.",]
        ],
        [
            r"i am (.*) (good|well|okay|ok)",
            ["Nice to hear that!", "Alright, great!",]
        ],
        [
            r"(.*) age?",
            ["I am a timeless computer program.", "Age is just a number, and in my case, it's a lot of them.",]
        ],
        [
            r"what (.*) want ?",
            ["I want to help you out!", "My goal is to have an interesting conversation.",]
        ],
        [
            r"what is your name|who are you",
            ["I'm a chatbot created in Python. You can call me PyBot.", "I am a humble CLI bot."]
        ],
        [
            r"what can you do|help",
            ["I can chat with you about many things. I can also tell you the time and date. Try asking me something!",]
        ],
        [
            r"quit|bye|exit|goodbye",
            ["Bye for now. Take care!", "It was nice chatting with you. Goodbye!",]
        ],
        [
            r"i work in (.*)",
            ["%1 must be an interesting place to work!", "That's cool! What's your role at %1?",]
        ],
        [
            r"i (.*) (like|love|enjoy) (.*)",
            ["Why do you %2 %3?", "That's great to hear! What is it about %3 that you %2?",]
        ],
        [
            r"i feel (.*)",
            ["Why do you feel %1?", "I hope you feel better soon if you're feeling down.", "It's interesting that you feel %1.",]
        ],
        [
            r"the time",
            [f"The current time is {datetime.now().strftime('%I:%M %p')}."]
        ],
        [
            r"the date",
            [f"Today's date is {datetime.now().strftime('%A, %B %d, %Y')}."]
        ],
        [
            r"(.*)", # Default fallback pattern
            [
                "That's an interesting point. Can you tell me more?",
                "I see. And what do you think about that?",
                "How does that make you feel?",
                "I'm not sure I understand completely. Could you rephrase?",
            ]
        ]
    ]

    print(f"{Colors.YELLOW}--- Intelligent CLI Chatbot v3.0 ---{Colors.RESET}")
    print_bot_message("Hello! I'm a more advanced chatbot now. Let's talk. Type 'bye' to quit.")

    # Create the Chat instance
    chat = Chat(pairs, reflections)

    while True:
        try:
            user_input = input(f"{Colors.GREEN}You: {Colors.RESET}")

            # Get response from the NLTK chat engine
            bot_reply = chat.respond(user_input)

            # --- Handle Memory ---
            # Check if user told us their name using the NLTK pattern
            if "my name is" in user_input.lower():
                name = user_input.split("is", 1)[1].strip().capitalize()
                chatbot_memory['name'] = name
                # Overwrite the NLTK response to be more personal
                bot_reply = f"Nice to meet you, {name}! I'll remember that."

            # Check if user is asking for their name
            elif "what is my name" in user_input.lower():
                if 'name' in chatbot_memory:
                    bot_reply = f"Your name is {chatbot_memory['name']}, of course!"
                else:
                    bot_reply = "I don't think you've told me your name yet."

            # Personalize greetings if name is known
            elif user_input.lower() in ("hi", "hey", "hello") and 'name' in chatbot_memory:
                bot_reply = f"Hello again, {chatbot_memory['name']}!"

            # --- Print response and check for exit ---
            print_bot_message(bot_reply)

            if user_input.lower() in ["bye", "exit", "quit", "goodbye"]:
                break

        except KeyboardInterrupt:
            print("\n")
            print_bot_message("Goodbye! Shutting down gracefully.")
            break
        except Exception as e:
            print_bot_message(f"Oops! Something went wrong: {e}")
            break

if __name__ == "__main__":
    main()

