import argparse
import json
import sys

from hemingway.report import format_markdown, format_markdown_error
from hemingway.validator import run_validator


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="hemingway-check",
        description=(
            "Validate Markdown against Hemingway writing rules.\n\n"
            "If no file is given, reads from stdin."
        ),
        add_help=False,
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Path to Markdown file (reads from stdin if omitted)",
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format (json or markdown, default: markdown)",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version and exit",
    )
    parser.add_argument(
        "--help",
        action="store_true",
        help="Show this help message and exit",
    )
    return parser


def cli(argv, stdin_text=None):
    if "--version" in argv[1:]:
        return {
            "exit_code": 0,
            "output": "hemingway-check 1.0.0\n",
        }
    if "--help" in argv[1:] or "-h" in argv[1:]:
        return {
            "exit_code": 0,
            "output": _build_parser().format_help(),
        }

    parsed = _build_parser().parse_args(argv[1:])

    file_path = parsed.file
    output_format = parsed.output_format

    if file_path is None and stdin_text is None:
        error = {
            "type": "no_input",
            "message": (
                "No input provided. Provide a file path or pipe "
                "content via stdin."
            ),
        }
        if output_format == "json":
            output = json.dumps({"error": error}, indent=2) + "\n"
        else:
            output = format_markdown_error(error)
        return {"exit_code": 1, "output": output}

    result = run_validator(file_path=file_path, stdin_text=stdin_text)

    if "error" in result:
        if output_format == "json":
            output = json.dumps(result, indent=2) + "\n"
        else:
            output = format_markdown_error(result["error"])
        return {"exit_code": 1, "output": output}

    if output_format == "json":
        output = json.dumps(result, indent=2) + "\n"
    else:
        output = format_markdown(result)

    return {
        "exit_code": 0,
        "output": output,
    }


def main():
    stdin_text = sys.stdin.read() if not sys.stdin.isatty() else None
    result = cli(sys.argv, stdin_text=stdin_text)
    sys.stdout.write(result["output"])
    sys.exit(result["exit_code"])
