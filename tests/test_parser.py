import pytest
from hemingway.parser import parse_markdown, extract_sentences


class TestParseMarkdown:
    def test_removes_fenced_code_block(self):
        md = "Hello\n\n```\ncode here\n```\n\nWorld"
        result = parse_markdown(md)
        texts = [t for _, t in result]
        assert all("code here" not in t for t in texts)
        assert any("Hello" in t for t in texts)
        assert any("World" in t for t in texts)

    def test_removes_inline_code(self):
        md = "Hello `code` world"
        result = parse_markdown(md)
        texts = [t for _, t in result]
        assert all("code" not in t.split() or t.strip() == "" for t in texts)
        assert any("Hello" in t for t in texts)
        assert any("world" in t for t in texts)

    def test_removes_yaml_frontmatter(self):
        md = "---\ntitle: Test\n---\n\nBody text"
        result = parse_markdown(md)
        texts = [t for _, t in result]
        assert all("title" not in t for t in texts)
        assert any("Body text" in t for t in texts)

    def test_removes_link_urls(self):
        md = "A [link](http://example.com) here"
        result = parse_markdown(md)
        texts = [t for _, t in result]
        assert any("http://example.com" not in t for t in texts)
        assert any("A link here" in t for t in texts)

    def test_removes_image_alt_and_urls(self):
        md = "An ![image](img.png)"
        result = parse_markdown(md)
        texts = [t for _, t in result]
        assert all("image" not in t and "img.png" not in t for t in texts)

    def test_removes_html_blocks(self):
        md = "Hello\n\n<div>html</div>\n\nWorld"
        result = parse_markdown(md)
        texts = [t for _, t in result]
        assert all("div" not in t and "html" not in t for t in texts)

    def test_keeps_paragraphs(self):
        md = "Paragraph one.\n\nParagraph two."
        result = parse_markdown(md)
        texts = [t for _, t in result]
        assert any("Paragraph one" in t for t in texts)
        assert any("Paragraph two" in t for t in texts)

    def test_keeps_list_items(self):
        md = "- item one\n- item two"
        result = parse_markdown(md)
        texts = [t for _, t in result]
        assert any("item one" in t for t in texts)
        assert any("item two" in t for t in texts)

    def test_removes_toml_frontmatter(self):
        md = "+++\ntitle = \"Test\"\n+++\n\nBody"
        result = parse_markdown(md)
        texts = [t for _, t in result]
        assert all("title" not in t for t in texts)
        assert any("Body" in t for t in texts)

    def test_removes_tilde_fenced_code(self):
        md = "Hello\n\n~~~\ncode here\n~~~\n\nWorld"
        result = parse_markdown(md)
        texts = [t for _, t in result]
        assert all("code here" not in t for t in texts)

    def test_preserves_line_numbers(self):
        md = "Line one\n\nLine two\n\nLine three"
        result = parse_markdown(md)
        lines = [l for l, _ in result]
        assert lines == [1, 3, 5]


class TestExtractSentences:
    def test_simple_sentence(self):
        result = extract_sentences("Hello world.")
        assert len(result) == 1
        assert result[0] == "Hello world."

    def test_multiple_sentences(self):
        result = extract_sentences("Hello world. How are you? I'm fine.")
        assert len(result) == 3

    def test_empty_text(self):
        result = extract_sentences("")
        assert result == []

    def test_exclamation_marks(self):
        result = extract_sentences("Stop! Don't go!")
        assert len(result) == 2

    def test_question_marks(self):
        result = extract_sentences("Is it true? Yes it is.")
        assert len(result) == 2
