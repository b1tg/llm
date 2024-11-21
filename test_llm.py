import os
import subprocess
import sys



def test_url():
    res = subprocess.run(
        [
            sys.executable,
            "llm.py",
            "--url",
            "https://blog.torproject.org/tor-is-still-safe",
            "--prompt",
            "summary",
        ],
        env=os.environ.copy(),
        capture_output=True,
    )
    # print(res.stdout.decode("utf8"))
    assert res.returncode == 0
    assert b"Tor" in res.stdout


def test_youtube():
    res = subprocess.run(
        [
            sys.executable,
            "llm.py",
            "--youtube",
            "https://www.youtube.com/watch?v=R8uxmXmtOrk",
            "--prompt",
            "summary",
        ],
        env=os.environ.copy(),
        capture_output=True,
    )
    print(res.stdout.decode("utf8"))
    assert res.returncode == 0
    assert "tinygrad" in str(res.stdout).lower()
