import json
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# --- Load model & tokenizer ---
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# --- Memory setup ---
memory_file = "terbot_memory.json"
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        memory = json.load(f)
else:
    memory = {"conversation_history": []}

print("🤖 TerBot: Hello! I remember what you tell me. Type 'bye' to exit.")

# --- Chat loop ---
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "bye":
        print("🤖 TerBot: Goodbye! I’ll remember our chat.")
        break

    # Build context from memory (last few exchanges)
    past_dialogue = ""
    for line in memory["conversation_history"][-6:]:  # last 3 exchanges
        past_dialogue += line + "\n"
    prompt = past_dialogue + f"User: {user_input}\nTerBot:"

    # Encode and generate
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output_ids = model.generate(input_ids, max_length=input_ids.shape[1]+50, do_sample=True, temperature=0.8)
    response = tokenizer.decode(output_ids[:, input_ids.shape[1]:][0], skip_special_tokens=True)

    print(f"🤖 TerBot: {response}")

    # Save conversation to memory
    memory["conversation_history"].append(f"User: {user_input}")
    memory["conversation_history"].append(f"TerBot: {response}")

    with open(memory_file, "w") as f:
        json.dump(memory, f, indent=4)
