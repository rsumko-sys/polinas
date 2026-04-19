from gitara.backends.llm_provider import LlamaCppProvider


def test_llama_cpp_provider_from_diff():
    prov = LlamaCppProvider()
    diff = (
        "diff --git a/README.md b/README.md\n"
        "index 123..456\n"
        "--- a/README.md\n"
        "+++ b/README.md\n"
        "@@ -1 +1,2 @@\n"
        "-Hello\n"
        "+Hello\n"
        "+World\n"
    )
    msg = prov.generate_commit_message(diff)
    assert isinstance(msg, str)
    assert msg == "chore: update README.md"


def test_llama_cpp_provider_fallback():
    prov = LlamaCppProvider()
    diff = "+ Added a small change\n- removed old\n"
    msg = prov.generate_commit_message(diff)
    assert isinstance(msg, str)
    assert msg.startswith("chore: update")
