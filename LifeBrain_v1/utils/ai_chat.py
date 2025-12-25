# utils/ai_chat.py
import os
import random

OPENAI_KEY = os.getenv("OPENAI_KEY", "")

def ai_reply_local(text: str, mode: str = "default"):
    """Local fallback mini-chat without OpenAI API."""
    text = text.lower()

    if mode == "study":
        return random.choice([
            "Let's break that down step-by-step.",
            "Focus on the core concept first.",
            "Try solving smaller examples before the big one."
        ])
    if mode == "coach":
        return random.choice([
            "You got this! One step at a time.",
            "Keep going — consistency is key.",
            "Believe in yourself, progress takes time!"
        ])
    if mode == "friend":
        return random.choice([
            "Haha, tell me more! 😄",
            "That's cool — what's next?",
            "I'm here for you anytime."
        ])

    return random.choice([
        "Interesting — tell me more!",
        "How can I assist further?",
        "I can summarize or help explain if you'd like."
    ])

def ai_reply(text: str, mode: str = "default"):
    """Main AI reply: uses OpenAI if available, else local fallback."""
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY

            system_prompt = {
                "study": "You are a helpful study assistant. Be clear and concise.",
                "coach": "You are a motivational coach. Be short and positive.",
                "friend": "You are a friendly chat companion.",
            }.get(mode, "You are a helpful assistant.")

            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                max_tokens=200,
                temperature=0.7,
            )
            return resp.choices[0].message.content.strip()

        except Exception as e:
            return f"(AI error: {e})"
    else:
        return ai_reply_local(text, mode)
