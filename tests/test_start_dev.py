import os
import shutil
import socket
import stat
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


PROJECT_ROOT = Path(__file__).parents[1]


def unused_local_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class StartDevScriptTests(unittest.TestCase):
    def test_exits_nonzero_without_success_message_when_api_fails_to_start(self):
        with TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            shutil.copy(PROJECT_ROOT / "start-dev.sh", temp_root / "start-dev.sh")

            gunicorn = temp_root / "src" / "venv" / "bin" / "gunicorn"
            gunicorn.parent.mkdir(parents=True)
            gunicorn.write_text("#!/usr/bin/env bash\nexit 42\n")
            gunicorn.chmod(gunicorn.stat().st_mode | stat.S_IXUSR)

            fake_bin = temp_root / "bin"
            fake_bin.mkdir()
            npx = fake_bin / "npx"
            npx.write_text("#!/usr/bin/env bash\nexit 43\n")
            npx.chmod(npx.stat().st_mode | stat.S_IXUSR)
            (temp_root / "web-server").mkdir()

            result = subprocess.run(
                ["bash", "start-dev.sh"],
                cwd=temp_root,
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                    "PATH": f"{fake_bin}:{os.environ['PATH']}",
                    "API_PORT": str(unused_local_port()),
                    "WEB_PORT": str(unused_local_port()),
                    "RUN_DIR": str(temp_root / "run"),
                },
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("API server failed to start", result.stderr)
            self.assertNotIn("Both servers started", result.stdout)


if __name__ == "__main__":
    unittest.main()
