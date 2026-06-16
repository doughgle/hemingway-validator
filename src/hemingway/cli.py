"""hemingway-check - Validate Markdown against Hemingway writing rules.

Usage:
  hemingway-check [<file>]
  hemingway-check --version
  hemingway-check --help

If no file is given, reads from stdin.
"""
import json
import sys

from hemingway.validator import run_validator


def cli(argv, stdin_text=None):
    if "--version" in argv:
        return {
            "exit_code": 0,
            "output": "hemingway-check 1.0.0\n",
        }
    if "--help" in argv or "-h" in argv:
        return {
            "exit_code": 0,
            "output": __doc__,
        }

    file_path = None
    positional = [a for a in argv[1:] if not a.startswith("-")]
    if positional:
        file_path = positional[0]

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

    return {
        "exit_code": 0,
        "output": json.dumps(result, indent=2) + "\n",
    }


def main():
    result = cli(sys.argv, stdin_text=sys.stdin.read() if not sys.stdin.isatty() else None)
    sys.stdout.write(result["output"])
    sys.exit(result["exit_code"])
