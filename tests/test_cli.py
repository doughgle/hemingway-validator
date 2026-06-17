import json

from hemingway.cli import cli


class TestCli:
    def test_no_args(self):
        args = ["hemingway-check"]
        result = cli(args)
        assert result["exit_code"] == 1
        assert "error" in result["output"]

    def test_file_path_default_markdown(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("Hello world.")
        args = ["hemingway-check", str(f)]
        result = cli(args)
        assert result["exit_code"] == 0
        assert "# Hemingway Validation Report" in result["output"]
        assert f"- Path: {f}" in result["output"]

    def test_file_not_found(self):
        args = ["hemingway-check", "/nonexistent/file.md"]
        result = cli(args)
        assert result["exit_code"] == 1
        data = json.loads(result["output"])
        assert data["error"]["type"] == "file_not_found"

    def test_stdin_input_default_markdown(self):
        args = ["hemingway-check"]
        result = cli(args, stdin_text="Hello world.")
        assert result["exit_code"] == 0
        assert "# Hemingway Validation Report" in result["output"]
        assert "- Path: <stdin>" in result["output"]

    def test_version(self):
        args = ["hemingway-check", "--version"]
        result = cli(args)
        assert result["exit_code"] == 0

    def test_help(self):
        args = ["hemingway-check", "--help"]
        result = cli(args)
        assert result["exit_code"] == 0

    def test_error_always_json(self):
        result = cli(["hemingway-check"])
        assert result["exit_code"] == 1
        data = json.loads(result["output"])
        assert "error" in data

    def test_markdown_report_structure(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text(
            "He ran quickly to the store. "
            "This exceptionally convoluted and unnecessarily complicated sentence "
            "is deliberately designed to trigger the absolute highest reading "
            "level possible within the constraints of the provided testing "
            "framework."
        )
        result = cli(["hemingway-check", str(f)])
        output = result["output"]
        assert "# Hemingway Validation Report" in output
        assert "## Document" in output
        assert "- Path:" in output
        assert "- Lines:" in output
        assert "- Words:" in output
        assert "## Summary" in output
        assert "## Issues" in output

    def test_markdown_no_issues(self, tmp_path):
        f = tmp_path / "clean.md"
        f.write_text("The cat sat on the mat.")
        result = cli(["hemingway-check", str(f)])
        output = result["output"]
        assert "No issues found." in output
        assert "0 warning, 0 error" in output

    def test_markdown_shows_issues(self, tmp_path):
        f = tmp_path / "issues.md"
        f.write_text("He ran quickly to the store.")
        result = cli(["hemingway-check", str(f)])
        output = result["output"]
        assert "1. adverb (warning)" in output
        assert "- Text: quickly" in output
        assert "- Message:" in output
        assert "- Suggestion:" in output

    def test_file_path_json(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("Hello world.")
        args = ["hemingway-check", "--output-format", "json", str(f)]
        result = cli(args)
        assert result["exit_code"] == 0
        data = json.loads(result["output"])
        assert data["document"]["path"] == str(f)

    def test_stdin_input_json(self):
        args = ["hemingway-check", "--output-format", "json"]
        result = cli(args, stdin_text="Hello world.")
        assert result["exit_code"] == 0
        data = json.loads(result["output"])
        assert data["document"]["path"] == "<stdin>"

    def test_json_output_format(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("Hello world.")
        args = ["hemingway-check", "--output-format", "json", str(f)]
        result = cli(args)
        data = json.loads(result["output"])
        assert "document" in data
        assert "summary" in data
        assert "issues" in data

    def test_json_with_issues(self, tmp_path):
        f = tmp_path / "issues.md"
        f.write_text("He ran quickly to the store.")
        args = ["hemingway-check", "--output-format", "json", str(f)]
        result = cli(args)
        data = json.loads(result["output"])
        assert len(data["issues"]) > 0
        assert data["issues"][0]["rule"] == "adverb"
