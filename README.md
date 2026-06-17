# hemingway-validator

**Check Markdown documents against Hemingway-style writing rules — hard sentences, adverbs, passive voice, qualifiers, and complex words — from the command line.**

Inspired by the [Hemingway Editor](https://hemingwayapp.com/) by Adam and Ben Long, this tool brings the same readability checks to your terminal. Feed it a Markdown file or pipe content via stdin, and get structured JSON feedback on what to tighten, simplify, or rewrite. No GUI, no colour, no auto-fix — just validation.

## Install

```bash
pip install git+https://github.com/doughgle/hemingway-validator.git
```

Or from a local checkout:

```bash
pip install -e .
```

## Usage

```bash
# Check a file
hemingway-check path/to/document.md

# Pipe content via stdin
cat document.md | hemingway-check

# Print usage
hemingway-check --help
```

### Output

The tool prints a single JSON object to stdout with document stats, a summary of issues per rule, and a detailed issue list with line numbers, columns, messages, and suggestions.

**Exit codes:** `0` — document checked successfully (issues may exist). `1` — error (file not found, I/O error, no input).

## Rules

| Check | Severity | What it finds |
|---|---|---|
| `hard_sentence` | warning / error | Sentences with 14+ words at reading level 10+ (yellow) or 14+ (red) |
| `adverb` | warning | Words ending in *-ly* (with exception list) that weaken prose |
| `passive_voice` | warning | *be*-verb + *-ed* word, optionally with an adverb between |
| `qualifier` | info | Hedging words like *perhaps*, *very*, *really*, *I think* |
| `complex_word` | info | Words with simpler alternatives: *utilize* → *use*, *terminate* → *end* |

## Development

Set up a local development environment with:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Lint

```bash
ruff check src/ tests/
```

## License

MIT — see [LICENSE](LICENSE).

## Credits

- [Adam Long](https://twitter.com/adamlong) and [Ben Long](https://twitter.com/benllong) for the original [Hemingway Editor](https://hemingwayapp.com/)
- The open-source community for reverse-engineering the Hemingway reading-level formula and style checks
