from commitgpt.prompt import build_prompt


def test_prompt_contains_rules():
    prompt = build_prompt("test diff")

    assert "Conventional Commits" in prompt
    assert "Return ONLY the commit message" in prompt


def test_prompt_includes_diff():
    diff = "sample diff"

    prompt = build_prompt(diff)

    assert diff in prompt