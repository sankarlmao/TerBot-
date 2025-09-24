import sys
import time
import random
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from colorama import Fore, Style, init

init(autoreset=True)

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

def type_text(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def get_bot_response(user_input):
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    output_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(output_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

def main():
    print(Fore.CYAN + "Welcome to TerBot! Type 'exit' to quit." + Style.RESET_ALL)

    while True:
        user_input = input(Fore.YELLOW + "You: " + Style.RESET_ALL)
        if user_input.lower() == "exit":
            type_text(Fore.CYAN + "TerBot: Goodbye! 👋" + Style.RESET_ALL)
            break

        response = get_bot_response(user_input)
        type_text(Fore.CYAN + "TerBot: " + Style.RESET_ALL + response, delay=random.uniform(0.03, 0.08))

if __name__ == "__main__":
    main()
