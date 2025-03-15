import re
from googletrans import Translator

translator = Translator()


def chunk_text(text, max_length=5000):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(sentence) > max_length:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            chunks.append(sentence)
            continue
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk = (current_chunk + " " + sentence).strip() if current_chunk else sentence
        else:
            chunks.append(current_chunk)
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def translate_text(text, dest_lang='ru'):
    if not text:
        return ""

    chunks = chunk_text(text)
    translated_chunks = []
    for chunk in chunks:
        try:
            result = translator.translate(chunk, dest=dest_lang)
            translated_chunks.append(result.text)
        except Exception as e:
            translated_chunks.append(chunk)
    return " ".join(translated_chunks)