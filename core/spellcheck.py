import requests


def correct_text(text):
    if not text:
        return text
    try:
        response = requests.get(
            "https://speller.yandex.net/services/spellservice.json/checkText",
            params={"text": text, "lang": "en"}
        )
    except Exception:
        return text

    if response.status_code != 200:
        return text
    corrections = response.json()
    corrected_text = text
    for err in corrections:
        word = err.get("word")
        suggestions = err.get("s") or []
        if suggestions:
            corrected_text = corrected_text.replace(word, suggestions[0], 1)
    return corrected_text
    if response.status_code != 200:
        return text
    corrections = response.json()
    corrected_text = text
    for err in corrections:
        word = err.get("word")
        suggestions = err.get("s") or []
        if suggestions:
            corrected_text = corrected_text.replace(word, suggestions[0], 1)
    return corrected_text
