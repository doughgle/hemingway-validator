# Hemingway Validator — Domain Specification

A command-line tool that checks a Markdown document against Hemingway-style writing rules and returns structured feedback. No editor, no coloured output — just validation.

---

## 1. Input

The tool accepts input in two mutually exclusive ways:

| Method | Mechanism |
|--------|-----------|
| **File path** | `hemingway-check path/to/document.md` |
| **Stdin pipe** | `cat document.md | hemingway-check` |

If both are provided, file path wins and stdin is ignored. If neither is provided, print a usage message and exit non-zero.

---

## 2. Markdown Parsing

The document is parsed as Markdown. The following elements are **skipped** (not analysed for any rule):

- Fenced code blocks (````` ``` ``, `~~~`)
- Inline code spans (`` `code` ``)
- YAML/TOML frontmatter (`---...---` at the start of file)
- Link URLs and reference definitions
- Image alt text and URLs
- HTML blocks

Everything else — paragraphs, headings, list items, blockquotes — is analysed as prose, sentence by sentence.

---

## 3. Rules (Hemingway Checks)

All rules apply only to prose content after Markdown stripping.

### 3.1 Sentence Complexity — `hard_sentence`

Based on the original Hemingway reading level formula:

```
reading_level = round(4.71 × (letters / words) + 0.5 × (words / sentences) - 21.43)
```

| Severity | Condition | Matches original colour |
|----------|-----------|------------------------|
| `warning` | words >= 14 AND reading_level >= 10 AND reading_level < 14 | Yellow |
| `error` | words >= 14 AND reading_level >= 14 | Red |

Where:
- `words` = word count in the sentence (split on whitespace)
- `letters` = character count in the sentence (excluding whitespace and punctuation)
- `sentences` = 1 (this formula is applied per sentence as a single-sentence paragraph)

### 3.2 Adverbs — `adverb`

A word is flagged as an adverb if it **ends in `ly`** AND is **not** in the non-adverb exception list.

Exception list (non-exhaustive; must include at minimum):

`apply, butterfly, consequently, dolly, early, family, fly, frequently, friendly, holy, Italy, likely, lily, lovely, melancholy, monthly, oily, only, presently, rarely, reply, shortly, silly, slippery, supply, ugly, weekly, wholly, worldly, yearly`

### 3.3 Passive Voice — `passive_voice`

A sentence contains passive voice if a **form of "be"** is immediately followed by a **word ending in `ed`** (with optional adverb between them).

Forms of "be": `am, are, is, was, were, be, been, being`

Example: *"The ball was thrown by him"* → flags `was thrown`.

### 3.4 Qualifiers / Weakeners — `qualifier`

A word or short phrase that hedges/weakens the writing. Matched case-insensitively against a fixed list.

Minimum qualifier list:

`almost, apparently, approximately, are: (when used to define), arguably, barely, comparatively, could, couldn't, deadly, deeply, direly, don't, downright, dreadful, each, especially, essentially, even, ever, extremely, fairly, far, far more, few, fewer, fortunately, frankly, free, full, fully, generally, greatly, hardly, honestly, I believe, I feel, I think, I'm not sure, incredibly, indeed, increasingly, just, kind of, largely, less, likely, many, maybe, merely, mildly, more, moreover, mostly, much, nearly, necessarily, neither, never, nonetheless, nor, notably, noticeably, oddly, only, outright, particularly, perhaps, plenty, predominantly, presumably, pretty, quite, rather, really, remarkably, roughly, significantly, simply, slightly, so, solely, some, somebody, somehow, someone, somewhat, suddenly, surprisingly, terribly, thankfully, truly, unfortunately, unusually, usually, very, virtually, yet`

### 3.5 Complex Words — `complex_word`

A word that has a simpler synonym. Matched case-insensitively.

Minimum complex-word → simpler mapping:

| Complex | Simpler |
|---------|---------|
| a considerable amount of | much |
| a number of | some |
| absolutely | — (remove) |
| accommodate | hold |
| accomplish | do |
| accordingly | so |
| additional | more |
| additionally | also |
| advise | tell |
| afford | give |
| aggregate | total |
| aid | help |
| alter | change |
| ameliorate | improve |
| an absence of | none |
| anticipate | expect |
| apparent | clear |
| appreciate | thank |
| assistance | help |
| attain | reach |
| attempt | try |
| beneficial | helpful |
| collaborate | work |
| commence | begin |
| communicate | talk |
| compensation | pay |
| component | part |
| considerably | much |
| constitute | make up |
| contains | has |
| contribution | — (remove) |
| demonstrate | show |
| depart | leave |
| designate | choose |
| determine | decide |
| detrimental | harmful |
| difficult | hard |
| disclose | show |
| discrepancy | difference |
| disseminate | spread |
| dramatically | greatly |
| duration | time |
| eliminate | end |
| elucidate | explain |
| employ | use |
| enable | allow |
| endeavor | try |
| enumerate | list |
| equitable | fair |
| equivalent | equal |
| establish | set up |
| evaluate | test |
| evident | clear |
| exclusively | only |
| expedite | speed up |
| facilitate | ease |
| following | after |
| for example | e.g. |
| for instance | e.g. |
| formulation | form |
| frequently | often |
| fundamental | basic |
| further | more |
| furthermore | also |
| has the ability to | can |
| hence | so |
| hesitate | wait |
| identical | same |
| illuminate | light |
| implementation | — (remove) |
| imply | suggest |
| importantly | — (remove) |
| in addition | also |
| in consequence | so |
| in contrast | but |
| in order to | to |
| in regard to | about |
| in spite of | despite |
| in the event that | if |
| inception | start |
| indicate | show |
| initiate | start |
| integral | — (remove) |
| integrity | honesty |
| interface | — (remove) |
| interim | — (remove) |
| intervention | — (remove) |
| iterative | repeated |
| jeopardize | risk |
| knowledge | — (remove) |
| limit | — (remove) |
| magnitude | size |
| maintain | keep |
| methodology | method |
| modification | change |
| monitor | check |
| multiple | many |
| necessitate | require |
| nevertheless | still |
| nonetheless | still |
| notwithstanding | despite |
| numerous | many |
| objective | aim |
| obligate | force |
| obtain | get |
| onward | — (remove) |
| operate | run |
| optional | — (remove) |
| parameter | — (remove) |
| participate | join |
| pertain | relate |
| plausible | likely |
| portion | part |
| possess | have |
| preclude | prevent |
| prior to | before |
| proactively | — (remove) |
| procure | get |
| proficient | skilled |
| propagate | spread |
| pursue | chase |
| qualified | able |
| regarding | about |
| regulate | control |
| relinquish | give up |
| remuneration | pay |
| require | must |
| requirements | — (remove) |
| residual | leftover |
| resolution | — (remove) |
| resolve | solve |
| resource | — (remove) |
| respond | answer |
| responsible | in charge |
| restructure | reorganize |
| reusable | — (remove) |
| revolution | uprising |
| robust | strong |
| routinely | often |
| segment | part |
| severe | harsh |
| significant | big |
| simplistic | simple |
| solely | only |
| solution | answer |
| somewhat | slightly |
| state-of-the-art | modern |
| strategize | plan |
| subsequent | later |
| substantial | large |
| sufficiently | enough |
| terminate | end |
| therefore | so |
| timely | — (remove) |
| tranquilize | calm |
| transmit | send |
| ultimate | last |
| undeniably | — (remove) |
| undergo | experience |
| unique | — (remove) |
| universal | general |
| unprecedented | — (remove) |
| until such time as | until |
| utilize | use |
| validate | confirm |
| variant | version |
| verification | check |
| versatile | flexible |
| viable | workable |
| voluntary | optional |
| whereas | while |
| with reference to | about |
| with the exception of | except for |
| witnessed | saw |

---

## 4. Output

The tool prints a report to stdout. The default format is Markdown KV (key-value), designed for easy parsing by both humans and LLMs without a parser tool. JSON output is available via the `--output-format json` flag.

### 4.1 Success — issues found (exit code 0)

**Markdown (default):**

```
# Hemingway Validation Report

## Document
- Path: path/to/document.md
- Lines: 142
- Words: 3450

## Summary
| Rule | Count |
| --- | --- |
| Hard sentences | 3 warning, 1 error |
| Adverbs | 12 |
| Passive voice | 5 |
| Qualifiers | 8 |
| Complex words | 6 |

## Issues

1. hard_sentence (error) — path/to/document.md:24:1
   - Text: The quick brown fox jumps over the lazy dog near the bank of the river where the fish swim downstream...
   - Message: Sentence is very hard to read (grade level 14).
   - Suggestion: Split into shorter sentences or simplify vocabulary.
2. adverb (warning) — path/to/document.md:42:10
   - Text: quickly
   - Message: Adverb "quickly" weakens your writing. Consider a stronger verb.
   - Suggestion: Use a stronger verb like "sprinted" instead of "ran quickly".
3. passive_voice (warning) — path/to/document.md:55:18
   - Text: was thrown
   - Message: Passive voice: "was thrown". Use active voice.
   - Suggestion: Rewrite so the subject performs the action (e.g. "He threw the ball").
4. qualifier (info) — path/to/document.md:67:5
   - Text: perhaps
   - Message: Qualifier "perhaps" weakens your writing.
   - Suggestion: Remove the qualifier or rephrase for confidence.
5. complex_word (info) — path/to/document.md:89:22
   - Text: utilize
   - Message: Complex word "utilize" has a simpler alternative.
   - Suggestion: Replace with "use".
```

**JSON (`--output-format json`):**

```json
{
  "document": {
    "path": "path/to/document.md",
    "line_count": 142,
    "word_count": 3450
  },
  "summary": {
    "hard_sentence": { "warning": 3, "error": 1 },
    "adverb": 12,
    "passive_voice": 5,
    "qualifier": 8,
    "complex_word": 6
  },
  "issues": [
    {
      "line": 24,
      "column": 1,
      "rule": "hard_sentence",
      "severity": "error",
      "text": "The quick brown fox jumps over the lazy dog near the bank of the river where the fish swim downstream...",
      "message": "Sentence is very hard to read (grade level 14). Consider splitting or simplifying.",
      "suggestion": "Split into shorter sentences or simplify vocabulary."
    },
    {
      "line": 42,
      "column": 10,
      "rule": "adverb",
      "severity": "warning",
      "text": "quickly",
      "message": "Adverb \"quickly\" weakens your writing. Consider a stronger verb.",
      "suggestion": "Use a stronger verb like \"sprinted\" instead of \"ran quickly\"."
    },
    {
      "line": 55,
      "column": 18,
      "rule": "passive_voice",
      "severity": "warning",
      "text": "was thrown",
      "message": "Passive voice: \"was thrown\". Use active voice.",
      "suggestion": "Rewrite so the subject performs the action (e.g. \"He threw the ball\")."
    },
    {
      "line": 67,
      "column": 5,
      "rule": "qualifier",
      "severity": "info",
      "text": "perhaps",
      "message": "Qualifier \"perhaps\" weakens your writing.",
      "suggestion": "Remove the qualifier or rephrase for confidence."
    },
    {
      "line": 89,
      "column": 22,
      "rule": "complex_word",
      "severity": "info",
      "text": "utilize",
      "message": "Complex word \"utilize\" has a simpler alternative.",
      "suggestion": "Replace with \"use\"."
    }
  ]
}
```

### 4.2 Success — no issues (exit code 0)

**Markdown (default):**

```
# Hemingway Validation Report

## Document
- Path: path/to/document.md
- Lines: 30
- Words: 400

## Summary
| Rule | Count |
| --- | --- |
| Hard sentences | 0 warning, 0 error |
| Adverbs | 0 |
| Passive voice | 0 |
| Qualifiers | 0 |
| Complex words | 0

## Issues

No issues found.
```

**JSON (`--output-format json`):**

```json
{
  "document": {
    "path": "path/to/document.md",
    "line_count": 30,
    "word_count": 400
  },
  "summary": {
    "hard_sentence": { "warning": 0, "error": 0 },
    "adverb": 0,
    "passive_voice": 0,
    "qualifier": 0,
    "complex_word": 0
  },
  "issues": []
}
```

### 4.3 Error (exit code 1)

**Markdown (default):**

```
# Hemingway Validation Report

## Error
- Type: file_not_found
- Message: File not found: path/to/missing.md
```

**JSON (`--output-format json`):**

```json
{
  "error": {
    "type": "file_not_found",
    "message": "File not found: path/to/missing.md"
  }
}
```

---

## 5. Severity Levels

| Severity | Used by |
|----------|---------|
| `error` | `hard_sentence` at red level |
| `warning` | `hard_sentence` at yellow level, `adverb`, `passive_voice` |
| `info` | `qualifier`, `complex_word` |

---

## 6. Limitations (Explicitly Out of Scope)

- No spelling or grammar checking.
- No generative AI rewrites or suggestions beyond the static suggestion text.
- No coloured/highlighted terminal output.
- No interactive editing.
- No auto-fix or file modification.
- No configuration files — thresholds and word lists are fixed.

---

## 7. Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Document checked successfully (issues may exist) |
| 1 | Error occurred (file not found, IO error, etc.) |

Issues in the output do **not** affect the exit code. The exit code signals whether the tool ran successfully, not whether the writing is "good".
