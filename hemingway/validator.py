import os
import sys

from hemingway.parser import parse_markdown, extract_sentences
from hemingway.rules import (
    check_hard_sentence,
    check_adverb,
    check_passive_voice,
    check_qualifier,
    check_complex_word,
)


def validate_document(text, path="<stdin>"):
    prose_lines = parse_markdown(text)
    all_issues = []
    total_words = 0
    line_count = len(text.rstrip("\n").split("\n")) if text else 0

    for line_num, line_text in prose_lines:
        sentences = extract_sentences(line_text)
        words_in_line = len(line_text.split())
        total_words += words_in_line

        for sentence in sentences:
            issue = check_hard_sentence(sentence, line_num)
            if issue:
                all_issues.append(issue)

            for issue in check_adverb(sentence, line_num):
                all_issues.append(issue)

            for issue in check_passive_voice(sentence, line_num):
                all_issues.append(issue)

            for issue in check_qualifier(sentence, line_num):
                all_issues.append(issue)

            for issue in check_complex_word(sentence, line_num):
                all_issues.append(issue)

    summary = {
        "hard_sentence": {"warning": 0, "error": 0},
        "adverb": 0,
        "passive_voice": 0,
        "qualifier": 0,
        "complex_word": 0,
    }

    for issue in all_issues:
        rule = issue["rule"]
        if rule == "hard_sentence":
            summary["hard_sentence"][issue["severity"]] += 1
        else:
            summary[rule] += 1

    return {
        "document": {
            "path": path,
            "line_count": line_count,
            "word_count": total_words,
        },
        "summary": summary,
        "issues": all_issues,
    }


def run_validator(file_path=None, stdin_text=None):
    if file_path:
        if not os.path.exists(file_path):
            return {
                "error": {
                    "type": "file_not_found",
                    "message": f"File not found: {file_path}",
                }
            }
        try:
            with open(file_path, "r") as f:
                text = f.read()
        except OSError as e:
            return {
                "error": {
                    "type": "io_error",
                    "message": f"Could not read file: {e}",
                }
            }
        return validate_document(text, path=file_path)

    if stdin_text is not None:
        return validate_document(stdin_text, path="<stdin>")

    return {
        "error": {
            "type": "no_input",
            "message": "No input provided. Provide a file path or pipe content via stdin.",
        }
    }
