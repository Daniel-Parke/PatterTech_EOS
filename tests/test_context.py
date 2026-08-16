"""Context packet tests: changed surface, summaries, references, routing."""

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.eos import contextgen  # noqa: E402


def _git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True,
                   capture_output=True, text=True)


@pytest.fixture
def git_repo(tmp_path):
    root = tmp_path / "repo"
    (root / "docs").mkdir(parents=True)
    _git(root, "init", "-b", "main")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "user.name", "Test")
    (root / "docs" / "guide.md").write_text(
        "---\nsummary: How the widget works\nkind: guide\n---\n\n# Guide\n",
        encoding="utf-8")
    (root / "docs" / "index.md").write_text(
        "# Index\n\nSee docs/guide.md for the widget guide.\n",
        encoding="utf-8")
    (root / "docs" / "unrelated.md").write_text(
        "# Unrelated\n\nNothing to see.\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-m", "base")
    (root / "docs" / "guide.md").write_text(
        "---\nsummary: How the widget works\nkind: guide\n---\n\n# Guide\n\nMore.\n",
        encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-m", "edit guide")
    return root


def test_packet_shape_and_changed_set(git_repo):
    packet = contextgen.build_packet(git_repo, base_ref="HEAD~1")
    assert set(packet) == {"changed", "summaries", "referencing_files",
                           "activated_packs", "routed"}
    assert packet["changed"] == ["docs/guide.md"]
    assert packet["activated_packs"] == []


def test_front_matter_summaries(git_repo):
    packet = contextgen.build_packet(git_repo, base_ref="HEAD~1")
    assert packet["summaries"]["docs/guide.md"] == "How the widget works"


def test_reverse_reference_scan(git_repo):
    packet = contextgen.build_packet(git_repo, base_ref="HEAD~1")
    refs = packet["referencing_files"].get("docs/guide.md", [])
    assert "docs/index.md" in refs
    assert "docs/unrelated.md" not in refs


def test_routed_tier_present(git_repo):
    packet = contextgen.build_packet(git_repo, base_ref="HEAD~1")
    assert packet["routed"]["tier"] in ("R0", "R1", "R2", "R3")
    assert isinstance(packet["routed"]["reasons"], list)


def test_explicit_files_mode_needs_no_git(tmp_path):
    root = tmp_path / "plain"
    root.mkdir()
    (root / "a.md").write_text(
        "---\nsummary: A file\nkind: record\n---\n", encoding="utf-8")
    (root / "b.md").write_text("mentions a.md here\n", encoding="utf-8")
    packet = contextgen.build_packet(root, files=["a.md"])
    assert packet["changed"] == ["a.md"]
    assert packet["summaries"]["a.md"] == "A file"
    assert "b.md" in packet["referencing_files"].get("a.md", [])
    assert packet["routed"]["tier"] == "R0"


def test_deleted_and_missing_files_are_marked(tmp_path):
    root = tmp_path / "plain"
    root.mkdir()
    packet = contextgen.build_packet(root, files=["gone.md"])
    assert packet["summaries"]["gone.md"] == "(deleted)"


def test_no_front_matter_is_named_not_invented(tmp_path):
    root = tmp_path / "plain"
    root.mkdir()
    (root / "plain.md").write_text("# Plain\n", encoding="utf-8")
    packet = contextgen.build_packet(root, files=["plain.md"])
    assert packet["summaries"]["plain.md"] == "(no front matter)"


# --- pack activation ----------------------------------------------------


def _pack(root, name, *, paths, predicates):
    d = root / "packs" / name
    d.mkdir(parents=True, exist_ok=True)
    display_name = name.replace("-", " ").title()
    namespace = name.replace("-", "").upper()
    (d / "PACK.md").write_text(
        "---\n"
        f"summary: The {name} pack\n"
        f"applies_when: [{', '.join(predicates)}]\n"
        f"activation_paths: [{', '.join(paths)}]\n"
        "kind: record\ntype: pack\ntags: [eos]\nreview: 2030-01\n"
        f"display_name: {display_name}\n"
        "category: engineering\n"
        f"id_namespace: {namespace}\n---\n\n"
        f"# {display_name}\n\nBody.\n",
        encoding="utf-8", newline="\n")


@pytest.mark.parametrize("path,pattern,want", [
    ("app/components/Button.tsx", "**/components/**", True),
    ("components/Button.tsx", "**/components/**", True),
    ("app/routes/x.py", "**/components/**", False),
    ("api/routes/invoices.py", "**/*.py", True),
    ("api/routes/invoices.ts", "**/*.py", False),
    ("README.md", "**/*.md", True),
    ("docs/deep/nested/guide.md", "**/*.md", True),
    ("Dockerfile.prod", "**/Dockerfile*", True),
    # The bug that made this pointless: fnmatch's * crosses separators,
    # so every pack activated on every change.
    ("anything/at/all.txt", "**/components/**", False),
    ("ops/deploy.yml", "**/*.tsx", False),
])
def test_glob_does_not_cross_separators(path, pattern, want):
    assert contextgen._match(path, pattern) is want


def test_activation_narrows_to_the_touched_domain(tmp_path):
    root = tmp_path / "r"
    _pack(root, "ui-ux", paths=["**/components/**", "**/*.css"],
          predicates=["has_user_interface"])
    _pack(root, "devops", paths=["**/migrations/**", "**/*.tf"],
          predicates=["deploys_to_environment"])
    got = contextgen.activated_packs(root, ["app/components/Button.tsx"])
    assert [r["pack"] for r in got] == ["ui-ux"]
    assert got[0]["matched_paths"] == ["app/components/Button.tsx"]


def test_activation_is_empty_when_nothing_matches(tmp_path):
    """A doc fix must not drag in twenty packs. The defect that shipped
    was the opposite: activated_packs was hardcoded to []."""
    root = tmp_path / "r"
    _pack(root, "ui-ux", paths=["**/components/**"], predicates=["has_user_interface"])
    assert contextgen.activated_packs(root, ["NOTES.txt"]) == []


def test_a_declared_predicate_activates_without_a_path_match(tmp_path):
    """Predicates are the real gate, so a task that declares one pulls
    its pack in even when the diff says nothing."""
    root = tmp_path / "r"
    _pack(root, "security", paths=["**/.env*"], predicates=["runs_agents"])
    got = contextgen.activated_packs(root, ["notes.md"],
                                     declared_predicates=["runs_agents"])
    assert [r["pack"] for r in got] == ["security"]
    assert got[0]["predicates_declared"] == ["runs_agents"]


def test_undeclared_predicates_are_returned_for_confirmation(tmp_path):
    """The diff cannot settle most predicates, and saying it did would
    be worse than narrowing and asking."""
    root = tmp_path / "r"
    _pack(root, "ui-ux", paths=["**/*.css"], predicates=["has_user_interface"])
    got = contextgen.activated_packs(root, ["a/site.css"])
    assert got[0]["predicates_to_confirm"] == ["has_user_interface"]
    assert got[0]["predicates_declared"] == []


def test_every_live_pack_declares_a_path_trigger():
    """PACK_CONTRACT requires a non-keyword trigger on every pack, because
    routing has to be deterministic given the same inputs.

    Counted against the packs on disk rather than against a number
    typed in here. The number was 20, and a twenty-first pack failed
    this test for existing, which tells a reader nothing about
    triggers.
    """
    triggers = contextgen.pack_triggers(REPO)
    built = sorted(p.parent.name for p in (REPO / "packs").glob("*/PACK.md"))
    assert sorted(t["pack"] for t in triggers) == built
    missing = [t["pack"] for t in triggers if not t["paths"]]
    assert missing == []
    no_predicate = [t["pack"] for t in triggers if not t["predicates"]]
    assert no_predicate == []


def test_the_real_repo_narrows_a_ui_change():
    got = contextgen.activated_packs(REPO, ["app/components/Button.tsx"])
    names = {r["pack"] for r in got}
    assert "ui-ux" in names
    assert len(names) < 6, f"activation too broad: {sorted(names)}"


# --- activation from declared facts, the Session 0 half -----------------


def _estate(root):
    """Three packs whose predicates do not overlap."""
    _pack(root, "ui-ux", paths=["**/components/**"],
          predicates=["has_user_interface"])
    _pack(root, "security-privacy", paths=["**/.env*"],
          predicates=["runs_agents", "handles_personal_data"])
    _pack(root, "devops", paths=["**/Dockerfile"],
          predicates=["deploys_to_environment"])


def test_facts_activate_only_the_packs_that_own_them(tmp_path):
    root = tmp_path / "r"
    _estate(root)
    got = contextgen.activation_from_facts(root, ["has_user_interface"])
    assert [r["pack"] for r in got["activated"]] == ["ui-ux"]
    assert got["activated"][0]["matched_predicates"] == ["has_user_interface"]


def test_the_packs_left_out_are_named_with_what_would_have_pulled_them(tmp_path):
    """The pack-level why-excluded half.

    D003 refuses a seed file with no reason to be there. Nothing recorded
    the packs nobody loaded, so a reader could not tell a pack ruled
    irrelevant from a pack nobody thought of.
    """
    root = tmp_path / "r"
    _estate(root)
    got = contextgen.activation_from_facts(root, ["has_user_interface"])
    left = {r["pack"]: r["would_activate_on"] for r in got["not_activated"]}
    assert set(left) == {"devops", "security-privacy"}
    assert left["devops"] == ["deploys_to_environment"]
    assert left["security-privacy"] == ["handles_personal_data", "runs_agents"]


def test_a_brochure_site_does_not_pull_in_deployment_or_agents(tmp_path):
    """Negative activation, which is the half that has to be measured.

    A system that never misses a pack because it activates everything has
    not solved activation.
    """
    root = tmp_path / "r"
    _estate(root)
    got = contextgen.activation_from_facts(root, ["has_user_interface"])
    assert [r["pack"] for r in got["activated"]] == ["ui-ux"]


def test_no_fact_activates_nothing_rather_than_everything(tmp_path):
    root = tmp_path / "r"
    _estate(root)
    got = contextgen.activation_from_facts(root, [])
    assert got["activated"] == []
    assert len(got["not_activated"]) == 3


def test_an_unknown_predicate_is_reported_not_swallowed(tmp_path):
    """A misspelled fact is a silent false negative, the expensive kind."""
    root = tmp_path / "r"
    _estate(root)
    got = contextgen.activation_from_facts(root, ["has_user_interfce"])
    assert got["unknown_predicates"] == ["has_user_interfce"]
    assert got["activated"] == []


def test_one_venture_fact_spelled_two_ways_splits_the_estate(tmp_path):
    """Why a shared predicate vocabulary is the next piece of work.

    In the live tree security-privacy declares handles_personal_data and
    legal-licensing declares processes_personal_data. They are the same
    answer to interview question 9, and a venture recording one of them
    loads one pack and silently misses the other.
    """
    root = tmp_path / "r"
    _pack(root, "security-privacy", paths=["**/.env*"],
          predicates=["handles_personal_data"])
    _pack(root, "legal-licensing", paths=["**/LICENSE"],
          predicates=["processes_personal_data"])
    one = contextgen.activation_from_facts(root, ["handles_personal_data"])
    assert [r["pack"] for r in one["activated"]] == ["security-privacy"]
    assert one["unknown_predicates"] == []
    both = contextgen.activation_from_facts(
        root, ["handles_personal_data", "processes_personal_data"])
    assert [r["pack"] for r in both["activated"]] == ["legal-licensing",
                                                      "security-privacy"]


def test_the_live_estate_no_longer_splits_on_personal_data(tmp_path):
    """The synonym this file used to guard is merged (ADR-0010).

    The earlier version of this test asserted the split and said a fix
    would retire it. This is that retirement, inverted rather than
    deleted, because the failure it describes is the kind that comes
    back: one answer to interview question 9 spelled two ways, so a
    venture recording either loaded one pack and missed the other.
    """
    triggers = contextgen.pack_triggers(REPO)
    owners = {}
    for t in triggers:
        for p in t["predicates"]:
            owners.setdefault(p, []).append(t["pack"])
    assert sorted(owners.get("handles_personal_data", [])) == [
        "legal-licensing", "security-privacy"]
    assert "processes_personal_data" not in owners
