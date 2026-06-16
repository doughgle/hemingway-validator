import re


def parse_markdown(text):
    lines = text.split("\n")
    prose_lines = []
    i = 0
    in_fenced_code = False
    fence_char = None
    in_frontmatter = False
    fm_delimiter = None
    in_html_block = False

    while i < len(lines):
        raw_line = lines[i]
        line_num = i + 1
        stripped = raw_line.strip()

        if not in_fenced_code and not in_frontmatter and not in_html_block:
            if stripped == "---":
                in_frontmatter = True
                fm_delimiter = "---"
                i += 1
                continue
            if stripped == "+++":
                in_frontmatter = True
                fm_delimiter = "+++"
                i += 1
                continue

        if in_frontmatter:
            if stripped == fm_delimiter:
                in_frontmatter = False
            i += 1
            continue

        if not in_fenced_code and not in_frontmatter and not in_html_block:
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fenced_code = True
                fence_char = stripped[0]
                i += 1
                continue

        if in_fenced_code:
            if stripped.startswith(fence_char) and stripped.strip(fence_char) == "":
                in_fenced_code = False
                fence_char = None
            i += 1
            continue

        if not in_html_block and not in_fenced_code and not in_frontmatter:
            if re.match(r"^\s*</?[a-zA-Z]", stripped):
                in_html_block = True
                i += 1
                continue

        if in_html_block:
            if "</" in stripped and ">" in stripped:
                in_html_block = False
            i += 1
            continue

        processed = raw_line
        processed = re.sub(r"`[^`]*`", "", processed)
        processed = re.sub(r"!\[([^\]]*)\]\([^)]*\)", "", processed)
        processed = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", processed)

        if processed.strip():
            prose_lines.append((line_num, processed))

        i += 1

    return prose_lines


def extract_sentences(text):
    if not text or not text.strip():
        return []
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]
