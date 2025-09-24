import random
import time

# --- ANSI Color Codes for Terminal Output ---
# Makes the chat more readable and fun.
class Colors:
    """A class to hold ANSI color codes for terminal text."""
    RESET = '\033[0m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'

def print_bot_message(message):
    """Prints a message from the bot with a typing effect."""
    print(f"{Colors.BLUE}Bot: ", end='', flush=True)
    for char in message:
        print(char, end='', flush=True)
        # Adjust the sleep time to change typing speed
        time.sleep(0.03)
    print(Colors.RESET)

def get_bot_response(user_input):
    """
    Analyzes the user's input and returns a suitable response.
    This is the core logic of the chatbot.
    """
    # Convert input to lowercase to make matching case-insensitive.
    lowered_input = user_input.lower()

    # --- Pre-defined keyword-response pairs ---
    # The bot checks if any keyword in the key exists in the user's input.
    # The value is a list of possible responses, from which one is chosen randomly.
    response_map = {
        ("hello", "hi", "hey", "greetings"): [
            "Well hello there, human!",
            "Greetings, carbon-based life form. What can I do for you?",
            "Hi! Ready to chat?"
        ],
        ("how are you", "how's it going", "how are things"): [
            "I'm just a bunch of code, but I'm running smoothly!",
            "Functioning within expected parameters. How about you?",
            "Excellent, thanks for asking. All my circuits are buzzing!"
        ],
        ("what is your name", "who are you"): [
            "I am a humble CLI Bot, at your service.",
            "You can call me the 'Terminal Terminator'. Or just Bot.",
            "I don't have a name. The budget didn't cover it."
        ],
        ("joke", "tell me a joke"): [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my computer I needed a break, and now it won’t stop sending me Kit-Kat ads.",
            "Why did the scarecrow win an award? Because he was outstanding in his field!"
        ],
        ("weather",): [
            "I'm not connected to the internet, but it's always 72 degrees and sunny in my source code.",
            "My forecast: 100% chance of you typing something else interesting.",
            "You'll have to look out the window for that one. I'm windowless."
        ],
        ("what can you do", "help"): [
            "I can tell you a joke, ask how you are, or just have a simple chat.",
            "My main function is to demonstrate a basic rule-based chatbot without any APIs.",
            "Try asking me for a joke or tell me about your day!"
        ],
        ("bye", "exit", "quit", "goodbye"): [
            "Farewell! Don't get into too much trouble.",
            "See you later, alligator!",
            "Goodbye! It was fun processing your inputs."
        ]
    }

    # --- Default/Fallback responses ---
    # Used when no keywords are matched.
    fallback_responses = [
        "Hmm, that's an interesting thought. I'll have to ponder that.",
        "I'm not quite sure how to respond to that. Try asking me for a joke!",
        "My programming is a bit limited. Could you rephrase that?",
        "That went right over my virtual head. Ask me something else?"
    ]

    # Iterate through the response map to find a match
    for keywords, responses in response_map.items():
        if any(keyword in lowered_input for keyword in keywords):
            return random.choice(responses)

    # If no match is found, return a random fallback response
    return random.choice(fallback_responses)

def main():
    """The main function to run the chatbot loop."""
    print(f"{Colors.YELLOW}--- Witty CLI Chatbot ---{Colors.RESET}")
    print_bot_message("Hello! I'm a simple chatbot. Type 'bye' or 'exit' to quit.")

    while True:
        try:
            # Get user input
            user_input = input(f"{Colors.GREEN}You: {Colors.RESET}")

            # Check for exit condition
            if user_input.lower() in ["bye", "exit", "quit"]:
                print_bot_message(get_bot_response(user_input))
                break

            # Get and print the bot's response
            bot_reply = get_bot_response(user_input)
            print_bot_message(bot_reply)

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n") # Move to a new line
            print_bot_message("Goodbye! Shutting down gracefully.")
            break
        except Exception as e:
            # Handle any other unexpected errors
            print_bot_message(f"Oops! Something went wrong: {e}")
            break

if __name__ == "__main__":
    main()
