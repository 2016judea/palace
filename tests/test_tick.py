"""bin/tick's commit step, driven against a throwaway git repo shaped like a fresh clone after the
public release: state/ written by a resident but ignored, journal/ and paths.json not yet written,
site/index.html tracked. No model is run.
Run: /Users/aidan/Desktop/bricks/.venv/bin/python -m pytest tests"""
import importlib.machinery, importlib.util, os, subprocess
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_tick():
    path = os.path.join(ROOT, "bin/tick")
    spec = importlib.util.spec_from_file_location("tick", path, loader=importlib.machinery.SourceFileLoader("tick", path))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def git(*a, **kw):
    return subprocess.run(["git", *a], capture_output=True, text=True, **kw)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    for k, v in {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@x"}.items():
        monkeypatch.setenv(k, v)
    git("init", "-q", str(tmp_path))
    (tmp_path / ".gitignore").write_text("state/\njournal/\npaths.json\n")
    (tmp_path / "site").mkdir(); (tmp_path / "state").mkdir()
    (tmp_path / "site/index.html").write_text("v1"); (tmp_path / "state/ledger.jsonl").write_text("{}\n")
    git("add", ".gitignore", "site", cwd=tmp_path); git("commit", "-qm", "init", cwd=tmp_path)
    tick = load_tick()           # importing bin/tick chdir's to the palace root, so load it BEFORE moving into the throwaway repo
    monkeypatch.chdir(tmp_path)
    return tmp_path, tick


def test_a_rendered_page_is_committed_even_though_state_is_gitignored(repo):
    repo, tick = repo
    (repo / "site/index.html").write_text("v2")
    (repo / "state/ledger.jsonl").write_text("{}\n{}\n")
    out = tick.git_commit_push(["state", "journal", "paths.json", "site"], "tick 1 · mason · $0.50 · x")
    assert out != "clean"                     # before the fix: 'fatal: pathspec journal did not match', nothing staged, 'clean'
    assert out.startswith("push failed")      # the throwaway repo has no remote; the commit itself must exist
    assert git("log", "--oneline", cwd=repo).stdout.count("\n") == 2
    assert git("status", "--short", cwd=repo).stdout.strip() == ""
    assert "site/index.html" in git("show", "--stat", "--oneline", "HEAD", cwd=repo).stdout


def test_nothing_changed_reports_clean(repo):
    repo, tick = repo
    assert tick.git_commit_push(["state", "journal", "paths.json", "site"], "m") == "clean"
    assert git("log", "--oneline", cwd=repo).stdout.count("\n") == 1


def test_addable_drops_ignored_and_missing_paths(repo):
    repo, tick = repo
    assert tick.addable(["state", "journal", "paths.json", "site", "nope"]) == ["site"]
