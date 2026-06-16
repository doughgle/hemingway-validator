import re

NON_ADVERBS = {
    "apply", "butterfly", "consequently", "dolly", "early", "family",
    "fly", "frequently", "friendly", "holy", "Italy", "likely", "lily",
    "lovely", "melancholy", "monthly", "oily", "only", "presently",
    "rarely", "reply", "shortly", "silly", "slippery", "supply", "ugly",
    "weekly", "wholly", "worldly", "yearly",
}

BE_FORMS = {"am", "are", "is", "was", "were", "be", "been", "being"}

QUALIFIERS = [
    "almost", "apparently", "approximately", "are:", "arguably", "barely",
    "comparatively", "could", "couldn't", "deadly", "deeply", "direly",
    "don't", "downright", "dreadful", "each", "especially", "essentially",
    "even", "ever", "extremely", "fairly", "far", "far more", "few",
    "fewer", "fortunately", "frankly", "free", "full", "fully",
    "generally", "greatly", "hardly", "honestly", "I believe", "I feel",
    "I think", "I'm not sure", "incredibly", "indeed", "increasingly",
    "just", "kind of", "largely", "less", "likely", "many", "maybe",
    "merely", "mildly", "more", "moreover", "mostly", "much", "nearly",
    "necessarily", "neither", "never", "nonetheless", "nor",
    "notably", "noticeably", "oddly", "only", "outright", "particularly",
    "perhaps", "plenty", "predominantly", "presumably", "pretty", "quite",
    "rather", "really", "remarkably", "roughly", "significantly",
    "simply", "slightly", "so", "solely", "some", "somebody",
    "somehow", "someone", "somewhat", "suddenly", "surprisingly",
    "terribly", "thankfully", "truly", "unfortunately", "unusually",
    "usually", "very", "virtually", "yet",
]

COMPLEX_WORDS = [
    ("a considerable amount of", "much"),
    ("a number of", "some"),
    ("absolutely", ""),
    ("accommodate", "hold"),
    ("accomplish", "do"),
    ("accordingly", "so"),
    ("additional", "more"),
    ("additionally", "also"),
    ("advise", "tell"),
    ("afford", "give"),
    ("aggregate", "total"),
    ("aid", "help"),
    ("alter", "change"),
    ("ameliorate", "improve"),
    ("an absence of", "none"),
    ("anticipate", "expect"),
    ("apparent", "clear"),
    ("appreciate", "thank"),
    ("assistance", "help"),
    ("attain", "reach"),
    ("attempt", "try"),
    ("beneficial", "helpful"),
    ("collaborate", "work"),
    ("commence", "begin"),
    ("communicate", "talk"),
    ("compensation", "pay"),
    ("component", "part"),
    ("considerably", "much"),
    ("constitute", "make up"),
    ("contains", "has"),
    ("contribution", ""),
    ("demonstrate", "show"),
    ("depart", "leave"),
    ("designate", "choose"),
    ("determine", "decide"),
    ("detrimental", "harmful"),
    ("difficult", "hard"),
    ("disclose", "show"),
    ("discrepancy", "difference"),
    ("disseminate", "spread"),
    ("dramatically", "greatly"),
    ("duration", "time"),
    ("eliminate", "end"),
    ("elucidate", "explain"),
    ("employ", "use"),
    ("enable", "allow"),
    ("endeavor", "try"),
    ("enumerate", "list"),
    ("equitable", "fair"),
    ("equivalent", "equal"),
    ("establish", "set up"),
    ("evaluate", "test"),
    ("evident", "clear"),
    ("exclusively", "only"),
    ("expedite", "speed up"),
    ("facilitate", "ease"),
    ("following", "after"),
    ("for example", "e.g."),
    ("for instance", "e.g."),
    ("formulation", "form"),
    ("frequently", "often"),
    ("fundamental", "basic"),
    ("further", "more"),
    ("furthermore", "also"),
    ("has the ability to", "can"),
    ("hence", "so"),
    ("hesitate", "wait"),
    ("identical", "same"),
    ("illuminate", "light"),
    ("implementation", ""),
    ("imply", "suggest"),
    ("importantly", ""),
    ("in addition", "also"),
    ("in consequence", "so"),
    ("in contrast", "but"),
    ("in order to", "to"),
    ("in regard to", "about"),
    ("in spite of", "despite"),
    ("in the event that", "if"),
    ("inception", "start"),
    ("indicate", "show"),
    ("initiate", "start"),
    ("integral", ""),
    ("integrity", "honesty"),
    ("interface", ""),
    ("interim", ""),
    ("intervention", ""),
    ("iterative", "repeated"),
    ("jeopardize", "risk"),
    ("knowledge", ""),
    ("limit", ""),
    ("magnitude", "size"),
    ("maintain", "keep"),
    ("methodology", "method"),
    ("modification", "change"),
    ("monitor", "check"),
    ("multiple", "many"),
    ("necessitate", "require"),
    ("nevertheless", "still"),
    ("nonetheless", "still"),
    ("notwithstanding", "despite"),
    ("numerous", "many"),
    ("objective", "aim"),
    ("obligate", "force"),
    ("obtain", "get"),
    ("onward", ""),
    ("operate", "run"),
    ("optional", ""),
    ("parameter", ""),
    ("participate", "join"),
    ("pertain", "relate"),
    ("plausible", "likely"),
    ("portion", "part"),
    ("possess", "have"),
    ("preclude", "prevent"),
    ("prior to", "before"),
    ("proactively", ""),
    ("procure", "get"),
    ("proficient", "skilled"),
    ("propagate", "spread"),
    ("pursue", "chase"),
    ("qualified", "able"),
    ("regarding", "about"),
    ("regulate", "control"),
    ("relinquish", "give up"),
    ("remuneration", "pay"),
    ("require", "must"),
    ("requirements", ""),
    ("residual", "leftover"),
    ("resolution", ""),
    ("resolve", "solve"),
    ("resource", ""),
    ("respond", "answer"),
    ("responsible", "in charge"),
    ("restructure", "reorganize"),
    ("reusable", ""),
    ("revolution", "uprising"),
    ("robust", "strong"),
    ("routinely", "often"),
    ("segment", "part"),
    ("severe", "harsh"),
    ("significant", "big"),
    ("simplistic", "simple"),
    ("solely", "only"),
    ("solution", "answer"),
    ("somewhat", "slightly"),
    ("state-of-the-art", "modern"),
    ("strategize", "plan"),
    ("subsequent", "later"),
    ("substantial", "large"),
    ("sufficiently", "enough"),
    ("terminate", "end"),
    ("therefore", "so"),
    ("timely", ""),
    ("tranquilize", "calm"),
    ("transmit", "send"),
    ("ultimate", "last"),
    ("undeniably", ""),
    ("undergo", "experience"),
    ("unique", ""),
    ("universal", "general"),
    ("unprecedented", ""),
    ("until such time as", "until"),
    ("utilize", "use"),
    ("validate", "confirm"),
    ("variant", "version"),
    ("verification", "check"),
    ("versatile", "flexible"),
    ("viable", "workable"),
    ("voluntary", "optional"),
    ("whereas", "while"),
    ("with reference to", "about"),
    ("with the exception of", "except for"),
    ("witnessed", "saw"),
]


def _words_and_letters(sentence):
    words = sentence.split()
    letters = sum(1 for c in sentence if c.isalpha())
    return len(words), letters


def check_hard_sentence(sentence, line, column=1):
    words, letters = _words_and_letters(sentence)
    if words < 14:
        return None
    reading_level = round(4.71 * (letters / words) + 0.5 * (words / 1) - 21.43)
    if reading_level >= 14:
        return {
            "line": line,
            "column": column,
            "rule": "hard_sentence",
            "severity": "error",
            "text": sentence.strip(),
            "message": (
                f"Sentence is very hard to read (grade level {reading_level}). "
                "Consider splitting or simplifying."
            ),
            "suggestion": "Split into shorter sentences or simplify vocabulary.",
        }
    elif reading_level >= 10:
        return {
            "line": line,
            "column": column,
            "rule": "hard_sentence",
            "severity": "warning",
            "text": sentence.strip(),
            "message": (
                f"Sentence is hard to read (grade level {reading_level}). "
                "Consider splitting or simplifying."
            ),
            "suggestion": "Split into shorter sentences or simplify vocabulary.",
        }
    return None


def check_adverb(sentence, line):
    results = []
    tokens = re.findall(r"[A-Za-z]+", sentence)
    for token in tokens:
        if token.lower().endswith("ly") and token.lower() not in NON_ADVERBS:
            col = sentence.lower().index(token.lower()) + 1
            results.append({
                "line": line,
                "column": col,
                "rule": "adverb",
                "severity": "warning",
                "text": token,
                "message": (
                    f'Adverb "{token}" weakens your writing. '
                    "Consider a stronger verb."
                ),
                "suggestion": (
                    f'Use a stronger verb like "sprinted" '
                    f'instead of "ran {token.lower()}".'
                ),
            })
    return results


def check_passive_voice(sentence, line):
    results = []
    words = re.findall(r"[A-Za-z']+", sentence)
    for i, word in enumerate(words):
        if word.lower() in BE_FORMS:
            if i + 1 < len(words) and words[i + 1].lower().endswith("ly"):
                if i + 2 < len(words) and words[i + 2].lower().endswith("ed"):
                    phrase = f"{word} {words[i + 1]} {words[i + 2]}"
                    col_start = sentence.lower().index(word.lower()) + 1
                    results.append({
                        "line": line,
                        "column": col_start,
                        "rule": "passive_voice",
                        "severity": "warning",
                        "text": phrase,
                        "message": f'Passive voice: "{phrase}". Use active voice.',
                        "suggestion": (
                            "Rewrite so the subject performs the action "
                            '(e.g. "He threw the ball").'
                        ),
                    })
            elif i + 1 < len(words) and words[i + 1].lower().endswith("ed"):
                phrase = f"{word} {words[i + 1]}"
                col_start = sentence.lower().index(word.lower()) + 1
                results.append({
                    "line": line,
                    "column": col_start,
                    "rule": "passive_voice",
                    "severity": "warning",
                    "text": phrase,
                    "message": f'Passive voice: "{phrase}". Use active voice.',
                    "suggestion": (
                        "Rewrite so the subject performs the action "
                        '(e.g. "He threw the ball").'
                    ),
                })
    return results


def check_qualifier(sentence, line):
    results = []
    lower_sent = sentence.lower()
    last_end = 0
    for qualifier in sorted(QUALIFIERS, key=len, reverse=True):
        idx = lower_sent.find(qualifier.lower(), last_end)
        while idx != -1:
            if qualifier == "are:":
                if idx + 4 < len(lower_sent) or idx == len(lower_sent) - 4:
                    pass
            col = idx + 1
            results.append({
                "line": line,
                "column": col,
                "rule": "qualifier",
                "severity": "info",
                "text": sentence[idx:idx + len(qualifier)],
                "message": (
                    f'Qualifier "{qualifier}" weakens your writing.'
                ),
                "suggestion": (
                    'Remove the qualifier or rephrase for confidence.'
                ),
            })
            last_end = idx + len(qualifier)
            idx = lower_sent.find(qualifier, last_end)
    seen_texts = set()
    unique_results = []
    for r in results:
        key = (r["line"], r["column"], r["text"].lower())
        if key not in seen_texts:
            seen_texts.add(key)
            unique_results.append(r)
    return unique_results


def check_complex_word(sentence, line):
    results = []
    lower_sent = sentence.lower()
    seen_starts = set()
    for complex_word, simpler in sorted(COMPLEX_WORDS, key=lambda x: -len(x[0])):
        idx = 0
        while True:
            idx = lower_sent.find(complex_word, idx)
            if idx == -1:
                break
            if idx in seen_starts:
                idx += 1
                continue
            seen_starts.add(idx)
            col = idx + 1
            if simpler:
                suggestion_text = f'Replace with "{simpler}".'
            else:
                suggestion_text = "Consider removing this word."
            results.append({
                "line": line,
                "column": col,
                "rule": "complex_word",
                "severity": "info",
                "text": sentence[idx:idx + len(complex_word)],
                "message": (
                    f'Complex word "{complex_word}" has a simpler alternative.'
                ),
                "suggestion": suggestion_text,
            })
            idx += len(complex_word)
    return results
