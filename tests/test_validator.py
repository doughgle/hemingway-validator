from hemingway.validator import run_validator, validate_document


class TestValidateDocument:
    def test_empty_document(self):
        text = ""
        result = validate_document(text, path="test.md")
        assert result["document"]["path"] == "test.md"
        assert result["document"]["word_count"] == 0
        assert result["document"]["line_count"] == 0
        assert result["issues"] == []

    def test_clean_document(self):
        text = "The cat sat on the mat."
        result = validate_document(text, path="test.md")
        assert result["document"]["word_count"] == 6
        assert result["issues"] == []

    def test_detects_issues(self):
        text = "He ran quickly to the store."
        result = validate_document(text, path="test.md")
        assert len(result["issues"]) >= 1
        assert result["issues"][0]["rule"] == "adverb"

    def test_summary_counts(self):
        text = "He ran quickly to the store."
        result = validate_document(text, path="test.md")
        assert result["summary"]["adverb"] >= 1

    def test_hard_sentence_in_summary(self):
        text = (
            "This exceptionally convoluted and unnecessarily complicated sentence "
            "is deliberately designed to trigger the absolute highest reading level "
            "possible within the constraints of the provided testing framework."
        )
        result = validate_document(text, path="test.md")
        assert result["summary"]["hard_sentence"]["error"] >= 1

    def test_line_count(self):
        text = "Line one.\nLine two.\nLine three."
        result = validate_document(text, path="test.md")
        assert result["document"]["line_count"] == 3

    def test_word_count(self):
        text = "one two three four five"
        result = validate_document(text, path="test.md")
        assert result["document"]["word_count"] == 5


class TestRunValidator:
    def test_file_not_found(self, tmp_path):
        missing = str(tmp_path / "nope.md")
        result = run_validator(file_path=missing)
        assert "error" in result
        assert result["error"]["type"] == "file_not_found"

    def test_valid_file(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("Hello world.")
        result = run_validator(file_path=str(f))
        assert "document" in result
        assert result["document"]["path"] == str(f)

    def test_stdin_input(self):
        result = run_validator(stdin_text="Hello world.")
        assert "document" in result
        assert result["document"]["path"] == "<stdin>"

    def test_file_wins_over_stdin(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("File content.")
        result = run_validator(file_path=str(f), stdin_text="Stdin content.")
        assert result["document"]["path"] == str(f)

    def test_no_input(self):
        result = run_validator()
        assert "error" in result
        assert result["error"]["type"] == "no_input"
