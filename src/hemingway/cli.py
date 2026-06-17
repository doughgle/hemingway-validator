"""hemingway-check - Validate Markdown against Hemingway writing rules.

Usage:
  hemingway-check [--output-format <fmt>] [<file>]
  hemingway-check --version
  hemingway-check --help

If no file is given, reads from stdin.

Options:
  --output-format <fmt>  Output format (json or markdown, default: markdown)
  --version              Show version.
  --help                 Show this message.
"""
import json
import sys

from docopt import docopt

from hemingway.report import format_markdown
from hemingway.validator import run_validator


def cli(argv, stdin_text=None):
    if "--version" in argv[1:]:
        return {
            "exit_code": 0,
            "output": "hemingway-check 1.0.0\n",
        }
    if "--help" in argv[1:] or "-h" in argv[1:]:
        return {
            "exit_code": 0,
            "output": __doc__,
        }

    args = docopt(__doc__, argv=argv[1:], help=False)

    file_path = args["<file>"]
    output_format = args["--output-format"]

    if file_path is None and stdin_text is None:
        return {
            "exit_code": 1,
            "output": json.dumps({
                "error": {
                    "type": "no_input",
                    "message": (
                        "No input provided. Provide a file path or pipe "
                        "content via stdin."
                    ),
                }
            }, indent=2) + "\n",
        }

    result = run_validator(file_path=file_path, stdin_text=stdin_text)

    if "error" in result:
        return {
            "exit_code": 1,
            "output": json.dumps(result, indent=2) + "\n",
        }

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
