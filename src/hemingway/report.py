def format_markdown(result):
    doc = result["document"]
    summary = result["summary"]
    issues = result["issues"]

    lines = [
        "# Hemingway Validation Report",
        "",
        "## Document",
        f"- Path: {doc['path']}",
        f"- Lines: {doc['line_count']}",
        f"- Words: {doc['word_count']}",
        "",
        "## Summary",
        "| Rule | Count |",
        "| --- | --- |",
    ]

    hs = summary["hard_sentence"]
    lines.append(f"| Hard sentences | {hs['warning']} warning, {hs['error']} error |")
    lines.append(f"| Adverbs | {summary['adverb']} |")
    lines.append(f"| Passive voice | {summary['passive_voice']} |")
    lines.append(f"| Qualifiers | {summary['qualifier']} |")
    lines.append(f"| Complex words | {summary['complex_word']}")

    lines.append("")
    lines.append("## Issues")

    if not issues:
        lines.append("")
        lines.append("No issues found.")
    else:
        lines.append("")
        for i, issue in enumerate(issues, 1):
            location = f"{doc['path']}:{issue['line']}:{issue['column']}"
            rule_label = f"{issue['rule']} ({issue['severity']})"
            lines.append(f"{i}. {rule_label} — {location}")
            lines.append(f"   - Text: {issue['text']}")
            lines.append(f"   - Message: {issue['message']}")
            lines.append(f"   - Suggestion: {issue['suggestion']}")
            lines.append("")

    return "\n".join(lines) + "\n"


def format_markdown_error(error):
    lines = [
        "# Hemingway Validation Report",
        "",
        "## Error",
        f"- Type: {error['type']}",
        f"- Message: {error['message']}",
        "",
    ]
    return "\n".join(lines) + "\n"
