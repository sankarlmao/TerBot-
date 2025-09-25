#!/usr/bin/env python3

import time
import random
from typing import List

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
except Exception as exc:
    print("Missing dependencies. Install with:")
    print("  pip install transformers torch")
    raise exc

MODEL_NAME = "microsoft/DialoGPT-medium"
MAX_HISTORY_TURNS = 6
MAX_NEW_TOKENS = 150
TEMPERATURE = 0.8
TOP_K = 50
TOP_P = 0.95
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

PERSONA = (
    "You are TerBot: a polite, encouraging, slightly witty CLI assistant. "
    "You are formal but relaxed, humble when appropriate, helpful, and concise. "
    "Keep replies short-to-moderate length unless the user asks for detail."
)

TYPING_SPEED = 0.01

class Colors:
    RESET = "\033[0m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"

def load_model_and_tokenizer(model_name: str):
    print(f"{Colors.YELLOW}Loading model ({model_name}) on {DEVICE}...{Colors.RESET}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.to(DEVICE)
    model.eval()
    return tokenizer, model

def typing_print(prefix: str, message: str):
    print(prefix, end="", flush=True)
    for c in message:
        print(c, end="", flush=True)
        time.sleep(TYPING_SPEED)
    print(Colors.RESET)

def build_input_from_history(tokenizer, history: List[str], persona: str):
    eos = tokenizer.eos_token or ""
    pieces = [persona.strip()] if persona else []
    pieces.extend([h.strip() for h in history if h.strip()])
    return (eos.join(pieces)) + eos

def generate_response(tokenizer, model, history: List[str]):
    input_text = build_input_from_history(tokenizer, history, PERSONA)
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        out_ids = model.generate(
            input_ids,
            do_sample=True,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            top_k=TOP_K,
            top_p=TOP_P,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    generated_ids = out_ids[0][input_ids.shape[-1]:]
    text = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()

    if text.lower().startswith("you are"):
        text = random.choice([
            "Sure — could you clarify that a bit?",
            "I hear you. Can you give me a bit more detail?",
            "Alright. What specifically would you like me to do?"
        ])

    return text

def main():
    tokenizer, model = load_model_and_tokenizer(MODEL_NAME)

    print(f"{Colors.YELLOW}--- TerBot (local model) ---{Colors.RESET}")
    typing_print(f"{Colors.BLUE}TerBot: {Colors.RESET}", "Hello — I'm TerBot. Type 'exit' or 'quit' to end the chat.")
    conversation_history: List[str] = []

    while True:
        try:
            user_input = input(f"{Colors.GREEN}You: {Colors.RESET}").strip()
            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit", "bye"):
                typing_print(f"{Colors.BLUE}TerBot: {Colors.RESET}", "Goodbye! Wishing you a productive day.")
                break

            conversation_history.append(user_input)
            max_items = MAX_HISTORY_TURNS * 2
            if len(conversation_history) > max_items:
                conversation_history = conversation_history[-max_items:]

            bot_reply = generate_response(tokenizer, model, conversation_history)
            conversation_history.append(bot_reply)

            typing_print(f"{Colors.BLUE}TerBot: {Colors.RESET}", bot_reply)

        except KeyboardInterrupt:
            print("")
            typing_print(f"{Colors.BLUE}TerBot: {Colors.RESET}", "Goodbye! Shutting down gracefully.")
            break
        except Exception as e:
            typing_print(f"{Colors.BLUE}TerBot: {Colors.RESET}", f"Error: {e}. Resetting conversation.")
            conversation_history = []
            continue

if __name__ == "__main__":
    main()
