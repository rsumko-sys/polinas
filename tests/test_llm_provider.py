from gitara.llm_provider import get_provider


def test_stub_provider_generates_from_added_line():
    p = get_provider()
    diff = """
diff --git a/foo b/foo
index 000000..111111 100644
--- a/foo
+++ b/foo
+Added feature X that improves performance
"""
    msg = p.generate_commit_message(diff)
    assert msg.startswith("feat:") or msg.startswith("chore:"), "unexpected commit message format"


def test_stub_empty_diff():
    p = get_provider()
    assert p.generate_commit_message("") == "chore: empty diff"
