#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

LANGS = {
    "af": ("\U0001F1FF\U0001F1E6", "Afrikaans"),
    "sq": ("\U0001F1E6\U0001F1F1", "Shqip"),
    "am": ("\U0001F1EA\U0001F1F9", "አማርኛ"),
    "ar": ("\U0001F1F8\U0001F1E6", "العربية"),
    "hy": ("\U0001F1E6\U0001F1F2", "Հայերեն"),
    "az": ("\U0001F1E6\U0001F1FF", "Azərbaycan"),
    "eu": ("\U0001F1EA\U0001F1F8", "Euskara"),
    "be": ("\U0001F1E7\U0001F1FE", "Беларуская"),
    "bn": ("\U0001F1E7\U0001F1E9", "বাংলা"),
    "bs": ("\U0001F1E7\U0001F1E6", "Bosanski"),
    "bg": ("\U0001F1E7\U0001F1EC", "Български"),
    "ca": ("\U0001F1EA\U0001F1F8", "Català"),
    "ceb": ("\U0001F1F5\U0001F1ED", "Cebuano"),
    "zh-CN": ("\U0001F1E8\U0001F1F3", "中文"),
    "zh-TW": ("\U0001F1F9\U0001F1FC", "中文(繁)"),
    "zh": ("\U0001F1E8\U0001F1F3", "中文"),
    "co": ("\U0001F1EB\U0001F1F7", "Corsu"),
    "hr": ("\U0001F1ED\U0001F1F7", "Hrvatski"),
    "cs": ("\U0001F1E8\U0001F1FF", "Čeština"),
    "da": ("\U0001F1E9\U0001F1F0", "Dansk"),
    "nl": ("\U0001F1F3\U0001F1F1", "Nederlands"),
    "en": ("\U0001F1EC\U0001F1E7", "English"),
    "eo": ("\U0001F310", "Esperanto"),
    "et": ("\U0001F1EA\U0001F1EA", "Eesti"),
    "fi": ("\U0001F1EB\U0001F1EE", "Suomi"),
    "fr": ("\U0001F1EB\U0001F1F7", "Français"),
    "fy": ("\U0001F1F3\U0001F1F1", "Frysk"),
    "gl": ("\U0001F1EA\U0001F1F8", "Galego"),
    "ka": ("\U0001F1EC\U0001F1EA", "ქართული"),
    "de": ("\U0001F1E9\U0001F1EA", "Deutsch"),
    "el": ("\U0001F1EC\U0001F1F7", "Ελληνικά"),
    "gu": ("\U0001F1EE\U0001F1F3", "ગુજરાતી"),
    "ht": ("\U0001F1ED\U0001F1F9", "Kreyòl"),
    "ha": ("\U0001F1F3\U0001F1EC", "Hausa"),
    "haw": ("\U0001F1FA\U0001F1F8", "ʻŌlelo Hawaiʻi"),
    "he": ("\U0001F1EE\U0001F1F1", "עברית"),
    "iw": ("\U0001F1EE\U0001F1F1", "עברית"),
    "hi": ("\U0001F1EE\U0001F1F3", "हिन्दी"),
    "hmn": ("\U0001F310", "Hmong"),
    "hu": ("\U0001F1ED\U0001F1FA", "Magyar"),
    "is": ("\U0001F1EE\U0001F1F8", "Íslenska"),
    "ig": ("\U0001F1F3\U0001F1EC", "Igbo"),
    "id": ("\U0001F1EE\U0001F1E9", "Indonesia"),
    "ga": ("\U0001F1EE\U0001F1EA", "Gaeilge"),
    "it": ("\U0001F1EE\U0001F1F9", "Italiano"),
    "ja": ("\U0001F1EF\U0001F1F5", "日本語"),
    "jv": ("\U0001F1EE\U0001F1E9", "Jawa"),
    "jw": ("\U0001F1EE\U0001F1E9", "Jawa"),
    "kn": ("\U0001F1EE\U0001F1F3", "ಕನ್ನಡ"),
    "kk": ("\U0001F1F0\U0001F1FF", "Қазақ"),
    "km": ("\U0001F1F0\U0001F1ED", "ខ្មែរ"),
    "rw": ("\U0001F1F7\U0001F1FC", "Kinyarwanda"),
    "ko": ("\U0001F1F0\U0001F1F7", "한국어"),
    "ku": ("\U0001F1EE\U0001F1F6", "Kurdî"),
    "ky": ("\U0001F1F0\U0001F1EC", "Кыргызча"),
    "lo": ("\U0001F1F1\U0001F1E6", "ລາວ"),
    "la": ("\U0001F3DB\uFE0F", "Latina"),
    "lv": ("\U0001F1F1\U0001F1FB", "Latviešu"),
    "lt": ("\U0001F1F1\U0001F1F9", "Lietuvių"),
    "lb": ("\U0001F1F1\U0001F1FA", "Lëtzebuergesch"),
    "mk": ("\U0001F1F2\U0001F1F0", "Македонски"),
    "mg": ("\U0001F1F2\U0001F1EC", "Malagasy"),
    "ms": ("\U0001F1F2\U0001F1FE", "Melayu"),
    "ml": ("\U0001F1EE\U0001F1F3", "മലയാളം"),
    "mt": ("\U0001F1F2\U0001F1F9", "Malti"),
    "mi": ("\U0001F1F3\U0001F1FF", "Māori"),
    "mr": ("\U0001F1EE\U0001F1F3", "मराठी"),
    "mn": ("\U0001F1F2\U0001F1F3", "Монгол"),
    "my": ("\U0001F1F2\U0001F1F2", "မြန်မာ"),
    "ne": ("\U0001F1F3\U0001F1F5", "नेपाली"),
    "no": ("\U0001F1F3\U0001F1F4", "Norsk"),
    "ny": ("\U0001F1F2\U0001F1FC", "Chichewa"),
    "or": ("\U0001F1EE\U0001F1F3", "ଓଡ଼ିଆ"),
    "ps": ("\U0001F1E6\U0001F1EB", "پښتو"),
    "fa": ("\U0001F1EE\U0001F1F7", "فارسی"),
    "pl": ("\U0001F1F5\U0001F1F1", "Polski"),
    "pt": ("\U0001F1F5\U0001F1F9", "Português"),
    "pa": ("\U0001F1EE\U0001F1F3", "ਪੰਜਾਬੀ"),
    "ro": ("\U0001F1F7\U0001F1F4", "Română"),
    "ru": ("\U0001F1F7\U0001F1FA", "Русский"),
    "sm": ("\U0001F1FC\U0001F1F8", "Samoan"),
    "gd": ("\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F", "Gàidhlig"),
    "sr": ("\U0001F1F7\U0001F1F8", "Српски"),
    "st": ("\U0001F1F1\U0001F1F8", "Sesotho"),
    "sn": ("\U0001F1FF\U0001F1FC", "Shona"),
    "sd": ("\U0001F1F5\U0001F1F0", "سنڌي"),
    "si": ("\U0001F1F1\U0001F1F0", "සිංහල"),
    "sk": ("\U0001F1F8\U0001F1F0", "Slovenčina"),
    "sl": ("\U0001F1F8\U0001F1EE", "Slovenščina"),
    "so": ("\U0001F1F8\U0001F1F4", "Soomaali"),
    "es": ("\U0001F1EA\U0001F1F8", "Español"),
    "su": ("\U0001F1EE\U0001F1E9", "Sunda"),
    "sw": ("\U0001F1F0\U0001F1EA", "Kiswahili"),
    "sv": ("\U0001F1F8\U0001F1EA", "Svenska"),
    "tl": ("\U0001F1F5\U0001F1ED", "Tagalog"),
    "tg": ("\U0001F1F9\U0001F1EF", "Тоҷикӣ"),
    "ta": ("\U0001F1EE\U0001F1F3", "தமிழ்"),
    "tt": ("\U0001F1F7\U0001F1FA", "Татар"),
    "te": ("\U0001F1EE\U0001F1F3", "తెలుగు"),
    "th": ("\U0001F1F9\U0001F1ED", "ไทย"),
    "tr": ("\U0001F1F9\U0001F1F7", "Türkçe"),
    "tk": ("\U0001F1F9\U0001F1F2", "Türkmen"),
    "uk": ("\U0001F1FA\U0001F1E6", "Українська"),
    "ur": ("\U0001F1F5\U0001F1F0", "اردو"),
    "ug": ("\U0001F1E8\U0001F1F3", "ئۇيغۇر"),
    "uz": ("\U0001F1FA\U0001F1FF", "Oʻzbek"),
    "vi": ("\U0001F1FB\U0001F1F3", "Tiếng Việt"),
    "cy": ("\U0001F3F4\U000E0067\U000E0062\U000E0077\U000E006C\U000E0073\U000E007F", "Cymraeg"),
    "xh": ("\U0001F1FF\U0001F1E6", "isiXhosa"),
    "yi": ("\U0001F310", "ייִדיש"),
    "yo": ("\U0001F1F3\U0001F1EC", "Yorùbá"),
    "zu": ("\U0001F1FF\U0001F1E6", "isiZulu"),
}

POS_DE = {
    "noun": "Substantiv", "verb": "Verb", "adjective": "Adjektiv",
    "adverb": "Adverb", "preposition": "Präposition", "conjunction": "Konjunktion",
    "pronoun": "Pronomen", "interjection": "Interjektion", "abbreviation": "Abkürzung",
    "exclamation": "Ausruf", "particle": "Partikel", "determiner": "Artikel",
    "phrase": "Redewendung", "prefix": "Präfix", "suffix": "Suffix",
}


def flag(lang):
    entry = LANGS.get(lang)
    return entry[0] if entry else "\U0001F310"


def lang_name(lang):
    entry = LANGS.get(lang)
    return entry[1] if entry else lang.upper()


def pos_label(pos):
    return POS_DE.get(pos.lower(), pos.capitalize()) if pos else ""


def google_translate_full(query, source, target):
    params = urllib.parse.urlencode({
        "client": "gtx",
        "sl": source,
        "tl": target,
        "dt": ["t", "at", "bd", "rm", "qca"],
        "q": query,
    }, doseq=True)
    url = f"https://translate.googleapis.com/translate_a/single?{params}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=4) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_response(data):
    result = {
        "translation": "",
        "detected": "",
        "transliteration_tgt": "",
        "alternatives": [],
        "dictionary": [],
        "autocorrect": "",
    }

    if data[0]:
        parts = []
        for seg in data[0]:
            if seg and seg[0]:
                parts.append(seg[0])
        result["translation"] = "".join(parts)

        for seg in data[0]:
            if seg and len(seg) > 2 and seg[2]:
                result["transliteration_tgt"] = seg[2]

    if len(data) > 2 and data[2]:
        result["detected"] = data[2]

    if len(data) > 1 and data[1]:
        for entry in data[1]:
            if isinstance(entry, list) and len(entry) >= 2:
                pos = entry[0] or ""
                translations = entry[1] if entry[1] else []
                if translations:
                    result["dictionary"].append({
                        "pos": pos,
                        "terms": translations[:6],
                    })

    if len(data) > 5 and data[5]:
        for block in data[5]:
            if isinstance(block, list) and len(block) > 2 and isinstance(block[2], list):
                for alt in block[2]:
                    if isinstance(alt, list) and alt[0] and alt[0] != result["translation"]:
                        result["alternatives"].append(alt[0])

    if len(data) > 7 and data[7]:
        try:
            if isinstance(data[7], list) and len(data[7]) > 0:
                corrected = None
                if len(data[7]) > 1 and data[7][1]:
                    corrected = data[7][1]
                elif data[7][0]:
                    corrected = data[7][0]
                if corrected and isinstance(corrected, str):
                    result["autocorrect"] = corrected.replace("<b>", "").replace("</b>", "")
        except (IndexError, TypeError):
            pass

    return result


def is_single_word(text):
    return len(text.split()) == 1


def translate(query):
    primary_lang = os.getenv("primary_lang", "de")
    target_lang = os.getenv("target_lang", "en")

    if not query or not query.strip():
        return json.dumps({"items": [{"title": "Text eingeben\u2026", "subtitle": "t <text>", "valid": False}]})

    query = query.strip()

    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            future_to_primary = pool.submit(google_translate_full, query, "auto", primary_lang)
            future_to_target = pool.submit(google_translate_full, query, primary_lang, target_lang)

            data_to_primary = future_to_primary.result()
            data_to_target = future_to_target.result()

        parsed_primary = parse_response(data_to_primary)
        parsed_target = parse_response(data_to_target)

        detected = parsed_primary["detected"]
        if detected == primary_lang or parsed_primary["translation"].strip().lower() == query.strip().lower():
            parsed = parsed_target
            src, tgt = primary_lang, target_lang
        else:
            parsed = parsed_primary
            src, tgt = detected or "?", primary_lang

        subtitle_base = f"{flag(src)} {lang_name(src)} \u2192 {flag(tgt)} {lang_name(tgt)}"
        items = []

        # We'll insert autocorrect at the very end to position 0
        autocorrect = parsed["autocorrect"] or parsed_primary.get("autocorrect", "") or parsed_target.get("autocorrect", "")

        # Main translation with transliteration
        main_subtitle = subtitle_base
        if parsed["transliteration_tgt"]:
            main_subtitle += f" \u00B7 {parsed['transliteration_tgt']}"

        items.append({
            "title": parsed["translation"],
            "subtitle": main_subtitle,
            "arg": parsed["translation"],
            "text": {"copy": parsed["translation"], "largetype": parsed["translation"]},
            "valid": True,
        })

        # Collect all "best match" words to exclude from dictionary lines
        best_matches = {parsed["translation"].strip().lower()}

        # Single word mode
        if is_single_word(query):
            # Alternative best matches as individual items
            for i, alt in enumerate(parsed["alternatives"][:3]):
                items.append({
                    "title": alt,
                    "subtitle": subtitle_base,
                    "arg": alt,
                    "text": {"copy": alt, "largetype": alt},
                    "valid": True,
                })
                best_matches.add(alt.strip().lower())

            # Dictionary entries as compact grouped lines, excluding already shown best matches
            if parsed["dictionary"]:
                for entry in parsed["dictionary"][:4]:
                    pos = pos_label(entry["pos"])
                    # Filter out terms already shown as best matches
                    remaining = [t for t in entry["terms"] if t.strip().lower() not in best_matches]
                    if remaining:
                        terms = ", ".join(remaining[:5])
                        items.append({
                            "title": terms,
                            "subtitle": f"\U0001F4D6 {pos}",
                            "arg": remaining[0],
                            "text": {"copy": terms, "largetype": terms},
                            "valid": True,
                        })
        else:
            # Sentence mode: alternatives
            for i, alt in enumerate(parsed["alternatives"][:3]):
                items.append({
                    "title": alt,
                    "subtitle": subtitle_base,
                    "arg": alt,
                    "text": {"copy": alt, "largetype": alt},
                    "valid": True,
                })

        # Insert autocorrect as very first item after everything else is built
        if autocorrect:
            items.insert(0, {
                "title": f"\u2728 Meintest du: {autocorrect}",
                "subtitle": "Enter \u2192 mit Korrektur \u00fcbersetzen",
                "arg": autocorrect,
                "autocomplete": autocorrect,
                "text": {"copy": autocorrect},
                "valid": False,
            })

    except Exception as e:
        items = [{
            "title": f"Fehler: {e}",
            "subtitle": "\u00dcbersetzung fehlgeschlagen",
            "valid": False,
        }]

    return json.dumps({"items": items}, ensure_ascii=False)


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    print(translate(query))
