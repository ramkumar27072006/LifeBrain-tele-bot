# utils/translator.py
import requests

def translate_text(text, lang_to="en"):
    """
    Simple wrapper using MyMemory free API for quick translations.
    """
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {"q": text, "langpair": f"auto|{lang_to}"}
        r = requests.get(url, params=params, timeout=10).json()
        return r.get("responseData", {}).get("translatedText", "⚠️ Translation failed.")
    except Exception as e:
        return f"⚠️ Translation error: {e}"
