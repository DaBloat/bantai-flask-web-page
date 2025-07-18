def chat():
    user_input = request.get_json()["message"]
    system_prompt = "You are an AI assistant specialized in Occupational Safety and Health (OSH) laws in the Philippines. Provide accurate, concise, and helpful information based on the Philippine OSH standards (RA 11058, DOLE D.O. 198-18)."
    prompt = f"""
                <|system|>
                {system_prompt}</s>
                <|user|>
                {user_input}</s>
                <|assistant|>"""

    # Token count for prompt
    prompt_tokens = len(tokenizer.encode(prompt))
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.6,
            "top_p": 0.9,
            "repetition_penalty": 1.1
        }
    }
    response = requests.post(HF_API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        return jsonify({"error": "API call failed", "details": response.text}), 500

    output = response.json()
    generated_text = output[0]["generated_text"]

    # Get only model reply (strip prompt from full response)
    start_idx = generated_text.find("<|assistant|>") + len("<|assistant|>")
    reply = generated_text[start_idx:].strip()
    print(reply)
    total_tokens = len(tokenizer.encode(generated_text))
    completion_tokens = total_tokens - prompt_tokens

    return jsonify({
        "reply": reply,
        "tokens": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        }
    })

"""
def chat():
    user_input = request.get_json()["message"]
    return jsonify({"reply": 'LOL BRO TESTING!'})
"""