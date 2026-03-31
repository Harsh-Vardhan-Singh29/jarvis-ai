def ask_llm(command, context=""):
    try:
        import ollama

        full_prompt = f"{context}\nUser: {command}"

        response = ollama.chat(
            model="phi",
            messages=[{"role": "user", "content": full_prompt}],
            options={"num_ctx": 256}
        )

        return response["message"]["content"]

    except Exception as e:
        print("LLM ERROR:", e)
        return "AI mode is currently offline."