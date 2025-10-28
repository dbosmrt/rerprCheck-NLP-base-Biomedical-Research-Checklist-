import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Say hi in one line"}]
)
print(response["message"]["content"])