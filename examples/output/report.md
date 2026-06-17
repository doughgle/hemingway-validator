# Hemingway Validation Report

## Document
- Path: examples/input/simple.md
- Lines: 11
- Words: 33

## Summary
| Rule | Count |
| --- | --- |
| Hard sentences | 0 warning, 0 error |
| Adverbs | 1 |
| Passive voice | 1 |
| Qualifiers | 1 |
| Complex words | 1

## Issues

1. adverb (warning) — examples/input/simple.md:3:8
   - Text: quickly
   - Message: Adverb "quickly" weakens your writing. Consider a stronger verb.
   - Suggestion: Use a stronger verb like "sprinted" instead of "ran quickly".

2. passive_voice (warning) — examples/input/simple.md:5:10
   - Text: was pushed
   - Message: Passive voice: "was pushed". Use active voice.
   - Suggestion: Rewrite so the subject performs the action (e.g. "He threw the ball").

3. qualifier (info) — examples/input/simple.md:7:9
   - Text: perhaps
   - Message: Qualifier "perhaps" weakens your writing.
   - Suggestion: Remove the qualifier or rephrase for confidence.

4. complex_word (info) — examples/input/simple.md:9:8
   - Text: utilize
   - Message: Complex word "utilize" has a simpler alternative.
   - Suggestion: Replace with "use".

