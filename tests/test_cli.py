import json

from hemingway.cli import cli


class TestCli:
    def test_no_args(self):
        args = ["hemingway-check"]
        result = cli(args)
        assert result["exit_code"] == 1
        assert "error" in result["output"]

    def test_file_path(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("Hello world.")
        args = ["hemingway-check", str(f)]
        result = cli(args)
        assert result["exit_code"] == 0
        data = json.loads(result["output"])
        assert data["document"]["path"] == str(f)

    def test_file_not_found(self):
        args = ["hemingway-check", "/nonexistent/file.md"]
        result = cli(args)
        assert result["exit_code"] == 1
        data = json.loads(result["output"])
        assert data["error"]["type"] == "file_not_found"

    def test_stdin_input(self):
        args = ["hemingway-check"]
        result = cli(args, stdin_text="Hello world.")
        assert result["exit_code"] == 0
        data = json.loads(result["output"])
        assert data["document"]["path"] == "<stdin>"

    def test_version(self):
        args = ["hemingway-check", "--version"]
        result = cli(args)
        assert result["exit_code"] == 0

    def test_help(self):
        args = ["hemingway-check", "--help"]
        result = cli(args)
        assert result["exit_code"] == 0
