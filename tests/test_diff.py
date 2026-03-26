from commitgpt.diff import truncate_diff


def test_truncate_diff_limits_size():
    large_diff = "\n".join(["+line"] * 20000)

    result = truncate_diff(large_diff)

    assert len(result) <= 12000


def test_truncate_diff_keeps_added_lines():
    diff = "\n".join([
        "+added_line",
        "-removed_line",
        " context_line"
    ])

    result = truncate_diff(diff)

    assert "+added_line" in result