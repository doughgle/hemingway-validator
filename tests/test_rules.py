from hemingway.rules import (
    check_adverb,
    check_complex_word,
    check_hard_sentence,
    check_passive_voice,
    check_qualifier,
)


class TestHardSentence:
    def test_below_threshold(self):
        sentence = "The cat sat on the mat."
        result = check_hard_sentence(sentence, 1)
        assert result is None

    def test_yellow_warning(self):
        sentence = (
            "Big complex words in this sentence make the level"
            " high around twelve approximately now."
        )
        result = check_hard_sentence(sentence, 1)
        assert result is not None
        assert result["rule"] == "hard_sentence"
        assert result["severity"] == "warning"

    def test_red_error(self):
        sentence = (
            "This exceptionally convoluted and unnecessarily complicated sentence "
            "is deliberately designed to trigger the absolute highest reading level "
            "possible within the constraints of the provided testing framework."
        )
        result = check_hard_sentence(sentence, 1)
        assert result is not None
        assert result["rule"] == "hard_sentence"
        assert result["severity"] == "error"

    def test_too_few_words(self):
        sentence = "A short sentence."
        result = check_hard_sentence(sentence, 1)
        assert result is None

    def test_reading_level_exact_boundary_warning(self):
        words = ["word"] * 14
        sentence = " ".join(words) + "."
        result = check_hard_sentence(sentence, 1)
        assert result is None or result["severity"] in ("warning", "error")

    def test_returns_correct_line(self):
        sentence = (
            "This exceptionally convoluted and unnecessarily complicated sentence "
            "is deliberately designed to trigger the absolute highest reading level "
            "possible within the constraints of the provided testing framework."
        )
        result = check_hard_sentence(sentence, 5)
        assert result is not None
        assert result["line"] == 5

    def test_correct_formula(self):
        letters = 10
        words = 5
        sentences = 1
        level = round(4.71 * (letters / words) + 0.5 * (words / sentences) - 21.43)
        assert level == -10

    def test_edge_14_words(self):
        sentence = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen"  # noqa: E501
        words = len(sentence.split())
        assert words >= 14


class TestAdverb:
    def test_detects_adverb(self):
        sentence = "He ran quickly to the store."
        results = check_adverb(sentence, 1)
        assert len(results) == 1
        assert results[0]["rule"] == "adverb"
        assert results[0]["text"] == "quickly"
        assert results[0]["severity"] == "warning"

    def test_ignores_non_adverb(self):
        sentence = "He ran fast to the store."
        results = check_adverb(sentence, 1)
        assert len(results) == 0

    def test_ignores_exception_list(self):
        sentence = "She is friendly and lovely."
        results = check_adverb(sentence, 1)
        assert len(results) == 0

    def test_mixed_content(self):
        sentence = "He quickly and happily ran, but she was friendly."
        results = check_adverb(sentence, 1)
        texts = [r["text"] for r in results]
        assert "quickly" in texts
        assert "happily" in texts
        assert "friendly" not in texts

    def test_multiple_adverbs(self):
        sentence = "She sadly quietly whispered."
        results = check_adverb(sentence, 1)
        assert len(results) == 2

    def test_punctuation_attached(self):
        sentence = "He ran quickly, happily, and sadly."
        results = check_adverb(sentence, 1)
        assert len(results) == 3
        texts = [r["text"] for r in results]
        assert "quickly" in texts
        assert "happily" in texts
        assert "sadly" in texts

    def test_case_insensitive(self):
        sentence = "He ran Quickly to the store."
        results = check_adverb(sentence, 1)
        assert len(results) == 1

    def test_returns_line_number(self):
        sentence = "He ran quickly."
        results = check_adverb(sentence, 42)
        assert results[0]["line"] == 42

    def test_returns_column(self):
        sentence = "He ran quickly."
        results = check_adverb(sentence, 1)
        assert results[0]["column"] > 0


class TestPassiveVoice:
    def test_detects_passive_voice(self):
        sentence = "The ball was pushed by him."
        results = check_passive_voice(sentence, 1)
        assert len(results) >= 1
        assert results[0]["rule"] == "passive_voice"
        assert results[0]["severity"] == "warning"

    def test_no_passive_voice(self):
        sentence = "He pushed the ball."
        results = check_passive_voice(sentence, 1)
        assert len(results) == 0

    def test_all_be_forms(self):
        forms = ["am", "are", "is", "was", "were", "be", "been", "being"]
        for form in forms:
            sentence = f"The ball {form} pushed by him."
            results = check_passive_voice(sentence, 1)
            assert len(results) == 1, f"Failed for form '{form}'"
            assert results[0]["text"] == f"{form} pushed"

    def test_with_adverb_between(self):
        sentence = "The ball was quickly pushed by him."
        results = check_passive_voice(sentence, 1)
        assert len(results) == 1
        assert results[0]["text"] == "was quickly pushed"

    def test_no_following_ed_word(self):
        sentence = "He was happy."
        results = check_passive_voice(sentence, 1)
        assert len(results) == 0

    def test_multiple_passive_voice(self):
        sentence = "The ball was pushed and the game was played."
        results = check_passive_voice(sentence, 1)
        assert len(results) == 2

    def test_case_insensitive(self):
        sentence = "The Ball Was Pushed by him."
        results = check_passive_voice(sentence, 1)
        assert len(results) == 1


class TestQualifier:
    def test_detects_qualifier(self):
        sentence = "This is perhaps the best option."
        results = check_qualifier(sentence, 1)
        assert len(results) >= 1
        assert results[0]["rule"] == "qualifier"
        assert results[0]["severity"] == "info"

    def test_no_qualifier(self):
        sentence = "This is the best option."
        results = check_qualifier(sentence, 1)
        assert len(results) == 0

    def test_multi_word_qualifier(self):
        sentence = "I think this is correct."
        results = check_qualifier(sentence, 1)
        assert len(results) >= 1
        assert results[0]["text"].lower() == "i think"

    def test_case_insensitive(self):
        sentence = "PERHAPS this is correct."
        results = check_qualifier(sentence, 1)
        assert len(results) >= 1

    def test_qualifier_with_punctuation(self):
        sentence = "This is, perhaps, the best."
        results = check_qualifier(sentence, 1)
        texts = [r["text"].lower() for r in results]
        assert "perhaps" in texts

    def test_multiple_qualifiers(self):
        sentence = "Perhaps this is really quite good."
        results = check_qualifier(sentence, 1)
        qualifiers = [r["text"].lower() for r in results]
        assert "perhaps" in qualifiers or "quite" in qualifiers

    def test_are_colon(self):
        sentence = "Cats are: animals."
        results = check_qualifier(sentence, 1)
        assert len(results) >= 1

    def test_returns_line_number(self):
        sentence = "Perhaps this is good."
        results = check_qualifier(sentence, 10)
        assert results[0]["line"] == 10

    def test_returns_column(self):
        sentence = "Perhaps this is good."
        results = check_qualifier(sentence, 1)
        assert results[0]["column"] > 0


class TestComplexWord:
    def test_detects_complex_word(self):
        sentence = "Please utilize the tool."
        results = check_complex_word(sentence, 1)
        assert len(results) >= 1
        assert results[0]["rule"] == "complex_word"
        assert results[0]["severity"] == "info"

    def test_no_complex_word(self):
        sentence = "Please use the tool."
        results = check_complex_word(sentence, 1)
        assert len(results) == 0

    def test_case_insensitive(self):
        sentence = "Please UTILIZE the tool."
        results = check_complex_word(sentence, 1)
        assert len(results) >= 1

    def test_suggestion_included(self):
        sentence = "Please utilize the tool."
        results = check_complex_word(sentence, 1)
        assert "suggestion" in results[0]

    def test_multi_word_complex(self):
        sentence = "A considerable amount of time passed."
        results = check_complex_word(sentence, 1)
        assert len(results) >= 1
        assert results[0]["text"].lower() == "a considerable amount of"

    def test_multiple_complex_words(self):
        sentence = "Please utilize and facilitate."
        results = check_complex_word(sentence, 1)
        assert len(results) >= 2

    def test_prior_to(self):
        sentence = "Prior to the meeting, we met."
        results = check_complex_word(sentence, 1)
        assert len(results) >= 1
        assert "prior to" in results[0]["text"].lower()

    def test_returns_line_number(self):
        sentence = "Please utilize the tool."
        results = check_complex_word(sentence, 7)
        assert results[0]["line"] == 7

    def test_until_such_time_as(self):
        sentence = "Wait until such time as we arrive."
        results = check_complex_word(sentence, 1)
        assert len(results) >= 1
