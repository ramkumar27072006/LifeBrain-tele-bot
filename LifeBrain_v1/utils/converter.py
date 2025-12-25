# utils/converter.py
import requests

def convert_currency(amount, from_curr, to_curr):
    """
    Uses exchangerate.host free API.
    """
    try:
        amount = float(amount)
    except:
        return "❌ Amount must be a number."

    url = f"https://api.exchangerate.host/convert?from={from_curr}&to={to_curr}&amount={amount}"
    try:
        r = requests.get(url, timeout=10).json()
        if r.get("result") is not None:
            return f"💱 {amount} {from_curr} = {round(r['result'], 2)} {to_curr}"
        return "⚠️ Conversion failed."
    except Exception as e:
        return f"⚠️ Error: {e}"
