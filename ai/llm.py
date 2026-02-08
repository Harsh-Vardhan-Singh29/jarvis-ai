import ollama

def ask_llm(prompt, memory_context=""):
    full_prompt = f"""
You are Jarvis, a concise assistant.
Answer in 2–3 sentences unless the user asks for detail.

Context:
{memory_context}

User:
{prompt}
"""
    response = ollama.chat(
        model="phi",
        messages=[{"role": "user", "content": full_prompt}],
        options={"num_ctx": 256}  # smaller context = faster
    )
    return response["message"]["content"]
