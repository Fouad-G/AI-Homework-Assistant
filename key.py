


# OpenRouter API-Schlüssel
API_KEY = "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"  # Dein OpenRouter API-Schlüssel

# Endpunkt-URL für OpenRouter API
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Modell für die Anfrage
MODEL_NAME = "deepseek/deepseek-r1-distill-llama-70b:free"  # DeepSeek-Modell über OpenRouter

# Funktion zur Kommunikation mit der OpenRouter-API
def openrouter_chat(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-app.com",  # Optional: Ersetze durch deine Website oder App-Name
        "X-Title": "YourAppName",  # Optional: Wird für Rankings auf openrouter.ai genutzt
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response_json = response.json()

        # Überprüfung, ob die Antwort eine gültige Ausgabe enthält
        if "choices" in response_json and response_json["choices"]:
            return response_json["choices"][0]["message"]["content"]
        else:
            return f"Fehler in der Antwort: {response_json}"

    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"

# Beispielhafte Nutzung der Funktion
if __name__ == "__main__":
    user_input = "Was sind die Vorteile von KI im Bildungsbereich?"
    antwort = openrouter_chat(user_input)
    print("OpenRouter-Antwort:", antwort)
