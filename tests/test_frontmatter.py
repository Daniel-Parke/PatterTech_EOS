"""Tests for the hardened front-matter parser."""

from tools.eos.frontmatter import parse


def test_absent_when_no_opener():
    fm = parse("# Title\n\nBody.\n")
    assert fm.present is False
    assert fm.data == {}
    assert fm.errors == []
    assert fm.body == "# Title\n\nBody.\n"


def test_simple_block_parses():
    fm = parse("---\nsummary: A thing\ntype: org\n---\n\nBody.\n")
    assert fm.present is True
    assert fm.data == {"summary": "A thing", "type": "org"}
    assert fm.errors == []
    assert fm.body == "\nBody."


def test_unterminated_block_is_error_and_absent():
    fm = parse("---\nsummary: no closer\n\nBody text.\n")
    assert fm.present is False
    assert fm.errors == [(1, "unterminated front-matter block")]
    assert fm.data == {}


def test_terminator_beyond_scan_window_counts_as_unterminated():
    filler = "\n".join(f"k{i}: v" for i in range(70))
    fm = parse("---\n" + filler + "\n---\nBody.\n")
    assert fm.present is False
    assert fm.errors == [(1, "unterminated front-matter block")]


def test_key_charset_rejects_bad_keys():
    fm = parse("---\n1bad: x\ngood_key-2: y\n---\n")
    assert fm.present is True
    assert fm.data == {"good_key-2": "y"}
    assert fm.errors == [(2, "unparseable front-matter line: 1bad: x")]


def test_inline_list():
    fm = parse("---\ntags: [eos, wargame]\n---\n")
    assert fm.data == {"tags": ["eos", "wargame"]}


def test_block_list():
    fm = parse("---\nrulings:\n  - first · argued · x\n  - second · inherited · y\n---\n")
    assert fm.data == {"rulings": ["first · argued · x", "second · inherited · y"]}


def test_dash_without_list_key_is_error():
    fm = parse("---\n- stray item\nkey: v\n---\n")
    assert fm.data == {"key": "v"}
    assert fm.errors == [(2, "list item without a list key: - stray item")]


def test_dash_after_scalar_key_is_error():
    fm = parse("---\nkey: value\n- item\n---\n")
    assert fm.errors == [(3, "list item without a list key: - item")]


def test_values_stay_strings_no_coercion():
    fm = parse("---\ncount: 3\nflag: true\nwhen: 2026-08\n---\n")
    assert fm.data == {"count": "3", "flag": "true", "when": "2026-08"}


def test_comments_and_blanks_ignored():
    fm = parse("---\n# a comment\n\nkey: v\n---\n")
    assert fm.data == {"key": "v"}
    assert fm.errors == []


def test_unparseable_line_is_error_not_silent_skip():
    fm = parse("---\nkey: v\n???\n---\n")
    assert fm.data == {"key": "v"}
    assert fm.errors == [(3, "unparseable front-matter line: ???")]


def test_unparseable_line_resets_pending_list():
    fm = parse("---\nitems:\n???\n  - late\n---\n")
    assert len(fm.errors) == 2
    assert fm.errors[0][0] == 3
    assert fm.errors[1] == (4, "list item without a list key: - late")


def test_empty_value_key_stays_empty_string():
    fm = parse("---\nkey:\nother: x\n---\n")
    assert fm.data == {"key": "", "other": "x"}
