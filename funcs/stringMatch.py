import unicodedata
import re
from difflib import SequenceMatcher


def normalize_category(text):
    text = text.lower().strip()

    #tolti accenti
    text = unicodedata.normalize("NFD", text)
    text = "".join(
        c for c in text
        if unicodedata.category(c) != "Mn"
    )

    # tolti spazi
    text = re.sub(r"\s+", " ", text)

    # tolta punteggiatura
    text = re.sub(r"[^\w\s]", "", text)

    return text


def similarity(a, b):
    return SequenceMatcher(
        None,
        normalize_category(a),
        normalize_category(b)
    ).ratio()



if __name__ == "__main__":

    r = similarity(
        "invenzioni piu importanti della storia",
        "invenzioni dell'uomo piu importanti della storia"
    )
    print(r)